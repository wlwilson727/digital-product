#!/usr/bin/env python3
"""Local, dependency-free product preparation. Never publishes or calls external APIs."""
import argparse
import csv
import hashlib
import io
import json
import math
import re
import sys
import zipfile
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('index.html', 'app.js', 'style.css', 'calc.js', 'GUIDE.md', 'LICENSE.md', 'FAQ.md', 'preview.svg')
WEIGHTS = {'demand': .25, 'profit': .20, 'differentiation': .15, 'automation': .15, 'acquisition': .15, 'simplicity': .10}

class ValidationError(ValueError):
    pass

def load_catalog(path):
    data = json.loads(Path(path).read_text())
    if data.get('schema_version') != 1 or data.get('currency') != 'USD' or not isinstance(data.get('products'), list) or not data['products']:
        raise ValidationError('Catalog requires schema_version 1, currency USD and products.')
    seen = set()
    for p in data['products']:
        for field in ('slug', 'version', 'name', 'customer', 'problem', 'category'):
            if not isinstance(p.get(field), str) or not p[field].strip():
                raise ValidationError(f'Missing string: {field}')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['slug']) or p['slug'] in seen:
            raise ValidationError('Unsafe or duplicate slug')
        seen.add(p['slug'])
        if not re.fullmatch(r'\d+\.\d+\.\d+', p['version']):
            raise ValidationError('Version must be semantic x.y.z')
        if isinstance(p.get('price'), bool) or not isinstance(p.get('price'), (int, float)) or not math.isfinite(p['price']) or p['price'] <= 0:
            raise ValidationError('Positive finite price required')
        for field in ('features', 'keywords', 'upsells'):
            if not isinstance(p.get(field), list) or any(not isinstance(x, str) or not x.strip() for x in p[field]) or (field != 'upsells' and not p[field]):
                raise ValidationError(f'Invalid list: {field}')
    for p in data['products']:
        if any(x not in seen or x == p['slug'] for x in p['upsells']):
            raise ValidationError('Upsells must reference other catalog products')
    return data

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'href') and value:
                self.links.append(value)

def validate_product(folder):
    folder = Path(folder).resolve()
    for name in REQUIRED:
        path = folder / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size < 10:
            raise ValidationError(f'Missing, empty or symlink product file: {path}')
        content = path.read_text(encoding='utf-8')
        if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}', content):
            raise ValidationError(f'Possible credential in {name}')
    parser = Links()
    parser.feed((folder / 'index.html').read_text())
    for link in parser.links:
        if link.startswith(('#', 'mailto:')):
            continue
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('//'):
            raise ValidationError(f'Offline product has external or executable link: {link}')
        local = link.split('#')[0].split('?')[0]
        target = (folder / local).resolve()
        if not target.is_relative_to(folder) or not target.is_file() or local not in REQUIRED:
            raise ValidationError(f'Unsafe or unbundled local link: {link}')
    return {name: hashlib.sha256((folder / name).read_bytes()).hexdigest() for name in REQUIRED}

def package(folder, destination):
    hashes = validate_product(folder)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(REQUIRED):
            info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (Path(folder) / name).read_bytes(), compresslevel=9)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValidationError('Archive CRC validation failed')
    return hashes

def verify_release(output):
    output = Path(output).resolve()
    data = json.loads((output / 'catalog.json').read_text())
    for record in data['products']:
        name = record['artifact']
        if Path(name).name != name or not name.endswith('.zip'):
            raise ValidationError('Unsafe artifact path')
        artifact = output / name
        if artifact.is_symlink() or hashlib.sha256(artifact.read_bytes()).hexdigest() != record['sha256']:
            raise ValidationError(f'Artifact checksum mismatch: {name}')
        with zipfile.ZipFile(artifact) as archive:
            if set(archive.namelist()) != set(REQUIRED) or len(archive.namelist()) != len(REQUIRED) or archive.testzip():
                raise ValidationError('Unexpected archive entries or failed CRC')
            for filename in REQUIRED:
                if hashlib.sha256(archive.read(filename)).hexdigest() != record['files'][filename]:
                    raise ValidationError('Packaged content checksum mismatch')
    return len(data['products'])

def csv_safe(value):
    text = str(value)
    return "'" + text if text.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else text

def description(p):
    return (f'<h2>{escape(p["name"])}</h2><p>{escape(p["problem"])}</p><p>For {escape(p["customer"])}.</p><ul>' + ''.join(f'<li>{escape(f)}</li>' for f in p['features']) + '</ul><p>Downloadable offline browser tool. Includes instructions, FAQ and single-business license. Use realistic fictional examples to learn the workflow, then enter your own assumptions. Inputs remain on your device; the product has no server connection. No physical item. Planning aid; verify assumptions independently. Introductory price is a hypothesis, not proven market value.</p>')

def build(root=ROOT, catalog_path=None, output=None):
    root = Path(root)
    data = load_catalog(catalog_path or root / 'product-factory/catalog.json')
    output = Path(output or root / 'releases')
    # Validate every input before writing outputs.
    for p in data['products']:
        validate_product(root / 'products' / p['slug'])
    output.mkdir(parents=True, exist_ok=True)
    published = []
    for p in data['products']:
        filename = f'{p["slug"]}-{p["version"]}.zip'
        artifact = output / filename
        hashes = package(root / 'products' / p['slug'], artifact)
        sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
        published.append({**p, 'approval_status': 'pending-owner-review', 'publication_status': 'unpublished', 'demand_status': 'unvalidated', 'artifact': filename, 'sha256': sha, 'files': hashes})
        listing = {**p, 'title': p['name'], 'description_html': description(p), 'status': 'draft', 'published': False, 'digital': True, 'ai_assistance_disclosure': 'Created with AI-assisted development and human owner review required.', 'benefits': ['Make assumptions explicit before quoting or committing cash', 'Compare planning scenarios without sharing private records with a server', 'Retain an export for your own review'], 'competitor_comparison': {'status': 'unverified market comparison', 'free_alternatives': 'A blank spreadsheet or manual calculation can solve parts of this problem. This package supplies a focused interface, validation and instructions. No superiority claim against named paid competitors is established.'}, 'faq_file': f'products/{p["slug"]}/FAQ.md', 'instructions_file': f'products/{p["slug"]}/GUIDE.md', 'license_file': f'products/{p["slug"]}/LICENSE.md', 'preview_source': f'products/{p["slug"]}/preview.svg', 'bundle_proposal': {'name': 'Service Business Planning Toolkit', 'price_usd': 89, 'status': 'hypothesis; not a live listing'}, 'manual_requirements': ['Review current marketplace policy and category', 'Upload preview and package manually', 'Configure digital fulfillment and test delivery', 'Owner approval before publishing']}
        (output / f'{p["slug"]}-listing.json').write_text(json.dumps(listing, indent=2) + '\n')
        (output / f'{p["slug"]}-etsy.md').write_text(f'# {p["name"]}\n\nDRAFT FOR OWNER REVIEW — not an upload file.\n\n{p["problem"]}\n\nFor: {p["customer"]}.\n\n' + '\n'.join('- ' + x for x in p['features']) + f'\n\nProposed USD price: {p["price"]:.2f}. Keywords: ' + ', '.join(p['keywords']) + '\n\nDigital download; open index.html in a modern browser. Planning aid, no professional advice. Single-business license; no redistribution. AI-assisted development: check current Etsy disclosure and creativity rules before listing. Review FAQ.md and GUIDE.md; convert preview.svg to marketplace-supported images and inspect screenshots. No sales claims or verified competitor superiority claims.\n')
    fields = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Variant SKU', 'Variant Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Status']
    with (output / 'shopify-products-draft.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fields)
        writer.writeheader()
        for p in data['products']:
            row = {'Handle': p['slug'], 'Title': p['name'], 'Body (HTML)': description(p), 'Vendor': 'Owner review required', 'Type': 'Digital planning tool', 'Tags': ', '.join(p['keywords']), 'Published': 'FALSE', 'Variant SKU': f'{p["slug"]}-{p["version"]}', 'Variant Price': f'{p["price"]:.2f}', 'Variant Requires Shipping': 'FALSE', 'Variant Taxable': 'TRUE', 'Variant Inventory Policy': 'continue', 'Variant Fulfillment Service': 'manual', 'Status': 'draft'}
            writer.writerow({k: csv_safe(v) for k, v in row.items()})
    (output / 'catalog.json').write_text(json.dumps({'schema_version': 1, 'currency': 'USD', 'products': published}, indent=2) + '\n')
    (output / 'SHA256SUMS').write_text(''.join(f'{p["sha256"]}  {p["artifact"]}\n' for p in published))
    (output / 'quality-report.json').write_text(json.dumps({'checks': ['manifest schema', 'required files', 'offline HTML references', 'path containment', 'known credential patterns', 'reproducible ZIP metadata', 'CRC integrity', 'SHA256 provenance'], 'passed': True, 'limitations': ['No automatic certification of originality or legal compliance', 'Browser workflow and accessibility review required', 'Credential pattern scanning is limited; owner review required', 'Commercial demand and prices are unvalidated', 'Shopify CSV does not configure digital download fulfillment or taxes']}, indent=2) + '\n')
    return published

def score(input_path, output):
    if Path(input_path).suffix.lower() == '.csv':
        with Path(input_path).open(newline='') as stream:
            raw = list(csv.DictReader(stream))
        rows = [{**r, 'name': r.get('niche', r.get('name')), 'sources': [], 'source_note': r.get('source_status', 'CSV does not include verified source URLs'), 'scores': {k: float(r[k]) for k in WEIGHTS}} for r in raw]
    else:
        rows = json.loads(Path(input_path).read_text())
    if isinstance(rows, dict):
        rows = rows.get('niches', rows.get('opportunities'))
    if not isinstance(rows, list):
        raise ValidationError('Research input must be list or {niches: [...]}')
    ranked = []
    for row in rows:
        ratings = row.get('scores', {})
        if set(ratings) != set(WEIGHTS) or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 1 <= v <= 5 for v in ratings.values()):
            raise ValidationError('Each opportunity needs six 1–5 scores: ' + ', '.join(WEIGHTS))
        if not row.get('name') or not isinstance(row.get('sources'), list):
            raise ValidationError('Name and sources list required; empty sources means hypothesis')
        ranked.append({**row, 'weighted_score': round(sum(ratings[k] * w for k, w in WEIGHTS.items()), 3), 'commercial_status': 'unvalidated'})
    ranked.sort(key=lambda x: (-x['weighted_score'], x['name']))
    Path(output).write_text(json.dumps({'weights': WEIGHTS, 'opportunities': ranked}, indent=2) + '\n')
    return ranked

def specs(catalog, output):
    data = load_catalog(catalog)
    Path(output).mkdir(parents=True, exist_ok=True)
    for p in data['products']:
        content = f'# Specification: {p["name"]} {p["version"]}\n\nCustomer: {p["customer"]}\n\nProblem: {p["problem"]}\n\n## Required behavior\n\n' + '\n'.join('- ' + f for f in p['features']) + '\n\n## Acceptance gates\n\n- Implement a dependency-free, offline browser tool with validated inputs.\n- Independently verify calculations and edge cases with tests.\n- Include guide, FAQ, single-business license and preview.\n- Validate responsive layout, keyboard use and exports manually.\n- Use fictional examples and explain financial assumptions.\n- Package only explicit manifest-approved files.\n- Demand remains unvalidated until approved customer experiments provide evidence.\n- Owner approves all publication and spending.\n'
        (Path(output) / f'{p["slug"]}-SPEC.md').write_text(content)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for action in ('build', 'check', 'verify'):
        p = sub.add_parser(action)
        p.add_argument('--catalog', default=str(ROOT / 'product-factory/catalog.json'))
        p.add_argument('--output', default=str(ROOT / 'releases'))
    p = sub.add_parser('score')
    p.add_argument('input'); p.add_argument('output')
    p = sub.add_parser('specs')
    p.add_argument('--catalog', default=str(ROOT / 'product-factory/catalog.json'))
    p.add_argument('--output', default=str(ROOT / 'product-factory/specs'))
    args = parser.parse_args()
    try:
        if args.command == 'build':
            print(json.dumps({'built': len(build(catalog_path=args.catalog, output=args.output)), 'published': False}))
        elif args.command == 'verify':
            print(json.dumps({'verified': verify_release(args.output)}))
        elif args.command == 'check':
            for p in load_catalog(args.catalog)['products']:
                validate_product(ROOT / 'products' / p['slug'])
            print('Product validation passed')
        elif args.command == 'score':
            print(json.dumps({'scored': len(score(args.input, args.output))}))
        else:
            specs(args.catalog, args.output)
            print('Specifications generated')
    except (ValidationError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Factory error: {exc}\n')
if __name__ == '__main__':
    main()
