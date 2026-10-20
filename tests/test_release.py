import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
spec = importlib.util.spec_from_file_location('package', Path(__file__).resolve().parents[1]/'scripts/package.py')
pkg = importlib.util.module_from_spec(spec); spec.loader.exec_module(pkg)

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name); self.src = self.base/'src'; self.src.mkdir()
        for name in pkg.REQUIRED:
            p=self.src/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('fixture')
        self.zip=self.base/'skill.zip'; pkg.build(self.src,self.zip)
    def test_build_extract_verify(self):
        dest=self.base/'extract'
        with zipfile.ZipFile(self.zip) as z: z.extractall(dest)
        self.assertEqual(pkg.verify(dest/'fde-problem-framing'),pkg.verify(self.src))
    def test_missing_reference_rejected(self):
        (self.src/'references/dialogue.md').unlink()
        with self.assertRaises(ValueError): pkg.verify(self.src)
    def test_modified_file_rejected(self):
        (self.src/'SKILL.md').write_text('changed')
        with self.assertRaises(ValueError): pkg.verify(self.src)
    def test_extra_file_rejected(self):
        (self.src/'private-notes').write_text('local')
        with self.assertRaises(ValueError): pkg.verify(self.src)
    def test_unsafe_manifest_rejected(self):
        for name in ['../outside','/tmp/out','a/../b','a\\b','C:/x']:
            (self.src/'MANIFEST.json').write_text(json.dumps({name:'0'*64}))
            with self.assertRaises(ValueError): pkg.verify(self.src)
    def test_symlink_rejected(self):
        (self.src/'link').symlink_to(self.src/'SKILL.md')
        with self.assertRaises(ValueError): pkg.build(self.src,self.zip)
    def test_install_and_safe_update(self):
        dest=self.base/'skills/installed';pkg.install(self.src,dest)
        with self.assertRaises(ValueError): pkg.install(self.src,dest)
        (self.src/'SKILL.md').write_text('new');pkg.build(self.src,self.zip)
        backup=pkg.install(self.src,dest,True,self.base/'backups')
        self.assertEqual((dest/'SKILL.md').read_text(),'new')
        self.assertEqual((backup/'SKILL.md').read_text(),'fixture')
        pkg.verify(dest)
    def test_preserve_local_edits(self):
        dest=self.base/'skills/installed';pkg.install(self.src,dest)
        (dest/'SKILL.md').write_text('user edit')
        with self.assertRaises(ValueError):pkg.install(self.src,dest,True,self.base/'backups')
        self.assertEqual((dest/'SKILL.md').read_text(),'user edit')
    def test_no_recursive_release(self):
        with self.assertRaises(ValueError):pkg.build(self.src,self.src/'release.zip')
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):pkg.install(self.src,self.src/'nested')
    def test_update_requires_external_backup(self):
        dest=self.base/'skills/installed';pkg.install(self.src,dest)
        with self.assertRaises(ValueError):pkg.install(self.src,dest,True)
        with self.assertRaises(ValueError):pkg.install(self.src,dest,True,self.base/'skills/backups')
        pkg.verify(dest)
    def test_update_rejects_incomplete_old_install(self):
        dest=self.base/'skills/installed';pkg.install(self.src,dest)
        (dest/'references/dialogue.md').unlink()
        with self.assertRaises(ValueError):pkg.install(self.src,dest,True,self.base/'backups')
        self.assertTrue((dest/'SKILL.md').exists())
    def test_build_is_reproducible(self):
        second=self.base/'second.zip';pkg.build(self.src,second)
        self.assertEqual(self.zip.read_bytes(),second.read_bytes())
    def test_git_metadata_not_distributed(self):
        (self.src/'.git').mkdir();(self.src/'.git/config').write_text('private configuration')
        pkg.build(self.src,self.zip)
        with zipfile.ZipFile(self.zip) as z:
            self.assertFalse(any('/.git/' in name for name in z.namelist()))
