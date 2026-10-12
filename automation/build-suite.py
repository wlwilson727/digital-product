"""Build a deterministic customer-only bundle without publishing or store access."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'releases'
catalog = json.loads((ROOT / 'product-factory/catalog.json').read_text())
# Workflow order follows price → scope → cash, independent of catalog order.
cards = ''.join(f'<article><p>{label}</p><h2>{name}</h2><p>{desc}</p><a href="{slug}/index.html">Open {name}</a></article>' for label, name, desc, slug in [
    ('01 · PRICE', 'Service Price Lab', 'Find the cost per billable hour and a sustainable target price.', 'service-pricing'),
    ('02 · SCOPE', 'Project Scope Studio', 'Turn a bounded scope into an estimate, deposit and change quote.', 'project-estimator'),
    ('03 · CASH', 'Cash Runway Planner', 'Schedule receipts and payments across thirteen weeks.', 'cashflow-planner')])
start = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Service Business Toolkit · Communication Artist</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f4fa;color:#202136;font:17px/1.6 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:56px 24px}small{color:#a90069;font-weight:700;letter-spacing:.12em}h1{font-size:clamp(32px,6vw,60px);line-height:1.08;margin:20px 0}h2{font-size:23px}section{margin-top:32px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}article,.guide{background:white;border:1px solid #ded9e8;border-radius:20px;padding:26px}article>p:first-child{font-size:13px;color:#a90069;font-weight:bold}a{color:#9d005e;text-underline-offset:4px}article a{display:inline-block;background:#a90069;color:white;padding:10px 16px;border-radius:10px;text-decoration:none}li{margin-bottom:10px}.note{font-size:14px;color:#55536b}a:focus-visible{outline:3px solid #2457e6;outline-offset:4px}@media print{body{background:white}main{padding:0}article{break-inside:avoid}}</style></head><body><main><small>COMMUNICATION ARTIST · VERSION 1.0</small><h1>Service Business Toolkit</h1><p>Price the work. Define the scope. Plan the cash.</p><p>Three independent browser tools for freelancers and small service businesses. Start with your own costs and capacity, then carry the assumptions into your project estimate and cash schedule.</p><section class="grid">''' + cards + '''</section><section class="guide"><h2>Start here</h2><ol><li>Extract the entire ZIP. Keep the folders together. Open this START-HERE.html file in a current desktop browser.</li><li>Open each tool and load its fictional example. Replace the sample assumptions before relying on the results.</li><li>Export editable JSON after each session. CSV is a report, not a backup of editable inputs. Print / save PDF uses your browser's print dialog.</li></ol><h2>Connect the tools without counting margin twice</h2><p>Use Service Price Lab's <strong>cost per billable hour</strong> as the labor cost rate in Project Scope Studio. Do not carry the target selling rate into that field unless you deliberately intend to add another margin. Enter project-specific direct costs once.</p><p>Enter the estimate's deposit and balance into Cash Runway Planner in the weeks you expect payment to reach your bank. Enter expenses when cash will leave. Owner-pay targets in the pricing tool do not automatically become cash payments.</p><p>These tools do not sync. Transfer figures manually and review them. The project estimator does not include payment fees; allow for those separately when reconciling a price.</p><h2>A worked example</h2><p>A fictional studio has $20,000 annual overhead and $60,000 desired take-home pay, with a 25% owner tax reserve. At 40 hours a week, 50 weeks and 50% billable time, its 1,000 billable hours carry $100 cost per hour.</p><p>A 10-hour project with $100 direct costs costs $1,100. In Project Scope Studio, a 10% contingency and 20% margin produce a $1,512.50 quote before any discount. A 40% deposit is $605; the remaining balance is $907.50.</p><p>For the cash schedule, assume $2,000 opening cash and a $1,000 reserve. If the $605 deposit arrives in week one and $700 of payments leave, closing cash is $1,905. If the $907.50 balance arrives in week two and $400 leaves, closing cash is $2,412.50. These are invented figures, not market benchmarks.</p><h2>Weekly review</h2><ol><li>Compare actual project hours with your estimate and revise future assumptions.</li><li>Move delayed receipts to their expected collection week. Check the lowest cash balance and reserve gap.</li><li>Save dated JSON backups for each tool; protect files containing client or financial information.</li></ol><h2>Guides and license</h2><p>Each product folder contains its GUIDE, FAQ and single-business LICENSE. Open the .md files in a text editor if your browser downloads them. The license permits use for one business and its client work; it does not permit redistribution of the software.</p><p class="note">No subscription, account or API key is required. No automatic bank feeds, tax calculations, signatures or invoicing are included. Browser storage may be unavailable for local files; use JSON backups. These are planning estimates with no guarantee of income or profit. Direct-file compatibility, Safari/Firefox and live download delivery still need customer-environment acceptance checks before sale.</p></section></main></body></html>'''
entries = {'START-HERE.html': start.encode()}
for product in catalog['products']:
    folder = ROOT / 'products' / product['slug']
    for file in sorted(folder.rglob('*')):
        if file.is_file():
            entries[f'{product["slug"]}/{file.relative_to(folder).as_posix()}'] = file.read_bytes()
archive = OUT / 'service-business-toolkit-1.0.0.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for name, data in sorted(entries.items()):
        info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, data)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(entries)
    for name, data in entries.items():
        assert z.read(name) == data
    for slug in ['service-pricing', 'project-estimator', 'cashflow-planner']:
        assert f'{slug}/index.html' in z.namelist()
(OUT / 'service-business-toolkit-START-HERE.html').write_text(start)
(OUT / 'service-business-toolkit-manifest.json').write_text(json.dumps({
    'name': 'Service Business Toolkit', 'version': '1.0.0', 'status': 'unpublished-review-candidate',
    'proposed_test_price_usd': 89, 'archive': archive.name,
    'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    'entries': {k: hashlib.sha256(v).hexdigest() for k, v in sorted(entries.items())}
}, indent=2) + '\n')
print(f'Built and verified {archive.name}: {len(entries)} customer files')
