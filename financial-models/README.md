# Financial planning model

Run `python financial-models/model.py` from the repository root. The standard-library CLI regenerates `assumptions.json`, `scenarios.csv` and `sensitivity.csv`. Supply `--assumptions path.json --output-dir path` for alternative scenarios using the same fields. Every number is a hypothesis; platform fee values are illustrative assumptions pending official-source/account verification. No demand, revenue or profitability has been measured.

Formula per initial paid order:

`contribution = price × (1 − refund rate) − price × processing fee rate − fixed transaction fee − CAC − support allowance`

`orders for target = ceil((monthly profit target + fixed operating cost) / contribution)`

`required sessions = ceil(orders / conversion)`

Gross sales include refunded orders. Fees are conservatively charged on the original order and assumed nonrefundable. CAC is a blended incremental acquisition cost per initially paid order, including refunded orders; it already represents advertising spending, so do not subtract advertising again. Support allowance represents a cash/labor provision; tax, owner salary, development labor, chargebacks, currency conversion and income-tax accounting are excluded. Fixed costs contain hosting + AI + subscriptions (zero paid hosting/AI in baseline; placeholder software/store reserve). Shopify subscription may already be paid by the existing business; inspect its incremental cost before treating it as new expense. Marketplace transaction/listing fees require a separate channel-specific rate, not layering a Gumroad fee on Shopify payment fees. Bulk discounts and bundle mix change average order value.

Conservative/moderate/optimistic are independent hypothetical business conditions, not probabilities. Owner earnings differ from modeled operating profit and require tax/cash distributions/accountant review. Annual $200,000–$300,000 earnings cannot be inferred from these targets.

Conversion and CAC are not independently observed. Sensitivity crosses them to expose traffic requirements; implied CPC = CAC × conversion, assuming paid traffic and one order per acquired customer. For example, fixed $0.50 CPC with 1% conversion implies $50 CAC, likely unprofitable at $49; at 4% conversion it implies $12.50 CAC. Holding CAC constant while varying conversion changes implied CPC and sessions, not contribution. Organic activity has time costs and cannot be assumed free or scalable.

Validate prices, refund rate, fee structure, paid clicks, attributed orders, repeat purchases, support minutes and conversion denominators with actual records. Reconcile payment processor payouts before evaluating realized profit. Zero or negative contribution produces blank (unreachable) units in CSV, rather than dividing by zero.
