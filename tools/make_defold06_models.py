"""Original rigid-part fixtures and the 0.9 sculpted orbital arena architecture.
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
  mod=o.modifiers.new('Sculpted edges','BEVEL');mod.width=min(b,min(s)*.42);mod.segments=2 if globals().get('WORLD_GEOMETRY',False) else 4;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
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
def local_round(label,along,cross,high,radius,depth,material,axis='up',vertices=24):
 # The cover builder binds local coordinates/dimensions for each footprint.
 px=x+along if horizontal else x+w/2+cross
 pz=z+h/2+cross if horizontal else z+along
 rotation=(0,0,0)
 if axis=='along':rotation=(0,math.pi/2,0)if horizontal else(math.pi/2,0,0)
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=point(px,pz,high),rotation=rotation)
 o=bpy.context.object;o.name=label
 bevel=o.modifiers.new('Machined rim','BEVEL');bevel.width=min(.022,depth*.18);bevel.segments=2
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');finish(o,material);return o
def local_torus(label,along,cross,high,radius,minor,material,axis='up'):
 px=x+along if horizontal else x+w/2+cross
 pz=z+h/2+cross if horizontal else z+along
 bpy.ops.mesh.primitive_torus_add(major_radius=radius,minor_radius=minor,major_segments=24,minor_segments=6,location=point(px,pz,high))
 o=bpy.context.object;o.name=label
 if axis=='along':o.rotation_euler=(0,math.pi/2,0)if horizontal else(math.pi/2,0,0)
 finish(o,material);return o
def local_crystal(label,along,cross,high,radius,depth,material):
 px=x+along if horizontal else x+w/2+cross;pz=z+h/2+cross if horizontal else z+along
 bpy.ops.mesh.primitive_cone_add(vertices=6,radius1=radius,radius2=0,depth=depth,location=point(px,pz,high))
 o=bpy.context.object;o.name=label;finish(o,material);return o
def sculpt_cover(name,height,length,width):
 # Large intentional silhouette features, not another array of flat control panels.
 # Every object remains inside the supplied wall rectangle, including its cap.
 for side in [-1,1]:
  aligned('Deep armored shoulder rail',length/2,side*(width/2-.13),height+.09,length-.13,.19,.24,ivory,.065)
  aligned('Recessed shoulder light',length/2,side*(width/2-.13),height+.217,length-.30,.045,.018,glow,0)
 for along in [.18,length-.18]:
  aligned('Sculpted end armor',along,0,height+.12,.29,width-.14,.38,plate,.11)
  aligned('End armor inlaid insignia',along,0,height+.318,.12,min(.48,width*.35),.026,brass,0)
 # Low dark front radiator and standoff ribs make the thick side face dimensional.
 for side in [-1,1]:
  aligned('Inset side radiator',length/2,side*(width/2-.022),height*.50,length-.50,.018,height*.44,darkglass,0)
  for j in range(max(1,int(length/.55))):
   along=.38+j*(length-.76)/max(1,int(length/.55)-1)
   aligned('Radiator cooling rib',along,side*(width/2-.010),height*.50,.045,.012,height*.38,ivory,0)
 count=max(1,math.ceil((length-.32)/1.70));segment=(length-.40)/count
 for j in range(count):
  c=.20+(j+.5)*segment;r=min(.47,width*.27,segment*.35)
  if name=='reactor':
   local_round('Containment socket',c,0,height+.08,r*1.19,.13,brass)
   local_round('Sculpted reactor chamber',c,0,height+.32,r,.45,darkglass)
   local_round('Luminous reactor interior',c,0,height+.38,r*.62,.38,glow)
   for dz in [-.17,.17]:local_torus('Porcelain containment collar',c,0,height+.32+dz,r*1.04,.055,ivory)
   local_torus('Luminous suspended lens',c,0,height+.57,r*.70,.028,glow)
   for side in [-1,1]:aligned('Reactor retaining claw',c,side*r*.97,height+.31,.15,.13,.53,plate,.04)
  elif name=='citadel':
   local_round('Royal resonator socket',c,0,height+.10,r*1.15,.13,brass,vertices=12)
   local_torus('Golden orbital crest',c,0,height+.28,r,.065,brass)
   local_torus('Violet force ring',c,0,height+.43,r*.78,.05,glow)
   local_crystal('Faceted citadel power crystal',c,0,height+.34,r*.49,.52,glow)
   for side in [-1,1]:
    aligned('Royal angled buttress',c,side*r*1.06,height+.25,.18,.13,.48,ivory,.055)
    local_crystal('Golden finial',c,side*r*1.06,height+.56,.08,.24,brass)
  elif name=='dock':
   aligned('Rounded cargo coffer',c,0,height+.28,max(.45,segment-.17),width-.48,.52,ivory,.13)
   aligned('Cobalt cargo inset',c,0,height+.56,max(.25,segment-.41),width-.76,.045,plate,.04)
   for side in [-1,1]:aligned('Cargo ratchet strap',c+side*segment*.24,0,height+.595,.085,width-.59,.055,brass,.015)
   local_round('Vent turbine recess',c,0,height+.598,r*.61,.025,darkglass)
   for k in range(5):
    q=k*math.tau/5
    blade=aligned('Cargo cooling turbine blade',c+math.cos(q)*r*.24,math.sin(q)*r*.24,height+.620,r*.49,.065,.025,plate,0)
    blade.rotation_euler[2]=(q if horizontal else math.pi/2-q)
   local_round('Luminous cargo seal',c,0,height+.646,r*.15,.035,glow)
  elif name=='forge':
   # A real horizontal magnetic spool instead of a painted rectangle.
   local_round('Horizontal magnetic drum',c,0,height+.32,r*.72,segment*.57,darkglass,'along')
   for side in [-1,1]:
    local_round('Magnet spool flange',c+side*segment*.27,0,height+.32,r,.11,plate,'along')
    local_torus('Luminous magnet pole',c+side*segment*.325,0,height+.32,r*.73,.035,glow,'along')
   for k in [-1,0,1]:local_torus('Heavy copper induction turn',c+k*segment*.12,0,height+.32,r*.74,.047,brass,'along')
   aligned('Magnetic assembly footing',c,0,height+.04,segment*.74,width-.46,.16,ivory,.06)
  elif name=='echo':
   local_round('Harmonic crystal cradle',c,0,height+.09,r*1.08,.12,brass,vertices=12)
   local_crystal('Harmonic facet lower',c,0,height+.26,r*.70,.36,ivory)
   local_crystal('Luminous harmonic crystal',c,0,height+.46,r*.72,.68,glow)
   for side in [-1,1]:
    aligned('Harmonic tuning fork',c,side*r*.97,height+.30,.10,.10,.51,ivory,.03)
    local_torus('Crystal suspension ring',c,0,height+.39,r*.88,.025,plate)
  else:
   local_round('Habitat pod footing',c,0,height+.10,r*1.12,.12,ivory)
   px=x+c if horizontal else x+w/2;pz=z+h/2 if horizontal else z+c
   ball('Habitat observation dome',point(px,pz,height+.26),(r*.95,r*.95,.30),darkglass)
   local_torus('Luminous habitat seal',c,0,height+.20,r,.034,glow)
   for k in range(3):
    q=k*math.tau/3
    leaf=aligned('Bioluminescent botanical vane',c+math.cos(q)*r*.30,math.sin(q)*r*.30,height+.45,r*.58,.13,.085,glow,.035)
    leaf.rotation_euler[2]=q if horizontal else math.pi/2-q
   local_round('Habitat air regulator',c,0,height+.60,r*.22,.10,brass)

def bake_world_ao(name):
 """Bake one real arena AOatlas without sacrificing named wall audit meshes."""
 # Convert curves once, then apply all mesh modifiers in a single operation.
 # The earlier per-object conversion caused quadratic dependency-graph updates.
 bpy.ops.object.select_all(action='DESELECT');curves=[o for o in bpy.context.scene.objects if o.type=='CURVE']
 if curves:
  for o in curves:o.select_set(True)
  bpy.context.view_layer.objects.active=curves[0];bpy.ops.object.convert(target='MESH')
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];names={}
 for i,o in enumerate(objects):
  group=o.vertex_groups.new(name='AO_ORIGIN_%04d'%i);group.add(range(len(o.data.vertices)),1,'REPLACE');names[group.name]=o.name
 bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();joined=bpy.context.object;joined.name='Temporary AO world'
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
 image=bpy.data.images.new(name+' arena AO',width=1024,height=1024,alpha=False);image.generated_color=(1,1,1,1)
 for material in joined.data.materials:
  node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;material.node_tree.nodes.active=node
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=False;scene.render.bake.margin=3;scene.world.color=(1,1,1)
 bpy.ops.object.bake(type='AO');image.filepath_raw=str(OUT/(name+'-ao.png'));image.file_format='PNG';image.save()
 source=joined.data;source.update();uv=source.uv_layers.active
 memberships={v.index:joined.vertex_groups[v.groups[0].group].name for v in source.vertices}
 face_groups={}
 for face in source.polygons:face_groups.setdefault(memberships[face.vertices[0]],[]).append(face)
 vertex_groups={}
 for v in source.vertices:vertex_groups.setdefault(memberships[v.index],[]).append(v.index)
 normals=[tuple(n.vector)for n in source.corner_normals];restored=[]
 for group,indices in vertex_groups.items():
  faces=face_groups[group];indexmap={v:i for i,v in enumerate(indices)}
  mesh=bpy.data.meshes.new(names[group]);mesh.from_pydata([source.vertices[i].co[:]for i in indices],[],[[indexmap[i]for i in face.vertices]for face in faces])
  for material in source.materials:mesh.materials.append(material)
  layer=mesh.uv_layers.new(name='UVMap');custom=[]
  for face,original in zip(mesh.polygons,faces):
   face.material_index=original.material_index;face.use_smooth=original.use_smooth
   for a,b in zip(face.loop_indices,original.loop_indices):layer.data[a].uv=uv.data[b].uv;custom.append(normals[b])
  mesh.normals_split_custom_set(custom)
  obj=bpy.data.objects.new(names[group],mesh);bpy.context.collection.objects.link(obj);restored.append(obj)
 bpy.data.objects.remove(joined,do_unlink=True)
 export(name,restored,texture=name+'-ao.png')
 print('WORLD AO COMPLETE',name,'source pieces',len(restored),flush=True)

# Original 23rd-century orbital architecture. Static decoration never changes gameplay.
WORLD_GEOMETRY=True
# Semantic SOLID source meshes preserve every exact collider footprint, and batching
# only joins this same evaluated geometry. Flush floor markings are walkable.
data=json.loads((R/'shared/defold04.json').read_text());surfaces=json.loads((OUT/'surfaces.json').read_text())if('--worlds'in sys.argv or'--first-world'in sys.argv)and(OUT/'surfaces.json').exists()else{}
palettes={
 'reactor':((.025,.82,.68),(.025,.09,.15),'ground-garden.png',[.70,.92,.95,1]),
 'citadel':((.60,.23,1),(.065,.035,.16),'ground-sand.png',[.75,.71,.98,1]),
 'dock':((.05,.63,1),(.018,.07,.19),'ground-sand.png',[.66,.84,1,1]),
 'forge':((1,.43,.035),(.09,.05,.12),'ground-sand.png',[.92,.81,.77,1]),
 'echo':((.28,.61,1),(.03,.06,.18),'ground-garden.png',[.71,.84,1,1]),
 'rescue':((.12,.92,.45),(.02,.10,.12),'ground-garden.png',[.73,.95,.85,1]),
}
selected_worlds=set(sys.argv[sys.argv.index('--worlds')+1].split(','))if '--worlds'in sys.argv else None
for mission in data['missions']:
 if selected_worlds and mission['id']not in selected_worlds:continue
 if '--first-world' in sys.argv and mission['id']!='reactor':continue
 clear();name=mission['id'];accent,wallcolor,texture,tint=palettes[name]
 hull=mat(name+' deep indigo hull',(.007,.017,.045));plate=mat(name+' naval ceramic',wallcolor)
 ivory=mat(name+' porcelain edge',(.44,.59,.69));brass=mat(name+' satin brass',(.56,.25,.045))
 glow=mat('Luminous '+name+' reactor seam',accent);darkglass=mat(name+' recessed glass',(.004,.013,.025))
 # Root can replace these explicit bindings with the new clean original floor art.
 o=plane('Orbital deck floor',21.5,15.5,texture);export(name+'_ground',[o],texture)
 metadata[name+'_ground']['color_tint']=tint;bpy.data.objects.remove(o,do_unlink=True)
 a=data['arena'];rows=[{'r':r,'type':'border'}for r in [[a[0],a[1],a[2],.3],[a[0],a[1]+a[3]-.3,a[2],.3],[a[0],a[1],.3,a[3]],[a[0]+a[2]-.3,a[1],.3,a[3]]]]+[{'r':v,'type':'cover'}for v in mission['covers']]+[{'r':v,'type':'reflector'}for v in mission['reflectors']];surfaces[name]=rows
 for i,row in enumerate(rows):
  x,z,w,h=row['r'];kind=row['type'];height=.86 if kind=='reflector'else .90 if kind=='cover'else 1.12
  cover_objects_before=set(bpy.context.scene.objects)
  box('SOLID '+str(i)+' '+kind,point(x+w/2,z+h/2,height/2),(max(.05,w-.035),max(.05,h-.035),height),hull,.065)
  box('SOLID crown '+str(i)+' '+kind,point(x+w/2,z+h/2,height+.035),(w,h,.07),plate,.025)
  row['geometry_r']=list(row['r']);horizontal=w>=h;length=max(w,h);width=min(w,h);count=max(1,math.ceil(length/1.25))
  def aligned(label,along,cross,high,lng,across,thick,material,bevel=.025):
   # along/cross and all dimensions are inside the unchanged footprint.
   px=x+along if horizontal else x+w/2+cross
   pz=z+h/2+cross if horizontal else z+along
   return box(label,point(px,pz,high),(lng,across,thick)if horizontal else(across,lng,thick),material,0 if min(lng,across,thick)<.05 else bevel)
  if kind=='cover'and width>.85:
   sculpt_cover(name,height,length,width)
  else:
   for j in range(count):
    c=(j+.5)*length/count;segment=length/count
    aligned('Armored module',c,0,height+.10,max(.04,segment-.055),max(.06,width-.045),.12,ivory,.035)
    aligned('Recessed reactor window',c,0,height+.17,max(.035,segment-.15),max(.045,width*.69),.025,darkglass,.025)
    # A narrow luminous channel is readable as reflection technology, not brick grout.
    aligned('Luminous inset channel',c,0,height+.188,max(.025,segment-.25),min(.075,width*.24),.014,glow,.006)
    # Vent fingers, braces and tiny brass fasteners give the armor a designed hierarchy.
    if width>.7:
     for k in [-1,1]:
      aligned('Raised shoulder casing',c,k*width*.38,height+.18,max(.05,segment-.13),min(.16,width*.14),.095,plate,.025)
      aligned('Luminous shoulder line',c,k*width*.38,height+.235,max(.03,segment-.29),.027,.014,glow,.004)
     for q in [-.25,0,.25]:
      aligned('Reactor grille',c+q*segment,0,height+.195,.025,min(.43,width*.48),.017,brass,.004)
    else:
     aligned('Brass latch',c+segment*.32,0,height+.20,.05,width*.68,.025,brass,.006)
    # Long visible faces remain nested within collider instead of decorative wall overhang.
    for k in [-1,1]:
     aligned('Side ceramic face',c,k*(width/2-.025),height*.55,max(.04,segment-.08),.027,height*.52,plate,.012)
     aligned('Luminous side circuit',c,k*(width/2-.007),height*.72,max(.025,segment-.22),.009,.036,glow,.003)
  evaluated=bpy.context.evaluated_depsgraph_get()
  row['height']=max((o.matrix_world@Vector(c)).z for o in set(bpy.context.scene.objects)-cover_objects_before for c in o.evaluated_get(evaluated).bound_box)
 # Sparse inlaid guidance traces read as paint; never as uncollidable walls.
 for side in [-1,1]:
  x=side*8.85
  for j in range(5):
   z=-5.5+j*2.35
   box('Flush navigation trace',point(x,z,.078),(.026,1.25,.012),glow,.003)
   box('Flush trace crossbar',point(x-side*.16,z+.61,.078),(.34,.025,.012),plate,.003)
 # Existing treasure clues remain visible with exactly the same semantic locations.
 for mark in mission['secret']['marks']:
  x,z=mark['position']
  if mark['kind']=='arrow':
   mesh=bpy.data.meshes.new('Treasure arrow');mesh.from_pydata([point(x-.20,z+.20,.085),point(x+.20,z+.20,.085),point(x,z-.29,.085)],[],[(0,1,2)]);o=bpy.data.objects.new('Treasure trail',mesh);bpy.context.collection.objects.link(o);finish(o,gold)
  else:
   box('Flush maintenance hatch',point(x,z,.082),(.63,.44,.018),darkglass,.06)
   for j in range(3):box('Treasure scratch',point(x-.12+j*.12,z,.095),(.032,.24,.012),gold,.003)
 for x,z in [mission['spawn'],mission['goal']]:
  ring('Inlaid energy portal',point(x,z,.083),.60,.025,glow)
  for q in range(4):
   a=q*math.pi/2;box('Landing marker',point(x+math.cos(a)*.70,z+math.sin(a)*.70,.085),(.10,.10,.014),brass,.015)
 # Scenery stays entirely outside every playable border. The battle deck is an
 # orbital place, not a garden with a few glowing boxes: towers, conduits and a
 # different themed far-horizon installation establish a coherent environment.
 for side in [-1,1]:
  for j in range(5):
   x=side*12.1;z=-6.6+j*3.2;ht=1.65+((j+len(name))%3)*.48
   box('Exterior dock pylon',point(x,z,ht/2-.20),(1.25,1.55,ht),hull,.17)
   box('Pylon porcelain shoulder',point(x,z,ht-.16),(1.31,1.61,.20),ivory,.06)
   box('Pylon recessed face',point(x-side*.64,z,ht*.46),(.05,.97,ht*.60),darkglass,.015)
   for q in [-1,0,1]:box('Luminous pylon vent',point(x-side*.67,z+q*.25,ht*.46),(.025,.065,ht*.47),glow,.008)
   cone('Signal cap',point(x,z,ht+.14),.20,.08,.45,brass)
   ball('Signal beacon',point(x,z,ht+.44),(.095,.095,.095),glow)
  # Parallel protected exterior conduits tie the environment to its reactors.
  for k in [-1,1]:
   tube('Exterior energy conduit',[point(side*11.55+k*.13,-7.3,-.05),point(side*11.55+k*.13,0,-.05),point(side*11.55+k*.13,7.3,-.05)],.055,glow)
 # Large landmark beyond far border. Silhouette and accent differ per sector.
 far=-9.2
 box('Horizon installation platform',point(0,far,-.15),(8.2,2.1,.50),hull,.18)
 if name in ['reactor','forge']:
  cone('Reactor base',point(0,far,.27),1.15,1.0,.48,plate)
  cone('Reactor energy column',point(0,far,1.60),.55,.55,2.4,darkglass)
  for q in range(5):ring('Luminous containment coil',point(0,far,.60+q*.45),.68,.055,glow)
  cone('Reactor crown',point(0,far,2.88),.95,.67,.28,ivory)
  for side in [-1,1]:
   x=side*2.1;box('Reactor retaining arm',point(x,far,1.16),(.55,.8,2.6),plate,.13)
   box('Retaining arm light',point(x,far+.405,1.25),(.16,.025,1.8),glow,.015)
 elif name=='citadel':
  for side in [-1,1]:
   x=side*2.65
   box('Citadel spire',point(x,far,1.65),(1.4,1.4,3.7),plate,.28)
   box('Citadel light blade',point(x,far+.71,1.95),(.25,.025,2.5),glow,.025)
   cone('Citadel crown',point(x,far,3.8),.48,.02,.65,brass)
  box('Horizon gateway',point(0,far,3.15),(5.3,.85,.35),ivory,.1)
  box('Luminous gateway',point(0,far+.44,3.15),(4.5,.025,.08),glow,.01)
 elif name=='dock':
  for side in [-1,1]:
   x=side*2.7;box('Orbital docking tower',point(x,far,1.35),(.75,1.2,3.0),plate,.12)
   box('Landing gantry',point(x-side*.8,far,2.8),(2.3,.7,.28),ivory,.06)
   box('Luminous gantry edge',point(x-side*.8,far+.36,2.8),(1.9,.025,.06),glow,.01)
  box('Distant shuttle hull',point(0,far,1.3),(2.5,1.35,.62),ivory,.25)
  for side in [-1,1]:cone('Shuttle thruster',point(side*1.35,far,1.20),.32,.26,.70,glow)
 elif name=='echo':
  for j in range(3):
   x=(j-1)*2.6;box('Resonator pedestal',point(x,far,.30),(1.3,1.3,.75),plate,.18)
   r=ring('Harmonic arch',point(x,far,1.65),.90,.12,ivory);r.rotation_euler[0]=math.pi/2
   r=ring('Luminous harmonic core',point(x,far,1.65),.70,.045,glow);r.rotation_euler[0]=math.pi/2
   ball('Echo crystal',point(x,far,1.65),(.16,.16,.32),glow)
 else:
  box('Rescue control hub',point(0,far,1.08),(4.2,1.55,2.5),plate,.30)
  box('Wide observation window',point(0,far+.79,1.38),(3.3,.035,.72),darkglass,.08)
  for j in range(5):box('Luminous control readout',point((j-2)*.50,far+.815,1.38),(.22,.02,.40-(j%2)*.14),glow,.015)
  box('Hub ivory canopy',point(0,far,2.44),(4.5,1.8,.22),ivory,.10)
  cone('Drone communication mast',point(0,far,3.05),.055,.035,1.1,brass)
  ball('Transmission orb',point(0,far,3.6),(.20,.20,.20),glow)
 # Hull, brass belt and suspended keel tie the arena to the same orbital station.
 box('Raised orbital deck',point(0,0,-.27),(22.1,16.1,.54),hull,.18)
 for side in [-1,1]:
  box('Deck exterior armor belt',point(side*10.96,0,-.24),(.17,15.7,.30),plate,.05)
  box('Luminous deck exterior seam',point(side*11.06,0,-.22),(.025,15.2,.05),glow,.006)
 bake_world_ao(name)
# Native closed energy gate: exact unit X/Z footprint, scaled by the live gate.
# An open gate still collapses below the floor; no decorative collision overhang.
clear();gate_ink=mat('Gate navy armor',(.012,.035,.07));gate_white=mat('Gate porcelain armor',(.53,.67,.76));gate_light=mat('Luminous gate energy',(.04,.88,.84));gate_gold=mat('Gate brass fittings',(.53,.28,.055))
box('Gate solid sill',point(0,0,.08),(1,1,.16),gate_ink,.045)
for side in [-1,1]:
 x=side*.44
 box('Gate sculpted pillar',point(x,0,.60),(.12,1,1.04),gate_white,.035)
 box('Gate pillar recessed channel',point(x,-.49,.60),(.06,.018,.71),gate_ink,0)
 box('Gate pillar energy indicator',point(x,-.501,.60),(.025,.012,.58),gate_light,0)
box('Gate upper bridge',point(0,0,1.145),(1,1,.17),gate_ink,.045)
box('Gate bridge gold crest',point(0,-.35,1.228),(.48,.20,.018),gate_gold,.008)
for high in [.30,.50,.70,.90]:box('Gate luminous energy rail',point(0,0,high),(.76,.18,.035),gate_light,.01)
export('gate')

# The lobby has no rectangular floor or clipped trees: a clean hero pedestal.
WORLD_GEOMETRY=False
clear();ring('Pedestal rim',(0,0,.035),.85,.065,gold);cone('Hero pedestal',(0,0,-.11),.91,.85,.23,teal)
for side in [-1,1]:
 x=side*.97
 for j in range(3):
  leaf=ball('Pedestal succulent',(x+(j-1)*.09,.22,.05+j*.055),(.09,.17,.035),teal);leaf.rotation_euler[0]=j*.3
export('lobby',tag='stage')
clear();ring('Hero selection ring',(0,0,.09),.40,.024,cyan);export('selection_ring')
clear();bpy.ops.mesh.primitive_plane_add(size=.60,location=(0,0,0),rotation=(math.pi/2,0,0));finish(bpy.context.object,cyan);export('glow',tag='glow')
(OUT/'models.json').write_text(json.dumps(metadata,indent=2)+'\n');(OUT/'rigs.json').write_text(json.dumps(rigs,indent=2)+'\n');(OUT/'surfaces.json').write_text(json.dumps(surfaces,indent=2)+'\n');(OUT/'dimensions.json').write_text(json.dumps(bounds,indent=2)+'\n')
print('Original actors / baked AO fixtures / 0.9 sculpted orbital arena kit COMPLETE')
