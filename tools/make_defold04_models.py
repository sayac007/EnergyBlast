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
def portrait(name):
 # Actual original model render, used only for the full-screen character picker.
 from mathutils import Vector
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False
 scene.render.resolution_x=320;scene.render.resolution_y=320;scene.render.resolution_percentage=100;scene.render.film_transparent=True
 scene.world.color=(.35,.35,.35)
 bpy.ops.object.camera_add(location=(3.2,-6,3.4));camera=bpy.context.object
 camera.rotation_euler=(Vector((0,0,1.05))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=2.85;scene.camera=camera
 lamps=[]
 for pos,power,size in [((2,-4,7),650,5),((-4,-2,3),350,4),((0,4,5),500,3)]:
  bpy.ops.object.light_add(type='AREA',location=pos);lamp=bpy.context.object;lamp.data.energy=power;lamp.data.shape='DISK';lamp.data.size=size;lamp.rotation_euler=(-lamp.location).to_track_quat('-Z','Y').to_euler();lamps.append(lamp)
 scene.view_settings.view_transform='Standard';scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
 for obj in lamps+[camera]:bpy.data.objects.remove(obj,do_unlink=True)
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
export('hero');portrait('hero')
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
# Original non-robot playable cast: a toy dragon and an adventurous fennec.
clear()
body=mat('Dragon turquoise',(.05,.73,.55));belly=mat('Dragon apricot',(1,.67,.24));horn=mat('Dragon cream',(1,.92,.64));orange=mat('Fire orange',(1,.28,.06),True)
orb('Dragon body',(0,0,.86),(.47,.34,.56),body);orb('Dragon belly',(0,-.28,.82),(.32,.10,.38),belly)
orb('Dragon head',(0,-.05,1.56),(.52,.42,.43),body);orb('Dragon snout',(0,-.43,1.44),(.40,.28,.24),belly)
for x in [-.25,.25]:
 orb('Eye white',(x,-.34,1.68),(.18,.13,.22),white);orb('Pupil',(x,-.46,1.68),(.08,.035,.12),navy);orb('Eye sparkle',(x-.025,-.49,1.73),(.03,.02,.04),white)
 orb('Nostril',(x*.65,-.67,1.49),(.045,.02,.035),navy)
 bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=.12,radius2=.015,depth=.38,location=(x,.06,1.98));bpy.context.object.data.materials.append(horn)
 orb('Dragon foot',(x,-.12,.18),(.24,.33,.18),belly);orb('Dragon arm',(x*2,-.08,.80),(.16,.19,.33),body)
for i in range(6):orb('Tail scale',(0,.33+i*.12,.52-i*.065),(.19-i*.024,.18-i*.02,.18-i*.021),body)
for z in [.25,.5,.75]:orb('Tail spine',(0,z,.8-z*.5),(.08,.11,.16),belly)
export('dragon')
# Portrait includes the same wing silhouette; native wings flap as separate parts.
for side in [-1,1]:
 vertices=[(side*.30,.13,1.22),(side*1.05,.25,1.68),(side*.91,.40,.87),(side*.48,.29,.96)]
 mesh=bpy.data.meshes.new('Portrait wing');mesh.from_pydata(vertices,[],[(0,1,2),(0,2,3)]);mesh.materials.append(orange);obj=bpy.data.objects.new('Portrait wing',mesh);bpy.context.collection.objects.link(obj);obj.modifiers.new('Wing thickness','SOLIDIFY').thickness=.04
portrait('dragon')
for side in [-1,1]:
 clear();vertices=[(side*.30,.13,1.22),(side*1.05,.25,1.68),(side*.91,.40,.87),(side*.48,.29,.96)]
 mesh=bpy.data.meshes.new('Original wing membrane');mesh.from_pydata(vertices,[],[(0,1,2),(0,2,3)]);mesh.materials.append(orange);o=bpy.data.objects.new('Dragon wing',mesh);bpy.context.collection.objects.link(o);solid=o.modifiers.new('Wing thickness','SOLIDIFY');solid.thickness=.04
 for x,y,z in [vertices[0],vertices[1],vertices[2]]:orb('Wing tip',(x,y,z),(.06,.06,.06),belly)
 export('wing_left'if side<0 else'wing_right')
clear();fur=mat('Fennec amber',(1,.46,.12));cream=mat('Fennec cream',(1,.88,.58));purple=mat('Explorer plum',(.39,.12,.62))
orb('Fennec torso',(0,0,.83),(.37,.29,.48),purple);cube('Jacket seam',(0,-.29,.88),(.055,.035,.56),gold,.01)
orb('Fennec head',(0,0,1.48),(.49,.34,.39),fur)
for x in [-.33,.33]:
 bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=.22,radius2=.015,depth=.72,location=(x,.02,1.96));bpy.context.object.data.materials.append(fur)
 orb('Ear cream',(x,-.12,1.95),(.10,.035,.20),cream)
 orb('Cheek',(x*.75,-.26,1.34),(.25,.13,.18),cream)
 orb('Eye',(x*.64,-.32,1.55),(.075,.04,.11),navy);orb('Eye shine',(x*.64-.02,-.36,1.59),(.025,.018,.028),white)
 orb('Boot',(x*.65,-.08,.14),(.20,.27,.15),navy);orb('Hand',(x*1.3,-.13,.75),(.14,.14,.22),fur)
orb('Nose',(0,-.40,1.38),(.08,.07,.06),navy)
orb('Big tail',(.36,.35,.60),(.28,.34,.47),fur);orb('Tail tip',(.37,.43,.94),(.24,.29,.22),cream)
cube('Explorer pack',(0,.29,.90),(.42,.18,.48),cyan,.1)
export('fox');portrait('fox')
# Native projectiles use the same depth buffer as walls, rather than GUI dots.
for name,material in [('bolt',cyan),('enemy_bolt',pink),('fireball',orange)]:
 clear();orb('Projectile core',(0,0,0),(.13,.13,.22),material)
 if name=='fireball':
  for x,z in [(-.09,.12),(.07,.18),(0,.28)]:orb('Flame',(x,z,.01),(.07,.13,.07),gold)
 export(name)
clear();cube('Shut gate',(0,0,.55),(1,1,1.1),pink,.08);cube('Gate crown',(0,0,1.12),(1,1,.12),gold,.04);export('gate')
clear();orb('Soft contact shadow',(0,0,.105),(.47,.38,.008),mat('Shadow',(.075,.14,.19)));export('shadow')
clear();orb('Rescue drone',(0,0,.58),(.39,.34,.3),gold);cube('Drone visor',(0,-.29,.62),(.48,.08,.14),navy,.05)
for x in [-.2,.2]:orb('Drone eye',(x,-.34,.62),(.05,.02,.05),cyan)
for x in [-.55,.55]:cube('Rotor arm',(x,0,.7),(.4,.10,.07),navy,.02);orb('Rotor',(x,0,.72),(.25,.25,.025),white)
export('drone')
clear();cube('Treasure',(0,0,.25),(.55,.40,.42),purple,.10);cube('Treasure lid',(0,0,.5),(.58,.44,.14),gold,.04);cube('Latch',(0,-.23,.34),(.11,.05,.18),gold,.015);export('chest')
# Every wall-like piece inside the arena is generated from exactly the collider.
# Floor paint, flat vents and shadows are intentionally not wall geometry.
surface_manifest={}
data=json.loads((R/'shared/defold04.json').read_text())
palettes={'reactor':((.18,.55,.39),(.94,.57,.22)), 'citadel':((.29,.31,.66),(.69,.28,.53)), 'dock':((.13,.52,.68),(.95,.60,.22)), 'forge':((.34,.30,.51),(.94,.39,.19)), 'echo':((.24,.47,.53),(.62,.33,.80)), 'rescue':((.30,.58,.32),(.89,.66,.30))}
for mission in data['missions']:
 clear();ground,wall_color=palettes[mission['id']];accent=cyan if mission['id']in['reactor','echo','rescue']else gold
 tile=mat('Terrain '+mission['id'],ground);wallmat=mat('Wall '+mission['id'],wall_color);capmat=mat('Crown '+mission['id'],tuple(min(1,c*1.22+.04)for c in wall_color))
 shades=[tile,mat('Panel light '+mission['id'],tuple(min(1,c*1.08)for c in ground)),mat('Panel deep '+mission['id'],tuple(c*.94 for c in ground))]
 cube('Floating island',point(0,0,-.38),(21.7,15.7,.65),navy,.30)
 cube('Ground',point(0,0,-.06),(21.2,15.2,.22),tile,.18)
 for x in range(-10,11,2):
  for z in range(-6,7,2):cube('Broad terrain tile',point(x,z,.065),(1.98,1.98,.025),shades[(x//2+z//2)%3],.035)
 a=data['arena'];surfaces=[{'r':r,'type':'border'}for r in [[a[0],a[1],a[2],.3],[a[0],a[1]+a[3]-.3,a[2],.3],[a[0],a[1],.3,a[3]],[a[0]+a[2]-.3,a[1],.3,a[3]]]]
 surfaces +=[{'r':v,'type':'cover'}for v in mission['covers']]+[{'r':v,'type':'reflector'}for v in mission['reflectors']]
 surface_manifest[mission['id']]=surfaces
 for index,surface in enumerate(surfaces):
  x,z,w,h=surface['r'];kind=surface['type'];height=.86 if kind=='reflector'else 1.12
  solid=cube('SOLID '+str(index)+' '+kind,point(x+w/2,z+h/2,height/2),(w,h,height),cyan if kind=='reflector'else wallmat,.06)
  crown=cube('SOLID crown '+str(index)+' '+kind,point(x+w/2,z+h/2,height+.04),(w,h,.08),white if kind=='reflector'else capmat,.025)
  bpy.context.view_layer.update()
  corners=[o.matrix_world@Vector(c)for o in [solid,crown]for c in o.evaluated_get(bpy.context.evaluated_depsgraph_get()).bound_box]
  surface['geometry_r']=[min(v.x for v in corners),-max(v.y for v in corners),max(v.x for v in corners)-min(v.x for v in corners),max(v.y for v in corners)-min(v.y for v in corners)]
  if kind=='cover':
   # Insets stay strictly inside the solid footprint.
   cube('Roof trim',point(x+w/2,z+h/2,height+.085),(max(.05,w-.18),max(.05,h-.18),.012),capmat,.01)
   for k in range(max(1,int(w/.7))):cube('Roof rivet',point(x+.16+k*.7,z+.16,height+.10),(.085,.085,.018),gold,.008)
 # Gate is spawned separately and uses live state, never a fake painted wall.
 for mark in mission['secret']['marks']:
  x,z=mark['position']
  if mark['kind']=='arrow':
   mesh=bpy.data.meshes.new('Trail arrow');mesh.from_pydata([point(x-.24,z+.2,.095),point(x+.24,z+.2,.095),point(x,z-.32,.095)],[],[(0,1,2)]);mesh.materials.append(gold);obj=bpy.data.objects.new('Painted treasure arrow',mesh);bpy.context.collection.objects.link(obj)
  else:
   orb('Scorch / mysterious hatch',point(x,z,.09),(.33,.24,.012),navy)
   for j in range(3):cube('Hatch scratch',point(x-.16+j*.13,z,.105),(.045,.26,.014),gold,.005)
 for z in [-5.8,5.8]:
  for x in range(-9,10,2):cube('Painted runway',point(x,z,.09),(.6,.055,.015),accent,.004)
 for x,z in [mission['spawn'],mission['goal']]:
  bpy.ops.mesh.primitive_torus_add(major_radius=.68,minor_radius=.045,major_segments=32,minor_segments=6,location=point(x,z,.105));bpy.context.object.name='Flat landing mark';bpy.context.object.data.materials.append(gold)
 # Distant architectural scenery outside every reachable boundary, never fake cover.
 for x in [-11.5,11.5]:
  for z in [-6,-3,0,3,6]:
   cube('Outside island support',point(x,z,-.4),(.7,.7,.8),wallmat,.12)
 export(mission['id'])
(OUT/'surfaces.json').write_text(json.dumps(surface_manifest,indent=2)+'\n')
(OUT/'dimensions.json').write_text(json.dumps(bounds,indent=2)+'\n')
print('Original Defold 0.5 toy-world and character kit exported')
