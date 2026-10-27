from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'pilots/godot/assets';dest.mkdir(parents=True,exist_ok=True)
shutil.copyfile(ROOT/'shared/pilot.json',dest/'pilot.json')
for name in ['robot.glb']:
 if (ROOT/'shared/assets'/name).exists():shutil.copyfile(ROOT/'shared/assets'/name,dest/name)
shutil.copytree(ROOT/'shared/audio',dest/'audio',dirs_exist_ok=True)

shutil.copytree(ROOT/'shared/notices',dest/'notices',dirs_exist_ok=True)
