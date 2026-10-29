"""Build and execute the actual native Defold 1.14 runtime, never a stale build."""
from pathlib import Path
import argparse,os,subprocess,tempfile,re,signal,sys
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--sdk',type=Path,default=Path('/tmp/energyblast-defold-tools'));a=p.parse_args();java=next(a.sdk.glob('Defold/packages/jdk-*/bin/java'))
with tempfile.TemporaryDirectory(prefix='energyblast-defold-test-',dir='/tmp')as d:
 state=Path(d)
 for name in ['data','cache','config']:(state/name).mkdir()
 env=dict(os.environ,XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1',PATH='/workspace/tools/xvfb/usr/bin:'+os.environ['PATH'])
 commands=[[str(java),'-Duser.home='+str(state/'java-user'),'-jar',str(a.sdk/'bob.jar'),'--root',str(ROOT/'pilots/defold'),'--platform','x86_64-linux','--max-cpu-threads','2','build'],['xvfb-run','-a',str(a.sdk/'dmengine'),'--config=project.test_mode=1',str(ROOT/'pilots/defold/build/default/game.projectc')]]
 commands+=[['xvfb-run','-a',str(a.sdk/'dmengine'),'--config=project.save_test='+mode,str(ROOT/'pilots/defold/build/default/game.projectc')]for mode in ['write','read']]
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_ui.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_audio.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_depth.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_ui.py'),'--engine',str(a.sdk/'dmengine'),'--resize','1280','800'])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_traps.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_flow_ui.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_direct_touch.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_energy.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_resilience_ui.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_polish_ui.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_hero_glow.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_traps.py'),'--engine',str(a.sdk/'dmengine'),'--zoom','1.75'])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_replay_ui.py'),'--engine',str(a.sdk/'dmengine')])
 commands.append(['xvfb-run','-a','-s','-screen 0 1600x1600x24',sys.executable,str(ROOT/'tools/check_defold_power_ui.py'),'--engine',str(a.sdk/'dmengine')])
 for i,cmd in enumerate(commands):
  process=subprocess.Popen(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd=ROOT,start_new_session=True)
  try:log,_=process.communicate(timeout=90)
  except subprocess.TimeoutExpired:
   os.killpg(process.pid,signal.SIGKILL);log,_=process.communicate();print(log[-7000:]);raise
  code=process.returncode
  if code or 'ERROR:'in log:print(log[-7000:]);raise SystemExit(code or 1)
  if i>0:
   expected=r'DEFOLD COMBAT: \d+ native checks PASS'if i==1 else('DEFOLD SAVE WRITE PASS'if i==2 else'DEFOLD SAVE RESTART PASS'if i==3 else'DEFOLD NATIVE MENU AND FIRE CLICK PASS'if i in [4,7] else'DEFOLD ACTUAL MUSIC OUTPUT / MUTE PASS'if i==5 else'DEFOLD NATIVE FIELD TRAP CANCEL / THREE TYPES / BATTLEFIELD COORDINATES PASS'if i==8 else'DEFOLD NATIVE HERO / SPENDING / TREASURE / BONUS / NEXT FLOW PASS'if i==9 else'DEFOLD NATIVE HOLD FIRE / IMMEDIATE PADDED TARGET / DRAG / BUFFER PASS'if i==10 else'DEFOLD ACTUAL ENERGY SHIELD PIXEL PASS'if i==11 else'DEFOLD NATIVE REFILL / WEAPON / ARMOR / SANCTUARY PASS'if i==12 else'DEFOLD NATIVE ZOOM / SIX TREASURES / HINTS PASS'if i==13 else'DEFOLD ACTUAL HERO SHIMMER PIXEL PASS'if i==14 else'DEFOLD NATIVE FIELD TRAP CANCEL / THREE TYPES / BATTLEFIELD COORDINATES PASS'if i==15 else'DEFOLD NATIVE REPLAY BONUS / TREASURE / SAVED STARS PASS'if i==16 else'DEFOLD NATIVE BONUS POWER / MILLION HEALTH / GROWTH / SAVE PASS'if i==17 else'DEFOLD ACTUAL WALL OCCLUSION PASS')
   assert re.search(expected,log),log
   print('\n'.join(line for line in log.splitlines()if 'PASS'in line))
