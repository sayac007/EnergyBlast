"""Offline asset/audio consistency and safety checks; no human listening claim."""
from pathlib import Path
import hashlib,json,math,struct,subprocess,unittest
ROOT=Path(__file__).resolve().parents[1]
class SharedChecks(unittest.TestCase):
 def test_shared_rules_and_models_are_identical(self):
  source=(ROOT/'shared/pilot.json').read_bytes()
  for copy in ['pilots/godot/assets/pilot.json','pilots/unity/Assets/Resources/EnergyBlast/pilot.json']:
   self.assertEqual(source,(ROOT/copy).read_bytes(),copy)
  for copy in ['pilots/godot/assets/robot.glb','pilots/gdevelop/assets/robot.glb']:
   self.assertEqual((ROOT/'shared/assets/robot.glb').read_bytes(),(ROOT/copy).read_bytes())
  self.assertEqual((ROOT/'shared/assets/robot.fbx').read_bytes(),(ROOT/'pilots/unity/Assets/Resources/EnergyBlast/robot.fbx').read_bytes())
  raw=(ROOT/'shared/assets/robot.glb').read_bytes()
  self.assertEqual(raw[:4],b'glTF');self.assertEqual(struct.unpack_from('<II',raw,4),(2,len(raw)))
  project=json.loads((ROOT/'pilots/gdevelop/game.json').read_text())
  js=project['layouts'][0]['events'][0]['inlineCode']
  self.assertIn((ROOT/'shared/raid.json').read_text(),js)
  self.assertEqual((ROOT/'shared/combat.json').read_bytes(),(ROOT/'pilots/godot/assets/combat.json').read_bytes())
  self.assertEqual((ROOT/'shared/defold04.json').read_bytes(),(ROOT/'pilots/defold/data/defold04.json').read_bytes())
 def test_all_audio_decodes_matches_manifest_and_will_not_clip(self):
  m=json.loads((ROOT/'shared/audio/de/manifest.json').read_text())
  self.assertEqual(len(m['clips']),26);self.assertEqual(len({c['id'] for c in m['clips']}),26)
  self.assertEqual(sum(c['source']=='Kinderwelt exact approved reuse' for c in m['clips']),4)
  for c in m['clips']:
   with self.subTest(clip=c['id']):
    f=ROOT/'shared/audio/de'/c['file'];raw=f.read_bytes();self.assertTrue(raw.startswith(b'OggS'))
    self.assertEqual(hashlib.sha256(raw).hexdigest(),c['sha256'])
    for folder in ['pilots/godot/assets/audio/de','pilots/gdevelop/assets','pilots/unity/Assets/Resources/EnergyBlast/de']:
     self.assertEqual((ROOT/folder/c['file']).read_bytes(),raw)
    pcm=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(f),'-ac','1','-ar','22050','-f','f32le','-'])
    values=struct.unpack('<'+'f'*(len(pcm)//4),pcm)
    peak=max(abs(v) for v in values)
    self.assertGreater(peak,.005);self.assertLess(peak,.999)
    self.assertLess(peak*10**((c['playback_gain_db']-1)/20),.95)
    self.assertAlmostEqual(len(values)/22050,c['seconds'],places=2)
    self.assertGreater(c['seconds'],1);self.assertLess(c['seconds'],16)
 def test_raid_provenance_models_and_new_audio(self):
  m=json.loads((ROOT/'shared/asset-origins.json').read_text())
  for row in m['assets']:
   self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['sha256'],row['path'])
  for f in (ROOT/'shared/assets/raid').glob('*.glb'):
   raw=f.read_bytes();self.assertEqual(raw[:4],b'glTF');self.assertEqual(struct.unpack_from('<II',raw,4),(2,len(raw)))
   self.assertEqual(raw,(ROOT/'pilots/gdevelop/assets'/f.name).read_bytes())
  for f in (ROOT/'shared/assets/defold06').iterdir():
   if f.suffix in ['.gltf','.bin','.png'] and f.name not in ['hero.png','dragon.png','fox.png']:self.assertEqual(f.read_bytes(),(ROOT/'pilots/defold/models'/f.name).read_bytes())
  raid=json.loads((ROOT/'shared/audio/raid/manifest.json').read_text());self.assertEqual(len(raid['clips']),3)
  for c in raid['clips']:
   raw=(ROOT/'shared/audio/raid'/c['file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),c['sha256'])
   for dest in ['pilots/gdevelop/assets','pilots/defold/audio']:self.assertEqual(raw,(ROOT/dest/c['file']).read_bytes())
   pcm=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(ROOT/'shared/audio/raid'/c['file']),'-ac','1','-ar','22050','-f','f32le','-'])
   samples=struct.unpack('<'+'f'*(len(pcm)//4),pcm);peak=max(abs(x)for x in samples)
   self.assertGreater(peak,.005);self.assertLess(peak*10**((c['playback_gain_db']-1)/20),.95)
   self.assertAlmostEqual(len(samples)/22050,c['seconds'],places=2)
 def test_defold_music_voice_and_larger_world(self):
  d=json.loads((ROOT/'shared/defold04.json').read_text());old=json.loads((ROOT/'shared/raid.json').read_text())
  self.assertEqual(d['arena'][2]*d['arena'][3],2.25*old['arena'][2]*old['arena'][3]);self.assertTrue(all(d['rewards'][k]==v for k,v in old['rewards'].items()));self.assertEqual(len(d['missions']),6)
  manifest=json.loads((ROOT/'shared/audio/defold04/manifest.json').read_text());self.assertEqual(len(manifest['clips']),12)
  music=json.loads((ROOT/'shared/audio/defold04/music.json').read_text())
  for c in manifest['clips']+music['files']:
   file=c.get('file');raw=(ROOT/'shared/audio/defold04'/file).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),c['sha256'])
   self.assertEqual(raw,(ROOT/'pilots/defold/audio'/file).read_bytes())
   pcm=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(ROOT/'shared/audio/defold04'/file),'-ac','1','-ar','22050','-f','f32le','-'])
   samples=struct.unpack('<'+'f'*(len(pcm)//4),pcm);peak=max(abs(x)for x in samples)
   self.assertLess(peak,.95);self.assertGreater(peak,.01);self.assertAlmostEqual(len(samples)/22050,c['seconds'],places=2)
   if file=='aurora-hop.ogg':
    self.assertEqual(c['seconds'],60);self.assertGreater(math.sqrt(sum(x*x for x in samples)/len(samples)),.05)
    self.assertLess(abs(samples[0]-samples[-1]),.005)
  sound=(ROOT/'pilots/defold/audio/music.sound').read_text();self.assertIn('looping: 1',sound);self.assertIn('gain: 1.0',sound)
  self.assertIn('defold_controls',(ROOT/'pilots/defold/main/main.go').read_text())
 def test_exported_wall_geometry_matches_every_collider(self):
  # Read actual exported POSITION buffers, not just the generator's claims.
  surfaces=json.loads((ROOT/'shared/assets/defold06/surfaces.json').read_text())
  for mission,rows in surfaces.items():
   gltf=json.loads((ROOT/'shared/assets/defold06'/(mission+'.gltf')).read_text());points={}
   for node in gltf['nodes']:
    name=node.get('name','')
    if not name.startswith('SOLID '):continue
    index=int(name.split()[2]if name.startswith('SOLID crown ')else name.split()[1])
    self.assertNotIn('rotation',node);self.assertNotIn('scale',node)
    translation=node.get('translation',[0,0,0]);mesh=gltf['meshes'][node['mesh']]
    for primitive in mesh['primitives']:
     acc=gltf['accessors'][primitive['attributes']['POSITION']];view=gltf['bufferViews'][acc['bufferView']]
     self.assertEqual(acc['componentType'],5126);self.assertEqual(acc['type'],'VEC3')
     raw=(ROOT/'shared/assets/defold06'/gltf['buffers'][view['buffer']]['uri']).read_bytes()
     start=view.get('byteOffset',0)+acc.get('byteOffset',0);stride=view.get('byteStride',12)
     for j in range(acc['count']):
      point=struct.unpack_from('<fff',raw,start+j*stride);points.setdefault(index,[]).append([point[k]+translation[k]for k in range(3)])
   self.assertEqual(len(points),len(rows),mission)
   for i,row in enumerate(rows):
    pts=points[i];xs=[p[0]for p in pts];zs=[p[2]for p in pts];actual=[min(xs),min(zs),max(xs)-min(xs),max(zs)-min(zs)]
    for value,expected in zip(actual,row['r']):self.assertAlmostEqual(value,expected,places=5,msg=mission+':'+str(i))
  gui=(ROOT/'pilots/defold/main/ui.gui_script').read_text()
  self.assertNotIn('for _,b in ipairs(g.bullets)',gui,'shots must be depth-tested native models')
 def test_ensemble_has_real_stereo_and_section_dynamics(self):
  pcm=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(ROOT/'shared/audio/defold04/aurora-hop.ogg'),'-ar','8000','-ac','2','-f','f32le','-'])
  samples=struct.unpack('<'+'f'*(len(pcm)//4),pcm);sections=[]
  for i in range(4):
   values=samples[i*15*8000*2:(i+1)*15*8000*2];sections.append(math.sqrt(sum(v*v for v in values)/len(values)))
  self.assertGreater(max(sections)/min(sections),1.5)
  self.assertGreater(math.sqrt(sum((l-r)**2 for l,r in zip(samples[::2],samples[1::2]))/(len(samples)//2)),.005)
 def test_preserved_legacy_rigs_and_active_ground_bindings(self):
  from PIL import Image,ImageStat
  art=ROOT/'shared/assets/defold06';models=json.loads((art/'models.json').read_text());rigs=json.loads((art/'rigs.json').read_text())
  for hero in ['hero','dragon','fox']:
   parts={p['part']for p in rigs[hero]};self.assertTrue({'body','leg_l','leg_r','arm_l','arm_r'}<=parts)
   ao=Image.open(art/(hero+'-ao.png')).convert('L');self.assertEqual(ao.size,(1024,1024));self.assertGreater(ImageStat.Stat(ao).stddev[0],10)
   for piece in rigs[hero]:
    self.assertEqual(models[piece['model']]['texture'],hero+'-ao.png')
    binding=(ROOT/'pilots/defold/models'/(piece['model']+'.model')).read_text();self.assertIn(hero+'-ao.png',binding)
    self.assertIn('tags: "actor"',(ROOT/'pilots/defold/models'/(piece['model']+'-0.material')).read_text())
  for mission in ['reactor','citadel','dock','forge','echo','rescue']:
   model=mission+'_ground';texture='floor.png';self.assertIn(texture,(ROOT/'pilots/defold/models'/(model+'.model')).read_text())
   self.assertEqual((ROOT/'shared/assets/defold07'/texture).read_bytes(),(ROOT/'pilots/defold/models'/texture).read_bytes())
  self.assertIn('self.glow',(ROOT/'pilots/defold/main/main.render_script').read_text())
 def test_illustrated_actors_have_real_transparent_distinct_animation_frames(self):
  from PIL import Image
  art=ROOT/'shared/assets/defold07';models=json.loads((art/'models.json').read_text())
  for name in ['hero','dragon','fox']:
   image=Image.open(art/(name+'-walk.png'));self.assertEqual(image.size,(1024,768));self.assertEqual(image.mode,'RGBA')
   frames=[image.crop((x*256,y*384,(x+1)*256,(y+1)*384))for y in range(2)for x in range(4)]
   self.assertEqual(len({hashlib.sha256(f.tobytes()).hexdigest()for f in frames}),8)
   for frame in frames:
    alpha=frame.getchannel('A');self.assertEqual(alpha.getextrema()[0],0);self.assertGreater(alpha.getextrema()[1],240)
    self.assertEqual(alpha.crop((0,0,8,384)).getextrema()[1],0,'atlas margin avoids adjacent-cell bleed')
   model='illustrated_'+name
   self.assertIn(name+'-walk.png',(ROOT/'pilots/defold/models'/(model+'.model')).read_text())
   self.assertIn('tags: "billboard"',(ROOT/'pilots/defold/models'/(model+'-0.material')).read_text())
  for name,meta in models.items():
   self.assertEqual((art/meta['texture']).read_bytes(),(ROOT/'pilots/defold/models'/meta['texture']).read_bytes())
  origins=json.loads((art/'PROVENANCE.json').read_text())
  self.assertEqual(len(origins['sheets']),10)
  for row in origins['sheets']:self.assertEqual(hashlib.sha256((art/row['path']).read_bytes()).hexdigest(),row['sha256'])
 def test_static_batches_preserve_source_geometry(self):
  import numpy as np
  art=ROOT/'shared/assets/defold06';models=json.loads((art/'models.json').read_text())
  def geometry(file):
   g=json.loads(file.read_text());result=set();primitive_count=0
   for node in g['nodes']:
    if 'mesh'not in node:continue
    self.assertNotIn('children',node)
    if 'matrix'in node:transform=np.array(node['matrix']).reshape((4,4),order='F')
    else:
     x,y,z,w=node.get('rotation',[0,0,0,1]);rot=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
     transform=np.eye(4);transform[:3,:3]=rot@np.diag(node.get('scale',[1,1,1]));transform[:3,3]=node.get('translation',[0,0,0])
    for primitive in g['meshes'][node['mesh']]['primitives']:
     primitive_count+=1;acc=g['accessors'][primitive['attributes']['POSITION']];view=g['bufferViews'][acc['bufferView']];raw=(file.parent/g['buffers'][view['buffer']]['uri']).read_bytes();offset=view.get('byteOffset',0)+acc.get('byteOffset',0);stride=view.get('byteStride',12)
     coords=np.array([struct.unpack_from('<fff',raw,offset+j*stride)for j in range(acc['count'])]);coords=np.c_[coords,np.ones(len(coords))]@transform.T
     result.update(tuple(point)for point in np.round(coords[:,:3],6))
   return result,primitive_count
  for name,m in models.items():
   if 'runtime'not in m:continue
   before,count_before=geometry(art/(name+'.gltf'));after,count_after=geometry(art/m['runtime'])
   # Exporting Float32 transforms can move the final decimal; compare positions
   # geometrically, rather than relying on rounding across a bin boundary.
   def covers(a,b):
    buckets={}
    for point in b:
     key=tuple(math.floor(v*10000)for v in point);buckets.setdefault(key,[]).append(point)
    for point in a:
     key=tuple(math.floor(v*10000)for v in point);found=False
     for dx in [-1,0,1]:
      for dy in [-1,0,1]:
       for dz in [-1,0,1]:
        if any(max(abs(p[i]-point[i])for i in range(3))<.00002 for p in buckets.get((key[0]+dx,key[1]+dy,key[2]+dz),[])):found=True;break
       if found:break
      if found:break
     if not found:return False
    return True
   self.assertTrue(covers(before,after)and covers(after,before),'batched position changed: '+name);self.assertLessEqual(count_after,count_before,name)
   if name in ['reactor','citadel','dock','forge','echo','rescue']:self.assertLess(count_after,count_before/4,name)
   self.assertIn(m['runtime'],(ROOT/'pilots/defold/models'/(name+'.model')).read_text())
 def test_shortlisted_engines_do_not_render_ballistic_previews(self):
  gui=(ROOT/'pilots/defold/main/ui.gui_script').read_text();js=(ROOT/'pilots/gdevelop/shooter.js').read_text()
  self.assertNotIn('g:shot()',gui);self.assertNotIn('this.line(this.shot()',js)
  d=json.loads((ROOT/'shared/raid.json').read_text());self.assertFalse(d['preview_trajectory'])
  self.assertEqual(len(d['missions']),3);self.assertEqual(sum(d['rewards'].values()),925)
  self.assertEqual(sum(v for k,v in d['rewards'].items()if not k.endswith((':bank',':guardian'))),600)
 def test_unlocks_and_rewards_have_a_bounded_unique_economy(self):
  d=json.loads((ROOT/'shared/pilot.json').read_text())
  self.assertEqual(sum(d['rewards'].values()),325)
  self.assertEqual(len(d['missions']),2)
  combat=json.loads((ROOT/'shared/combat.json').read_text());self.assertEqual(sum(combat['rewards'].values()),650)
  self.assertEqual(sum(v for k,v in combat['rewards'].items()if k.endswith((':reactor',':citadel'))),325)
  for m in d['missions']:
   self.assertTrue(all(key+':'+m['id'] in d['rewards'] for key in ['mission','skill','secret']))
  self.assertEqual([u['stars'] for u in d['unlocks']],[100,160,230,300])
 def test_android_sources_do_not_request_permissions_or_backup(self):
  manifest=(ROOT/'pilots/gdevelop/android/app/src/main/AndroidManifest.xml').read_text()
  self.assertNotIn('<uses-permission',manifest);self.assertIn('android:allowBackup="false"',manifest)
  preset=(ROOT/'pilots/godot/export_presets.cfg').read_text()
  self.assertIn('permissions/internet=false',preset);self.assertIn('user_data_backup/allow=false',preset)
  native=(ROOT/'pilots/defold/main/AndroidManifest.xml').read_text();self.assertNotIn('<uses-permission',native);self.assertIn('android:allowBackup="false"',native)
  import configparser
  cfg=configparser.ConfigParser();cfg.read(ROOT/'pilots/defold/game.project');self.assertEqual(cfg['bootstrap']['render'],'/main/main.renderc')
if __name__=='__main__':unittest.main(verbosity=2)
