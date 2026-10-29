"""Technical import of original polished hero sheets into isolated HD atlas cells.

Creative image edits are supplied by image generation. This tool only separates
the eight alpha silhouettes, crops/resamples uniformly and exports native quads.
Original images remain unchanged, with complete parent/intermediate hashes.
"""
from pathlib import Path
from collections import deque
import argparse,hashlib,json,shutil,struct
from PIL import Image,ImageChops,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'shared/assets/defold11'
CELL=(384,512)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def isolate(image,column,row):
    # Generative sheets sometimes extend a gauntlet/tail a few pixels past a
    # nominal cell edge. An expanded crop keeps it whole; the largest connected
    # alpha silhouette separates its neighbour without repainting either pose.
    w,h=image.size;cw,ch=w/4,h/2
    bounds=(max(0,round(column*cw-cw*.18)),round(row*ch),min(w,round((column+1)*cw+cw*.18)),round((row+1)*ch))
    patch=image.crop(bounds).convert('RGBA');alpha=patch.getchannel('A')
    pw,ph=patch.size;values=bytearray(alpha.tobytes());seen=bytearray(pw*ph);best=[]
    for start,value in enumerate(values):
        if value<128 or seen[start]:continue
        queue=deque([start]);seen[start]=1;component=[]
        while queue:
            current=queue.popleft();component.append(current);x=current%pw
            for nxt in (current-pw,current+pw,current-1 if x else -1,current+1 if x<pw-1 else -1):
                if 0<=nxt<len(values) and not seen[nxt] and values[nxt]>=128:
                    seen[nxt]=1;queue.append(nxt)
        if len(component)>len(best):best=component
    assert len(best)>2000,'No complete character silhouette in atlas cell'
    mask=Image.new('L',patch.size);raw=bytearray(pw*ph)
    for index in best:raw[index]=255
    mask.frombytes(bytes(raw));mask=mask.filter(ImageFilter.MaxFilter(7))
    patch.putalpha(ImageChops.multiply(alpha,mask))
    bbox=patch.getchannel('A').getbbox();assert bbox
    return patch.crop(bbox),{'source_crop':list(bounds),'silhouette_bbox':list(bbox),'source_subject_pixels':len(best)}

def quad(name,texture):
    w,h=1.45,2.1;points=[(-w/2,0,0),(w/2,0,0),(w/2,h*.6,-h*.8),(-w/2,h*.6,-h*.8)]
    blob=b''.join(struct.pack('<3f',*v)for v in points)+b''.join(struct.pack('<3f',0,.8,.6)for _ in points)+b''.join(struct.pack('<2f',*uv)for uv in [(0,0),(1,0),(1,1),(0,1)])+struct.pack('<6H',0,1,2,0,2,3)
    (ART/(name+'.bin')).write_bytes(blob)
    g={'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'buffers':[{'uri':name+'.bin','byteLength':len(blob)}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':48,'target':34962},{'buffer':0,'byteOffset':48,'byteLength':48,'target':34962},{'buffer':0,'byteOffset':96,'byteLength':32,'target':34962},{'buffer':0,'byteOffset':128,'byteLength':12,'target':34963}],'accessors':[{'bufferView':0,'componentType':5126,'count':4,'type':'VEC3','min':[-w/2,0,-h*.8],'max':[w/2,h*.6,0]},{'bufferView':1,'componentType':5126,'count':4,'type':'VEC3'},{'bufferView':2,'componentType':5126,'count':4,'type':'VEC2'},{'bufferView':3,'componentType':5123,'count':6,'type':'SCALAR'}],'materials':[{'name':'Original polished '+name,'doubleSided':True}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'indices':3,'material':0}]}]}
    (ART/(name+'.gltf')).write_text(json.dumps(g)+'\n')
    return {'texture':texture,'tag':'billboard','columns':4,'rows':2}

def import_images(sources):
    ART.mkdir(parents=True,exist_ok=True);records=[];models={}
    for name,paths in sources.items():
        source=Path(paths['source']);dest=ART/(name+'-hd-original.png')
        if source.resolve()!=dest.resolve():shutil.copyfile(source,dest)
        intermediate=Path(paths['intermediate']);interdest=ART/(name+'-hd-polish-original.png')
        if intermediate.resolve()!=interdest.resolve():shutil.copyfile(intermediate,interdest)
        image=Image.open(dest).convert('RGBA');frames=[];rows=[]
        for row in range(2):
            for column in range(4):
                frame,info=isolate(image,column,row);frames.append(frame);rows.append(info)
        scale=min(1,(CELL[0]-40)/max(f.width for f in frames),(CELL[1]-32)/max(f.height for f in frames))
        sheet=Image.new('RGBA',(CELL[0]*4,CELL[1]*2))
        for index,frame in enumerate(frames):
            size=(max(1,round(frame.width*scale)),max(1,round(frame.height*scale)));scaled=frame.resize(size,Image.Resampling.LANCZOS)
            x=(CELL[0]-scaled.width)//2;y=CELL[1]-16-scaled.height
            sheet.alpha_composite(scaled,((index%4)*CELL[0]+x,(index//4)*CELL[1]+y))
            rows[index]['runtime_size']=list(size);rows[index]['runtime_offset']=[x,y]
        runtime=ART/(name+'-hd-walk.png');sheet.save(runtime,optimize=True)
        portrait=Image.new('RGBA',(512,640));original=frames[0];portrait_scale=min(472/original.width,608/original.height);frame=original.resize((round(original.width*portrait_scale),round(original.height*portrait_scale)),Image.Resampling.LANCZOS);portrait.alpha_composite(frame,((512-frame.width)//2,624-frame.height));portrait.save(ART/(name+'-hd-portrait.png'),optimize=True)
        models['illustrated_'+name]=quad('illustrated_'+name,runtime.name)
        parent=ROOT/'shared/assets/defold07'/(name+'-original.png')
        records.append({'id':name,'path':dest.name,'sha256':digest(dest),'source_size':list(image.size),'intermediate':{'path':interdest.name,'sha256':digest(interdest)},'original_parent':{'path':str(parent.relative_to(ROOT)),'sha256':digest(parent)},'runtime':{'path':runtime.name,'sha256':digest(runtime),'size':list(sheet.size),'cell':list(CELL),'scale_from_generated_pixels':scale,'frames':rows}})
    (ART/'models.json').write_text(json.dumps(models,indent=2)+'\n')
    provenance={'created':'2026-10-29','generator':'OpenAI image generation','origin':'New polished edits of our own original 0.7 EnergyBlast characters; no external game artwork input','runtime_import':'tools/import_defold11_art.py','animation':'Eight generated walk keyframes, four front and four rear; native transformations and rim shaders supply additional continuous motion, not skeletal 3D.','resolution':'1536x1024 runtime atlases,384x512 per frame, twice the pixel count of the previous1024x768 atlases. Runtime walk-atlas import never upscales the generated sprite pixels; portraits are fitted separately to the established512x640 UI canvas.','sheets':records}
    (ART/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print('Original HD hero atlases imported:',', '.join(sources))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sources',required=True,type=Path);args=p.parse_args();import_images(json.loads(args.sources.read_text()))
