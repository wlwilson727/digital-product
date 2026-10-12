# Automation architecture and limits

Use modular local scripts and explicit review gates instead of pretending each function needs a continuously running AI agent.

| Function | Current/local role | Future integration requirement | Control |
|---|---|---|---|
| Research | Dated CSV, source outcomes, scored hypotheses | Permitted sources and human evidence review | No restricted scraping or fabricated sales |
| Development | Reusable product calculation/UI modules | Local build environment | Original inputs; versioned deliverables |
| QA | Automated arithmetic/package checks | Browser runner for UI checks | Release blocked on failures |
| Listing preparation | Catalog and copy/previews/export build | Approved storefront access to upload | Preparation never equals publication |
| Operations | Local dashboard and CSV import | Store/payment exports or least-privilege API | Separate real/demo mode |
| Analytics | Financial model and reconciled CSV metrics | Consent-compliant actual event/order data | Actual contribution before recommendations |
| Support | Approved documentation and drafted FAQ replies | Inbox integration, policy and human review | Never send messages autonomously |
| Marketing | Intent pages, experiments and draft copy | Approved channels, consent and budget | No ads/outreach without approval |

The desired 80% automation is a target, not a measured result. Measure repeatable task count/time before and after automation; include exception handling and maintenance. A meaningful metric is `automated recurring task minutes / total recurring task minutes`, measured from actual operations, not script counts.

Codex stops when the session ends. Local scripts run only when invoked; continuous scheduling requires a deployed scheduler, approved hosting, credentials, retry policy, monitoring and accountable owner. A future nightly pipeline could import encrypted/private order exports, reconcile totals, refresh metrics and draft recommendations. It must never auto-spend, publish, refund, overwrite store settings or email customers. Required Shopify scopes should be chosen from the concrete future operation; start read-only and keep secrets in environment settings, never Git.

Maintain idempotent build steps, input schemas, provenance, version manifests and reproducible packages. Research facts require dated sources; model changes require expected-value tests; listings require approval; sensitive customer exports must be ignored/private and excluded from downloadable releases.
