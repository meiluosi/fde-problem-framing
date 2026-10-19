"""在临时目录模拟整包复制，不改用户技能配置。"""
from pathlib import Path
import tempfile,shutil,subprocess,sys
source=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='fde-skill-install-') as temp:
 dest=Path(temp)/'skills'/source.name
 shutil.copytree(source,dest,ignore=shutil.ignore_patterns('__pycache__'))
 assert (dest/'SKILL.md').is_file()
 result=subprocess.run([sys.executable,str(dest/'scripts/check_math.py'),'--stage','20','--share','.5','--target','22'],cwd=temp,capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 import json
 assert json.loads(result.stdout)['allowed_stage']==2
 print('PASS: 完整复制后，从其他工作目录执行脚本成功；未改真实安装目录。')
