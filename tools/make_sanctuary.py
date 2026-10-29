"""Original small, passable sanctuary platform and holographic ziggurat beacon."""
from pathlib import Path
import hashlib,json,math
import bpy
R=Path(__file__).resolve().parents[1];A=R/'shared/assets/defold10';A.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
navy=material('Sanctuary ceramic',(0.045,.16,.23));metal=material('Sanctuary gold',(.35,.48,.40));light=material('Luminous sanctuary mint',(.15,1,.68))
def cylinder(name,radius,depth,z,mat,vertices=64):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=(0,0,z));o=bpy.context.object;o.name=name;o.data.materials.append(mat);return o
def box(name,location,scale,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=location);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 b=o.modifiers.new('Soft edge','BEVEL');b.width=.035;b.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name);return o
# All floor tiers are shallow and traversable; this is not a new physical wall.
cylinder('Passable luminous perimeter',1.20,.035,.043,light)
cylinder('Passable platform',1.13,.035,.066,navy)
for j in range(4):
 angle=j*math.pi/2;x,y=math.cos(angle)*.96,math.sin(angle)*.96
 o=box('Floor guidance lane',(x,y,.093),(.15,.33,.018),light);o.rotation_euler.z=angle
# Small raised holographic stepped beacon at the rear edge leaves the center clear.
for j in range(3):
 size=.58-j*.14;box('Ziggurat luminous terrace '+str(j),(0,-.86,.18+j*.19),(size,size,.045),light)
 box('Ziggurat terrace core '+str(j),(0,-.86,.13+j*.19),(size*.93,size*.93,.08),metal)
bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.19,radius2=0,depth=.35,location=(0,-.86,.81));bpy.context.object.name='Luminous ziggurat beacon';bpy.context.object.data.materials.append(light)
objects=list(bpy.context.scene.objects);bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
path=A/'sanctuary.gltf';bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLTF_SEPARATE',use_selection=True,export_yup=True)
(A/'models.json').write_text(json.dumps({'sanctuary':{'tag':'model','texture':None}},indent=2)+'\n')
(A/'PROVENANCE.json').write_text(json.dumps({'created':'2026-10-29','origin':'Original procedural geometry by tools/make_sanctuary.py; no downloaded art or reference-game assets','role':'Passable protection platform and stepped light beacon; real projectile absorption is enforced in gameplay','files':[{'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [path,A/'sanctuary.bin']]},indent=2)+'\n')
print('Original sanctuary geometry exported')
