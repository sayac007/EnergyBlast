"""Run Godot integration tests, then verify a save in a fresh process."""
import argparse,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--godot',type=Path,default=Path('/workspace/tools/godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64'));a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='energyblast-test-',dir='/tmp') as d:
 env=dict(os.environ,XDG_DATA_HOME=d+'/data',XDG_CONFIG_HOME=d+'/config',XDG_CACHE_HOME=d+'/cache')
 base=[str(a.godot),'--headless','--audio-driver','Dummy','--path',str(ROOT/'pilots/godot')]
 commands=[['--editor','--import','--quit'],['--script','res://tests/pilot.gd'],['--script','res://tests/combat.gd'],['--script','res://tests/persistence.gd','--','--write'],['--script','res://tests/persistence.gd']]
 for args in commands:
  r=subprocess.run(base+args,env=env,capture_output=True,text=True,timeout=90)
  text=r.stdout+r.stderr
  if args[0]!='--editor' or r.returncode:print(text,end='')
  if r.returncode or any(x in text for x in ['SCRIPT ERROR','ERROR:','WARNING: ObjectDB','leaked']):raise SystemExit(1)
print('GODOT INTEGRATION AND PROCESS RESTART: PASS (test audio disabled; media decoded separately)')
