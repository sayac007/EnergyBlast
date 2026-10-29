"""Real native zoom buttons and treasure collection in all six arenas via XTest.

The explicit fixture grants completion stars for hint credits, starts on a real
free approach, and disables hostile AI. It never grants or forces treasure pickup.
Pinch pointer packets are covered by native Lua checks, not claimed as hardware
multitouch here. Run only after a successful Bob build, under Xvfb.
"""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab,ImageChops

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py):
 xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(.06)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.17)
def frame():return ImageGrab.grab().crop((0,0,1280,720))
def changed_world(left,right):
 diff=ImageChops.difference(left.crop((144,96,1136,624)).convert('RGB'),right.crop((144,96,1136,624)).convert('RGB'))
 raw=diff.tobytes()
 return sum(max(r,g,b)>18 for r,g,b in zip(raw[::3],raw[1::3],raw[2::3]))

with tempfile.TemporaryDirectory(prefix='energyblast-native-polish-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
 for folder in ['data','cache','config']:(root/folder).mkdir()
 log=root/'runtime.log'
 env=dict(os.environ,XDG_DATA_HOME=str(root/'data'),XDG_CACHE_HOME=str(root/'cache'),XDG_CONFIG_HOME=str(root/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
 def wait(pattern,after=0,timeout=10):
  deadline=time.monotonic()+timeout
  while time.monotonic()<deadline:
   text=log.read_text();assert 'ERROR:'not in text,text
   m=re.search(pattern,text[after:])
   if m:return m
   time.sleep(.025)
  raise AssertionError('Missing '+pattern+'\n'+log.read_text())
 def view(mission,zoom,after=0):
  return wait(r'DEFOLD POLISH VIEW mission='+mission+r' zoom='+re.escape(f'{zoom:.3f}')+r' x=(-?\d+) y=(-?\d+) hero_height=([0-9.]+) score=(\d+) discovered=(true|false) scale=([0-9.]+)',after)
 def visible_world():
  deadline=time.monotonic()+5;visible=0
  while time.monotonic()<deadline:
   raw=frame().crop((1155,340,1182,366)).convert('RGB').tobytes()
   gold=sum(r>170 and g>100 and b<150 and r>g and g>1.25*b for r,g,b in zip(raw[::3],raw[1::3],raw[2::3]))
   visible=visible+1 if gold>=len(raw)/3*.75 else 0
   if visible>=2:return
   time.sleep(.05)
  raise AssertionError('No visible first battlefield frame\n'+log.read_text())
 def capture(name):
  image=frame()
  if a.output:image.save(root/(name+'.png'))
  return image
 with log.open('w')as stream:
  process=subprocess.Popen([str(a.engine),'--config=project.polish_ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
  try:
   wait('DEFOLD POLISH MENU READY');baseline=2400
   for index,mission in enumerate(['reactor','citadel','dock','forge','echo','rescue']):
    before=len(log.read_text());click(772 if index%2==0 else 1090,534-(index//2)*153)
    initial=view(mission,1, before);visible_world();time.sleep(.12)
    assert int(initial.group(4))==baseline,log.read_text()
    if index==0:
     normal=capture('zoom-normal');normal_height=float(initial.group(3))
     before=len(log.read_text());click(240,44);view(mission,1.15,before)
     before=len(log.read_text());click(240,44);near=view(mission,1.3,before);time.sleep(.10);close=capture('zoom-close')
     assert abs(float(near.group(3))/normal_height-1.3)<.015
     assert changed_world(normal,close)>5000,'Zoom must alter the rendered battlefield, not only its HUD label'
     for zoom in [1.15,1.0,.85]:
      before=len(log.read_text());click(174,44);wide=view(mission,zoom,before)
     time.sleep(.10);wide_frame=capture('zoom-wide')
     assert abs(float(wide.group(3))/normal_height-.85)<.015
     assert changed_world(normal,wide_frame)>5000
     before=len(log.read_text());click(240,44);initial=view(mission,1.0,before)
     print('DEFOLD NATIVE ZOOM BUTTONS / WORLD SCALE PASS',flush=True)
    before=len(log.read_text());click(72,210)
    wait(r'DEFOLD POLISH HINT TRACKS mission='+mission+r' goal=treasure',before)
    time.sleep(.12);capture(mission+'-hint')
    px,py=int(initial.group(1)),int(initial.group(2));assert 144<px<1136 and 96<py<624
    before=len(log.read_text());click(px,py)
    m=wait(r'DEFOLD POLISH TREASURE FOUND mission='+mission+r' score=(\d+) delta=(\d+) shots=(\d+)',before)
    assert int(m.group(1))==baseline+75 and int(m.group(2))==75 and int(m.group(3))==0,log.read_text()
    baseline+=75;time.sleep(.12);capture(mission+'-found')
    if index<5:click(1215,674);time.sleep(.15)
    print('DEFOLD NATIVE TREASURE '+mission.upper()+' PASS',flush=True)
   assert baseline==2850
  finally:process.terminate();process.wait(timeout=5)
 print('DEFOLD NATIVE ZOOM / SIX TREASURES / HINTS PASS')
