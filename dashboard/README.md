# Internal business operations dashboard

Run from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/dashboard/. No package installation, account, secret, or paid service is required. JavaScript modules require HTTP; double-clicking index.html is not supported. This local dashboard has no authentication: bind to localhost, and do not deploy with private data.

The initial records are fictional, clearly labeled synthetic examples. Product slugs match the prepared product catalog, but example orders, prices, costs, and status do not indicate verified sales or publication. No Shopify connection is implemented. Imported records are labeled user-imported and unverified.

## Use

1. Inspect the demonstration metrics and definitions. Download the CSV template or export the example as a structure reference.
2. Click **Start empty dataset** before entering real aggregate records. The confirmation explains the destructive replacement. Export a backup first.
3. Populate CSV with one unique ID per product/reporting period. Use exact headers. Import via **Import CSV (replace all)**. Invalid files leave the prior dataset unchanged. Valid files require confirmation before replacement.
4. Filter by product to review profit, conversion, CAC and monthly trends. Export to maintain an external backup.
5. Update development/approval/listing values by editing an export and replacing records. These values are user-supplied statuses, not verified storefront activity. Pending actions derive from the latest product status.

All amount fields are USD totals per row except price (USD per order). Delivery is the total variable fulfillment cost. Fixed costs should be allocated once; production expenses should be recorded once, not copied into every period. Orders and visits must use consistent reporting scopes. New customers may not exceed orders. Deduplicate customers manually across products to prevent understating CAC. Dashboard profit excludes taxes and owner distributions. See the expandable definitions inside the application.

No data leaves the browser through the application. Records persist in unencrypted localStorage on the current browser and origin until reset or storage deletion. Do not enter customer details, credentials or confidential financial records. Storage can be unavailable; then the application displays a warning and data survives only until refresh. Export backups. A different port/browser has a separate storage scope. Browser caches/downloads are outside this application's reset scope.

CSV headers are strict, record IDs unique, dates calendar-validated, numeric values finite and nonnegative, and integer counts enforced. Quotes, commas, CRLF and multiline quoted cells are supported. Spreadsheet formula prefixes are neutralized with an apostrophe on export; that apostrophe remains if reimported. Text renders with textContent instead of HTML. Maximum import size 2 MB and 10,000 records.

## Verification

```sh
node --test tests/test_dashboard.mjs
```

Tests independently check accounting, zero denominators, quoted CSV roundtrips, invalid types, malformed dates/CSV, duplicate IDs, and formula neutralization. Browser tests should additionally inspect responsive layout, import confirmation/cancel, filters, persistence/reset and downloads. No automated live-integration test applies because integrations are not implemented.
