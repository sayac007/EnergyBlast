"""Real native menu/control clicks via XTest under Xvfb; no game-input mock."""
import argparse,ctypes,os,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));a=p.parse_args()
# Run inside the selected X display. The caller owns Xvfb and the state directories.
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py):
 xt.XTestFakeMotionEvent(display,0,px,py,0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(.06);xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.15) # Allow a native input poll to observe release before the next press.
with tempfile.TemporaryDirectory(prefix='energyblast-native-ui-',dir='/tmp')as d:
 log=Path(d)/'runtime.log'
 with log.open('w')as stream:
  proc=subprocess.Popen([str(a.engine),'--config=project.ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=os.environ,stdout=stream,stderr=subprocess.STDOUT)
  try:
   time.sleep(1.0);click(360,715) # The visible third-sector pill, not g.choose().
   deadline=time.monotonic()+5
   while time.monotonic()<deadline and 'DEFOLD UI READY dock'not in log.read_text():time.sleep(.03)
   assert 'DEFOLD UI READY dock'in log.read_text(),log.read_text()
   click(570,1172) # Visible FIRE: exercises the sound callback from GUI context.
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:print(log.read_text());raise
  finally:
   if proc.poll()is None:proc.terminate();proc.wait(timeout=5)
 text=log.read_text();assert proc.returncode==0 and 'ERROR:'not in text and 'DEFOLD NATIVE MENU CLICK PASS'in text,text
 print('DEFOLD NATIVE MENU AND FIRE CLICK PASS')
