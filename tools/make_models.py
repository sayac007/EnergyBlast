"""Original low-poly robot kit, shared by all engine attempts; Blender background."""
import bpy,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'shared/assets';out.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
mint=mat('Mint armor',(.12,.8,.7));navy=mat('Dark joints',(.025,.08,.14));white=mat('Warm white',(.9,.96,.91));gold=mat('Solar gold',(1,.68,.12));eye=mat('Teal LED',(.3,1,.95))
root=bpy.data.objects.new('Robot',None);bpy.context.collection.objects.link(root)
def part(name,loc,scale,material,parent=root,roundness=.10):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 bevel=o.modifiers.new('Soft bevels','BEVEL');bevel.width=roundness;bevel.segments=2
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');o.parent=parent;return o
part('Body',(0,0,.9),(.7,.42,.58),mint)
part('Chest',(0,-.23,.94),(.38,.06,.25),gold,roundness=.04)
part('Head',(0,0,1.43),(.8,.5,.55),white)
part('Face',(0,-.265,1.42),(.64,.055,.3),navy,roundness=.06)
for x in [-.18,.18]:part('Eye', (x,-.304,1.45),(.11,.035,.12),eye,roundness=.025)
part('Antenna',(0,0,1.79),(.07,.07,.23),gold,roundness=.03)
for x,label in [(-.27,'L'),(.27,'R')]:
 part('Leg_'+label,(x,0,.32),(.23,.28,.5),navy,roundness=.08)
 part('Boot_'+label,(x,-.07,.1),(.28,.4,.18),mint,roundness=.07)
for x,label in [(-.49,'L'),(.49,'R')]:part('Arm_'+label,(x,0,.9),(.22,.25,.58),mint)
part('Blaster',(.49,-.27,.8),(.18,.48,.19),gold,roundness=.04)
# Native scene nodes are animated procedurally in each engine; no actor/reference art.
bpy.ops.export_scene.gltf(filepath=str(out/'robot.glb'),export_format='GLB',export_apply=True)
bpy.ops.export_scene.fbx(filepath=str(out/'robot.fbx'),apply_unit_scale=True,axis_forward='-Z',axis_up='Y',bake_anim=False)
print('Original robot exports:',[(p.name,p.stat().st_size) for p in out.iterdir()])
