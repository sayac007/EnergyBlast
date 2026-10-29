"""Create the Unity input kit from the common arena/assets, without an Editor claim."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=json.loads((R/'shared/pilot.json').read_text());A=R/'pilots/unity/Assets';dest=A/'Resources/EnergyBlast'
shutil.copyfile(R/'shared/assets/robot.fbx',dest/'robot.fbx')
for p in (R/'shared/audio/de').iterdir():
 if p.suffix in ['.ogg','.txt']:shutil.copyfile(p,dest/'de'/p.name)
shutil.copyfile(R/'shared/pilot.json',dest/'pilot.json')
f=lambda n:str(float(n))+'f'
v=lambda a:'new Vector2('+','.join(map(f,a))+')'
rects=lambda arr:'new Rect[] {'+','.join('new Rect('+','.join(map(f,a))+')' for a in arr)+'}'
lines=['using UnityEngine;\nusing System.Collections.Generic;\nnamespace EnergyBlast {\npublic static class PilotData {\npublic static Mission[] Missions = new Mission[] {']
for m in D['missions']:
 lines.append('new Mission { Id="'+m['id']+'", Title="'+m['title']+'", Spawn='+v(m['spawn'])+', Goal='+v(m['goal'])+', Covers='+rects(m['covers'])+', Reflectors='+rects(m['reflectors'])+', Secret='+v(m['secret']['position'])+', Landmark='+v(m['secret']['hint_landmark'])+', Gate='+('new Rect('+','.join(map(f,m['gate_rect']))+')' if 'gate_rect'in m else 'new Rect()')+', Patrol=new Vector2[] {'+','.join(v(p) for p in m.get('patrol',[]))+'}},')
lines+=['};\npublic static Dictionary<string,int> Rewards = new Dictionary<string,int> {']
for k,value in D['rewards'].items():lines.append('{"'+k+'",'+str(value)+'},')
lines+=['};\n}\npublic class Mission {public string Id,Title; public Vector2 Spawn,Goal,Secret,Landmark; public Rect[] Covers,Reflectors; public Rect Gate; public Vector2[] Patrol;}\n}']
(A/'EnergyBlast/PilotData.cs').write_text('\n'.join(lines))

shutil.copytree(R/'shared/notices',dest/'notices',dirs_exist_ok=True)
