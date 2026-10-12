# Local automation and approval boundary

Run `bash automation/run-local.sh` from the checkout. It runs repository tests and generates product specs, draft listings and release archives. This is a finite local job. Codex does not keep operating after the session ends.

Research ingestion uses the product-factory scoring CLI. It consumes manually collected permitted evidence; no marketplace scraping is performed. Development requires actual implementation and independent tests. QA rejects structurally incomplete artifacts. Listing preparation always produces drafts. Operations uses the local dashboard and explicitly labeled synthetic demo data until owner-imported sales exist. Analytics recommendations remain estimates. Customer support can reuse approved FAQ/guide files; no email is sent. Marketing materials remain owner-reviewed drafts.

To schedule repeat execution later, use CI or an approved scheduler with a pinned runtime, minimal read permissions, and artifact uploads. Production publication, Shopify access, app installation, paid subscriptions, outreach, advertising and spending require explicit owner authorization. Future adapters should use least-privilege credentials from secret storage and separate dry-run preparation from authorized writes. An import CSV is not a credentialed Shopify integration.

Required launch sequence: review product behavior and license; verify marketplace requirements; approve listing copy and pricing; configure digital fulfillment only with store authorization; test an owner-approved checkout and delivery; confirm customer communications, refund process and taxes; publish only after explicit approval. Bundles can combine catalog products after review; there is no live bundle or upsell integration yet.
