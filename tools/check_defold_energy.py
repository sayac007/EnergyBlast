"""Positive pixel control: the native shield must actually reach the renderer."""
from pathlib import Path
import argparse,os,subprocess,tempfile,time
from PIL import ImageGrab,ImageChops
import numpy as np
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));a=p.parse_args()
images={}
with tempfile.TemporaryDirectory(prefix='energyblast-energy-',dir='/tmp')as directory:
 for mode in ['off','on']:
  state=Path(directory)/mode;state.mkdir()
  for name in ['data','cache','config']:(state/name).mkdir()
  env=dict(os.environ,ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1',XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'))
  with(state/'runtime.log').open('w')as stream:
   proc=subprocess.Popen([str(a.engine),'--config=project.capture_mode=1','--config=project.capture_sector=1','--config=project.capture_depth=none','--config=project.capture_field_off='+('1'if mode=='off'else'0'),str(R/'pilots/defold/build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
   try:
    deadline=time.monotonic()+6
    while 'DEFOLD DEPTH READY'not in(state/'runtime.log').read_text()and time.monotonic()<deadline:time.sleep(.025)
    assert 'DEFOLD DEPTH READY'in(state/'runtime.log').read_text(),(state/'runtime.log').read_text()
    time.sleep(.5);images[mode]=ImageGrab.grab().crop((144,96,1136,624)).convert('RGB')
   finally:proc.terminate();proc.wait(timeout=5)
  assert 'ERROR:'not in(state/'runtime.log').read_text(),(state/'runtime.log').read_text()
 difference=ImageChops.difference(images['off'],images['on'])
 count=int(np.count_nonzero(np.max(np.asarray(difference),axis=2)>5))
 for mode,im in images.items():im.save('/tmp/energyblast09-energy-'+mode+'.png')
 assert count>40,('native energy shield invisible',count)
 print('DEFOLD ACTUAL ENERGY SHIELD PIXEL PASS; visible changed pixels=%d'%count)
