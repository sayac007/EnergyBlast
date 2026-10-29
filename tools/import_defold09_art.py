"""Technical import of original 0.9 floor paintings and native analytic effect quads."""
from pathlib import Path
import argparse,hashlib,json,shutil,struct
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'shared/assets/defold09';A.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);args=p.parse_args()
origins=[];sources=json.loads(args.sources.read_text())
for name,path in sources.items():
 dest=A/(name+'-original.png')
 if Path(path).resolve()!=dest.resolve():shutil.copyfile(path,dest)
 Image.open(dest).convert('RGB').resize((1024,1024),Image.Resampling.LANCZOS).save(A/('floor-'+name+'.png'))
 origins.append({'path':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'origin':'Original OpenAI image generation 2026-10-29, based only on our own original floor design atlas; no reference-game art input'})
models={}
def quad(name,points,normal,tag,fragment):
 blob=b''.join(struct.pack('<3f',*v)for v in points)+b''.join(struct.pack('<3f',*normal)for _ in points)+b''.join(struct.pack('<2f',*uv)for uv in [(0,0),(1,0),(1,1),(0,1)])+struct.pack('<6H',0,1,2,0,2,3)
 (A/(name+'.bin')).write_bytes(blob)
 g={'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'buffers':[{'uri':name+'.bin','byteLength':len(blob)}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':48,'target':34962},{'buffer':0,'byteOffset':48,'byteLength':48,'target':34962},{'buffer':0,'byteOffset':96,'byteLength':32,'target':34962},{'buffer':0,'byteOffset':128,'byteLength':12,'target':34963}],'accessors':[{'bufferView':0,'componentType':5126,'count':4,'type':'VEC3','min':[min(v[i]for v in points)for i in range(3)],'max':[max(v[i]for v in points)for i in range(3)]},{'bufferView':1,'componentType':5126,'count':4,'type':'VEC3'},{'bufferView':2,'componentType':5126,'count':4,'type':'VEC2'},{'bufferView':3,'componentType':5123,'count':6,'type':'SCALAR'}],'materials':[{'name':name}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'indices':3,'material':0}]}]}
 (A/(name+'.gltf')).write_text(json.dumps(g)+'\n');models[name]={'tag':tag,'fragment':fragment,'texture':None}
quad('cover_shadow',[(-.5,0,.5),(.5,0,.5),(.5,0,-.5),(-.5,0,-.5)],(0,1,0),'shadow','cover_shadow.fp')
quad('energy_field',[(-1.35,0,0),(1.35,0,0),(1.35,1.68,-2.24),(-1.35,1.68,-2.24)],(0,.8,.6),'energy','energy_field.fp')
(A/'models.json').write_text(json.dumps(models,indent=2)+'\n')
provenance={'created':'2026-10-29','original_images':origins,'geometry':'Original camera-facing and floor quad geometry, tools/import_defold09_art.py','effects':'Original analytic depth-tested shield and floor contact-shadow shaders'}
atlas=A/'design-atlas-original.png'
if atlas.exists():provenance['design_atlas']={'path':atlas.name,'sha256':hashlib.sha256(atlas.read_bytes()).hexdigest(),'origin':'Original OpenAI-generated design atlas,2026-10-29, no external game reference input'}
(A/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
print('0.9 original floor/effect assets imported')
