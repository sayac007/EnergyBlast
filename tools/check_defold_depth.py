"""Pixel-test the actual native depth buffer: a shot behind cover must be hidden.
The isolated render fixture freezes actors/camera. Front shot is the positive
control, so a missing projectile renderer cannot produce a false success.
"""
from pathlib import Path
import argparse,os,subprocess,tempfile,time
from PIL import ImageGrab,ImageChops
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));a=p.parse_args()
images={}
with tempfile.TemporaryDirectory(prefix='energyblast-depth-',dir='/tmp')as directory:
 root=Path(directory)
 for mode in ['none','behind','front']:
  state=root/mode;state.mkdir()
  for name in ['data','cache','config']:(state/name).mkdir()
  env=dict(os.environ,ALSOFT_DRIVERS='null',XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'))
  with(state/'runtime.log').open('w')as stream:
   proc=subprocess.Popen([str(a.engine),'--config=project.capture_mode=1','--config=project.capture_sector=1','--config=project.capture_depth='+mode,str(R/'pilots/defold/build/default/game.projectc')],env=env,stdout=stream,stderr=subprocess.STDOUT)
   try:
    deadline=time.monotonic()+6
    while 'DEFOLD DEPTH READY'not in(state/'runtime.log').read_text()and time.monotonic()<deadline:time.sleep(.025)
    assert 'DEFOLD DEPTH READY'in(state/'runtime.log').read_text(),(state/'runtime.log').read_text()
    time.sleep(.7)
    images[mode]=ImageGrab.grab().crop((144,96,1136,624)).convert('RGB')
   finally:proc.terminate();proc.wait(timeout=5)
  assert 'ERROR:'not in(state/'runtime.log').read_text(),(state/'runtime.log').read_text()
 hidden=ImageChops.difference(images['none'],images['behind'])
 visible=ImageChops.difference(images['none'],images['front'])
 hidden_count=sum(max(p)>4 for p in hidden.getdata());visible_count=sum(max(p)>4 for p in visible.getdata())
 if hidden_count>0 or visible_count<20:
  for key,im in images.items():im.save('/tmp/energyblast-depth-'+key+'.png')
 assert hidden_count==0 and visible_count>=20,(hidden_count,visible_count)
 print('DEFOLD ACTUAL WALL OCCLUSION PASS; hidden shot pixels=%d, front control pixels=%d'%(hidden_count,visible_count))
