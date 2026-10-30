"""Original low-poly EnergyBlast units; no downloaded geometry or textures.

Each unit is one native glTF model. Parts are batched by material; the engine
animates hovering, banking, throbbing and electrical destruction without one
extra game object per rotor/leg. PNG icons are offline orthographic renders of
these same original triangles, not third-party pictures.
"""
from pathlib import Path
import hashlib,json,math,struct
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'shared/assets/defold14_units';OUT.mkdir(parents=True,exist_ok=True)
COLORS={
 'Hull midnight':(.025,.07,.14,1),'Titanium silver':(.55,.72,.80,1),
 'Jade enamel':(.03,.63,.58,1),'Solar gold':(1,.59,.08,1),
 'Coral armor':(.87,.13,.20,1),'Iris enamel':(.39,.18,.72,1),
 'Luminous cyan':(.18,1,1,1),'Luminous amber':(1,.79,.19,1),
 'Luminous red':(1,.15,.3,1),'Luminous lightning':(.52,.87,1,1)}
class Shape:
 def __init__(self):self.triangles=[]
 def triangle(self,a,b,c,material):self.triangles.append((a,b,c,material))
 def box(self,p,s,material):
  x,y,z=p;w,h,d=(v/2 for v in s)
  v=[(x+dx*w,y+dy*h,z+dz*d)for dx,dy,dz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
  for a,b,c,d in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)]:self.triangle(v[a],v[b],v[c],material);self.triangle(v[a],v[c],v[d],material)
 def sphere(self,p,s,material,n=12,rings=6):
  rows=[]
  for j in range(rings+1):
   a=math.pi*j/rings
   rows.append([(p[0]+s[0]*math.sin(a)*math.cos(2*math.pi*i/n),p[1]+s[1]*math.cos(a),p[2]+s[2]*math.sin(a)*math.sin(2*math.pi*i/n))for i in range(n)])
  for j in range(rings):
   for i in range(n):
    k=(i+1)%n;self.triangle(rows[j][i],rows[j+1][k],rows[j+1][i],material);self.triangle(rows[j][i],rows[j][k],rows[j+1][k],material)
 def rod(self,a,b,radius,material,n=8):
  d=[b[i]-a[i]for i in range(3)];length=math.sqrt(sum(v*v for v in d));d=[v/length for v in d]
  helper=(0,1,0)if abs(d[1])<.9 else(1,0,0)
  u=[d[1]*helper[2]-d[2]*helper[1],d[2]*helper[0]-d[0]*helper[2],d[0]*helper[1]-d[1]*helper[0]];size=math.sqrt(sum(v*v for v in u));u=[v/size for v in u]
  v=[d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0]]
  rows=[[(p[k]+radius*(u[k]*math.cos(i*2*math.pi/n)+v[k]*math.sin(i*2*math.pi/n)))for k in range(3)]for p in[a,b]for i in range(n)]
  for i in range(n):
   j=(i+1)%n;self.triangle(rows[i],rows[j],rows[n+j],material);self.triangle(rows[i],rows[n+j],rows[n+i],material)
   self.triangle(a,rows[j],rows[i],material);self.triangle(b,rows[n+i],rows[n+j],material)
 def ring(self,p,radius,tube,material,n=16,k=4):
  rows=[]
  for i in range(n):
   a=i*2*math.pi/n
   rows.append([(p[0]+(radius+tube*math.cos(j*2*math.pi/k))*math.cos(a),p[1]+tube*math.sin(j*2*math.pi/k),p[2]+(radius+tube*math.cos(j*2*math.pi/k))*math.sin(a))for j in range(k)])
  for i in range(n):
   ni=(i+1)%n
   for j in range(k):nj=(j+1)%k;self.triangle(rows[i][j],rows[ni][nj],rows[ni][j],material);self.triangle(rows[i][j],rows[i][nj],rows[ni][nj],material)
 def export(self,name,tag='model',fragment=None):
  raw=bytearray();views=[];access=[];primitives=[];materials=[]
  def write(values,fmt,kind,target=None):
   while len(raw)%4:raw.append(0)
   offset=len(raw)
   for row in values:raw.extend(struct.pack('<'+fmt,*row))
   view={'buffer':0,'byteOffset':offset,'byteLength':len(raw)-offset}
   if target:view['target']=target
   views.append(view);a={'bufferView':len(views)-1,'componentType':5126,'count':len(values),'type':kind}
   if kind=='VEC3':a.update(min=[min(v[i]for v in values)for i in range(3)],max=[max(v[i]for v in values)for i in range(3)])
   access.append(a);return len(access)-1
  for material,color in COLORS.items():
   tris=[t for t in self.triangles if t[3]==material]
   if not tris:continue
   pos=[];norm=[];uv=[]
   for a,b,c,_ in tris:
    d=[b[i]-a[i]for i in range(3)];e=[c[i]-a[i]for i in range(3)]
    normal=[d[1]*e[2]-d[2]*e[1],d[2]*e[0]-d[0]*e[2],d[0]*e[1]-d[1]*e[0]];length=math.sqrt(sum(v*v for v in normal));normal=[v/length for v in normal]if length>1e-8 else[0,1,0]
    pos.extend([a,b,c]);norm.extend([normal]*3);uv.extend([(0,0),(1,0),(.5,1)])
   pi=write(pos,'fff','VEC3',34962);ni=write(norm,'fff','VEC3',34962);ui=write(uv,'ff','VEC2',34962)
   materials.append({'name':material,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':color,'roughnessFactor':.4,'metallicFactor':.5}})
   primitives.append({'attributes':{'POSITION':pi,'NORMAL':ni,'TEXCOORD_0':ui},'material':len(materials)-1,'mode':4})
  (OUT/(name+'.bin')).write_bytes(raw)
  gltf={'asset':{'version':'2.0','generator':'EnergyBlast original procedural units 0.14'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'buffers':[{'uri':name+'.bin','byteLength':len(raw)}],'bufferViews':views,'accessors':access,'materials':materials,'meshes':[{'primitives':primitives}]}
  (OUT/(name+'.gltf')).write_text(json.dumps(gltf,separators=(',',':'))+'\n')
  meta={'runtime':name+'.gltf','tag':tag,'texture':None}
  if fragment:meta['fragment']=fragment
  return meta

def copter(attack=False):
 s=Shape();body='Coral armor'if attack else'Jade enamel'
 s.sphere((0,.38,0),(.32,.18,.4),body)
 s.box((0,.53,.01),(.25,.12,.24),'Hull midnight');s.box((0,.6,.01),(.18,.035,.18),'Solar gold')
 for x in[-.42,.42]:
  for z in[-.37,.37]:
   s.rod((0,.38,0),(x,.43,z),.045,'Titanium silver');s.ring((x,.45,z),.23,.035,'Hull midnight')
   s.ring((x,.46,z),.2,.018,'Luminous amber'if attack else'Luminous cyan')
   s.box((x,.45,z),(.33,.015,.045),'Titanium silver');s.box((x,.45,z),(.045,.015,.33),'Titanium silver')
 s.sphere((0,.38,-.36),(.13,.12,.07),'Hull midnight');s.sphere((0,.39,-.42),(.075,.075,.025),'Luminous red'if attack else'Luminous cyan')
 if attack:
  s.sphere((0,.2,0),(.18,.12,.22),'Solar gold');s.box((0,.08,0),(.16,.08,.14),'Luminous amber')
 else:s.box((0,.19,.1),(.19,.08,.17),'Solar gold')
 return s

def splitter():
 s=Shape();s.sphere((0,.55,0),(.56,.38,.48),'Iris enamel');s.ring((0,.57,0),.56,.045,'Solar gold')
 for x in[-.43,.43]:s.sphere((x,.53,.17),(.26,.27,.32),'Hull midnight');s.ring((x,.73,.17),.18,.035,'Luminous cyan')
 s.sphere((0,.68,-.43),(.22,.12,.10),'Hull midnight')
 for x in[-.1,.1]:s.sphere((x,.7,-.51),(.055,.06,.025),'Luminous red')
 for x in[-.45,.45]:s.rod((x,.6,.1),(x*1.5,.83,.25),.045,'Titanium silver')
 return s

def crawler():
 s=Shape();s.sphere((0,.32,0),(.47,.27,.52),'Hull midnight');s.box((0,.55,.02),(.53,.15,.55),'Coral armor')
 for side in[-1,1]:
  for z in[-.35,0,.35]:
   a=(side*.3,.35,z);b=(side*.65,.25,z+.12);c=(side*.79,.08,z+.22)
   s.rod(a,b,.055,'Solar gold');s.rod(b,c,.045,'Titanium silver');s.sphere(b,(.075,.075,.075),'Jade enamel',8,4)
 s.box((0,.48,-.5),(.4,.1,.13),'Titanium silver')
 for x in[-.12,.12]:s.sphere((x,.49,-.59),(.065,.055,.025),'Luminous red')
 return s

def wisp():
 s=Shape();s.sphere((0,.5,0),(.24,.36,.24),'Luminous cyan',8,4)
 s.ring((0,.5,0),.42,.04,'Solar gold');s.ring((0,.7,0),.31,.025,'Luminous amber');s.ring((0,.3,0),.31,.025,'Iris enamel')
 for i in range(4):
  a=i*math.pi/2;s.sphere((math.cos(a)*.42,.5,math.sin(a)*.42),(.085,.11,.085),'Titanium silver',8,4)
 return s

def lightning():
 s=Shape()
 for phase in[0,math.pi]:
  points=[]
  for i in range(8):
   a=phase+i*.63;points.append((math.sin(a)*(.2+(i%2)*.25),i*.24,math.cos(a)*.18))
  for a,b in zip(points,points[1:]):s.rod(a,b,.035,'Luminous lightning',5)
 return s

def icon(shape,name):
 size=256;image=Image.new('RGBA',(size,size),(0,0,0,0));shadow=Image.new('RGBA',image.size);d=ImageDraw.Draw(shadow);d.ellipse((27,99,229,237),fill=(50,170,210,90));shadow=shadow.filter(ImageFilter.GaussianBlur(14));image.alpha_composite(shadow)
 # Isometric-looking original orthographic triangle renderer of the same model.
 def project(p):return(128+(p[0]-p[2])*.72*112,171+(p[0]+p[2])*.36*112-p[1]*112)
 triangles=sorted(shape.triangles,key=lambda t:sum(p[0]+p[2]-p[1]*.4 for p in t[:3])/3)
 draw=ImageDraw.Draw(image)
 for a,b,c,material in triangles:
  d1=[b[i]-a[i]for i in range(3)];d2=[c[i]-a[i]for i in range(3)];n=[d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0]];length=math.sqrt(sum(v*v for v in n)) or 1
  light=.68+.32*abs((n[0]*-.4+n[1]*.8+n[2]*-.5)/length)
  if material.startswith('Luminous'):light=1
  color=tuple(round(min(1,c*light)*255)for c in COLORS[material][:3])+(255,)
  draw.polygon([project(a),project(b),project(c)],fill=color)
 image.save(OUT/(name+'.png'))

models={};shapes={
 'enemy_mini_drone':copter(), 'enemy_splitter':splitter(),
 'enemy_crawler':crawler(), 'enemy_wisp':wisp(), 'attack_drone':copter(True)}
for name,shape in shapes.items():models[name]=shape.export(name)
models['unit_lightning']=lightning().export('unit_lightning','hero_aura','bright.fp')
icon(shapes['attack_drone'],'ui_attack_drone');icon(shapes['enemy_mini_drone'],'ui_swarm')
(OUT/'models.json').write_text(json.dumps(models,indent=2)+'\n')
files=[]
for f in sorted(OUT.iterdir()):
 if f.suffix in['.gltf','.bin','.png']:files.append({'path':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(OUT/'PROVENANCE.json').write_text(json.dumps({'generator':'tools/make_defold14_units.py','origin':'Original procedural geometry and offline rendered icons; no external images/models','files':files},indent=2)+'\n')
print(json.dumps({'models':list(models),'total_bytes':sum(f['bytes']for f in files)}))
