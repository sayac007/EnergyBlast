"""Exercise the real native battlefield catalogue/preview/floor placement via XTest.

Run under Xvfb after a successful native build. Optional --output retains real
catalogue/preview/planted screenshots and process logs for visual review.
"""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--project',type=Path,default=ROOT/'pilots/defold');p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py,duration=.07):
 xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(duration)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.18)
with tempfile.TemporaryDirectory(prefix='energyblast-native-traps-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary)
 root.mkdir(parents=True,exist_ok=True)
 for kind in ['magnet','frost','pulse']:
  state=root/kind;state.mkdir();log=state/'runtime.log'
  for folder in ['data','cache','config']:(state/folder).mkdir()
  env=dict(os.environ,XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
  def wait_for(marker):
   until=time.monotonic()+7
   while time.monotonic()<until:
    text=log.read_text()
    if marker in text:return text
    time.sleep(.03)
   raise AssertionError(log.read_text())
  def coordinates(marker):
   text=wait_for(marker);match=re.search(re.escape(marker)+r' (\d+) (\d+)',text);assert match,text
   px,py=map(int,match.groups());assert 144<px<1136 and 96<py<624,(marker,px,py)
   return px,py
  def screenshot(name):
   if a.output:ImageGrab.grab().crop((0,0,1280,720)).save(state/(name+'.png'))
  with log.open('w')as stream:
   process=subprocess.Popen([str(a.engine),'--config=project.capture_mode=1','--config=project.capture_sector=4','--config=project.trap_test=1',str(a.project/'build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
   try:
    badge=coordinates('DEFOLD FIELD TRAP READY');click(*badge)
    wait_for('DEFOLD FIELD TRAP CATALOGUE PASS shots=0');screenshot('catalogue')
    if kind=='magnet':
     click(*coordinates('DEFOLD FIELD TRAP CANCEL'));wait_for('DEFOLD FIELD TRAP CANCEL PASS traps=0 shots=0');click(*badge)
    click(*coordinates('DEFOLD FIELD TRAP OPTION '+kind));wait_for('DEFOLD FIELD TRAP SELECT PASS '+kind);screenshot('preview')
    click(*coordinates('DEFOLD FIELD TRAP FLOOR'));wait_for('DEFOLD FIELD TRAP PLACED PASS '+kind+' shots=0');screenshot('planted')
    assert 'ERROR:'not in log.read_text(),log.read_text()
   finally:
    process.terminate();process.wait(timeout=5)
  print('DEFOLD NATIVE FIELD TRAP '+kind.upper()+' / SELECT / PREVIEW / PLACE / NO SHOT PASS',flush=True)
 print('DEFOLD NATIVE FIELD TRAP CANCEL / THREE TYPES / BATTLEFIELD COORDINATES PASS')
