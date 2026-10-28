"""Record actual native movement, hold/release and shots using real XTest input.
No generated animation frames; all frames come from the running game.
"""
from pathlib import Path
import argparse,ctypes,os,re,subprocess,time
from PIL import ImageGrab
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.output.resolve();root.mkdir(parents=True,exist_ok=False)
for n in ['data','cache','config']:(root/n).mkdir()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;d=x.XOpenDisplay(None);assert d
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def event(px,py,pressed):
 xt.XTestFakeMotionEvent(d,0,px,py,0);xt.XTestFakeButtonEvent(d,1,int(pressed),0);x.XFlush(d)
env=dict(os.environ,ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1',XDG_DATA_HOME=str(root/'data'),XDG_CACHE_HOME=str(root/'cache'),XDG_CONFIG_HOME=str(root/'config'))
with(root/'runtime.log').open('w')as log:
 proc=subprocess.Popen(['/tmp/energyblast-defold-tools/dmengine','--config=project.capture_mode=1','--config=project.capture_sector=3','--config=project.capture_character=dragon','--config=project.capture_motion=1',str(R/'pilots/defold/build/default/game.projectc')],env=env,stdout=log,stderr=subprocess.STDOUT)
 try:
  deadline=time.monotonic()+7;match=None
  while time.monotonic()<deadline:
   match=re.search(r'DEFOLD MOTION READY (\d+) (\d+) (\d+) (\d+)',(root/'runtime.log').read_text())
   if match:break
   time.sleep(.025)
  assert match,(root/'runtime.log').read_text();px,py,ax,ay=map(int,match.groups());py=720-py;ay=720-ay;time.sleep(.35)
  event(px,py,True);time.sleep(.06);event(px,py,False)
  frames=[];events=[(.75,ax,ay,True),(1.20,ax,ay,False),(1.65,1208,380,True),(2.45,1208,380,False)]
  start=time.monotonic()
  while time.monotonic()-start<3:
   elapsed=time.monotonic()-start
   while events and elapsed>=events[0][0]:_,ex,ey,press=events.pop(0);event(ex,ey,press)
   im=ImageGrab.grab().crop((0,0,1280,720));im.thumbnail((960,540));frames.append(im);time.sleep(.07)
  assert len(frames)>15
  frames[0].save(root/'gameplay.gif',save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=False)
  frames[len(frames)//2].save(root/'action.png')
 finally:proc.terminate();proc.wait(timeout=5)
runtime=(root/'runtime.log').read_text()
assert 'ERROR:'not in runtime,runtime
assert 'DEFOLD CAPTURE WALK FRAME PASS'in runtime and 'DEFOLD CAPTURE FIRED PASS'in runtime,runtime
print('ACTUAL NATIVE MOVEMENT / AIM / FIRE CAPTURE PASS:',len(frames),'frames; scripted XTest input, not a physical phone round')
