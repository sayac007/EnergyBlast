"""Real native current-campaign menus, migration, bounded view and mission flow.

The explicit fixture seeds a previous 0.13 ledger and quiets hostile AI; input,
world allocation, drone impact, mission completion and navigation stay real.
Run after a successful Bob build under Xvfb. Desktop testing is not a device claim.
"""
from pathlib import Path
import argparse,ctypes,os,re,subprocess,tempfile,time
from PIL import ImageGrab

ROOT=Path(__file__).resolve().parents[1]

class NativeDriver:
 def __init__(self,engine,folder,mode='1',restart=False,resize=None):
  self.engine=engine;self.folder=folder;self.mode=mode;self.resize=resize
  folder.mkdir(parents=True,exist_ok=True)
  for name in ['data','cache','config']:(folder/name).mkdir(exist_ok=True)
  self.log=folder/('restart.log'if restart else'runtime.log')
  self.x=ctypes.CDLL('libX11.so.6');self.x.XOpenDisplay.restype=ctypes.c_void_p;self.display=self.x.XOpenDisplay(None);assert self.display
  self.xt=ctypes.CDLL('libXtst.so.6')
  self.xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong]
  self.xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong]
  self.x.XFlush.argtypes=[ctypes.c_void_p];self.x.XCloseDisplay.argtypes=[ctypes.c_void_p]
  self.width,self.height=1280,720
 def __enter__(self):
  env=dict(os.environ,XDG_DATA_HOME=str(self.folder/'data'),XDG_CACHE_HOME=str(self.folder/'cache'),XDG_CONFIG_HOME=str(self.folder/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
  env.pop('ENERGYBLAST_REGRESSION_RULES',None)
  self.stream=self.log.open('w')
  self.process=subprocess.Popen([str(self.engine),'--config=project.campaign_ui_test='+self.mode,str(ROOT/'pilots/defold/build/default/game.projectc')],env=env,stdout=self.stream,stderr=subprocess.STDOUT)
  try:
   self.wait('DEFOLD CAMPAIGN FIXTURE READY')
   if self.resize:
    x=self.x;display=self.display
    x.XDefaultRootWindow.argtypes=[ctypes.c_void_p];x.XDefaultRootWindow.restype=ctypes.c_ulong
    x.XQueryTree.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.POINTER(ctypes.c_ulong),ctypes.POINTER(ctypes.c_ulong),ctypes.POINTER(ctypes.POINTER(ctypes.c_ulong)),ctypes.POINTER(ctypes.c_uint)]
    root=ctypes.c_ulong();parent=ctypes.c_ulong();children=ctypes.POINTER(ctypes.c_ulong)();count=ctypes.c_uint()
    assert x.XQueryTree(display,x.XDefaultRootWindow(display),ctypes.byref(root),ctypes.byref(parent),ctypes.byref(children),ctypes.byref(count))and count.value>0
    x.XResizeWindow.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.c_uint,ctypes.c_uint]
    x.XResizeWindow(display,children[count.value-1],*self.resize);x.XFlush(display);self.width,self.height=self.resize;time.sleep(.4)
  except BaseException:
   self.__exit__();raise
  return self
 def __exit__(self,*unused):
  self.process.terminate();self.process.wait(timeout=5);self.stream.close();self.x.XCloseDisplay(self.display)
 def text(self):return self.log.read_text()
 def wait(self,pattern,after=0,timeout=10):
  deadline=time.monotonic()+timeout
  while time.monotonic()<deadline:
   value=self.text();assert 'ERROR:'not in value,value
   match=re.search(pattern,value[after:])
   if match:return match
   if self.process.poll()is not None:raise AssertionError('Native process stopped\n'+value)
   time.sleep(.025)
  raise AssertionError('Missing '+pattern+'\n'+self.text())
 def coords(self,marker,after=0):
  m=self.wait(re.escape(marker)+r' (\d+) (\d+)',after);return tuple(map(int,m.groups()))
 def move(self,px,py):
  self.xt.XTestFakeMotionEvent(self.display,0,round(px*self.width/1280),round((720-py)*self.height/720),0);self.x.XFlush(self.display)
 def press(self,px,py):
  self.move(px,py);self.xt.XTestFakeButtonEvent(self.display,1,1,0);self.x.XFlush(self.display)
 def release(self,px=None,py=None):
  if px is not None:self.move(px,py)
  self.xt.XTestFakeButtonEvent(self.display,1,0,0);self.x.XFlush(self.display)
 def click(self,px,py,duration=.055):
  self.press(px,py);time.sleep(duration);self.release();time.sleep(.15)
 def drag(self,start,end):
  self.press(*start);time.sleep(.08)
  for step in range(1,13):
   self.move(start[0]+(end[0]-start[0])*step/12,start[1]+(end[1]-start[1])*step/12);time.sleep(.018)
  self.release();time.sleep(.15)
 def capture(self,name,enabled):
  if enabled:ImageGrab.grab().crop((0,0,self.width,self.height)).save(self.folder/(name+'.png'))
 def choose(self,index,after=0):
  slot=(index-1)%6
  self.click(772 if slot%2==0 else 1090,534-(slot//2)*153)
  self.wait('DEFOLD CAMPAIGN CHOOSE mission='+str(index)+r' id=\S+ protected=true hp=\d+ arena=\S+ bonus=0 treasure=0 score=4350 wallet=2690',after)
  self.wait('DEFOLD CAMPAIGN SCENE READY mission='+str(index)+r' models=\d+ hp=\d+ shots=0',after)
 def page(self,index,current_page):
  wanted=(index-1)//6+1
  while current_page!=wanted:
   before=len(self.text());self.click(1207 if current_page<wanted else 657,134)
   current_page+=1 if current_page<wanted else-1
   self.wait('DEFOLD CAMPAIGN MENU PAGE '+str(current_page),before)
  return current_page

def check_tour(engine,folder,keep,resize):
 with NativeDriver(engine,folder,resize=resize)as d:
  d.wait('restarted=false score=4350 wallet=2690');d.wait('DEFOLD CAMPAIGN MENU PAGE 1')
  page=1
  for index in range(1,17):
   page=d.page(index,page);before=len(d.text());d.choose(index,before)
   if index in [1,6,7,12,16]:d.capture('mission-'+str(index),keep)
   before=len(d.text());d.click(410,649);d.wait('DEFOLD CAMPAIGN OBJECTIVE PAGE mission='+str(index),before)
   d.capture('objective-'+str(index),keep and index in [1,7,16])
   d.click(930,78);d.wait('DEFOLD CAMPAIGN ACTION objective_close mission='+str(index),before)
   if index in [1,7,16]:
    before=len(d.text());d.click(670,649);d.wait('DEFOLD CAMPAIGN OBJECTIVE PAGE mission='+str(index),before);d.click(930,78)
   if index==16:
    for unused in range(12):
     if re.search(r'DEFOLD CAMPAIGN MINIMUM VIEW mission=16 ',d.text()):break
     d.click(174,44)
    m=d.wait(r'DEFOLD CAMPAIGN MINIMUM VIEW mission=16 zoom=[0-9.]+ matte_x=(\d+) matte_y=(\d+)')
    d.capture('minimum-bounded-arena',keep);d.click(*map(int,m.groups()))
    d.wait('DEFOLD CAMPAIGN MATTE INPUT IGNORED PASS mission=16')
   before=len(d.text());d.click(900,649);d.wait('DEFOLD CAMPAIGN MENU PAGE '+str(page),before)
   print('DEFOLD NATIVE ACTIVE CAMPAIGN MISSION '+str(index)+' / SAFE SPAWN / OBJECTIVE / MENU PASS',flush=True)
  d.capture('page-3',keep)
 with NativeDriver(engine,folder,restart=True)as d:
  d.wait('restarted=true score=4350 wallet=2690');d.wait('DEFOLD CAMPAIGN MENU PAGE 3')
  page=d.page(1,3);d.choose(1);d.capture('migrated-ledger-restart',keep)
 print('DEFOLD NATIVE OLD MILLION LEDGER / HEALTH CAP / PURCHASES / RESTART PASS',flush=True)

def check_next(engine,folder,keep):
 with NativeDriver(engine,folder,mode='next')as d:
  d.wait('DEFOLD CAMPAIGN MENU PAGE 1');d.choose(1)
  badge=d.coords('DEFOLD CAMPAIGN DRONE BADGE')
  before=len(d.text());d.click(*badge);option=d.coords('DEFOLD CAMPAIGN DRONE OPTION',before)
  before=len(d.text());d.click(*option);d.wait('DEFOLD CAMPAIGN DRONE PREVIEW',before)
  target=d.coords('DEFOLD CAMPAIGN DRONE TARGET',before);d.capture('real-spawn-target-overview',keep);d.click(*target)
  d.wait('DEFOLD CAMPAIGN DRONE FLYING PASS');d.wait('DEFOLD CAMPAIGN DRONE IMPACT / NATIVE LIGHTNING PASS')
  d.wait('DEFOLD CAMPAIGN REAL WIN READY next=2');d.capture('real-mission-completion',keep)
  before=len(d.text());d.click(930,231);d.wait('DEFOLD CAMPAIGN CHOOSE mission=2 ',before);d.wait('DEFOLD CAMPAIGN SCENE READY mission=2 ',before)
  d.wait('DEFOLD CAMPAIGN DRONE NEXT VIEW RESTORED PASS',before)
  d.capture('real-next-mission',keep)
 print('DEFOLD NATIVE REAL DRONE MISSION WIN / NEXT / PROTECTED SPAWN PASS',flush=True)

def check_stress(engine,folder,keep):
 with NativeDriver(engine,folder,mode='stress')as d:
  page=d.page(16,1);d.choose(16)
  d.wait('DEFOLD CAMPAIGN FIFTY NATIVE HOSTILES PASS alive=50 models=50',timeout=15);d.capture('fifty-native-hostiles',keep)
 print('DEFOLD NATIVE FIFTY HOSTILES / REAL OFFSPRING / MODEL BUDGET PASS',flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);p.add_argument('--resize',type=int,nargs=2);p.add_argument('--scenario',choices=['all','tour','next','stress'],default='all');a=p.parse_args()
 with tempfile.TemporaryDirectory(prefix='energyblast-native-campaign-',dir='/tmp')as temporary:
  root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
  if a.scenario in ['all','tour']:check_tour(a.engine,root/'tour',a.output is not None,a.resize)
  if a.scenario in ['all','next']:check_next(a.engine,root/'next',a.output is not None)
  if a.scenario in ['all','stress']:check_stress(a.engine,root/'stress',a.output is not None)
 print('DEFOLD NATIVE SIXTEEN MISSIONS / ACTIVE MENUS / BOUNDED CAMERA / MIGRATION PASS')

if __name__=='__main__':main()
