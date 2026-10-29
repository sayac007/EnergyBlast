"""Replay actual native optional challenges from a fully earned/purchased old save.

Run under Xvfb after a successful Bob build. The explicit fixture only seeds an
old ledger, stages the player and disables hostile AI. Real XTest taps fire live
projectiles, solve all six pattern tasks, walk to all six chests, reload each
mission and restart the native process. No task/hit/reward is forced by a fixture.
Desktop XTest is not a claim of a physical Android device test.
"""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py):
 xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(.055)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.18)
def screenshot(root,name):
 if a.output:ImageGrab.grab().crop((0,0,1280,720)).save(root/(name+'.png'))

with tempfile.TemporaryDirectory(prefix='energyblast-native-replay-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
 for folder in ['data','cache','config']:(root/folder).mkdir()
 env=dict(os.environ,XDG_DATA_HOME=str(root/'data'),XDG_CACHE_HOME=str(root/'cache'),XDG_CONFIG_HOME=str(root/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
 cmd=[str(a.engine),'--config=project.replay_ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')]
 for restart in [False,True]:
  log=root/('restart.log'if restart else'runtime.log')
  def wait(pattern,after=0,timeout=8):
   deadline=time.monotonic()+timeout
   while time.monotonic()<deadline:
    text=log.read_text();assert 'ERROR:'not in text,text
    match=re.search(pattern,text[after:])
    if match:return match
    time.sleep(.025)
   raise AssertionError('Missing '+pattern+'\n'+log.read_text())
  def choose(index,mission,visit):
   before=len(log.read_text());click(772 if index%2==0 else 1090,534-(index//2)*153)
   m=wait(r'DEFOLD REPLAY CHOOSE mission='+mission+r' visit='+str(visit)+r' alive=(\d+) bonus_done=0 treasure=true score=4350 wallet=4090',before)
   expected=4 if mission in ['reactor','dock','forge']else 2
   assert int(m.group(1))==expected,log.read_text()
   wait('DEFOLD REPLAY SCENE READY mission='+mission,before)
   return before
  with log.open('w')as stream:
   process=subprocess.Popen(cmd,env=env,stdout=stream,stderr=subprocess.STDOUT)
   try:
    wait('DEFOLD REPLAY MENU READY score=4350 wallet=4090 restarted='+str(restart).lower())
    if restart:
     choose(0,'reactor',1)
     screenshot(root,'restart-rearmed')
     print('DEFOLD NATIVE REPLAY SAVE / PROCESS RESTART / PURCHASES PASS',flush=True)
    else:
     for index,mission in enumerate(['reactor','citadel','dock','forge','echo','rescue']):
      before=choose(index,mission,1)
      screenshot(root,mission+'-rearmed')
      radio_start=len(log.read_text());click(1208,210)
      wait('DEFOLD REPLAY VOICE mission='+mission+r' id=bonus_(sequence|wait)',radio_start)
      print('DEFOLD NATIVE REPLAY CONTEXT RADIO '+mission.upper()+' PASS',flush=True)
      # Actual HINWEIS uses the mission guidance path; an earned chest must
      # not suppress an unfinished/rearmed bonus with "already collected".
      click(72,210)
      wait('DEFOLD REPLAY HINT PASS mission='+mission+r' goal=bonus voice=bonus_(sequence|wait)',before)
      screenshot(root,mission+'-hint')
      sequence=mission in ['reactor','dock','forge'];steps=3 if sequence else 1
      for progress in range(steps):
       m=wait(r'DEFOLD REPLAY SHOT READY mission='+mission+' progress='+str(progress)+r' x=(\d+) y=(\d+) kind=' +('sequence'if sequence else'wait'),before)
       px,py=map(int,m.groups());assert 144<px<1136 and 96<py<624,(mission,px,py)
       click(px,py)
      wait('DEFOLD REPLAY BONUS PASS mission='+mission+r' shots=\d+ score=4350 wallet=4090 delta=0',before)
      m=wait('DEFOLD REPLAY CHEST READY mission='+mission+r' x=(\d+) y=(\d+) visible=true',before)
      screenshot(root,mission+'-chest')
      click(*map(int,m.groups()))
      wait('DEFOLD REPLAY CHEST PASS mission='+mission+' score=4350 wallet=4090 delta=0',before)
      screenshot(root,mission+'-found')
      # The same real mission card reloads a live scene a second time, while
      # all lifetime stars and purchased equipment remain intact.
      click(1215,674);choose(index,mission,2);screenshot(root,mission+'-second-visit')
      click(1215,674)
      print('DEFOLD NATIVE REPLAY '+mission.upper()+' / BONUS SHOT / CHEST WALK / RELOAD / NO DUPLICATE STARS PASS',flush=True)
    assert 'ERROR:'not in log.read_text(),log.read_text()
   finally:
    process.terminate();process.wait(timeout=5)
 print('DEFOLD NATIVE REPLAY BONUS / TREASURE / SAVED STARS PASS')
