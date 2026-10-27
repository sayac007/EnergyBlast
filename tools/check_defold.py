"""Build and execute the actual native Defold 1.14 runtime, never a stale build."""
from pathlib import Path
import argparse,os,subprocess,tempfile,re
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--sdk',type=Path,default=Path('/tmp/energyblast-defold-tools'));a=p.parse_args();java=next(a.sdk.glob('Defold/packages/jdk-*/bin/java'))
with tempfile.TemporaryDirectory(prefix='energyblast-defold-test-',dir='/tmp')as d:
 state=Path(d)
 for name in ['data','cache','config']:(state/name).mkdir()
 env=dict(os.environ,XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1',PATH='/workspace/tools/xvfb/usr/bin:'+os.environ['PATH'])
 commands=[[str(java),'-Duser.home='+str(state/'java-user'),'-jar',str(a.sdk/'bob.jar'),'--root',str(ROOT/'pilots/defold'),'--platform','x86_64-linux','--max-cpu-threads','2','build'],['xvfb-run','-a',str(a.sdk/'dmengine'),'--config=project.test_mode=1',str(ROOT/'pilots/defold/build/default/game.projectc')]]
 commands+=[['xvfb-run','-a',str(a.sdk/'dmengine'),'--config=project.save_test='+mode,str(ROOT/'pilots/defold/build/default/game.projectc')]for mode in ['write','read']]
 for i,cmd in enumerate(commands):
  r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=90,cwd=ROOT);log=r.stdout+r.stderr
  if r.returncode or 'ERROR:'in log:print(log[-7000:]);raise SystemExit(r.returncode or 1)
  if i>0:
   expected=r'DEFOLD COMBAT: \d+ native checks PASS'if i==1 else('DEFOLD SAVE WRITE PASS'if i==2 else'DEFOLD SAVE RESTART PASS')
   assert re.search(expected,log),log
   print('\n'.join(line for line in log.splitlines()if 'PASS'in line))
