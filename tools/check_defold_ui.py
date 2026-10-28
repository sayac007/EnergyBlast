"""Real native menu, short tap, long hold and fire clicks via XTest under Xvfb."""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--resize',type=int,nargs=2);p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py,duration=.06):
 xt.XTestFakeMotionEvent(display,0,round(px*(a.resize[0]/1280 if a.resize else 1)),round(py*(a.resize[1]/720 if a.resize else 1)),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(duration)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.15)
with tempfile.TemporaryDirectory(prefix='energyblast-native-ui-',dir='/tmp')as d:
 log=Path(d)/'runtime.log'
 for folder in ['data','cache','config']:(Path(d)/folder).mkdir()
 env=dict(os.environ,XDG_DATA_HOME=str(Path(d)/'data'),XDG_CACHE_HOME=str(Path(d)/'cache'),XDG_CONFIG_HOME=str(Path(d)/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
 def wait_for(marker):
  until=time.monotonic()+5
  while time.monotonic()<until:
   text=log.read_text()
   if marker in text:return text
   time.sleep(.03)
  raise AssertionError(log.read_text())
 with log.open('w')as stream:
  proc=subprocess.Popen([str(a.engine),'--config=project.ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
  try:
   wait_for('DEFOLD MENU READY')
   if a.resize:
    x.XDefaultRootWindow.argtypes=[ctypes.c_void_p];x.XDefaultRootWindow.restype=ctypes.c_ulong
    x.XQueryTree.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.POINTER(ctypes.c_ulong),ctypes.POINTER(ctypes.c_ulong),ctypes.POINTER(ctypes.POINTER(ctypes.c_ulong)),ctypes.POINTER(ctypes.c_uint)]
    root_id=ctypes.c_ulong();parent=ctypes.c_ulong();children=ctypes.POINTER(ctypes.c_ulong)();count=ctypes.c_uint()
    assert x.XQueryTree(display,x.XDefaultRootWindow(display),ctypes.byref(root_id),ctypes.byref(parent),ctypes.byref(children),ctypes.byref(count))and count.value>0
    x.XResizeWindow.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.c_uint,ctypes.c_uint];x.XResizeWindow(display,children[count.value-1],*a.resize);x.XFlush(display);time.sleep(.35)
   click(284,657) # Actual full-screen character picker.
   click(930,483);wait_for('DEFOLD CHARACTER PICK PASS dragon')
   click(1135,483);wait_for('DEFOLD CHARACTER PICK PASS fox')
   click(930,483);wait_for('DEFOLD CHARACTER PICK PASS dragon')
   click(930,637);click(1130,637) # Main menu, Arsenal.
   click(1130,199);wait_for('DEFOLD SHOP PURCHASE PASS buy:prism')
   click(1130,302);wait_for('DEFOLD SHOP PURCHASE PASS buy:armor')
   click(1090,647);click(772,325) # Menu, actual third-sector card.
   text=wait_for('DEFOLD UI READY dock');match=re.search(r'DEFOLD UI READY dock (\d+) (\d+)',text);assert match,text
   px,py=map(int,match.groups());py=720-py
   click(px,py);wait_for('DEFOLD UI SHORT TAP shots=0');wait_for('DEFOLD ACTUAL ARTICULATED WALK PASS')
   click(px,py,.65);wait_for('DEFOLD UI LONG HOLD shots=1')
   time.sleep(.5);click(1208,380) # Retained visible FIRE control.
   click(1105,46);time.sleep(.3);click(1105,46);wait_for('DEFOLD AUDIO PAUSE RESUME PASS')
   try:proc.wait(timeout=11)
   except subprocess.TimeoutExpired:print(log.read_text());raise
  finally:
   if proc.poll()is None:proc.terminate();proc.wait(timeout=5)
 text=log.read_text();assert proc.returncode==0 and 'ERROR:'not in text and 'DEFOLD NATIVE MENU CLICK PASS'in text,text
 print('DEFOLD NATIVE MENU AND FIRE CLICK PASS; SHORT TAP / LONG HOLD / SHOP / CHARACTERS / HUD / MUSIC PASS')
