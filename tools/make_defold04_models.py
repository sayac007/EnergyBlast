"""Original stylized 3D kit. Blender only; no downloaded art or image references."""
import bpy, math, json
from mathutils import Vector
bounds={}
from pathlib import Path
R=Path(__file__).resolve().parents[1];OUT=R/'shared/assets/defold04';OUT.mkdir(parents=True,exist_ok=True)
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
 bpy.context.view_layer.update()
 points=[o.matrix_world@Vector(c) for o in bpy.context.scene.objects if o.type=='MESH' for c in o.evaluated_get(bpy.context.evaluated_depsgraph_get()).bound_box]
 bounds[name]=[max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
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
# New silhouette: twin ion tanks, antenna, shoulder armour and white cheek fins.
for x in [-.22,.22]:
 orb('Ion tank',(x,.37,.89),(.14,.14,.35),cyan,root)
 cube('Shoulder armor',(x*2.3,0,1.12),(.32,.32,.12),white,.05,root)
cube('Antenna',(.32,.05,1.96),(.045,.045,.35),navy,.01,root)
orb('Antenna light',(.32,.05,2.15),(.08,.08,.08),gold,root)
export('hero')
clear();cube('CannonBase',(0,0,.19),(1.10,.96,.32),navy,.15);orb('Pivot',(0,0,.65),(.49,.44,.40),blue);cube('Armor',(0,.13,.72),(.93,.56,.58),white,.16);cube('Barrel',(0,-.48,.7),(.38,.88,.36),navy,.12);cube('Muzzle',(0,-.96,.7),(.34,.12,.27),pink,.06);orb('Warning lamp',(0,.08,1.10),(.17,.17,.10),pink)
for x in [-.45,.45]:cube('Side light',(x,-.05,.72),(.05,.47,.19),gold,.02)
export('cannon')
def point(x,z,h):return(x,-z,h)
# Relay is a distinct shootable floating crystal, never confused with a cannon.
clear();cube('Relay pedestal',(0,0,.18),(.85,.85,.3),navy,.12)
orb('Relay crystal',(0,0,.85),(.31,.31,.57),gold)
for x in [-.44,.44]:cube('Relay fin',(x,0,.66),(.12,.5,.9),white,.04)
export('relay')
# A rotating dish is placed on real cover, never on an invisible blocker.
clear();cube('Radar foot',(0,0,.12),(.55,.55,.24),navy,.08)
cube('Radar mast',(0,0,.5),(.12,.12,.75),white,.04)
dish=orb('Radar dish',(0,0,.98),(.52,.38,.15),gold)
dish.rotation_euler[0]=.55
cube('Radar receiver',(0,-.3,1.18),(.06,.55,.06),navy,.02)
orb('Radar signal',(0,-.58,1.18),(.09,.09,.09),cyan)
export('radar')

# Native energy fragments for animated final-hit explosions.
for name,material in [('spark',cyan),('spark_hot',gold)]:
 clear();bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.15,location=(0,0,0))
 o=bpy.context.object;o.name='Angular energy fragment';o.scale=(.8,.65,1.5);o.data.materials.append(material);export(name)
for mission in json.loads((R/'shared/defold04.json').read_text())['missions']:
 clear();accent={'reactor':cyan,'citadel':pink,'dock':gold}[mission['id']]
 tile=mat('Bright '+mission['id'],{'reactor':(.20,.34,.38),'citadel':(.31,.24,.40),'dock':(.23,.31,.43)}[mission['id']])
 shades=[tile,mat('Panel light '+mission['id'],tuple(min(1,c*1.10)for c in tile.diffuse_color[:3])),mat('Panel deep '+mission['id'],tuple(c*.9 for c in tile.diffuse_color[:3]))]
 cube('Floating foundation',point(0,0,-.38),(21.7,15.7,.65),navy,.32)
 cube('Arena floor',point(0,0,-.06),(21.2,15.2,.22),tile,.18)
 for x in range(-10,11,2):
  for z in range(-6,7,2):cube('Floor panel',point(x,z,.065),(1.94,1.94,.025),shades[(x//2+z//2)%3],.06)
 for z in [-7.4,7.4]:cube('Edge light',point(0,z,.13),(20.5,.09,.07),accent,.02)
 for x in [-10.4,10.4]:cube('Edge light',point(x,0,.13),(.09,14.5,.07),accent,.02)
 for x,z,w,h in mission['covers']:
  cube('Cover',point(x+w/2,z+h/2,.53),(w,h,1.06),blue,.14)
  cube('Cover cap',point(x+w/2,z+h/2,1.09),(w+.07,h+.07,.13),white,.05)
  for k in range(max(1,round(w/.5))):cube('Hazard stripe',point(x+.18+k*.5,z-.015,.65),(.2,.04,.32),gold,.015)
  cube('Cover inlay',point(x+w/2,z+h/2,1.17),(max(.1,w-.25),.09,.025),accent,.01)
 for x,z,w,h in mission['reflectors']:
  cube('Reflector base',point(x+w/2,z+h/2,.30),(w,h,.6),navy,.08)
  cube('Reflector beam',point(x+w/2,z+h/2,.64),(w+.02,h+.02,.13),cyan,.04)
 for x in [-10.15,10.15]:
  for z in [-6.9,6.9]:
   cube('Corner pillar',point(x,z,.6),(.45,.45,1.2),white,.1);orb('Beacon',point(x,z,1.24),(.23,.23,.12),gold)
 for z in [-5.8,5.8]:
  for x in range(-9,10):cube('Runway dash',point(x,z,.09),(.42,.045,.035),accent,.01)
 for x in [-9,-5,-1,3,7]:
  for k in range(4):cube('Vent grille',point(x+k*.15,5.8,.08),(.055,.55,.025),navy,.01)
 for x in [-11.1,11.1]:
  for z in [-6,-3,0,3,6]:
   cube('Dock buttress',point(x,z,-.15),(.7,.7,.95),blue,.12)
   cube('Power strip',point(x,z,.36),(.5,.5,.10),accent,.04)
 for x,z in [(-9,-8.1),(7.5,8.1)]:
  cube('Service tower',point(x,z,.65),(.8,.65,2.0),navy,.16)
  for k in range(3):cube('Tower light',point(x,z-.34,.2+k*.45),(.56,.06,.1),accent,.02)
 # Painted circuit tracks and docking markings enrich clear walkable space.
 for z in [-4,0,4]:
  cube('Floor conduit',point(0,z,.09),(19.5,.035,.016),navy,.005)
  for x in [-8,-4,0,4,8]:cube('Conduit glow',point(x,z,.105),(.36,.05,.018),accent,.005)
 for x,z,w,h in mission['covers']:
  for dx in [.15,w-.15]:
   for dz in [.15,h-.15]:orb('Roof bolt',point(x+dx,z+dz,1.18),(.055,.055,.018),navy)
 for x,z in [mission['spawn'],mission['goal']]:
  bpy.ops.mesh.primitive_torus_add(major_radius=.68,minor_radius=.045,major_segments=32,minor_segments=6,location=point(x,z,.09))
  bpy.context.object.name='Landing ring';bpy.context.object.data.materials.append(accent)
 export(mission['id'])
(OUT/'dimensions.json').write_text(json.dumps(bounds,indent=2)+'\n')
print('Original Defold 0.4 models exported')
