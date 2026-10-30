"""Original compact campaign geometry and reproducible sixteen-mission data.

No external art is fetched. The six existing original floor illustrations are
reused; the procedural room, armor and shelter meshes stay inside real colliders.
Run --data once to regenerate current rules from the frozen 0.13 baseline, then
run without arguments after ordinary rule edits to regenerate only geometry.
"""
from pathlib import Path
from collections import Counter
import argparse, copy, hashlib, json, math, struct

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'shared/assets/defold14'
THEMES=['reactor','citadel','dock','forge','echo','rescue']
PALETTES={
 'reactor':([.035,.20,.23,1],[.10,.86,.74,1]),
 'citadel':([.12,.065,.24,1],[.67,.35,1,1]),
 'dock':([.035,.11,.23,1],[.14,.66,1,1]),
 'forge':([.19,.09,.10,1],[1,.51,.12,1]),
 'echo':([.055,.105,.24,1],[.29,.69,1,1]),
 'rescue':([.04,.17,.14,1],[.27,.92,.60,1]),
}

def shelter(arena):
 x,z,w,h=arena;sx,sz=x+2.5,z+h-2.5
 walls=[[sx-2,sz-2,.3,4],[sx-2,sz-2,4,.3],
        [sx-2,sz+1.7,4,.3],[sx+1.7,sz-2,.3,2.5],
        [sx+3,sz+.15,.3,1.95]]
 return [sx,sz],walls

def turret(x,z,kind='sentinel',hp=2,phase=.2,**extra):
 return dict(position=[x,z],kind=kind,hp=hp,phase=phase,**extra)

def base_mission(id,title,theme,index,arena):
 start,walls=shelter(arena)
 return dict(id=id,title=title,theme=theme,arena=arena,
             arena_model='campaign_'+id,complexity=index,
             spawn=start,sanctuary=dict(position=start[:],radius=1.2),
             shelter_walls=walls,goal=[arena[0]+arena[2]-2.0,arena[1]+2.0],
             covers=copy.deepcopy(walls),reflectors=[],turrets=[],absorbers=[],
             description='',kind='combat',voice='defold_campaign_mission',
             exit_required=False,radar=[0,0],attack_drone=dict(stock=3,speed=7),
             lesson='Deckung, Abpraller und geeignete Wege selbst entdecken.')

def generate_data():
 d=json.loads((ROOT/'shared/defold13-regression.json').read_text())
 d.update(id='energyblast-defold-14',campaign_enabled=True,campaign_v14=True,
          max_hostiles=50,bonuses_enabled=False,optional_replay=False)
 d.pop('treasure_guidance',None)
 d['player']['hit_points']=20
 for i,m in enumerate(d['missions'],1):
  m.pop('bonuses',None);m.pop('secret',None);m.pop('escort',None)
  m['arena']=d['arena'][:];m['theme']=m['id'];m['arena_model']='campaign_'+m['id'];m['complexity']=i
  start,walls=shelter(m['arena']);m['spawn']=start;m['sanctuary']={'position':start[:],'radius':1.2};m['shelter_walls']=walls
  m['covers']=copy.deepcopy(walls)+m['covers'];m['attack_drone']={'stock':3,'speed':7}
  m['lesson']=['Abprallwinkel finden.','Deckung wechseln und das Torfenster nutzen.',
               'Erst die Relais, dann den geschützten Kern ausschalten.',
               'Fallen vorbereiten und den Wächter hineinlocken.',
               'Lichtfolge beobachten und in derselben Reihenfolge treffen.',
               'Eine Angriffsdrohne auswählen und ein Ziel bestimmen.'][i-1]
  m['description']=m['lesson']
  if m['id']=='echo':m['voice']='defold_campaign_sequence'
  elif m['id']=='forge':m['voice']='defold_forge'
  else:m['voice']='defold_campaign_mission'
  if m['id']=='rescue':
   m['title']='DROHNEN-ANGRIFF';m['kind']='combat';m['exit_required']=False
   m['voice']='defold_drone_open'
   m['turrets']=[turret(7,3.8,'sentinel',3,1),turret(2,-4.8,'crawler',3,.6),
                 turret(-4,-4.5,'mini_drone',1,1.6),turret(7,-2,'mini_drone',1,2.1)]
 new=[]
 # Every later map is at least 50% longer AND wider, not merely 50% more pixels.
 a=[-15.75,-11.25,31.5,22.5]
 m=base_mission('crystal_pass','KRISTALLPASS','reactor',7,a[:]);m['covers'] += [[-4,-5,2,10],[3,-8,2,6],[5,2,5,1.2]]
 m['reflectors']=[[-14.9,-10.5,29.8,.35],[14.55,-9.5,.35,18]]
 m['turrets']=[turret(8,-6,hp=3,shield=True),turret(11,5,hp=3,phase=1.2),turret(-8,-7,hp=2,phase=2.1),turret(4,8,'crawler',3,2.5)]
 m['description']='Nutze mehrere Deckungen und finde einen Abpraller für den Schild.';m['lesson']='Zwei Sichtlinien und reflektierte Wege kombinieren.';new.append(m)
 m=base_mission('swarm_nest','SCHWARMNEST','echo',8,a[:]);m['covers'] += [[-6,-6,1.5,9],[1,-3,2,8],[6,3,4,1.2]]
 m['turrets']=[turret(x,z,'mini_drone',1,.4+i*.28,replication_period=8,max_generation=2)for i,(x,z)in enumerate([(-8,-6),(-6,-9),(0,-8),(4,-7),(9,-7),(10,1),(7,6),(1,8)])]
 m['turrets'] += [turret(7,-2,'splitter',3,1,replication_period=8,max_generation=2),turret(-3,-7,'splitter',3,2,replication_period=9,max_generation=2)]
 m['voice']='defold_campaign_swarm';m['description']='Schwärme teilen sich. Nutze freie Schusslinien und unterbrich die Ausbreitung.';m['lesson']='Wachsende Gruppen früh erkennen und sichere Wege offen halten.';new.append(m)
 m=base_mission('relay_ring','RELAISRING','dock',9,a[:]);m['covers'] += [[-5,-7,1.4,10],[2,-3,6,1.4],[7,2,1.4,6]]
 m['relays']=[{'position':[-8,-8]},{'position':[9,7]}]
 m['turrets']=[turret(10,-7,hp=7,boss=True,burst=3),turret(5,8,'crawler',3,1),turret(-1,-7,'crawler',3,1.5),turret(10,2,'wisp',2,2),turret(-8,-3,'wisp',2,2.5)]
 m['reflectors']=[[-14.9,-10.5,29.8,.35]];m['attack_drone']['stock']=4;m['description']='Zwei Relais schützen den Kern. Triff sie zuerst.';m['lesson']='Zielreihenfolge trotz mehrerer Gegner beibehalten.';new.append(m)
 m=base_mission('double_signal','DOPPELTES SIGNAL','forge',10,a[:]);m['covers'] += [[-5,-4,2,8],[2,-5,1.5,7],[7,3,4,1.4]]
 m['sequence']=[3,1,2];m['sequence_nodes']=[[-7,-8],[0,-8],[7,-8]]
 m['turrets']=[turret(7,-3,hp=4,shield=True,trap_shield=True,patrol=[[7,-3],[11,-3],[11,1.7],[7,1.7]],speed=1.1),turret(9,7,'sentinel',3,1.5),turret(-6,-2,'mini_drone',1,2),turret(-1,7,'mini_drone',1,2.5)]
 m['attack_drone']['stock']=4;m['kind']='sequence';m['voice']='defold_campaign_sequence';m['description']='Schalte den Wächter aus und spiele die Lichterfolge nach.';m['lesson']='Vorbereitung, Gegnerbeobachtung und Reihenfolge verbinden.';new.append(m)
 a=[-17.5,-12.5,35,25]
 m=base_mission('ghost_sparks','SPUKFUNKEN','citadel',11,a[:]);m['covers'] += [[-8,-7,1.5,10],[-1,-4,2,8],[6,-7,1.5,11],[9,5,5,1.2]]
 m['turrets']=[turret(x,z,'wisp',2,.3+i*.45)for i,(x,z)in enumerate([(-9,-9),(-3,-9),(4,-10),(11,-6)])]
 m['turrets'] += [turret(x,z,'crawler',3,1+i*.35)for i,(x,z)in enumerate([(-6,2),(3,5),(11,3),(8,9)])]
 m['attack_drone']['stock']=5;m['description']='Leuchtwesen und Krabbler greifen aus verschiedenen Richtungen an.';m['lesson']='Gegnerarten unterscheiden und zwischen Deckungen planen.';new.append(m)
 m=base_mission('drone_corridor','DROHNENKORRIDOR','rescue',12,a[:]);m['covers'] += [[-8,-6,1.5,11],[-1,-9,1.5,11],[6,-3,1.5,10],[10,6,5,1.2]]
 m['relays']=[{'position':[-10,-10]},{'position':[12,9]}]
 m['turrets']=[turret(11,-8,hp=7,boss=True,burst=2),turret(3,-5,hp=3,phase=1),turret(12,1,hp=3,phase=1.5),turret(-5,5,'crawler',3,2),turret(3,8,'wisp',3,2.5)]
 m['turrets'] += [turret(x,z,'mini_drone',1,3+i*.25)for i,(x,z)in enumerate([(-9,-3),(-4,-9),(6,-10),(13,5)])]
 m['attack_drone']['stock']=5;m['description']='Finde den offenen Korridor und setze Angriffsdrohnen gezielt ein.';m['lesson']='Einen entfernten Zielweg zwischen Deckungen auswählen.';new.append(m)
 m=base_mission('magnetic_cascade','MAGNETKASKADE','forge',13,a[:]);m['covers'] += [[-7,-7,1.6,12],[0,-3,2,8],[7,-8,1.6,11],[10,6,4,1.3]]
 m['turrets']=[turret(x,z,'sentinel',4,.5+i*.7,shield=True,trap_shield=True,patrol=[[x,z],[x+3,z],[x+3,z+(2.3 if i==2 else 3)],[x,z+(2.3 if i==2 else 3)]],speed=1.05)for i,(x,z)in enumerate([(-3,-8),(10.5,-7),(10.5,2.5)])]
 m['turrets'] += [turret(x,z,'mini_drone',1,3+i*.3)for i,(x,z)in enumerate([(-10,-8),(-3,5),(4,8),(12,9),(12,-10),(2,-10)])]
 m['attack_drone']['stock']=6;m['description']='Drei Wächter verlangen vorbereitete Fallen oder gezielte Drohnen.';m['lesson']='Mehrere vorbereitete Gelegenheiten nacheinander nutzen.';new.append(m)
 a=[-21,-15,42,30]
 m=base_mission('light_maze','LICHTLABYRINTH','echo',14,a[:]);m['covers'] += [[-12,-10,1.5,16],[-5,-5,1.5,15],[3,-12,1.5,14],[11,-4,1.5,16]]
 m['sequence']=[2,3,1];m['sequence_nodes']=[[-10,-12],[0,-12],[10,-12]];m['kind']='sequence'
 m['turrets']=[turret(x,z,'wisp',3,.5+i*.5)for i,(x,z)in enumerate([(-9,-8),(-2,0),(7,-6),(16,6)])]
 m['turrets'] += [turret(x,z,'mini_drone',1,3+i*.3,replication_period=10,max_generation=1)for i,(x,z)in enumerate([(-8,8),(0,9),(6,6),(17,-9),(15,-12),(7,12)])]
 m['turrets'] += [turret(-1,-8,'splitter',4,2,replication_period=9,max_generation=2),turret(15,0,'splitter',4,2.5,replication_period=9,max_generation=2)]
 m['voice']='defold_campaign_sequence';m['attack_drone']['stock']=6;m['description']='Plane Wege im großen Labyrinth und behalte die Lichtfolge im Kopf.';m['lesson']='Räumliche Planung und eine getrennte Signalaufgabe verbinden.';new.append(m)
 m=base_mission('triple_core','DREIFACHKERN','dock',15,a[:]);m['covers'] += [[-12,-9,1.7,16],[-5,-10,8,1.7],[2,-3,1.7,13],[10,-11,1.7,13],[13,6,5,1.4]]
 m['relays']=[{'position':[-15,-12]},{'position':[6,11]},{'position':[17,0]}]
 m['turrets']=[turret(16,-11,hp=10,boss=True,burst=3),turret(-6,-5,'crawler',4,1),turret(6,5,'crawler',4,1.5),turret(15,10,'wisp',3,2),turret(4,-12,'wisp',3,2.5)]
 m['turrets'] += [turret(x,z,'mini_drone',1,3+i*.35,replication_period=10,max_generation=1)for i,(x,z)in enumerate([(-9,-12),(-7,9),(-2,10),(6,-7),(15,-5),(18.6,4.8)])]
 m['attack_drone']['stock']=7;m['description']='Drei Relais schützen den Kern. Öffne zuerst die richtigen Sichtlinien.';m['lesson']='Mehrstufige Zielprioritäten in einer großen Arena verfolgen.';new.append(m)
 m=base_mission('storm_center','STURMZENTRUM','citadel',16,a[:]);m['covers'] += [[-12,-9,1.6,15],[-5,-11,1.6,15],[2,-4,1.6,15],[9,-11,1.6,15],[14,7,5,1.3]]
 m['relays']=[{'position':[-15,-12]},{'position':[17,9]}]
 locations=[(-8,-12),(-1,-12),(5,-12),(15,-12),(-9,-4),(-1,5),(6,6),(15,2)]
 m['turrets']=[turret(x,z,'splitter',4,.4+i*.3,replication_period=8,max_generation=2)for i,(x,z)in enumerate(locations)]
 m['turrets'] += [turret(x,z,'wisp',3,3+i*.3)for i,(x,z)in enumerate([(-8,7),(0,-7),(7,11),(16,-5)])]
 m['turrets'] += [turret(x,z,'crawler',4,4+i*.3)for i,(x,z)in enumerate([(-9,-8),(-2,9),(6,-6),(17,5)])]
 m['turrets'] += [turret(x,z,'mini_drone',1,5+i*.3,replication_period=8,max_generation=2)for i,(x,z)in enumerate([(-7,11),(0,12),(14,11),(17,-10)])]
 m['turrets'] += [turret(17,-2,hp=10,boss=True,burst=3,phase=5.5)]
 m['attack_drone']['stock']=8;m['voice']='defold_campaign_swarm';m['description']='Stoppe den wachsenden Schwarm, schalte Relais aus und erreiche den Kern.';m['lesson']='Bekannte Werkzeuge flexibel kombinieren; maximal fünfzig Gegner gleichzeitig.';new.append(m)
 d['missions']+=new
 icons=['aim','armor','cannon','trap_magnet','radio','attack_drone','aim','swarm','cannon','radio','swarm','attack_drone','trap_magnet','radio','cannon','swarm']
 subtitles=['ABPRALLER','DECKUNG & TIMING','RELAIS & KERN','MAGNETFALLEN','LICHTERFOLGE','DROHNE ZUM ZIEL','MEHRERE SCHUSSLINIEN','SCHWARM STOPPEN','RELAISREIHENFOLGE','WAECHTER & LICHTER','WISPS & KRABBLER','DROHNENKORRIDOR','DREI WAECHTER','WEGE & SIGNALE','DREI RELAIS','ALLE WERKZEUGE']
 for mission,icon,subtitle in zip(d['missions'],icons,subtitles):mission.update(icon=icon,subtitle=subtitle)
 for m in new:
  d['rewards']['mission:'+m['id']]=300+25*(m['complexity']-6)
  d['rewards']['skill:'+m['id']]=100
  d['progress_mission_ids'].append(m['id']);d['hint_completion_keys'].append('mission:'+m['id'])
 cfg=d['bonus_power'];cfg['mode']='missions';cfg['cap_health']=100;cfg['minimum_fire_cooldown']=.16
 cfg['steps']=[dict(bonuses=i,title=('ENTDECKER'if i<4 else'PFADFINDER'if i<8 else'TAKTIKHELD'if i<12 else'STERNENWAECHTER'if i<16 else'MEISTER'),health=20+i*5,damage_multiplier=1+i/16,shield=math.ceil(i*20/16),detection_multiplier=1-i*.0125,visual_scale=1+i*.0125)for i in range(1,17)]
 cfg['milestones']=[1,4,8,12,16]
 (ROOT/'shared/defold04.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 return d

class Geometry:
 def __init__(self):self.groups=[]
 def box(self,label,x,y,z,w,h,d,material):
  vertices=[];normals=[];uv=[];indices=[]
  for normal,points in [
   ((0,1,0),[(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)]),
   ((0,-1,0),[(-1,-1,1),(-1,-1,-1),(1,-1,-1),(1,-1,1)]),
   ((1,0,0),[(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),
   ((-1,0,0),[(-1,-1,1),(-1,1,1),(-1,1,-1),(-1,-1,-1)]),
   ((0,0,1),[(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),
   ((0,0,-1),[(1,-1,-1),(-1,-1,-1),(-1,1,-1),(1,1,-1)])]:
   start=len(vertices)
   vertices += [(x+px*w/2,y+py*h/2,z+pz*d/2)for px,py,pz in points]
   normals += [normal]*4;uv += [(0,0),(0,1),(1,1),(1,0)];indices += [start,start+1,start+2,start,start+2,start+3]
  self.groups.append((label,material,vertices,normals,uv,indices))
 def floor(self,label,arena):
  x,z,w,h=arena;verts=[(x,.035,z),(x,.035,z+h),(x+w,.035,z+h),(x+w,.035,z)]
  # Retain the original illustration's texel density on the larger battlefields.
  # The runtime material explicitly repeats these UVs instead of stretching/clamping.
  u,v=w/21,h/15
  self.groups.append((label,0,verts,[(0,1,0)]*4,[(0,v),(0,0),(u,0),(u,v)],[0,1,2,0,2,3]))
 def write(self,name,materials,batch=False):
  groups=self.groups
  if batch:
   combined={}
   for label,material,v,n,uv,idx in groups:
    row=combined.setdefault(material,[[],[],[],[]]);offset=len(row[0]);row[0]+=v;row[1]+=n;row[2]+=uv;row[3]+=[i+offset for i in idx]
   groups=[('BATCH material '+str(m),m,*row)for m,row in combined.items()]
  raw=bytearray();views=[];accessors=[];meshes=[];nodes=[]
  def add(values,fmt,kind,component,target):
   while len(raw)%4:raw.append(0)
   start=len(raw);flat=[v for row in values for v in row]if isinstance(values[0],tuple)else values
   raw.extend(struct.pack('<'+fmt*len(flat),*flat));view=len(views);views.append(dict(buffer=0,byteOffset=start,byteLength=len(raw)-start,target=target))
   acc=dict(bufferView=view,componentType=component,count=len(values),type=kind)
   if kind=='VEC3':acc.update(min=[min(v[i]for v in values)for i in range(3)],max=[max(v[i]for v in values)for i in range(3)])
   accessors.append(acc);return len(accessors)-1
  for label,material,v,n,uv,idx in groups:
   p=add(v,'f','VEC3',5126,34962);normal=add(n,'f','VEC3',5126,34962);u=add(uv,'f','VEC2',5126,34962);ind=add(idx,'I','SCALAR',5125,34963)
   meshes.append({'name':label,'primitives':[{'attributes':{'POSITION':p,'NORMAL':normal,'TEXCOORD_0':u},'indices':ind,'material':material}]});nodes.append({'name':label,'mesh':len(meshes)-1})
  (OUT/(name+'.bin')).write_bytes(raw)
  obj=dict(asset={'version':'2.0','generator':'EnergyBlast original procedural campaign14'},scene=0,scenes=[{'nodes':list(range(len(nodes)))}],nodes=nodes,meshes=meshes,buffers=[{'uri':name+'.bin','byteLength':len(raw)}],bufferViews=views,accessors=accessors,materials=[{'name':label,'pbrMetallicRoughness':{'baseColorFactor':color,'roughnessFactor':.5}}for label,color in materials])
  (OUT/(name+'.gltf')).write_text(json.dumps(obj,separators=(',',':'))+'\n')

def build_worlds(data):
 OUT.mkdir(parents=True,exist_ok=True);models={};surfaces={};provenance=[]
 for m in data['missions']:
  name=m['arena_model'];a=m['arena'];base,accent=PALETTES[m['theme']]
  materials=[('Hull',[.025,.04,.07,1]),('Ceramic',base),('Porcelain rim',[.43,.57,.67,1]),('Luminous campaign circuit',accent),('Brass fastener',[.62,.32,.055,1])]
  g=Geometry();rows=[{'r':r,'type':'border'}for r in [[a[0],a[1],a[2],.3],[a[0],a[1]+a[3]-.3,a[2],.3],[a[0],a[1],.3,a[3]],[a[0]+a[2]-.3,a[1],.3,a[3]]]]+[{'r':r,'type':'cover'}for r in m['covers']]+[{'r':r,'type':'reflector'}for r in m['reflectors']]
  for index,row in enumerate(rows):
   x,z,w,h=row['r'];height=1.35 if row['r']in m['shelter_walls']else 1.10 if row['type']=='border'else 1.0
   row['height']=height+.10;row['geometry_r']=row['r'][:]
   # All solid decorative elements remain within this exact collider footprint.
   g.box('SOLID '+str(index)+' '+row['type'],x+w/2,height/2,z+h/2,w,height,h,0)
   g.box('SOLID crown '+str(index)+' '+row['type'],x+w/2,height+.035,z+h/2,w,.07,h,1)
   if w>=h:
    g.box('Luminous circuit '+str(index),x+w/2,height+.08,z+h/2,max(.05,w-.10),.025,min(.065,h*.20),3)
   else:g.box('Luminous circuit '+str(index),x+w/2,height+.08,z+h/2,min(.065,w*.20),.025,max(.05,h-.10),3)
   if row['type']=='cover'and min(w,h)>.7:
    # Porcelain shoulders and ribbed inset make substantial cover distinguishable.
    for side in [-1,1]:
     if w>=h:g.box('Armor shoulder',x+w/2,height+.075,z+h/2+side*h*.34,w*.90,.05,h*.16,2)
     else:g.box('Armor shoulder',x+w/2+side*w*.34,height+.075,z+h/2,w*.16,.05,h*.90,2)
   length=max(w,h)
   for i in range(max(1,int(length/3))):
    position=(i+.5)*length/max(1,int(length/3))
    px=x+position if w>=h else x+w/2;pz=z+h/2 if w>=h else z+position
    g.box('Brass latch',px,height+.09,pz,min(.10,w*.4),.02,min(.10,h*.4),4)
  source=name;g.write(source,materials);g.write(name+'.runtime',materials,True)
  models[name]={'tag':'model','texture':None,'runtime':name+'.runtime.gltf'}
  ground=Geometry();ground.floor('PLAYABLE FLOOR '+m['id'],a);ground.write(name+'_ground',[('Floor albedo',[.84,.88,.96,1])])
  models[name+'_ground']={'tag':'model','texture':'floor-'+m['theme']+'.png','color_tint':[.84,.88,.96,1],'campaign_ground':True,'repeat':True}
  surfaces[m['id']]=rows
 for filename in ['models.json','surfaces.json']:
  (OUT/filename).write_text(json.dumps(models if filename=='models.json'else surfaces,ensure_ascii=False,indent=2)+'\n')
 for file in sorted(OUT.iterdir()):
  if file.suffix in ['.gltf','.bin']:
   provenance.append({'path':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'bytes':file.stat().st_size,'origin':'Original deterministic geometry from tools/make_defold14_worlds.py; no external image/model import'})
 (OUT/'PROVENANCE.json').write_text(json.dumps({'schema':1,'generator':'tools/make_defold14_worlds.py','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'floor_images':'Unmodified original shared/assets/defold09/floor-THEME.png; reused without new image downloads','assets':provenance},indent=2)+'\n')
 print('Generated',len(data['missions']),'arenas;',sum(f.stat().st_size for f in OUT.iterdir()),'bytes')

def check_generated(data):
 """Read actual exported buffers; verify geometry, batching and physical bounds."""
 count=0
 def read(path):
  g=json.loads(path.read_text());raw=[(path.parent/b['uri']).read_bytes()for b in g['buffers']]
  def accessor(index):
   a=g['accessors'][index];v=g['bufferViews'][a['bufferView']];width={'VEC2':2,'VEC3':3}[a['type']]
   start=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',width*4)
   assert a['componentType']==5126
   return[struct.unpack_from('<'+'f'*width,raw[v['buffer']],start+i*stride)for i in range(a['count'])]
  points=Counter();nodes=[]
  for node in g['nodes']:
   for p in g['meshes'][node['mesh']]['primitives']:
    xyz=accessor(p['attributes']['POSITION']);normal=accessor(p['attributes']['NORMAL']);uv=accessor(p['attributes']['TEXCOORD_0'])
    for vertex,n,t in zip(xyz,normal,uv):points[(vertex,n,t,p['material'])]+=1
    nodes.append((node['name'],xyz))
  return points,nodes
 models=json.loads((OUT/'models.json').read_text());surfaces=json.loads((OUT/'surfaces.json').read_text())
 for m in data['missions']:
  name=m['arena_model'];a=m['arena'];before,nodes=read(OUT/(name+'.gltf'));after,_=read(OUT/(name+'.runtime.gltf'))
  assert before==after,'Material batching changed exported vertices: '+m['id'];count+=1
  expected=surfaces[m['id']]
  for label,points in nodes:
   for x,y,z in points:
    assert a[0]-3e-6<=x<=a[0]+a[2]+3e-6 and a[1]-3e-6<=z<=a[1]+a[3]+3e-6,(m['id'],label,'outside arena')
   if label.startswith('SOLID '):
    index=int(label.split()[2]if label.startswith('SOLID crown ')else label.split()[1]);r=expected[index]['r']
    xmin,xmax=min(p[0]for p in points),max(p[0]for p in points);zmin,zmax=min(p[2]for p in points),max(p[2]for p in points)
    assert max(abs(xmin-r[0]),abs(xmax-r[0]-r[2]),abs(zmin-r[1]),abs(zmax-r[1]-r[3]))<3e-6,(m['id'],label,'collider mismatch')
    count+=1
   else:
    assert any(all(r['r'][0]-3e-6<=p[0]<=r['r'][0]+r['r'][2]+3e-6 and r['r'][1]-3e-6<=p[2]<=r['r'][1]+r['r'][3]+3e-6 for p in points)for r in expected),(m['id'],label,'decorative solid outside collision footprint')
    count+=1
  _,ground=read(OUT/(name+'_ground.gltf'));vertices=ground[0][1]
  assert min(p[0]for p in vertices)==a[0]and max(p[0]for p in vertices)==a[0]+a[2]
  assert min(p[2]for p in vertices)==a[1]and max(p[2]for p in vertices)==a[1]+a[3]
  assert models[name+'_ground']['repeat']and models[name+'_ground']['texture']=='floor-'+m['theme']+'.png';count+=1
 manifest=json.loads((OUT/'PROVENANCE.json').read_text())
 assert manifest['generator_sha256']==hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'Regenerate after changing generator'
 for row in manifest['assets']:
  raw=(ROOT/row['path']).read_bytes();assert len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'];count+=1
 print('CAMPAIGN GEOMETRY:',count,'exported-buffer, collider, batch and origin checks PASS')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--data',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
 data=generate_data()if args.data else json.loads((ROOT/'shared/defold04.json').read_text())
 if not args.check:build_worlds(data)
 check_generated(data)
