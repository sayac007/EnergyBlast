"""Actual direct relay shot and slower native signal pixels via XTest.

The explicit fixture stages real free-floor positions and quiets hostile AI.
Switch damage still comes from one genuine player press and timed projectile;
sequence checkpoints observe real runtime time without setting answers.
"""
from pathlib import Path
import argparse,os,re,subprocess,tempfile,time
from PIL import ImageGrab
from check_defold_campaign_ui import NativeDriver,ROOT

class TacticsDriver(NativeDriver):
 def __enter__(self):
  env=dict(os.environ,XDG_DATA_HOME=str(self.folder/'data'),XDG_CACHE_HOME=str(self.folder/'cache'),XDG_CONFIG_HOME=str(self.folder/'config'),ALSOFT_DRIVERS='null',LIBGL_ALWAYS_SOFTWARE='1')
  env.pop('ENERGYBLAST_REGRESSION_RULES',None)
  self.stream=self.log.open('w')
  self.process=subprocess.Popen([str(self.engine),'--config=project.tactics_ui_test=1',str(ROOT/'pilots/defold/build/default/game.projectc')],env=env,stdout=self.stream,stderr=subprocess.STDOUT)
  try:self.wait('DEFOLD TACTICS FIXTURE READY')
  except BaseException:self.__exit__();raise
  return self
 def select(self,index):
  slot=index-1;self.click(772 if slot%2==0 else 1090,534-(slot//2)*153)
  self.wait('DEFOLD TACTICS CHOOSE mission='+str(index))


def main():
 p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
 with tempfile.TemporaryDirectory(prefix='energyblast-native-tactics-',dir='/tmp')as temporary:
  root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
  with TacticsDriver(a.engine,root/'relay')as d:
   d.select(3);target=d.coords('DEFOLD TACTICS RELAY READY');d.capture('direct-relay-ready',a.output is not None)
   d.click(*target);d.wait('DEFOLD TACTICS REAL DIRECT RELAY PASS shots=1 bounces=0 boss_locked=true')
   d.wait('DEFOLD TACTICS COMPLETE VOICE / CONTEXT REPLACE / NO RESTART PASS');d.capture('direct-relay-completed',a.output is not None)
   assert 'raid_relays'not in d.text(),d.text()
  print('DEFOLD NATIVE ACTUAL DIRECT RELAY / BOSS LOCK / FREE CHOICE VOICE PASS',flush=True)
  with TacticsDriver(a.engine,root/'sequence')as d:
   d.select(5);d.wait('DEFOLD TACTICS SEQUENCE READY')
   for checkpoint in range(1,7):
    signal=d.wait(r'DEFOLD TACTICS SIGNAL checkpoint='+str(checkpoint)+r' clock=([0-9.]+) lit=(\d+)',timeout=12)
    clock,lit=float(signal[1]),int(signal[2]);time.sleep(.025)
    screenshot=ImageGrab.grab().crop((0,0,1280,720)).convert('RGB')
    for order,y in [(1,545),(2,505),(3,465)]:
     rgb=screenshot.getpixel((1216,720-y))
     bright=rgb[0]>200 and rgb[1]>170 and rgb[2]<190
     dark=rgb[0]<140 and rgb[1]<160 and rgb[2]>60
     assert bright if order==lit else dark,(checkpoint,clock,lit,order,rgb)
    if a.output:screenshot.save(root/'sequence'/('actual-signal-'+str(checkpoint)+'.png'))
    print('DEFOLD NATIVE SLOW SIGNAL PIXELS checkpoint='+str(checkpoint)+' clock='+str(clock)+' lit='+str(lit)+' PASS',flush=True)
  print('DEFOLD NATIVE FREE RELAYS / OPTIONAL BOUNCE / SLOW LIGHTS PASS')

if __name__=='__main__':main()
