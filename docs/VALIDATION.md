# Validation evidence

Executed October 11, 2026, America/Chicago, in the current cloud workspace. This report concerns locally built tools, not a live store or demand validation.

| Check | Actual result |
|---|---|
| `make test` | 20 Node tests passed (16 product calculations, 4 dashboard); 13 Python tests passed (9 factory, 4 financial) |
| `python3 product-factory/factory.py build` | Three unpublished version 1.0.0 customer archives and listing drafts generated |
| `python3 product-factory/factory.py verify` | Three archives passed catalog hash, entry/content hash and archive integrity verification |
| `npm run test:browser` | 18 recorded workflow checks passed in Chromium 154 using pinned Playwright 1.64.0 |
| Financial CLI | Conservative, moderate, optimistic target calculations and 24 CAC/conversion sensitivities executed; fresh output reproduced committed scenario values |
| Persistent local HTTP startup | Dashboard response contains expected application and data-handling text |
| Public market-source access | 13 requests blocked by cloud proxy; no current prices, demand, reviews, or fulfillment policies verified |

The browser checks exercise independent calculation scenarios for all three tools, numeric-input recalculation, editable JSON roundtrips, invalid-import recovery, CSV downloads, print controls and PDF rendering. They test dashboard CSV template download, schema-error preservation, successful import with independently expected $87 operating profit, text injection safety, persistence, reset and empty controls. Desktop and 390-pixel layouts have no page-level horizontal overflow. Product local startup uses no external network destinations. Screenshot inspection covered desktop pricing and narrow cashflow layouts; wide tables deliberately scroll inside their containers.

Calculation cases include owner-pay gross-up, capacity, margin rather than markup, payment fees, signed financing, reserve thresholds, starting cash deficits, scope-change pricing, discounts, deposits, zero denominators, malformed data, extreme finite input rejection and no input mutation. Package tests include fixed ZIP metadata, reproducibility, traversal rejection, CSV formula escaping and tamper detection.

`docs/browser-report.json` preserves the actual browser runner's outcomes. Fresh screenshots and PDFs are written under ignored `test-results/`; approved-example PNG candidates are copied to `marketing/previews/`. Run `npm run test:browser` then `python3 automation/prepare-previews.py` to refresh preview candidates after a reviewed product change.

## Blocked and manual checks

**Three direct-file startup checks were blocked**, rather than passed: this machine's managed Chromium policy returns `ERR_BLOCKED_BY_ADMINISTRATOR` for `file:` URLs. The same assets function through a local server. No policy bypass was attempted. Customer instructions target direct offline file use, which must be manually checked in a normal customer browser before sale. Screen-reader use, full keyboard audit, Safari/Firefox compatibility, mobile-device printing, real Shopify upload/import, checkout, delivery, refunds, taxes and current marketplace policy remain unverified.

The three ZIPs are complete review candidates, not certified universally compatible products. Automated structural/credential/license checks have limited coverage; they cannot prove originality, certify legal compliance, or replace owner review. No tests establish willingness to pay, profitable acquisition, actual sales or owner earnings.

## Reproduction

```sh
npm ci --ignore-scripts --no-audit --no-fund --cache /workspace/.npm-cache
make test
python3 product-factory/factory.py check
python3 product-factory/factory.py build
python3 product-factory/factory.py verify
npm run test:browser
python3 financial-models/model.py --output-dir /tmp/digital-product-financial-check
```

The manual GitHub Actions workflow runs these checks when dispatched; it has not been executed remotely. Its browser uses downloaded Playwright Chromium, so cloud-machine file-policy results can differ. Builds do not automatically publish, deploy, spend or send messages.
