"""Import original generated animation sheets as native depth-tested game assets.

Cropping/resampling is a reproducible technical atlas import, not a new drawing.
Original sheets and their hashes remain alongside the runtime derivatives.
"""
from pathlib import Path
import json, hashlib, struct, shutil, argparse
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'shared/assets/defold07';A.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);args=p.parse_args()
sources=json.loads(args.sources.read_text());provenance=[]
def source(name):
 path=Path(sources[name]);dest=A/(name+'-original.png');shutil.copyfile(path,dest)
 provenance.append({'path':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'origin':'Original OpenAI image generation, 2026-10-28, no reference-game assets','transparency':name in ['hero','dragon','fox','enemies','icons']})
 return Image.open(dest).convert('RGBA')
def cells(image,cols,rows):
 return [image.crop((round(x*image.width/cols),round(y*image.height/rows),round((x+1)*image.width/cols),round((y+1)*image.height/rows))) for y in range(rows)for x in range(cols)]
def trim(im):
 bounds=im.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox();return im.crop(bounds)if bounds else im
def fit(im,size):
 im=trim(im);im.thumbnail((size[0]-16,size[1]-20),Image.Resampling.LANCZOS);out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,size[1]-10-im.height));return out
models={}
def quad(name,texture,w,h,cols=1,rows=1,tag='billboard'):
 # Camera-facing world plane, foot anchored. Uses the SAME 24:18 view as View.lua.
 points=[(-w/2,0,0),(w/2,0,0),(w/2,h*.6,-h*.8),(-w/2,h*.6,-h*.8)]
 blob=b''.join(struct.pack('<3f',*v)for v in points)+b''.join(struct.pack('<3f',0,.8,.6)for _ in points)+b''.join(struct.pack('<2f',*uv)for uv in [(0,0),(1,0),(1,1),(0,1)])+struct.pack('<6H',0,1,2,0,2,3)
 (A/(name+'.bin')).write_bytes(blob)
 gltf={'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}], 'buffers':[{'uri':name+'.bin','byteLength':len(blob)}], 'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':48,'target':34962},{'buffer':0,'byteOffset':48,'byteLength':48,'target':34962},{'buffer':0,'byteOffset':96,'byteLength':32,'target':34962},{'buffer':0,'byteOffset':128,'byteLength':12,'target':34963}],'accessors':[{'bufferView':0,'componentType':5126,'count':4,'type':'VEC3','min':[-w/2,0,-h*.8],'max':[w/2,h*.6,0]},{'bufferView':1,'componentType':5126,'count':4,'type':'VEC3'},{'bufferView':2,'componentType':5126,'count':4,'type':'VEC2'},{'bufferView':3,'componentType':5123,'count':6,'type':'SCALAR'}],'materials':[{'name':'Original illustrated '+name,'doubleSided':True}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'indices':3,'material':0}]}]}
 (A/(name+'.gltf')).write_text(json.dumps(gltf)+'\n');models[name]={'texture':texture,'tag':tag,'columns':cols,'rows':rows}
for name in ['hero','dragon','fox']:
 frames=[fit(c,(256,384))for c in cells(source(name),4,2)];sheet=Image.new('RGBA',(1024,768))
 for i,c in enumerate(frames):sheet.alpha_composite(c,((i%4)*256,(i//4)*384))
 sheet.save(A/(name+'-walk.png'))
 portrait=trim(frames[0]);portrait=portrait.resize((round(portrait.width*600/portrait.height),600),Image.Resampling.LANCZOS)
 fit(portrait,(512,640)).save(A/(name+'-portrait.png'));quad('illustrated_'+name,name+'-walk.png',1.45,2.1,4,2)
enemy=cells(source('enemies'),4,3)
for row,name in enumerate(['sentinel','guardian','boss']):
 sheet=Image.new('RGBA',(1536,384))
 for i in range(4):sheet.alpha_composite(fit(enemy[row*4+i],(384,384)),(i*384,0))
 sheet.save(A/(name+'-states.png'));quad('illustrated_'+name,name+'-states.png',2.25 if name!='boss'else 3.1,2.15 if name!='boss'else 3.0,4,1)
sheet=Image.new('RGBA',(1536,768))
for i,c in enumerate(cells(source('explosion'),4,2)):
 # Preserve growing/shrinking effect silhouettes; do not independently fit them.
 c=c.resize((384,384),Image.Resampling.LANCZOS);sheet.alpha_composite(c,((i%4)*384,(i//4)*384))
sheet.save(A/'explosion-frames.png');quad('illustrated_explosion','explosion-frames.png',3.2,3.2,4,2)
for name,im in zip(['chest','drone','relay','heal'],cells(source('props'),2,2)):
 fit(im,(384,384)).save(A/(name+'-prop.png'))
 quad('illustrated_'+name,name+'-prop.png',1.2 if name!='relay'else 1.0,1.2 if name!='relay'else 1.7)
names=['trap_magnet','trap_frost','trap_pulse','trap_cancel','cannon','armor','boots','cloak']
for name,im in zip(names,cells(source('icons'),4,2)):
 fit(im,(256,256)).save(A/('ui_'+name+'.png'))
 if name.startswith('trap_')and name!='trap_cancel':quad('device_'+name,'ui_'+name+'.png',.9,.65)
for name,im in zip(['reactor','citadel','dock','forge','echo','rescue'],cells(source('cards'),3,2)):
 im.resize((512,288),Image.Resampling.LANCZOS).save(A/('mission_'+name+'.png'))
source('floor').resize((1024,1024),Image.Resampling.LANCZOS).save(A/'floor.png')
source('lobby').resize((1536,864),Image.Resampling.LANCZOS).save(A/'lobby.png')
(A/'models.json').write_text(json.dumps(models,indent=2)+'\n')
(A/'PROVENANCE.json').write_text(json.dumps({'created':'2026-10-28','generator':'OpenAI image generation','runtime_import':'tools/import_defold07_art.py','sheets':provenance,'animation':'4 walk frames each of front/back, mirrored for left; enemy idle/windup/charge/fire frames. Camera-facing native quads, not skeletal 3D.'},indent=2)+'\n')
print('Original illustrated animation, equipment and environment assets imported')
