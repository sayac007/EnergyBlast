"""Original detailed rigid-part characters, AO baking and themed arena geometry.
Reference research: docs/ART_DIRECTION.md. No reference-game geometry is imported.
Run with Blender 4.3.2; output contains real, runtime-consumed meshes and textures.
"""
from pathlib import Path
import bpy,bmesh,math,json,random
from mathutils import Vector
R=Path(__file__).resolve().parents[1];OUT=R/'shared/assets/defold06';OUT.mkdir(exist_ok=True)
metadata={};rigs={};bounds={};rng=random.Random(606)
def clear():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,c):
 m=bpy.data.materials.get(name)or bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=.48
 return m
ink=mat('Deep blue ink',(.025,.045,.095));cream=mat('Warm ivory',(.96,.86,.62));white=mat('Porcelain',(.91,.97,1));teal=mat('Jade',(.035,.58,.52));cyan=mat('Mint light',(.13,.89,.85));gold=mat('Honey gold',(1,.61,.075));coral=mat('Coral',(.94,.16,.28));purple=mat('Royal iris',(.38,.14,.70));leather=mat('Warm leather',(.26,.10,.06));orange=mat('Tangerine',(.97,.31,.065))
part='body'
def finish(o,m):
 o.data.materials.append(m);o['rig_part']=part
 for p in o.data.polygons:p.use_smooth=True
 return o
def box(n,p,s,m,b=.08):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.scale=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if b:
  mod=o.modifiers.new('Sculpted edges','BEVEL');mod.width=min(b,min(s)*.42);mod.segments=4;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return finish(o,m)
def ball(n,p,s,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=p);o=bpy.context.object;o.name=n;o.scale=s;return finish(o,m)
def cone(n,p,r1,r2,h,m,rot=(0,0,0)):
 bpy.ops.mesh.primitive_cone_add(vertices=20,radius1=r1,radius2=r2,depth=h,location=p,rotation=rot);o=bpy.context.object;o.name=n;mod=o.modifiers.new('Round rim','BEVEL');mod.width=.035;mod.segments=3;return finish(o,m)
def tube(n,points,radius,m):
 curve=bpy.data.curves.new(n,'CURVE');curve.dimensions='3D';curve.bevel_depth=radius;curve.bevel_resolution=3
 spline=curve.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
 for b,p in zip(spline.bezier_points,points):b.co=p;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 o=bpy.data.objects.new(n,curve);bpy.context.collection.objects.link(o);o.data.materials.append(m);o['rig_part']=part;return o
def ring(n,p,major,minor,m):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=40,minor_segments=8,location=p);return finish(bpy.context.object,m)
def export(name,objects=None,texture=None,tag='model'):
 bpy.ops.object.select_all(action='DESELECT');objects=objects or[o for o in bpy.context.scene.objects if o.type=='MESH']
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.context.view_layer.update()
 points=[o.matrix_world@Vector(c)for o in objects for c in o.evaluated_get(bpy.context.evaluated_depsgraph_get()).bound_box]
 bounds[name]=[max(p[i]for p in points)-min(p[i]for p in points)for i in range(3)]
 for fmt,ext in [('GLTF_SEPARATE','.gltf'),('GLB','.glb')]:bpy.ops.export_scene.gltf(filepath=str(OUT/(name+ext)),export_format=fmt,export_apply=True,use_selection=True)
 metadata[name]={'texture':texture,'tag':tag}
 if tag in ['model','stage']and len(objects)>1:
  # Keep semantic source meshes for audit, batch the identical static geometry for runtime.
  bpy.ops.object.select_all(action='DESELECT')
  for o in objects:o.select_set(True)
  bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();batch=bpy.context.object
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
  bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.runtime.gltf')),export_format='GLTF_SEPARATE',export_apply=True,use_selection=True)
  metadata[name]['runtime']=name+'.runtime.gltf'
def portrait(name):
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False;scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.27,.30,.38)
 bpy.ops.object.camera_add(location=(3,-7,3.9));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,1.05))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=2.9;scene.camera=camera
 lamps=[]
 for p,power,size in [((-3,-4,7),550,5),((4,-2,4),250,4),((1,3,5),600,3)]:
  bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.data.energy=power;o.data.size=size;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler();lamps.append(o)
 scene.view_settings.view_transform='AgX';scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
 for o in lamps+[camera]:bpy.data.objects.remove(o,do_unlink=True)
def actor(name,pivots):
 # Apply meshes, keep rigid-part vertex groups, unwrap once and bake real AO.
 objects=[o for o in bpy.context.scene.objects if o.type in ['MESH','CURVE']]
 for o in objects:
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
  group=o.vertex_groups.new(name=o.get('rig_part','body'));group.add(range(len(o.data.vertices)),1,'REPLACE')
 bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();joined=bpy.context.object
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.015);bpy.ops.object.mode_set(mode='OBJECT')
 image=bpy.data.images.new(name+' AO',width=1024,height=1024,alpha=False);image.generated_color=(1,1,1,1)
 for material in joined.data.materials:
  node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;material.node_tree.nodes.active=node
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.bake.margin=4;scene.world.color=(1,1,1)
 bpy.ops.object.bake(type='AO');image.filepath_raw=str(OUT/(name+'-ao.png'));image.file_format='PNG';image.save()
 # Render the same detailed model for picker thumbnails before separation.
 portrait(name)
 source=joined.data;uv=source.uv_layers.active;groups={v.index:g.name for g in joined.vertex_groups for v in []}
 memberships={v.index:joined.vertex_groups[v.groups[0].group].name for v in source.vertices}
 rigid=[]
 for group in joined.vertex_groups:
  indices=[v.index for v in source.vertices if memberships[v.index]==group.name];indexmap={v:i for i,v in enumerate(indices)}
  faces=[p for p in source.polygons if all(v in indexmap for v in p.vertices)]
  if not faces:continue
  mesh=bpy.data.meshes.new(name+' '+group.name);mesh.from_pydata([source.vertices[i].co[:]for i in indices],[],[[indexmap[i]for i in p.vertices]for p in faces]);mesh.materials.clear()
  for m in source.materials:mesh.materials.append(m)
  layer=mesh.uv_layers.new(name='UVMap')
  for face,original in zip(mesh.polygons,faces):
   face.material_index=original.material_index;face.use_smooth=True
   for a,b in zip(face.loop_indices,original.loop_indices):layer.data[a].uv=uv.data[b].uv
  obj=bpy.data.objects.new(name+' '+group.name,mesh);bpy.context.collection.objects.link(obj);pivot=pivots.get(group.name,(0,0,0))
  for v in mesh.vertices:v.co-=Vector(pivot)
  runtime_name=name if group.name=='body'else(name+'_'+group.name)
  export(runtime_name,[obj],name+'-ao.png','actor');rigid.append({'model':runtime_name,'part':group.name,'pivot':[pivot[0],pivot[2],-pivot[1]]})
 bpy.data.objects.remove(joined,do_unlink=True);rigs[name]=rigid
import sys
if '--world-only' not in sys.argv:
 # Nova: an original young explorer, not the old box robot.
 clear();skin=mat('Nova skin',(.78,.43,.24));hair=mat('Nova hair',(.065,.035,.045));jacket=mat('Nova cobalt',(.07,.24,.64));part='body'
 ball('Torso',(0,0,.92),(.35,.23,.43),jacket);box('Vest',(0,-.20,.97),(.45,.12,.46),teal,.10);box('Zipper',(0,-.28,.96),(.035,.025,.4),gold,.008)
 ball('Head',(0,-.035,1.65),(.43,.34,.44),skin);ball('Nose',(0,-.36,1.61),(.075,.10,.07),skin)
 for x in [-.18,.18]:
  ball('White eye',(x,-.31,1.73),(.12,.065,.15),white);ball('Dark iris',(x,-.37,1.73),(.065,.025,.09),ink);ball('Eye glint',(x-.018,-.397,1.77),(.022,.009,.029),white)
  tube('Expressive brow',[(x-.10,-.35,1.94),(x,-.38,1.97),(x+.09,-.34,1.94)],.027,hair)
 ball('Smile opening',(0,-.355,1.48),(.105,.035,.058),ink);ball('Friendly teeth',(0,-.385,1.50),(.064,.014,.019),white);ball('Smile tongue',(0,-.386,1.453),(.033,.012,.015),coral)
 for i in range(7):ball('Sculpted hair lock',(-.3+i*.095,-.1+(i%3)*.07,1.99+math.sin(i)*.05),(.17,.22,.16),hair)
 # Raised teal goggles, scarf, pack and belt make a readable explorer silhouette.
 for x in [-.19,.19]:ball('Goggle rim',(x,-.24,2.04),(.16,.07,.10),gold);ball('Goggle glass',(x,-.295,2.04),(.12,.026,.068),cyan)
 ring('Neck scarf',(0,0,1.29),.24,.075,coral);box('Belt',(0,-.01,.66),(.65,.40,.12),leather,.04);box('Buckle',(0,-.23,.66),(.17,.07,.14),gold,.03)
 box('Backpack',(0,.25,1.03),(.48,.22,.49),leather,.12);ball('Pack badge',(0,.385,1.1),(.10,.025,.10),gold)
 for side in [-1,1]:
  part='leg_l'if side<0 else'leg_r';x=side*.21
  box('Trousers',(x,0,.43),(.27,.28,.45),ink,.09);box('Adventure boot',(x,-.08,.15),(.32,.49,.25),leather,.08);box('Boot sole',(x,-.08,.04),(.34,.5,.07),gold,.025)
  part='arm_l'if side<0 else'arm_r';x=side*.43
  ball('Sleeve',(x,0,1.03),(.17,.19,.27),jacket);ball('Glove',(x,-.10,.78),(.15,.15,.15),leather);box('Wrist cuff',(x,-.02,.83),(.25,.26,.11),teal,.03)
  if side>0:box('Pulse tool',(x,-.36,.83),(.25,.48,.24),gold,.08);box('Tool muzzle',(x,-.62,.83),(.20,.08,.17),cyan,.03)
 actor('hero',{'arm_l':(-.43,0,1.08),'arm_r':(.43,0,1.08),'leg_l':(-.21,0,.63),'leg_r':(.21,0,.63)})
 # Flammi: expressive young dragon with horns, webbed wings and a neckerchief.
 clear();part='body';body=mat('Dragon jade',(.055,.58,.40));belly=mat('Dragon butter',(1,.75,.26));membrane=mat('Dragon wings',(.89,.24,.12));iris=mat('Dragon amber',(1,.50,.04))
 ball('Dragon torso',(0,.02,.84),(.42,.31,.50),body);ball('Sculpted belly',(0,-.26,.80),(.32,.10,.34),belly)
 ball('Dragon head',(0,-.10,1.54),(.49,.40,.43),body);ball('Broad dragon snout',(0,-.44,1.42),(.39,.30,.25),belly)
 for side in [-1,1]:
  x=side*.25;ball('Cheek',(x,-.28,1.44),(.19,.18,.20),body);ball('Eye white',(x,-.37,1.68),(.17,.10,.21),white);ball('Amber iris',(x,-.465,1.69),(.095,.035,.13),iris);ball('Pupil',(x,-.49,1.69),(.047,.018,.10),ink);ball('Catchlight',(x-.025,-.51,1.75),(.03,.012,.035),white)
  tube('Dragon eyebrow',[(x-.13,-.35,1.90),(x,-.37,1.94),(x+.11,-.32,1.90)],.042,body)
  cone('Swept horn',(x,.05,1.99),.11,.01,.37,cream,rot=(0,side*.28,0));ball('Nostril',(x*.62,-.70,1.47),(.035,.02,.025),ink)
 cone('Crown horn',(0,.17,1.92),.12,0,.30,belly,rot=(.35,0,0));tube('Friendly smile',[(-.18,-.66,1.32),(0,-.70,1.28),(.18,-.66,1.32)],.018,ink)
 ring('Explorer neckerchief',(0,0,1.17),.29,.075,purple);box('Scarf tip',(.20,-.24,.99),(.19,.06,.34),purple,.03);ball('Medallion',(0,-.35,1.1),(.10,.035,.11),gold)
 for side in [-1,1]:
  x=side*.26;part='leg_l'if side<0 else'leg_r';ball('Dragon haunch',(x,.04,.40),(.22,.25,.32),body);ball('Dragon paw',(x,-.15,.14),(.23,.32,.15),belly)
  for dx in [-.10,0,.10]:ball('Ivory claw',(x+dx,-.43,.13),(.036,.07,.035),cream)
  part='arm_l'if side<0 else'arm_r';ball('Dragon arm',(side*.43,-.04,.83),(.15,.18,.29),body);ball('Dragon hand',(side*.44,-.14,.65),(.16,.18,.14),belly)
  part='wing_l'if side<0 else'wing_r'
  vertices=[(side*.32,.19,1.17),(side*.96,.31,1.70),(side*.86,.44,.92),(side*.49,.34,.99)]
  mesh=bpy.data.meshes.new('Webbed wing');mesh.from_pydata(vertices,[],[(0,1,2),(0,2,3)]);o=bpy.data.objects.new('Webbed wing',mesh);bpy.context.collection.objects.link(o);finish(o,membrane);o.modifiers.new('Membrane thickness','SOLIDIFY').thickness=.04
  tube('Wing leading edge',[vertices[0],vertices[1],vertices[2]],.035,belly);tube('Wing rib',[vertices[0],vertices[2]],.022,belly)
 part='tail';tube('Dragon tail',[(0,.25,.64),(.1,.55,.40),(.38,.85,.22),(.57,.87,.3)],.12,body)
 for i in range(3):cone('Tail spike',(.14+i*.14,.52+i*.13,.55-i*.08),.075,0,.17,belly)
 actor('dragon',{'arm_l':(-.43,0,1.0),'arm_r':(.43,0,1.0),'leg_l':(-.26,0,.60),'leg_r':(.26,0,.60),'wing_l':(-.32,.19,1.17),'wing_r':(.32,.19,1.17),'tail':(0,.25,.64)})
 # Fennek: a jacketed fox explorer with distinct silhouette and articulated limbs.
 clear();part='body';fur=mat('Fox copper',(.95,.35,.075));jacket=mat('Fox plum',(.27,.095,.46));scarf=mat('Fox seafoam',(.12,.73,.58))
 ball('Fox torso',(0,0,.88),(.34,.25,.43),jacket);box('Jacket placket',(0,-.23,.90),(.10,.045,.47),gold,.025)
 ball('Fox skull',(0,-.02,1.57),(.42,.31,.35),fur)
 for side in [-1,1]:
  x=side*.29;cone('Great fennec ear',(x,.04,1.97),.20,.01,.68,fur,rot=(0,side*.24,0));ball('Ear inner',(x,-.085,1.98),(.10,.035,.21),cream)
  ball('White cheek',(side*.19,-.25,1.44),(.24,.14,.17),cream);ball('Eye',(side*.18,-.31,1.64),(.085,.035,.115),ink);ball('Glint',(side*.18-.024,-.342,1.68),(.025,.012,.03),white)
  tube('Brow',[(side*.18-.09,-.30,1.80),(side*.18,-.32,1.83),(side*.18+.09,-.30,1.79)],.025,fur)
 ball('Fox nose',(0,-.42,1.49),(.075,.06,.055),ink);tube('Fox smile',[(-.08,-.37,1.39),(0,-.40,1.36),(.08,-.37,1.39)],.016,ink)
 ring('Seafoam scarf',(0,0,1.25),.24,.075,scarf);box('Scarf flap',(-.20,-.20,1.08),(.18,.06,.28),scarf,.035)
 box('Satchel',(0,.26,.94),(.44,.20,.40),leather,.10);ball('Satchel clasp',(0,.375,.97),(.085,.025,.085),gold)
 for side in [-1,1]:
  part='leg_l'if side<0 else'leg_r';x=side*.20;box('Fox trousers',(x,0,.41),(.25,.27,.42),ink,.08);box('Fox boots',(x,-.08,.14),(.30,.46,.24),leather,.08);box('Fox soles',(x,-.08,.035),(.31,.47,.06),gold,.02)
  part='arm_l'if side<0 else'arm_r';x=side*.41;ball('Coat sleeve',(x,0,1.0),(.15,.18,.25),jacket);ball('Fox glove',(x,-.1,.73),(.14,.14,.17),fur)
  if side>0:box('Star projector',(x,-.33,.79),(.24,.43,.21),teal,.07);ball('Projector lens',(x,-.58,.79),(.10,.045,.095),gold)
 part='tail';tube('Expressive tail',[(.15,.27,.58),(.38,.47,.63),(.47,.50,.96)],.18,fur);ball('Ivory tail tip',(.47,.50,1.01),(.18,.19,.21),cream)
 actor('fox',{'arm_l':(-.41,0,1.06),'arm_r':(.41,0,1.06),'leg_l':(-.20,0,.62),'leg_r':(.20,0,.62),'tail':(.15,.27,.58)})
 # Compact animated target models and scenery helpers.
 part='body'
 clear();box('Cannon plinth',(0,0,.16),(1.05,.9,.30),ink,.12);ring('Gimbal',(0,0,.34),.35,.07,gold);ball('Turret housing',(0,.05,.68),(.45,.40,.36),coral);box('Cannon visor',(0,-.30,.76),(.53,.13,.19),ink,.06)
 for x in [-.15,.15]:ball('Angry target eye',(x,-.38,.78),(.055,.025,.04),gold)
 box('Barrel',(0,-.48,.58),(.35,.71,.30),leather,.09);box('Muzzle rim',(0,-.88,.58),(.41,.12,.34),gold,.04);box('Bore',(0,-.95,.58),(.25,.025,.20),ink,.025);export('cannon')
 clear();box('Relay plinth',(0,0,.15),(.72,.72,.26),ink,.10);cone('Crystal lower',(0,0,.65),.0,.27,.50,cyan);cone('Crystal upper',(0,0,1.07),.27,0,.34,cyan)
 for x in [-.32,.32]:box('Golden cradle',(x,0,.49),(.10,.45,.57),gold,.03)
 export('relay')
 clear();box('Radar base',(0,0,.14),(.5,.5,.26),leather,.07);cone('Radar mast',(0,0,.54),.07,.055,.65,cream);ball('Radar bowl',(0,0,.89),(.43,.35,.11),teal);tube('Antenna',[(0,0,.9),(0,-.3,1.15)],.03,gold);export('radar')
 for name,m in [('spark',cyan),('spark_hot',gold),('bolt',cyan),('enemy_bolt',coral),('fireball',orange)]:
  clear();ball(name,(0,0,0),(.13,.13,.19)if name not in ['spark','spark_hot']else(.09,.07,.15),m)
  if name=='fireball':
   for i in range(3):cone('Fire tongue',((i-1)*.07,.12+i*.04,.02),.065,0,.23,gold,rot=(math.pi/2,0,0))
  export(name)
 clear();box('Treasure chest',(0,0,.23),(.63,.46,.42),leather,.10);box('Arched lid',(0,0,.49),(.66,.49,.16),gold,.08)
 for x in [-.22,.22]:box('Chest band',(x,0,.32),(.065,.49,.40),gold,.015)
 box('Star lock',(0,-.25,.32),(.16,.06,.16),cyan,.035);export('chest')
 clear();ball('Drone housing',(0,0,.53),(.35,.32,.25),gold);box('Drone visor',(0,-.27,.58),(.40,.08,.12),ink,.035)
 for x in [-.5,.5]:box('Rotor arm',(x,0,.63),(.5,.08,.07),leather,.02);ring('Rotor',(x,0,.68),.23,.025,cyan)
 export('drone')
 clear();box('Solid closed gate',(0,0,.54),(1,1,1.08),teal,.08);box('Gate crown',(0,0,1.1),(1,1,.09),gold,.025);export('gate')
 # A soft transparent contact shadow is rendered in its own blended depth pass.
 clear();bpy.ops.mesh.primitive_plane_add(size=1,location=(0,0,.105));o=bpy.context.object;o.scale=(1.45,1.15,1);finish(o,ink);export('shadow',tag='shadow')
else:
 metadata=json.loads((OUT/'models.json').read_text());rigs=json.loads((OUT/'rigs.json').read_text());bounds=json.loads((OUT/'dimensions.json').read_text())
def point(x,z,h):return(x,-z,h)
def plane(name,w,h,texture,scale=1):
 bpy.ops.mesh.primitive_plane_add(size=1,location=(0,0,.065));o=bpy.context.object;o.name=name;o.scale=(w,h,1);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);finish(o,white)
 # Pack a shared base-color image material for sync_defold's explicit binding.
 material=mat(name+' material',(1,1,1));o.data.materials.clear();o.data.materials.append(material);return o
# Themed walls preserve exactly the previous collider rectangles.
data=json.loads((R/'shared/defold04.json').read_text());surfaces={}
palettes={'reactor':((.25,.60,.48),(.66,.39,.20),'ground-garden.png'),'citadel':((.33,.31,.62),(.33,.20,.55),'ground-sand.png'),'dock':((.12,.40,.57),(.16,.38,.50),'ground-sand.png'),'forge':((.65,.36,.22),(.60,.25,.16),'ground-sand.png'),'echo':((.20,.41,.55),(.25,.33,.55),'ground-garden.png'),'rescue':((.27,.57,.32),(.50,.36,.20),'ground-garden.png')}
for mission in data['missions']:
 clear();name=mission['id'];ground,wallcolor,texture=palettes[name];stone=mat(name+' masonry',wallcolor);cap=mat(name+' cap',tuple(min(1,c*1.22+.08)for c in wallcolor));mortar=mat(name+' mortar',tuple(c*.64 for c in wallcolor))
 # Ground is exported separately: real textured material, no checkerboard boxes.
 o=plane('Painted ground',21.5,15.5,texture);export(name+'_ground',[o],texture)
 metadata[name+'_ground']['color_tint']={'reactor':[1,1,.94,1],'citadel':[.72,.65,1,1],'dock':[.64,.87,1,1],'forge':[1,.87,.74,1],'echo':[.72,.89,1,1],'rescue':[.95,1,.91,1]}[name]
 bpy.data.objects.remove(o,do_unlink=True)
 a=data['arena'];rows=[{'r':r,'type':'border'}for r in [[a[0],a[1],a[2],.3],[a[0],a[1]+a[3]-.3,a[2],.3],[a[0],a[1],.3,a[3]],[a[0]+a[2]-.3,a[1],.3,a[3]]]]+[{'r':v,'type':'cover'}for v in mission['covers']]+[{'r':v,'type':'reflector'}for v in mission['reflectors']];surfaces[name]=rows
 for i,row in enumerate(rows):
  x,z,w,h=row['r'];height=.86 if row['type']=='reflector'else 1.12
  body=box('SOLID '+str(i)+' '+row['type'],point(x+w/2,z+h/2,height/2),(w if row['type']=='reflector'else max(.05,w-.05),h if row['type']=='reflector'else max(.05,h-.05),height),teal if row['type']=='reflector'else mortar,.055)
  crown=box('SOLID crown '+str(i)+' '+row['type'],point(x+w/2,z+h/2,height+.035),(w,h,.07),cyan if row['type']=='reflector'else mortar,.025)
  row['geometry_r']=list(row['r'])
  if row['type']!='reflector':
   nx=max(1,math.ceil(w/.85));nz=max(1,math.ceil(h/.85))
   for ix in range(nx):
    for iz in range(nz):box('Inset crown tile',point(x+(ix+.5)*w/nx,z+(iz+.5)*h/nz,height+.095),(max(.03,w/nx-.025),max(.03,h/nz-.025),.10),cap,.025)
  # Staggered masonry panels and bevel highlights stay strictly within footprint.
  if row['type']!='reflector':
   length=max(w,h);horizontal=w>=h;n=max(1,math.ceil(length/.85))
   for layer in range(2):
    for j in range(n):
     lo=j*length/n;hi=(j+1)*length/n
     if horizontal:pos=point(x+(lo+hi)/2,z+h/2,.29+layer*.45);dims=(max(.03,hi-lo-.035),max(.05,h-.035),.40)
     else:pos=point(x+w/2,z+(lo+hi)/2,.29+layer*.45);dims=(max(.05,w-.035),max(.03,hi-lo-.035),.40)
     box('Inset masonry',pos,dims,stone,.045)
  else:
   for j in range(max(1,int(max(w,h)/.65))):
    px=x+min(w-.05,.15+j*.65)if w>h else x+w/2;pz=z+h/2 if w>h else z+min(h-.05,.15+j*.65)
    ball('Reflective stud',point(px,pz,.94),(.035,.035,.025),gold)
 for mark in mission['secret']['marks']:
  x,z=mark['position']
  if mark['kind']=='arrow':
   mesh=bpy.data.meshes.new('Treasure arrow');mesh.from_pydata([point(x-.20,z+.20,.08),point(x+.20,z+.20,.08),point(x,z-.29,.08)],[],[(0,1,2)]);o=bpy.data.objects.new('Treasure trail',mesh);bpy.context.collection.objects.link(o);finish(o,gold)
  else:
   ball('Dark hatch',point(x,z,.075),(.30,.23,.009),ink)
   for j in range(3):box('Scratch',point(x-.12+j*.12,z,.085),(.032,.24,.012),gold,.003)
 for x,z in [mission['spawn'],mission['goal']]:ring('Inlaid portal',point(x,z,.075),.60,.035,gold)
 # Lush original scenery is OUTSIDE the collision border, never fake in-field cover.
 for side in [-1,1]:
  for j in range(9):
   x=side*(11.0+rng.uniform(.2,.8));z=-7.4+j*1.85
   box('Outer retaining stone',point(x,z,.20),(.8,1.4,.6),stone,.14)
   if texture=='ground-garden.png':
    cone('Tree trunk',point(x,z,.85),.10,.065,1.2,leather)
    for dx,dz,h in [(-.18,0,1.65),(.20,.09,1.8),(0,-.14,2.1)]:ball('Sculpted canopy',point(x+dx,z+dz,h),(.47,.48,.48),teal)
   else:
    cone('Exterior cactus',point(x,z,.9),.16,.13,1.35,teal);ball('Cactus crown',point(x,z,1.58),(.14,.14,.14),teal);ball('Cactus blossom',point(x,z,1.74),(.10,.10,.06),coral)
 # Foundation and generous outer terrain remove the black floating-board void.
 box('Raised arena foundation',point(0,0,-.23),(22.1,16.1,.46),stone,.18)
 export(name)
# The lobby has no rectangular floor or clipped trees: a clean hero pedestal.
clear();ring('Pedestal rim',(0,0,.035),.85,.065,gold);cone('Hero pedestal',(0,0,-.11),.91,.85,.23,teal)
for side in [-1,1]:
 x=side*.97
 for j in range(3):
  leaf=ball('Pedestal succulent',(x+(j-1)*.09,.22,.05+j*.055),(.09,.17,.035),teal);leaf.rotation_euler[0]=j*.3
export('lobby',tag='stage')
clear();ring('Hero selection ring',(0,0,.09),.40,.024,cyan);export('selection_ring')
clear();bpy.ops.mesh.primitive_plane_add(size=.60,location=(0,0,0),rotation=(math.pi/2,0,0));finish(bpy.context.object,cyan);export('glow',tag='glow')
(OUT/'models.json').write_text(json.dumps(metadata,indent=2)+'\n');(OUT/'rigs.json').write_text(json.dumps(rigs,indent=2)+'\n');(OUT/'surfaces.json').write_text(json.dumps(surfaces,indent=2)+'\n');(OUT/'dimensions.json').write_text(json.dumps(bounds,indent=2)+'\n')
print('Original 0.6 detailed actors / baked AO / arena kit COMPLETE')
