"""Actual native bonus gains, growth, readable million-health panel and restart.

The fixture seeds only earlier known achievements and stages a real green-window
target. XTest fires the actual projectile; production bonus/reward logic grants
the new power. This is a desktop native regression, not an Android device claim.
"""
import argparse,ctypes,os,re,subprocess,tempfile,time
from pathlib import Path
from PIL import ImageGrab

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.restype=ctypes.c_void_p;display=x.XOpenDisplay(None);assert display
xt=ctypes.CDLL('libXtst.so.6');xt.XTestFakeMotionEvent.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ulong];xt.XTestFakeButtonEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_ulong];x.XFlush.argtypes=[ctypes.c_void_p]
def click(px,py):
 xt.XTestFakeMotionEvent(display,0,round(px),round(720-py),0);xt.XTestFakeButtonEvent(display,1,1,0);x.XFlush(display);time.sleep(.06)
 xt.XTestFakeButtonEvent(display,1,0,0);x.XFlush(display);time.sleep(.18)
def capture(folder,name):
 if a.output:ImageGrab.grab().crop((0,0,1280,720)).save(folder/(name+'.png'))

with tempfile.TemporaryDirectory(prefix='energyblast-native-power-',dir='/tmp')as temporary:
 root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
 for profile,before_count,after_count,hp in [('first',0,1,20),('thousand',7,8,1005),('million',11,12,1000005)]:
  folder=root/profile;folder.mkdir()
  for child in ['data','cache','config']:(folder/child).mkdir()
  env=dict(os.environ,XDG_DATA_HOME=str(folder/'data'),XDG_CACHE_HOME=str(folder/'cache'),XDG_CONFIG_HOME=str(folder/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
  modes=[False,True]if profile=='million'else[False]
  for restart in modes:
   log=folder/('restart.log'if restart else'runtime.log')
   def wait(pattern,after=0,timeout=12):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
     text=log.read_text();assert 'ERROR:'not in text,text
     match=re.search(pattern,text[after:])
     if match:return match
     time.sleep(.025)
    raise AssertionError('Missing '+pattern+'\n'+log.read_text())
   cmd=[str(a.engine),'--config=project.power_ui_test='+profile,str(ROOT/'pilots/defold/build/default/game.projectc')]
   with log.open('w')as stream:
    process=subprocess.Popen(cmd,env=env,stdout=stream,stderr=subprocess.STDOUT)
    try:
     expected=after_count if restart else before_count
     wait('DEFOLD POWER MENU READY profile='+profile+' restarted='+str(restart).lower()+' count='+str(expected))
     click(1090,534)
     wait('DEFOLD POWER CHOOSE profile='+profile+' restarted='+str(restart).lower()+' count='+str(expected))
     before=wait(r'DEFOLD POWER RENDER BEFORE profile='+profile+r' count=\d+ hp=\d+ shield=\d+ scale=([0-9.]+) opacity=([0-9.]+) strength=([0-9.]+) shield_scale=([0-9.]+) shots=\d+ score=(\d+) wallet=(\d+)')
     capture(folder,'restart-before'if restart else'before')
     ready=wait('DEFOLD POWER SHOT READY profile='+profile+r' x=(\d+) y=(\d+) count='+str(expected))
     px,py=map(int,ready.groups());assert 144<px<1136 and 96<py<624
     click(px,py)
     wait('DEFOLD POWER EARNED profile='+profile+' count='+str(after_count)+' hp='+str(hp)+r' shield=\d+ delta='+('0'if restart else'150'))
     after=wait(r'DEFOLD POWER RENDER AFTER profile='+profile+r' count=\d+ hp=\d+ shield=\d+ scale=([0-9.]+) opacity=([0-9.]+) strength=([0-9.]+) shield_scale=([0-9.]+) shots=\d+ score=(\d+) wallet=(\d+)')
     wait('DEFOLD POWER MAX ZOOM NORTH BOUNDS PASS profile='+profile+' count='+str(after_count))
     capture(folder,'restart-north-max-zoom'if restart else'north-max-zoom')
     wait('DEFOLD POWER GAIN AND NATIVE GROWTH PASS profile='+profile+' replay='+str(restart).lower())
     if not restart:assert float(after.group(1))>float(before.group(1))*1.02
     assert float(after.group(2))<1 and float(after.group(3))>0 and float(after.group(4))>.001
     capture(folder,'restart-after'if restart else'after')
     panel_start=len(log.read_text());click(1208,593)
     wait('DEFOLD POWER PAGE READY count='+str(after_count)+' hp='+str(hp),panel_start)
     wait('DEFOLD POWER STAGE BOUNDS PASS count='+str(after_count),panel_start)
     capture(folder,'restart-panel'if restart else'power-panel')
     click(930,78)
     wait('DEFOLD POWER PANEL CLOSED PASS count='+str(after_count),panel_start)
     wait('DEFOLD POWER HUD READY count='+str(after_count)+r' hp=[0-9.]+ width=[0-9.]+')
     assert 'ERROR:'not in log.read_text(),log.read_text()
    finally:
     process.terminate();process.wait(timeout=5)
   print('DEFOLD NATIVE POWER '+profile.upper()+' / '+('PERSISTED REPLAY'if restart else'BONUS SHOT AND GROWTH')+' / PANEL PASS',flush=True)
 print('DEFOLD NATIVE BONUS POWER / MILLION HEALTH / GROWTH / SAVE PASS')
