# Service Business Toolkit

The chosen first suite is Service Price Lab ($39 proposed test price), Project Scope Studio ($39), and Cash Runway Planner ($49). The proposed combined price is $89. These are test prices, not proven willingness to pay.

This suite extends the working repository products rather than introducing three unrelated industry prototypes. It follows one customer workflow: establish labor economics, price a bounded project, then schedule receipts and expenses. The suite start page explains manual transfer and prevents using a selling rate as a cost rate and adding margin twice.

Build the combined customer download with `python3 automation/build-suite.py`. The resulting `releases/service-business-toolkit-1.0.0.zip` contains 25 customer files: a branded START-HERE.html with a worked example and all three complete product folders. The companion manifest records each entry's SHA-256. It includes no internal dashboard, research, customer data or credentials. Nothing is installed, uploaded to Shopify or published by this command.

## Validation of this build

The resumed checkout passed all 20 Node tests and 13 Python tests, product structural checks, and verification of the existing three individual archives. The bundle builder verifies all 25 ZIP entries and their bytes. The worked example independently gives $100 labor cost/hour, $1,512.50 project quote, $605 deposit, $907.50 balance, and week-one/week-two cash of $1,905/$2,412.50.

The combined archive rebuilt byte-for-byte identically. All 21 local HTML links and asset references resolve inside the ZIP. A browser executable is unavailable in this resumed environment, so browser execution was not repeated and the new start page has not received visual browser QA. Live purchase/download delivery and the previously documented manual browser checks remain necessary before sale. Shopify was inspected separately, but this build changes no store settings or product records.
