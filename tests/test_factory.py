import csv
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'product-factory/factory.py'
spec = importlib.util.spec_from_file_location('factory', MODULE)
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)

class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.folder = self.root / 'products/sample-tool'
        self.folder.mkdir(parents=True)
        for name in f.REQUIRED:
            (self.folder / name).write_text('Original substantive content for customer use.\n')
        (self.folder / 'index.html').write_text('<html><head><link href="style.css"></head><body><script src="app.js"></script><a href="GUIDE.md">Guide</a></body></html>')
        self.product = {'slug':'sample-tool','version':'1.0.0','name':'Sample Tool','customer':'Freelancers','problem':'Prepare estimates','category':'Business','price':29,'features':['Export CSV'],'keywords':['estimates'],'upsells':[]}
        self.catalog = self.root / 'catalog.json'
        self.write_catalog()
    def write_catalog(self):
        self.catalog.write_text(json.dumps({'schema_version':1,'currency':'USD','products':[self.product]}))
    def tearDown(self):
        self.temp.cleanup()
    def test_reproducible_archive_and_content_integrity(self):
        a, b = self.root/'a.zip', self.root/'b.zip'
        hashes = f.package(self.folder, a)
        (self.folder/'GUIDE.md').touch()
        f.package(self.folder, b)
        self.assertEqual(a.read_bytes(), b.read_bytes())
        with zipfile.ZipFile(a) as z:
            self.assertEqual(set(z.namelist()), set(f.REQUIRED))
            self.assertIsNone(z.testzip())
            self.assertEqual(hashes['GUIDE.md'], f.hashlib.sha256(z.read('GUIDE.md')).hexdigest())
    def test_traversal_and_external_links_rejected(self):
        for link in ('../catalog.json','/etc/passwd','https://example.com/a.js','javascript:alert(1)','//example.com/a.js'):
            with self.subTest(link=link):
                (self.folder/'index.html').write_text(f'<html><a href="{link}">unsafe target</a></html>')
                with self.assertRaises(f.ValidationError):
                    f.validate_product(self.folder)
    def test_unbundled_file_rejected(self):
        (self.folder/'bonus.txt').write_text('Important content')
        (self.folder/'index.html').write_text('<a href="bonus.txt">Bonus file</a>')
        with self.assertRaises(f.ValidationError):
            f.validate_product(self.folder)
    def test_symlink_and_secret_rejected(self):
        (self.folder/'app.js').unlink()
        (self.folder/'app.js').symlink_to(self.catalog)
        with self.assertRaises(f.ValidationError):
            f.validate_product(self.folder)
        (self.folder/'app.js').unlink()
        (self.folder/'app.js').write_text('-----BEGIN PRIVATE KEY-----')
        with self.assertRaises(f.ValidationError):
            f.validate_product(self.folder)
    def test_schema_rejects_invalid_price_slug_and_version(self):
        for field, value in [('slug','../../etc'),('version','latest'),('price',0),('price',float('nan')),('price',True),('features',[])]:
            with self.subTest(field=field):
                original = self.product[field]
                self.product[field] = value
                self.write_catalog()
                with self.assertRaises(f.ValidationError):
                    f.load_catalog(self.catalog)
                self.product[field] = original
    def test_drafts_and_csv_injection(self):
        self.product['name'] = '=HYPERLINK("malicious")'
        self.write_catalog()
        out = self.root/'release'
        records = f.build(self.root, self.catalog, out)
        with (out/'shopify-products-draft.csv').open() as stream:
            row = next(csv.DictReader(stream))
        self.assertEqual(row['Published'], 'FALSE')
        self.assertEqual(row['Status'], 'draft')
        self.assertTrue(row['Title'].startswith("'="))
        self.assertEqual(records[0]['publication_status'],'unpublished')
        self.assertTrue(records[0]['sha256'])
    def test_release_verification_detects_modified_artifact(self):
        output = self.root/'releases'
        records = f.build(self.root, self.catalog, output)
        self.assertEqual(f.verify_release(output), 1)
        artifact = output/records[0]['artifact']
        with artifact.open('ab') as stream:
            stream.write(b'altered')
        with self.assertRaises(f.ValidationError):
            f.verify_release(output)
    def test_failure_does_not_write_releases(self):
        (self.folder/'GUIDE.md').unlink()
        output = self.root/'releases'
        with self.assertRaises(f.ValidationError):
            f.build(self.root, self.catalog, output)
        self.assertFalse(output.exists())
    def test_opportunity_weights_and_invalid_rating(self):
        research = self.root/'research.json'
        out = self.root/'ranked.json'
        research.write_text(json.dumps([{'name':'A','sources':[],'scores':{k:5 for k in f.WEIGHTS}}, {'name':'B','sources':[],'scores':{k:1 for k in f.WEIGHTS}}]))
        result = f.score(research,out)
        self.assertEqual(result[0]['weighted_score'],5)
        self.assertEqual(result[1]['weighted_score'],1)
        self.assertEqual(result[0]['commercial_status'],'unvalidated')
        research.write_text(json.dumps([{'name':'A','sources':[],'scores':{k:float('nan') for k in f.WEIGHTS}}]))
        with self.assertRaises(f.ValidationError):
            f.score(research,out)
if __name__ == '__main__':
    unittest.main()
