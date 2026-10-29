"""Generate a native Defold project from the same original glTFs and rules."""
from pathlib import Path
import json,shutil,zipfile,struct
R=Path(__file__).resolve().parents[1];D=R/'pilots/defold'
shutil.copyfile(R/'shared/defold04.json',D/'data/defold04.json')
shutil.copyfile(R/'shared/defold07-regression.json',D/'data/defold07.json')
shutil.copyfile(R/'shared/defold12-regression.json',D/'data/defold12.json')
shutil.copytree(R/'shared/notices',D/'data/notices',dirs_exist_ok=True)
shutil.copyfile(R/'shared/audio/de/manifest.json',D/'data/audio.json')
shutil.copyfile(R/'shared/audio/de/LICENSE.txt',D/'data/AUDIO_LICENSE.txt')
art=R/'shared/assets/defold06'
models=json.loads((art/'models.json').read_text())
illustrations=R/'shared/assets/defold07'
if illustrations.exists():
 models.update(json.loads((illustrations/'models.json').read_text()))
 for f in illustrations.iterdir():
  if f.suffix in ['.gltf','.bin','.png'] and '-original' not in f.name:shutil.copyfile(f,D/'models'/f.name)
effects=R/'shared/assets/defold09'
if effects.exists():
 models.update(json.loads((effects/'models.json').read_text()))
 for f in effects.iterdir():
  if f.suffix in ['.gltf','.bin','.png']and '-original'not in f.name:shutil.copyfile(f,D/'models'/f.name)
sanctuary=R/'shared/assets/defold10'
if sanctuary.exists():
 models.update(json.loads((sanctuary/'models.json').read_text()))
 for f in sanctuary.iterdir():
  if f.suffix in ['.gltf','.bin','.png']:shutil.copyfile(f,D/'models'/f.name)
polished=R/'shared/assets/defold11'
if (polished/'models.json').exists():
 models.update(json.loads((polished/'models.json').read_text()))
 for f in polished.iterdir():
  if f.suffix in ['.gltf','.bin','.png']and '-original'not in f.name:shutil.copyfile(f,D/'models'/f.name)
models['hero_aura']={'runtime':'glow.gltf','tag':'hero_aura','texture':None,'fragment':'glow.fp'}
models['hero_power_shield']={'runtime':'energy_field.gltf','tag':'hero_aura','texture':None,'fragment':'energy_field.fp'}
for key in models:
 if key.endswith('_ground'):
  mission=key[:-7];models[key]['texture']='floor-'+mission+'.png'if effects.exists()else'floor.png';models[key]['color_tint']=[.84,.88,.96,1]
for f in art.iterdir():
 if f.suffix in ['.gltf','.bin','.png']:shutil.copyfile(f,D/'models'/f.name)
for name in models:
 mesh=models[name].get('runtime',name+'.gltf');gltf=json.loads((D/'models'/mesh).read_text());model=['mesh: "/models/'+mesh+'"']
 for i,m in enumerate(gltf['materials']):
  color=models[name].get('color_tint',m.get('pbrMetallicRoughness',{}).get('baseColorFactor',[1,1,1,1]));key=name+'-'+str(i);tag=models[name]['tag'];fragment=models[name].get('fragment')or('billboard.fp'if tag=='billboard'else'shadow.fp'if tag=='shadow'else'glow.fp'if tag=='glow'else'bright.fp');texture=models[name]['texture']or'white.png';ground=1 if name.endswith('_ground')else 0;emissive=1 if m.get('name','').startswith('Luminous ')else 0;material='''name: "%s"
tags: "%s"
vertex_program: "/builtins/materials/model.vp"
fragment_program: "/main/%s"
vertex_space: VERTEX_SPACE_LOCAL
vertex_constants { name: "mtx_worldview" type: CONSTANT_TYPE_WORLDVIEW }
vertex_constants { name: "mtx_view" type: CONSTANT_TYPE_VIEW }
vertex_constants { name: "mtx_proj" type: CONSTANT_TYPE_PROJECTION }
vertex_constants { name: "mtx_normal" type: CONSTANT_TYPE_NORMAL }
vertex_constants { name: "light" type: CONSTANT_TYPE_USER value { x: -40 y: 100 z: 60 w: 1 } }
fragment_constants { name: "tint" type: CONSTANT_TYPE_USER value { x: %s y: %s z: %s w: %s } }
fragment_constants { name: "surface" type: CONSTANT_TYPE_USER value { x: %s y: %s z: 0 w: 0 } }
fragment_constants { name: "edge" type: CONSTANT_TYPE_USER value { x: %s y: 0 z: 0 w: 0 } }
fragment_constants { name: "hero_fx" type: CONSTANT_TYPE_USER value { x: 0 y: 0 z: 0 w: 0 } }
fragment_constants { name: "frame" type: CONSTANT_TYPE_USER value { x: 0 y: 0 z: %s w: %s } }
samplers { name: "tex0" wrap_u: WRAP_MODE_CLAMP_TO_EDGE wrap_v: WRAP_MODE_CLAMP_TO_EDGE filter_min: FILTER_MODE_MIN_LINEAR filter_mag: FILTER_MODE_MAG_LINEAR }
'''%(key,tag,fragment,*color,ground,emissive,1.25 if name in ['illustrated_hero','illustrated_dragon','illustrated_fox','illustrated_sentinel','illustrated_guardian','illustrated_boss']else 0,models[name].get('columns',1),models[name].get('rows',1))
  if fragment=='billboard.fp':
   width,height=struct.unpack('>II',(D/'models'/texture).read_bytes()[16:24])
   material+='fragment_constants { name: \"atlas_texel\" type: CONSTANT_TYPE_USER value { x: '+str(1/width)+' y: '+str(1/height)+' z: 0 w: 0 } }\n'
   material+='fragment_constants { name: "power_fx" type: CONSTANT_TYPE_USER value { x: 1 y: 0 z: 0 w: 0 } }\n'
  material='\n'.join(line for line in material.splitlines()if not(('name: \"tint\"'in line and fragment in ['shadow.fp','cover_shadow.fp'])or('name: \"frame\"'in line and fragment not in ['billboard.fp','cover_shadow.fp','energy_field.fp'])or('name: \"hero_fx\"'in line and fragment!='billboard.fp')or('name: \"edge\"'in line and fragment!='billboard.fp')or('name: \"surface\"'in line and fragment!='bright.fp')or('samplers {'in line and fragment in ['shadow.fp','glow.fp','cover_shadow.fp','energy_field.fp'])))+'\n'
  (D/'models'/(key+'.material')).write_text(material)
  model.append('materials { name: '+json.dumps(m['name'])+' material: "/models/'+key+'.material" textures { sampler: "tex0" texture: "/models/'+texture+'" } }')
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
 if c['id'].startswith(('combat_','raid_','defold_','flow_','bonus_')) or c['id'] in ['hint_bank','hint_guardian','hints_empty']:
  shutil.copyfile(R/('shared/audio/defold04'if c['id'].startswith(('defold_','flow_','bonus_'))else'shared/audio/raid'if c['id'].startswith('raid_')else'shared/audio/de')/c['file'],D/'audio'/c['file'])
  (D/'audio'/(c['id']+'.sound')).write_text('sound: "/audio/'+c['file']+'"\nlooping: 0\ngroup: "master"\ngain: '+str(10**((c['playback_gain_db']-1)/20))+'\n')
# Keep Android entirely offline. Native Defold's default manifest requests network permissions.
z=zipfile.ZipFile('/tmp/energyblast-defold-tools/bob.jar');text=z.read('builtins/manifests/android/AndroidManifest.xml').decode()
import re
text=text.replace('<!-- BEGIN_INCLUDE(manifest) -->','<!-- Modified for EnergyBlast 2026-10-27: offline-only manifest; no network/wake permissions; app backup disabled. -->\n<!-- BEGIN_INCLUDE(manifest) -->')
text=re.sub(r'\s*<uses-permission[^>]+/>','',text).replace('android:hasCode="true"','android:hasCode="true" android:allowBackup="false"')
(D/'main/AndroidManifest.xml').write_text(text)
components=['components { id: "logic" component: "/main/main.script" }','components { id: "ui" component: "/main/ui.gui" }']
for name in models:
 if illustrations.exists()and models[name]['tag']=='actor':continue
 components.append('components { id: "'+name+'" component: "/models/'+name+'.factory" }')
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

# Original portrait renders, not external character art.
for name in ['hero','dragon','fox']:
 portrait=(polished/(name+'-hd-portrait.png'))if (polished/(name+'-hd-portrait.png')).exists()else(illustrations/(name+'-portrait.png'))if illustrations.exists()else(art/(name+'.png'))
 shutil.copyfile(portrait,D/'models'/(name+'.png'))
(D/'models/portraits.atlas').write_text('\n'.join('images { image: "/models/'+n+'.png" }'for n in ['hero','dragon','fox'])+'\nextrude_borders: 2\n')
shutil.copyfile(art/'surfaces.json',D/'data/surfaces.json')

shutil.copyfile(art/'rigs.json',D/'data/rigs.json')

ui_names=['button_blue','button_gold','button_green','button_violet','panel']+['ui_'+n for n in ['star','heart','aim','dash','hint','radio','gear','menu','sound','trap']]+['ui_background']
if illustrations.exists():ui_names += ['ui_'+n for n in ['trap_magnet','trap_frost','trap_pulse','trap_cancel','cannon','armor','boots','cloak']]+['mission_'+n for n in ['reactor','citadel','dock','forge','echo','rescue']]+['lobby','chest-prop']
(D/'models/interface.atlas').write_text('\n'.join('images { image: "/models/'+n+'.png" }'for n in ui_names)+'\nextrude_borders: 2\n')
components.append('components { id: "backdrop" component: "/main/backdrop.gui" }')
(D/'main/main.go').write_text('\n'.join(components)+'\n')
