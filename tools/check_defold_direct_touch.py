"""Actual native XTest gestures, observed before release, not simulated input.

Run under Xvfb after a successful Bob build. The explicit main fixture places
the hero and shielded turret in view and disables hostile AI only in this test.
No physical Android touch-latency or hardware-FPS claim is made.
"""
import argparse,ctypes,json,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def move(px,py):xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);x.XFlush(display)
def button(pressed):xt.XTestFakeButtonEvent(display,1,int(pressed),0);x.XFlush(display)
def tap(px,py):move(px,py);button(True);time.sleep(.05);button(False)
with tempfile.TemporaryDirectory(prefix='energyblast-native-direct-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
 for name in ['ground-tap','ground-held-fire','padded-enemy','buffered-taps','hero-drag']:
  state=root/name;state.mkdir();log=state/'runtime.log'
  for folder in ['data','cache','config']:(state/folder).mkdir()
  env=dict(os.environ,XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
  def wait(marker):
   until=time.monotonic()+8
   while time.monotonic()<until:
    text=log.read_text()
    if 'ERROR:'in text:raise AssertionError(text)
    if marker in text:return text
    time.sleep(.02)
   raise AssertionError(log.read_text())
  def capture(label):
   if a.output:ImageGrab.grab().crop((0,0,1280,720)).save(state/(label+'.png'))
  with log.open('w')as stream:
   process=subprocess.Popen([str(a.engine),'--config=project.direct_touch_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
   try:
    text=wait('DEFOLD DIRECT READY');m=re.search(r'DEFOLD DIRECT READY ((?:\d+ ?){8})',text);assert m,text
    hx,hy,tx,ty,ax,ay,ex,ey=map(int,m.group(1).split())
    for px,py in [(hx,hy),(tx,ty),(ax,ay),(ex,ey)]:assert 144<px<1136 and 96<py<624,(name,px,py)
    if name=='ground-tap':
     tap(tx,ty);wait('DEFOLD DIRECT GROUND TAP shots=0');wait('DEFOLD DIRECT GROUND MOVED shots=0');capture('walking')
    elif name=='ground-held-fire':
     move(ax,ay);button(True)
     text=wait('DEFOLD DIRECT COUNT shots=2 held=true mode=fire')
     assert 'DEFOLD DIRECT FIRE RELEASE'not in text,'test must observe two shots while contact is still down'
     m=re.search(r'GROUND HOLD shots=1 elapsed=([0-9.]+) emitted=true',text);assert m and .13<=float(m.group(1))<.30,text
     capture('firing-before-release');button(False);text=wait('DEFOLD DIRECT FIRE RELEASE')
     count=int(re.search(r'FIRE RELEASE shots=(\d+)',text).group(1));time.sleep(.4)
     actual=[int(n)for n in re.findall(r'COUNT shots=(\d+)',log.read_text())];assert max(actual)==count,log.read_text()
    elif name=='padded-enemy':
     move(ex,ey);button(True);text=wait('DEFOLD DIRECT ENEMY PRESS shots=1 elapsed=0.000 emitted=true')
     assert 'DEFOLD DIRECT FIRE RELEASE'not in text
     capture('immediate-padded-press');button(False);text=wait('DEFOLD DIRECT ENEMY AIM')
     m=re.search(r'ENEMY AIM target_x=([-0-9.]+) target_z=([-0-9.]+)',text);assert m,text
     actual=list(map(float,m.groups()));expected=json.loads((ROOT/'shared/defold04.json').read_text())['missions'][0]['turrets'][0]['position']
     assert all(abs(x-y)<.001 for x,y in zip(actual,expected)),(actual,expected)
    elif name=='buffered-taps':
     tap(ex,ey);wait('DEFOLD DIRECT ENEMY PRESS shots=1');time.sleep(.02);tap(ex,ey)
     wait('DEFOLD DIRECT BUFFERED PRESS shots=1');wait('DEFOLD DIRECT BUFFERED SHOT shots=2');time.sleep(.4)
     counts=list(map(int,re.findall(r'COUNT shots=(\d+)',log.read_text())));assert max(counts)==2,log.read_text();capture('two-intended-shots')
    else:
     move(hx,hy);button(True);wait('DEFOLD DIRECT HERO PRESS shots=0');time.sleep(.3)
     for i in range(1,11):move(hx+i*9,hy);time.sleep(.02)
     wait('DEFOLD DIRECT HERO MOVED shots=0');capture('moving-before-release');button(False);wait('DEFOLD DIRECT HERO RELEASE shots=0');time.sleep(.25)
     assert max(map(int,re.findall(r'COUNT shots=(\d+)',log.read_text())))==0,log.read_text()
    assert 'ERROR:'not in log.read_text(),log.read_text()
   finally:button(False);process.terminate();process.wait(timeout=5)
  print('DEFOLD NATIVE DIRECT '+name.upper()+' PASS',flush=True)
 print('DEFOLD NATIVE HOLD FIRE / IMMEDIATE PADDED TARGET / DRAG / BUFFER PASS')
