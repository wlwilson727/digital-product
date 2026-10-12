#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.mjs
python3 product-factory/factory.py specs
python3 product-factory/factory.py build
python3 product-factory/factory.py verify
