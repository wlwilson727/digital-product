#!/usr/bin/env python3
"""Copy browser-tested fictional example screenshots into draft sales assets."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / 'test-results/browser-report.json').read_text())
if report.get('status') != 'passed':
    raise SystemExit('Run npm run test:browser successfully before preparing screenshots.')
catalog = json.loads((ROOT / 'product-factory/catalog.json').read_text())
out = ROOT / 'marketing/previews'
out.mkdir(parents=True, exist_ok=True)
for product in catalog['products']:
    slug = product['slug']
    for viewport in ('desktop', 'mobile'):
        source = ROOT / f'test-results/{slug}-{viewport}.png'
        if not source.is_file():
            raise SystemExit(f'Missing current browser screenshot: {source}')
        shutil.copyfile(source, out / source.name)
print('Prepared fictional-example PNG previews for 3 products; owner review required.')
