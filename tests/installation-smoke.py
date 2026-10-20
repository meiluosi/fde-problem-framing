"""Build/extract/verify/install in a temporary directory; never edits host settings."""
from pathlib import Path
import importlib.util,json,shutil,subprocess,sys,tempfile,zipfile
source=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('package',source/'scripts/package.py')
package=importlib.util.module_from_spec(spec);spec.loader.exec_module(package)
with tempfile.TemporaryDirectory(prefix='fde-skill-install-') as temp:
 base=Path(temp);copy=base/'source'
 shutil.copytree(source,copy,ignore=shutil.ignore_patterns('.git','__pycache__','.DS_Store'))
 archive=package.build(copy,base/'release.zip')
 with zipfile.ZipFile(archive) as z:z.extractall(base/'unpacked')
 unpacked=base/'unpacked/fde-problem-framing'
 package.verify(unpacked)
 dest=base/'skills/fde-problem-framing';package.install(unpacked,dest)
 package.verify(dest)
 result=subprocess.run([sys.executable,str(dest/'scripts/check_math.py'),'--stage','20','--share','.5','--target','22'],cwd=base,capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 assert json.loads(result.stdout)['allowed_stage']==2
 print('PASS: release built, extracted, full manifest verified, installed and executed from unrelated directory.')
