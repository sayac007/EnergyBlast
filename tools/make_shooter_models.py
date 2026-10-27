"""Original stylized 3D kit. Blender only; no downloaded art or image references."""
import bpy, math, json
from pathlib import Path
R=Path(__file__).resolve().parents[1];OUT=R/'shared/assets/shooter';OUT.mkdir(parents=True,exist_ok=True)
def clear():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color,glow=False):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.44;bs.inputs['Metallic'].default_value=.12
 if glow:bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=.7
 return m
navy=mat('Midnight titanium',(.035,.065,.16));white=mat('Porcelain armor',(.82,.92,1));cyan=mat('Ion cyan',(.08,.82,.83),True);pink=mat('Pulse coral',(1,.16,.36),True);gold=mat('Solar gold',(1,.65,.13),True);blue=mat('Ultramarine',(.13,.29,.63));stone=mat('Indigo stone',(.14,.18,.32));floor=mat('Blue slate',(.23,.36,.43));sand=mat('Sand trail',(.49,.52,.48));leaf=mat('Mint foliage',(.13,.56,.42))
def cube(name,pos,scale,material,bevel=.1,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if bevel:
  b=o.modifiers.new('Soft edges','BEVEL');b.width=min(bevel,min(scale)*.4);b.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 o.parent=parent;return o
def orb(name,pos,scale,material,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=pos);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material);o.parent=parent
 for p in o.data.polygons:p.use_smooth=True
 return o
def export(name):
 bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')),export_format='GLB',export_apply=True)
 bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.gltf')),export_format='GLTF_SEPARATE',export_apply=True)
clear();root=bpy.data.objects.new('Hero',None);bpy.context.collection.objects.link(root)
cube('Body',(0,0,.92),(.73,.48,.58),blue,.15,root);cube('Chest',(0,-.28,.96),(.42,.07,.24),white,.06,root);orb('Power core',(0,-.33,.97),(.1,.035,.1),cyan,root)
orb('Helmet',(0,0,1.48),(.49,.36,.41),white,root);cube('Visor',(0,-.32,1.48),(.72,.1,.27),navy,.12,root)
for x in [-.18,.18]:cube('Eye',(x,-.38,1.5),(.12,.02,.12),cyan,.04,root)
for x,l in [(-.25,'L'),(.25,'R')]:
 cube('Leg_'+l,(x,0,.37),(.25,.29,.48),navy,.08,root);cube('Boot_'+l,(x,-.10,.14),(.32,.46,.23),white,.07,root);cube('Sole_'+l,(x,-.1,.045),(.33,.46,.06),gold,.02,root)
for x,l in [(-.48,'L'),(.48,'R')]:
 orb('Shoulder_'+l,(x,0,1.06),(.19,.22,.23),cyan,root);cube('Arm_'+l,(x,-.025,.8),(.23,.28,.42),blue,.10,root);orb('Hand_'+l,(x,-.1,.59),(.14,.15,.14),white,root)
cube('Blaster',(.49,-.36,.75),(.26,.57,.26),navy,.09,root);cube('Emitter',(.49,-.67,.75),(.22,.07,.18),pink,.04,root);cube('Backpack',(0,.30,.94),(.4,.18,.44),navy,.08,root)
export('hero')
clear();cube('CannonBase',(0,0,.19),(1.10,.96,.32),navy,.15);orb('Pivot',(0,0,.65),(.49,.44,.40),blue);cube('Armor',(0,.13,.72),(.93,.56,.58),white,.16);cube('Barrel',(0,-.48,.7),(.38,.88,.36),navy,.12);cube('Muzzle',(0,-.96,.7),(.34,.12,.27),pink,.06);orb('Warning lamp',(0,.08,1.10),(.17,.17,.10),pink)
for x in [-.45,.45]:cube('Side light',(x,-.05,.72),(.05,.47,.19),gold,.02)
export('cannon')
def point(x,z,h):return(x,-z,h)
for mission in json.loads((R/'shared/combat.json').read_text())['missions']:
 clear();cube('Floating foundation',point(0,0,-.38),(14.7,10.7,.65),navy,.32);cube('Arena floor',point(0,0,-.06),(14.2,10.2,.22),floor,.18)
 # Inlaid paths; tiles are graphics, never invisible collision obstacles.
 for x in range(-6,7,2):
  for z in range(-4,5,2):cube('Floor panel',point(x,z,.065),(1.90,1.90,.025),stone,.06)
 for z in [-4.9,4.9]:cube('Edge light',point(0,z,.13),(13.5,.08,.07),cyan,.02)
 for x in [-6.9,6.9]:cube('Edge light',point(x,0,.13),(.08,9.5,.07),cyan,.02)
 for rect in mission['covers']:
  x,z,w,h=rect;cube('Cover',point(x+w/2,z+h/2,.53),(w,h,1.06),blue,.14);cube('Cover cap',point(x+w/2,z+h/2,1.09),(w+.07,h+.07,.13),white,.05)
  for k in range(max(1,round(w/.4))):cube('Gold hazard stripe',point(x+.18+k*.4,z-.015,.65),(.16,.04,.32),gold,.015)
 for rect in mission['reflectors']:
  x,z,w,h=rect;cube('Reflector base',point(x+w/2,z+h/2,.30),(w,h,.6),navy,.08);cube('Reflector beam',point(x+w/2,z+h/2,.64),(w+.02,h+.02,.13),cyan,.04)
 for x in [-6.7,6.7]:
  for z in [-4.5,4.5]:
   cube('Corner pillar',point(x,z,.6),(.45,.45,1.2),white,.1);orb('Beacon',point(x,z,1.24),(.23,.23,.12),gold)
 for x,z in [(-6.2,3.8),(-5.9,-3.9),(5.8,3.8),(5.8,-3.9)]:
  cube('Planter',point(x,z,.2),(.65,.65,.35),navy,.12)
  for k in range(3):orb('Plant',point(x+(k-1)*.15,z,.55+k*.13),(.17,.17,.35),leaf)
 export(mission['id'])
print('Shooter meshes exported',[(p.name,p.stat().st_size) for p in OUT.glob('*.glb')])
