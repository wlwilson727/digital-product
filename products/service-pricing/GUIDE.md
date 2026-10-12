# Service Price Lab — customer guide

## Who this helps
Independent service businesses, consultants and creative professionals who need a price that connects capacity, owner pay and overhead. It estimates a sustainable floor and target; it does not measure willingness to pay.

## Quick start
Extract all files together and open index.html. Load the fictional example, then replace each assumption. Export JSON to preserve editable inputs and CSV or PDF to discuss results. Changing currency changes formatting, never exchange rates.

## Inputs and definitions
- Working hours are total hours you intend to work, including administration.
- Working weeks exclude vacation, illness and closures. Billable share is the percentage of working time you expect customers to pay for.
- Annual overhead includes software, rent, insurance and other business costs, excluding direct job costs and owner pay. Avoid double counting.
- Owner take-home pay is the annual amount desired after the modeled owner tax reserve. Tax reserve is a rough effective rate, not a statutory tax calculation.
- Operating margin is additional business surplus after costs and modeled owner pay, as a share of revenue. It is not a markup on costs.
- Payment percentage is the fee as a share of revenue. Fixed payment fee applies once to each job.
- Hours per job reflect delivery plus job-specific preparation. Direct costs cover costs incurred once per job.

## Calculation method
Annual billable hours = weekly hours × working weeks × billable share.
Annual owner cost = take-home pay ÷ (1 − tax reserve).
Cost per billable hour = (overhead + annual owner cost) ÷ annual billable hours.
Target hourly service price = cost per hour ÷ (1 − margin − payment percentage). This service-hour figure excludes job materials and fixed payment fees.
Target job price = (cost per hour × job hours + direct job costs + fixed payment fee) ÷ (1 − margin − payment percentage).
Annual jobs = annual billable hours ÷ job hours. Fractional capacity is a planning average. Annual revenue = annual jobs × job price. Surplus subtracts payment fees, direct costs, overhead and owner cost from revenue. No rounded display figures are used inside formulas. General numeric inputs are limited to an absolute value of one trillion; percentage and capacity inputs have the narrower limits shown in the form.

## Fictional example and interpretation
A fictional design studio works 35 hours per week for 46 weeks with 65% billable utilization: 1,046.5 sellable hours. Its $60,000 take-home target and 25% reserve imply $80,000 owner cost, plus $18,000 overhead. A six-hour job also incurs $45 of materials. Compare the displayed target with actual customer conversations, scope and competing offers. These are invented inputs, not market benchmarks.

## Three practical exercises
1. **Capacity stress test:** reduce billable share by 10 percentage points and record how required price changes. Choose an achievable utilization level.
2. **Cost audit:** list the five largest overhead items. For each, record whether reducing it affects delivery quality, sales or risk. Enter only credible savings.
3. **Price validation:** quote the same well-defined scope to qualified prospects, record accepted and declined offers, and compare actual hours after delivery. Do not assume model output proves demand.

## Limits
No VAT/sales tax, progressive tax brackets, payroll rules, debt financing, inventory timing, refunds or capacity ramp-up are modeled automatically. Effective tax and payment-fee assumptions must be checked independently. All planned billable capacity is assumed sold; lower demand reduces realized revenue and can create losses. The app does not guarantee a feasible price.

## Saving and privacy
Browser storage is best-effort and may be unavailable for local files. Export JSON routinely and keep secure backups. Clear inputs before sharing the source folder on a shared computer. CSV report fields are unrounded numeric values; use spreadsheet number formatting for presentation. Printing includes input assumptions and displayed results.
