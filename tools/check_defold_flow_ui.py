"""Real native taps exercise discoverable heroes, spending and the next-mission path.

The win fixture calls the real completion path in a controlled test process; it
does not claim a manually completed mission. All navigation is actual GUI input.
"""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py):
 xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(.07)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.18)
with tempfile.TemporaryDirectory(prefix='energyblast-native-flow-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
 for name,win in [('menu-shop',False),('next-with-unfound-treasure',True),('optional-loot',True)]:
  state=root/name;state.mkdir();log=state/'runtime.log'
  for folder in ['data','cache','config']:(state/folder).mkdir()
  env=dict(os.environ,XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
  def wait(marker):
   until=time.monotonic()+8
   while time.monotonic()<until:
    text=log.read_text()
    if marker in text:return text
    if 'ERROR:'in text:raise AssertionError(text)
    time.sleep(.03)
   raise AssertionError(log.read_text())
  def capture(label):
   if a.output:ImageGrab.grab().crop((0,0,1280,720)).save(state/(label+'.png'))
  cmd=[str(a.engine),'--config=project.flow_ui_test=1']
  if win:cmd+=['--config=project.flow_win=1']
  cmd+=[str(ROOT/'pilots/defold/build/default/game.projectc')]
  with log.open('w')as stream:
   process=subprocess.Popen(cmd,env=env,stdout=stream,stderr=subprocess.STDOUT)
   try:
    if not win:
     wait('DEFOLD FLOW MENU READY');capture('menu')
     click(284,193);wait('hero=dragon');capture('dragon')
     click(284,63);wait('DEFOLD FLOW SHOP READY');capture('shop')
     click(1130,510);text=wait('DEFOLD FLOW PURCHASE prism owned=true')
     first=int(re.search(r'DEFOLD FLOW PURCHASE prism owned=true wallet=(\d+)',text).group(1))
     click(930,578);wait('DEFOLD SHOP TAB armor');click(1130,510);text=wait('DEFOLD FLOW PURCHASE armor owned=true')
     match=re.search(r'DEFOLD FLOW PURCHASE armor owned=true wallet=(\d+) hp=(\d+) max=(\d+)',text);assert match,text
     remaining,hp,max_hp=map(int,match.groups());assert remaining==first-160 and hp==max_hp==20,text
     # The next weapon remains visible but cannot be bought with 40 stars.
     click(720,578);wait('DEFOLD SHOP TAB weapon');click(1130,409);text=wait('DEFOLD FLOW PURCHASE arc owned=false')
     actual=int(re.search(r'DEFOLD FLOW PURCHASE arc owned=false wallet=(\d+)',text).group(1));assert actual==remaining,text
     capture('purchased')
     click(1090,73);wait('DEFOLD FLOW ACTION menu');click(772,534)
     wait('DEFOLD FLOW PLAY READY mission=1 treasure=1 bonus=2');capture('mission')
     click(904,648);wait('DEFOLD FLOW TREASURE TRACK PASS remaining=1');capture('treasure-guide')
     click(720,648);wait('DEFOLD FLOW BONUS TRACK PASS total=2');capture('bonus-guide')
     click(1215,674);wait('DEFOLD FLOW ACTION menu');click(1090,381)
     wait('DEFOLD FLOW PLAY READY mission=4 treasure=1 bonus=2');capture('new-mission')
    else:
     wait('DEFOLD FLOW WIN READY remaining=1 next=2');capture('win')
     if name=='next-with-unfound-treasure':
      click(930,231);wait('DEFOLD FLOW PLAY READY mission=2 treasure=1 bonus=2');capture('next')
     else:
      click(930,99);wait('DEFOLD FLOW ACTION loot');wait('DEFOLD FLOW PLAY READY mission=1 treasure=1 bonus=2');capture('optional-search')
      # Leaving the optional search is always available; treasure never locks next.
      click(72,124);wait('DEFOLD FLOW PLAY READY mission=2 treasure=1 bonus=2');capture('next')
    assert 'ERROR:'not in log.read_text(),log.read_text()
   finally:process.terminate();process.wait(timeout=5)
  print('DEFOLD NATIVE FLOW '+name.upper()+' PASS',flush=True)
 print('DEFOLD NATIVE HERO / SPENDING / TREASURE / BONUS / NEXT FLOW PASS')
