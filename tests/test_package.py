import re,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class PackageTests(unittest.TestCase):
 def test_links(self):
  for p in R.rglob('*.md'):
   for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
    if '://' in dest or dest.startswith('#'): continue
    with self.subTest(file=str(p),link=dest): self.assertTrue((p.parent/dest.split('#')[0]).exists())
 def test_source_fingerprints(self):
  rows=json.loads((R/'references/upstream-sources.json').read_text());self.assertEqual(len(rows),4)
  for r in rows: self.assertRegex(r['blob_sha'],r'^[0-9a-f]{40}$')
 def test_portable_paths(self):
  for p in list((R/'references').glob('*.md'))+[R/'SKILL.md']: self.assertNotIn('/Users/meros/',p.read_text())
