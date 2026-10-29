"""Capture the real native renderer under Xvfb; no concept art or fake UI."""
import argparse,os,subprocess,time
from pathlib import Path
from PIL import ImageGrab
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.output.resolve();root.mkdir(parents=True,exist_ok=False)
for name,options in [('menu',[]),('characters',['--config=project.capture_page=characters']),('arsenal',['--config=project.capture_page=gear'])]+[(m,['--config=project.capture_mode=1','--config=project.capture_sector='+str(i),'--config=project.capture_character='+('dragon'if i%2 else'fox')])for i,m in enumerate(['prisma','citadel','dock','forge','echo','rescue'],1)]:
 state=root/name;state.mkdir()
 for folder in ['data','cache','config']:(state/folder).mkdir()
 env=dict(os.environ,LIBGL_ALWAYS_SOFTWARE='1',ALSOFT_DRIVERS='null',XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'))
 with(state/'runtime.log').open('w')as log:
  proc=subprocess.Popen(['/tmp/energyblast-defold-tools/dmengine']+options+[str(R/'pilots/defold/build/default/game.projectc')],env=env,stdout=log,stderr=subprocess.STDOUT)
  try:time.sleep(1.1);ImageGrab.grab().crop((0,0,1280,720)).save(root/(name+'.png'))
  finally:proc.terminate();proc.wait(timeout=5)
 assert 'ERROR:'not in(state/'runtime.log').read_text(),(state/'runtime.log').read_text()
 print(name,'native capture PASS',flush=True)
