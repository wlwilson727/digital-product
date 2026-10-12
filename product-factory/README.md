# Product factory

Python 3.10+ standard library; no paid services, accounts or API keys. This repository already runs in an isolated cloud checkout: use it directly; do not create worktrees unless the owner requests one.

```sh
python3 -m unittest discover -s tests -p 'test_factory*.py'
python3 product-factory/factory.py specs
python3 product-factory/factory.py check
python3 product-factory/factory.py build
python3 product-factory/factory.py verify
python3 product-factory/factory.py score product-factory/opportunities-example.json /tmp/ranked-opportunities.json
```

The versioned `catalog.json` is the production manifest. Add a catalog record for a new original product, generate a specification, implement its eight required files under `products/<slug>/`, add independently verified calculation tests, and run checks/build. The specification template is reusable; it does not invent product implementations. Supported production format: self-contained, offline HTML/CSS/JavaScript browser tools. Adding other formats requires an explicit validator and packager.

`factory.py` separates catalog validation, research scoring, specifications, product checks, package generation and listing preparation. Only eight allowed files enter each archive. Product HTML references must stay within that list. Symlinks, missing files, known credential patterns, external dependencies and unsafe links fail validation. ZIP metadata is fixed, entries are sorted, and CRC and SHA256 checks document content integrity. Rebuild in the same Python runtime produces identical archives. Different compression-library versions can affect bytes; hashes identify the actual artifact. No timestamps or synthetic sales enter releases.

`releases/catalog.json` records versions, file hashes, proposed prices, unpublished approval status and unvalidated commercial demand. Shopify CSV uses `Published=FALSE` and `Status=draft`; it is a manual import starting point, not fulfillment setup. Product listing JSON and Etsy markdown are preparation files, not live integrations. CSV formula-prefix escaping protects text in spreadsheet software. Check imported values in a staging preview: the leading apostrophe can remain visible. Taxable=TRUE is a conservative import default requiring store-jurisdiction review; no tax advice is implied.

`opportunities-example.json` demonstrates the scoring contract, not market evidence. The scorer also accepts research/niches.csv with the six named score columns and preserves its evidence status; CSV input has no asserted verified URLs. Supply permitted real research as an array of `{name,sources,scores}`. Scores are 1–5 for demand (25%), profit (20%), differentiation (15%), automation (15%), acquisition (15%) and simplicity (10%). Preserve evidence, collection date and uncertainty as additional fields; the scorer carries them through. Rankings organize hypotheses and cannot establish demand by themselves.

Build checks are structural and integrity checks. Independent calculation tests, browser workflow tests and human reviews must also pass. The scanner is limited and cannot prove that secrets are absent, copyright ownership, legal compliance, accessibility, security or commercial viability. Inspect content, assumptions, licensing, preview screenshots, keyboard/mobile behavior and delivery before approval. No code in this factory deploys, publishes, contacts customers or spends money.
