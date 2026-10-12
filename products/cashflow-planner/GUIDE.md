# Cash Runway Planner — customer guide

## Who this helps
Owner-managed businesses and freelancers needing a short-term view of bank cash, late receipts and upcoming obligations. This is a cash schedule, not an income statement or bank reconciliation.

## Start in 15 minutes
1. Open index.html from the extracted folder and load the fictional example.
2. Replace opening cash with usable bank cash at the start of your first week. You can enter negative cash to represent an overdraft. Do not count unavailable credit as cash.
3. Set the cash reserve needed for essential obligations.
4. Rename each weekly row with your week-ending date. Enter receipts when you expect cash to reach the bank, not when you invoice.
5. Enter payments in the week due, including tax payments, wages, supplier costs and owner withdrawals if you choose to classify them there.
6. Enter actual expected financing separately: positive for borrowing or capital, negative for principal repayment or distributions. Avoid counting the same movement as both a payment and financing.
7. Export JSON, CSV and a dated PDF for your review meeting.

## Method
Scenario receipts = base receipts × receipts scenario percentage. Scenario payments = base payments × payments scenario percentage. Financing is unchanged by those multipliers. Weekly closing = opening + scenario receipts − scenario payments + financing. The next week's opening equals the previous closing. Reserve gap = max(0, reserve − closing). Peak funding need is the largest reserve gap including the starting position; it is not the sum of weekly gaps. Lowest cash also includes the starting position. First below-reserve and first negative alerts refer to weekly closing balances, so a separate notice flags an already-insufficient opening position.

## Fictional example
A fictional agency starts with $12,000 and keeps a $5,000 reserve. Receipts vary because client payments arrive unevenly. A $7,000 payment week illustrates cash timing pressure. These amounts do not represent actual customer performance or a forecast for your business.

## Repeatable weekly review
- Compare last week's actual cash movements with expectations. Explain timing changes before revising amounts.
- Move delayed receipts to their new expected dates; do not simply delete a shortfall.
- Compare a downside scenario, such as 80% receipts and 110% payments, with the base case. Uniform multipliers are stress tests, not probabilities.
- Note three actions with owners and dates: collect a specific invoice, reschedule a discretionary expense by agreement, or arrange approved financing.
- Save a new JSON file with the date. Roll your schedule manually by relabeling weeks and updating amounts. Keep previous versions for comparison.

## Limits and judgment
Weekly summaries can hide intraweek shortfalls. Check daily timing when headroom is tight. There is no automatic bank feed, interest accrual, currency conversion, tax calculation or loan amortization. Negative financing is allowed but does not validate lender terms. Forecast receipts are uncertain; funded cash must be independently confirmed. A zero funding need is conditional on entered assumptions and does not establish solvency. No automatic calendar or rollover is included. General numeric inputs are limited to an absolute value of one trillion; scenario percentages are limited to 0–300%.

## Exports and privacy
CSV contains scenario-adjusted weekly results and is for reporting; JSON preserves base inputs and scenario settings for re-import. No data is sent to a server. Browser saves are best-effort: maintain JSON backups. Protect exports as business financial records. Printing includes the whole 13-week table, summary and scenario inputs.
