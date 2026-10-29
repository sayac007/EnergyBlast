"""Actual native GUI purchases and a real walk into the protected sanctuary.

The explicit controller fixture starts wounded with earned test stars and disables
hostile AI. It injects real swept hostile projectiles only after the player walks
into the refuge; no physical Android latency/performance claim is made here.
"""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py):
 xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(.05)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.15)
with tempfile.TemporaryDirectory(prefix='energyblast-native-resilience-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True);log=root/'runtime.log'
 for folder in ['data','cache','config']:(root/folder).mkdir()
 env=dict(os.environ,XDG_DATA_HOME=str(root/'data'),XDG_CACHE_HOME=str(root/'cache'),XDG_CONFIG_HOME=str(root/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
 def wait(pattern,after=0,timeout=12):
  until=time.monotonic()+timeout
  while time.monotonic()<until:
   text=log.read_text()
   assert 'ERROR:'not in text,text
   m=re.search(pattern,text[after:])
   if m:return m
   time.sleep(.03)
  raise AssertionError('Missing '+pattern+'\n'+log.read_text())
 def capture(name):
  if a.output:ImageGrab.grab().crop((0,0,1280,720)).save(root/(name+'.png'))
 def purchase(item,px,py):
  before=len(log.read_text());click(px,py)
  # Purchase handlers report actual state after the real g:buy call, including
  # rejected/full-health attempts. Repeatable health deliberately stays unowned.
  m=wait(r'DEFOLD FLOW PURCHASE '+re.escape(item)+r' owned=(true|false) wallet=(\d+) hp=(\d+) max=(\d+)',before)
  return m.group(1)=='true',*map(int,m.groups()[1:])
 with log.open('w')as stream:
  process=subprocess.Popen([str(a.engine),'--config=project.resilience_ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
  try:
   wait('DEFOLD FLOW MENU READY');click(284,63);m=wait(r'DEFOLD FLOW SHOP READY wallet=(\d+)');initial=int(m.group(1))
   wait(r'DEFOLD SHOP ITEM health 284 166 can=true full=false hp=5 max=15')
   wait(r'DEFOLD SHOP ITEM arc 1130 409 can=false owned=false locked=true');capture('initial-shop')
   owned,wallet,hp,maximum=purchase('arc',1130,409);assert not owned and wallet==initial and hp==5 and maximum==15
   owned,wallet,hp,maximum=purchase('health',284,166);assert not owned and wallet==initial-40 and hp==maximum==15
   wait(r'DEFOLD SHOP ITEM health 284 166 can=false full=true hp=15 max=15');capture('refill-complete')
   _,same,hp,maximum=purchase('health',284,166);assert same==wallet and hp==maximum==15,'Full health must not spend stars twice'
   owned,wallet,hp,maximum=purchase('prism',1130,510);assert owned and wallet==initial-140
   owned,wallet,hp,maximum=purchase('arc',1130,409);assert owned and wallet==initial-360
   wait(r'DEFOLD SHOP ITEM nova 1130 308 can=true owned=false locked=false');capture('weapon-progression')
   click(930,578);wait('DEFOLD SHOP TAB armor')
   wait(r'DEFOLD SHOP ITEM armor2 1130 409 can=false owned=false locked=true')
   owned,wallet,hp,maximum=purchase('armor',1130,510);assert owned and wallet==initial-520 and hp==maximum==20
   capture('armor-progression');click(1140,578);wait('DEFOLD SHOP TAB extra');capture('extras')
   assert 'DEFOLD SHOP ITEM boots 'not in log.read_text(),'Speed must not be a new shop purchase'
   click(1090,63);click(772,534);wait(r'DEFOLD RESILIENCE ZONE [-0-9.]+ [-0-9.]+');capture('mission-before-refuge')
   click(72,136)
   m=wait(r'DEFOLD RESILIENCE SHIELD PASS hp=(\d+) injected=(\d+) absorbed=(\d+) damage=(\d+)',timeout=25)
   healed,injected,absorbed,damage=map(int,m.groups());assert healed==20 and injected>=absorbed>=10 and damage==0,log.read_text()
   capture('sanctuary-protected-healing')
   assert 'ERROR:'not in log.read_text(),log.read_text()
  finally:process.terminate();process.wait(timeout=5)
 print('DEFOLD NATIVE REFILL / WEAPON / ARMOR / SANCTUARY PASS')
