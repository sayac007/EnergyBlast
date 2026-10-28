"""Generate a native Defold project from the same original glTFs and rules."""
from pathlib import Path
import json,shutil,zipfile
R=Path(__file__).resolve().parents[1];D=R/'pilots/defold'
shutil.copyfile(R/'shared/defold04.json',D/'data/defold04.json')
shutil.copytree(R/'shared/notices',D/'data/notices',dirs_exist_ok=True)
shutil.copyfile(R/'shared/audio/de/manifest.json',D/'data/audio.json')
shutil.copyfile(R/'shared/audio/de/LICENSE.txt',D/'data/AUDIO_LICENSE.txt')
for f in (R/'shared/assets/defold04').iterdir():
 if f.suffix in ['.gltf','.bin']:shutil.copyfile(f,D/'models'/f.name)
for name in ['hero','cannon','relay','radar','spark','spark_hot','reactor','citadel','dock']:
 gltf=json.loads((D/'models'/(name+'.gltf')).read_text());model=['mesh: "/models/'+name+'.gltf"']
 for i,m in enumerate(gltf['materials']):
  color=m.get('pbrMetallicRoughness',{}).get('baseColorFactor',[1,1,1,1]);key=name+'-'+str(i);material='''name: "%s"
tags: "model"
vertex_program: "/builtins/materials/model.vp"
fragment_program: "/main/bright.fp"
vertex_space: VERTEX_SPACE_LOCAL
vertex_constants { name: "mtx_worldview" type: CONSTANT_TYPE_WORLDVIEW }
vertex_constants { name: "mtx_view" type: CONSTANT_TYPE_VIEW }
vertex_constants { name: "mtx_proj" type: CONSTANT_TYPE_PROJECTION }
vertex_constants { name: "mtx_normal" type: CONSTANT_TYPE_NORMAL }
vertex_constants { name: "light" type: CONSTANT_TYPE_USER value { x: -100 y: 160 z: 80 w: 1 } }
fragment_constants { name: "tint" type: CONSTANT_TYPE_USER value { x: %s y: %s z: %s w: %s } }
samplers { name: "tex0" wrap_u: WRAP_MODE_CLAMP_TO_EDGE wrap_v: WRAP_MODE_CLAMP_TO_EDGE filter_min: FILTER_MODE_MIN_LINEAR filter_mag: FILTER_MODE_MAG_LINEAR }
'''%(key,*color)
  (D/'models'/(key+'.material')).write_text(material)
  model.append('materials { name: '+json.dumps(m['name'])+' material: "/models/'+key+'.material" textures { sampler: "tex0" texture: "/models/white.png" } }')
 (D/'models'/(name+'.model')).write_text('\n'.join(model)+'\n')
 (D/'models'/(name+'.go')).write_text('components { id: "model" component: "/models/'+name+'.model" position {x:0 y:0 z:0} rotation {x:0 y:0 z:0 w:1} }\n')
 (D/'models'/(name+'.factory')).write_text('prototype: "/models/'+name+'.go"\n')
shutil.copyfile(R/'pilots/gdevelop/assets/white.png',D/'models/white.png')
shutil.copyfile(R/'shared/raid.json',D/'data/raid-03.json')
manifest=json.loads((R/'shared/audio/de/manifest.json').read_text())
raid=json.loads((R/'shared/audio/raid/manifest.json').read_text());manifest['clips']+=raid['clips']
manifest['clips']+=json.loads((R/'shared/audio/defold04/manifest.json').read_text())['clips']
(D/'data/audio.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for c in manifest['clips']:
 if c['id'].startswith(('combat_','raid_','defold_')) or c['id'] in ['hint_bank','hint_guardian','hints_empty']:
  shutil.copyfile(R/('shared/audio/defold04'if c['id'].startswith('defold_')else'shared/audio/raid'if c['id'].startswith('raid_')else'shared/audio/de')/c['file'],D/'audio'/c['file'])
  (D/'audio'/(c['id']+'.sound')).write_text('sound: "/audio/'+c['file']+'"\nlooping: 0\ngroup: "master"\ngain: '+str(10**((c['playback_gain_db']-1)/20))+'\n')
# Keep Android entirely offline. Native Defold's default manifest requests network permissions.
z=zipfile.ZipFile('/tmp/energyblast-defold-tools/bob.jar');text=z.read('builtins/manifests/android/AndroidManifest.xml').decode()
import re
text=text.replace('<!-- BEGIN_INCLUDE(manifest) -->','<!-- Modified for EnergyBlast 2026-10-27: offline-only manifest; no network/wake permissions; app backup disabled. -->\n<!-- BEGIN_INCLUDE(manifest) -->')
text=re.sub(r'\s*<uses-permission[^>]+/>','',text).replace('android:hasCode="true"','android:hasCode="true" android:allowBackup="false"')
(D/'main/AndroidManifest.xml').write_text(text)
components=['components { id: "logic" component: "/main/main.script" }','components { id: "ui" component: "/main/ui.gui" }']
for name in ['hero','cannon','relay','radar','spark','spark_hot','reactor','citadel','dock']:components.append('components { id: "'+name+'" component: "/models/'+name+'.factory" }')
for c in manifest['clips']:
 if (D/'audio'/(c['id']+'.sound')).exists():components.append('components { id: "'+c['id']+'" component: "/audio/'+c['id']+'.sound" }')
(D/'main/main.go').write_text('\n'.join(components)+'\n')

for f in (R/'shared/audio/sfx').glob('*.wav'):
 shutil.copyfile(f,D/'audio'/f.name)
 (D/'audio'/('fx_'+f.stem+'.sound')).write_text('sound: "/audio/'+f.name+'"\nlooping: 0\ngroup: "master"\ngain: 0.6\n')
 components.append('components { id: "fx_'+f.stem+'" component: "/audio/fx_'+f.stem+'.sound" }')
(D/'main/main.go').write_text('\n'.join(components)+'\n')

shutil.copytree(R/'shared/fonts',D/'data/fonts',dirs_exist_ok=True)
shutil.copyfile(R/'shared/audio/de/MODEL_CARD.txt',D/'data/AUDIO_MODEL_CARD.txt')

shutil.copyfile(R/'shared/audio/defold04/music.json',D/'data/music.json')
for file,name,loop,gain in [('aurora-hop.ogg','music',1,1.0),('energy-burst.ogg','fx_explode',0,.35)]:
 shutil.copyfile(R/'shared/audio/defold04'/file,D/'audio'/file)
 (D/'audio'/(name+'.sound')).write_text('sound: "/audio/'+file+'"\nlooping: '+str(loop)+'\ngroup: "master"\ngain: '+str(gain)+'\n')
 components.append('components { id: "'+name+'" component: "/audio/'+name+'.sound" }')
(D/'main/main.go').write_text('\n'.join(components)+'\n')
