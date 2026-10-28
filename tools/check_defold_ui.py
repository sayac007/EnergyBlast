"""Real native menu, short tap, long hold and fire clicks via XTest under Xvfb."""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py,duration=.06):
 xt.XTestFakeMotionEvent(display,0,px,py,0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(duration)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.15)
with tempfile.TemporaryDirectory(prefix='energyblast-native-ui-',dir='/tmp')as d:
 log=Path(d)/'runtime.log'
 def wait_for(marker):
  until=time.monotonic()+5
  while time.monotonic()<until:
   text=log.read_text()
   if marker in text:return text
   time.sleep(.03)
  raise AssertionError(log.read_text())
 with log.open('w')as stream:
  proc=subprocess.Popen([str(a.engine),'--config=project.ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=os.environ,stdout=stream,stderr=subprocess.STDOUT)
  try:
   wait_for('DEFOLD MENU READY');click(185,955) # HELDEN: full-screen picker.
   click(360,730);wait_for('DEFOLD CHARACTER PICK PASS dragon')
   click(595,730);wait_for('DEFOLD CHARACTER PICK PASS fox')
   click(360,730);wait_for('DEFOLD CHARACTER PICK PASS dragon')
   click(360,1000);click(535,955) # Back, then Arsenal.
   click(570,358);wait_for('DEFOLD SHOP PURCHASE PASS buy:prism')
   click(570,513);wait_for('DEFOLD SHOP PURCHASE PASS buy:armor')
   click(535,1060);click(185,539) # Menu, sector 3.
   text=wait_for('DEFOLD UI READY dock');match=re.search(r'DEFOLD UI READY dock (\d+) (\d+)',text);assert match,text
   px,py=map(int,match.groups());py=1280-py
   click(px,py);wait_for('DEFOLD UI SHORT TAP shots=0')
   click(px,py,.42);wait_for('DEFOLD UI LONG HOLD shots=1')
   time.sleep(.5);click(610,1180) # Retained visible FIRE control.
   click(555,45);time.sleep(.3);click(555,45);wait_for('DEFOLD AUDIO PAUSE RESUME PASS')
   try:proc.wait(timeout=6)
   except subprocess.TimeoutExpired:print(log.read_text());raise
  finally:
   if proc.poll()is None:proc.terminate();proc.wait(timeout=5)
 text=log.read_text();assert proc.returncode==0 and 'ERROR:'not in text and 'DEFOLD NATIVE MENU CLICK PASS'in text,text
 print('DEFOLD NATIVE MENU AND FIRE CLICK PASS; SHORT TAP / LONG HOLD / SHOP / CHARACTERS / HUD / MUSIC PASS')
