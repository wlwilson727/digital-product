# Digital Product Studio

An original digital-product business foundation: three offline planning tools, a reusable production pipeline, a CSV-powered operations dashboard, draft launch assets, and reproducible financial scenarios.

**Commercial status: unvalidated. Nothing is published. No actual sales, customer records, spending, live Shopify integration, or unattended service exists.** Public market-source requests were blocked by the cloud network policy; the 18-niche ranking is explicitly a hypothesis comparison. See [RESEARCH.md](RESEARCH.md).

## Run the workspace

Use this existing checkout; cloud tasks are already isolated. Do not create a Git worktree unless the owner requests one.

Requirements: Python 3.10+, Node 22+, npm 10+. Product runtime needs only a modern browser. Development browser tests use pinned Playwright and Chromium; the current cloud machine provides `/usr/bin/chromium`.

```sh
cd /workspace/digital-product
npm ci --ignore-scripts --no-audit --no-fund --cache /workspace/.npm-cache
make test
python3 product-factory/factory.py specs
python3 product-factory/factory.py check
python3 product-factory/factory.py build
python3 product-factory/factory.py verify
npm run test:browser
make serve
```

`make serve` runs a local development server on port 8000. The internal desk is `index.html`; the dashboard is `dashboard/index.html`. These are development paths, not public storefront links. Individual customer products can be unzipped and opened directly through their own `index.html`, without a server or internet access. The dashboard uses JavaScript modules and should use the development server.

If Chromium is elsewhere, set `CHROMIUM_PATH` for browser tests. For GitHub CI only, the workflow installs Playwright Chromium. Node/npm are development tools, not customer requirements. No API keys or Shopify credentials are needed for this local workflow.

## Repository map

| Location | Purpose |
|---|---|
| `products/` | Original applications, calculation modules, customer guides, FAQs, licenses, SVG previews |
| `product-factory/` | Manifest, scoring, specifications, validators, deterministic packaging and listing generation |
| `releases/` | Customer ZIPs, hashes, release catalog, unpublished Shopify CSV and listing drafts |
| `dashboard/` | Synthetic-data business dashboard and aggregate CSV templates |
| `research/`, `RESEARCH.md` | Eighteen niches, source access log, evidence limits and weighted comparison |
| `financial-models/` | Assumptions, conservative/moderate/optimistic scenarios and sensitivity calculations |
| `marketing/` | Budgeted demand tests, channel plan, platform investigation and support preparation |
| `automation/`, `AUTOMATION_PLAN.md` | Repeatable local jobs and future integration architecture |
| `tests/`, `docs/VALIDATION.md` | Independent calculations, CSV checks, package integrity, browser workflows and limitations |
| `TASKS.md`, `LAUNCH_CHECKLIST.md` | Remaining work and owner approval gates |

## Owner review

Start with the service-pricing tool. Proposed prices are test hypotheses, not verified market prices. Customer packages are review candidates; current browser testing cannot certify every browser or accessibility configuration.

Before selling: obtain permitted competitor and customer evidence, inspect products/licenses, approve a small demand experiment, then explicitly authorize a draft Shopify integration and end-to-end delivery test. File delivery, taxes, refunds, customer communications and listing policies require verification in the actual store. The CSV never configures these services.

See [BUSINESS_PLAN.md](BUSINESS_PLAN.md), [PRODUCT_CATALOG.md](PRODUCT_CATALOG.md), [COST_TRACKER.md](COST_TRACKER.md), [docs/AUTHORIZATION.md](docs/AUTHORIZATION.md), and the full [project brief](docs/PROJECT_BRIEF.md). Financial outputs estimate operating profit before taxes and owner-specific obligations, not guaranteed owner earnings.
