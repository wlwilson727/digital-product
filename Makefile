.PHONY: install test build serve check
install:
	npm ci --ignore-scripts --no-audit --no-fund
test:
	node --test tests/test_*.mjs
	python3 -m unittest discover -s tests -p 'test_*.py'
check: test
	python3 product-factory/factory.py check
	node tests/browser.cjs
build:
	python3 product-factory/factory.py build
serve:
	python3 -m http.server 8000 --bind 127.0.0.1
