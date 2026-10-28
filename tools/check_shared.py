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
  self.assertEqual((ROOT/'shared/raid.json').read_bytes(),(ROOT/'pilots/defold/data/raid.json').read_bytes())
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
  for f in (ROOT/'shared/assets/raid').iterdir():
   if f.suffix in ['.gltf','.bin']:self.assertEqual(f.read_bytes(),(ROOT/'pilots/defold/models'/f.name).read_bytes())
  raid=json.loads((ROOT/'shared/audio/raid/manifest.json').read_text());self.assertEqual(len(raid['clips']),3)
  for c in raid['clips']:
   raw=(ROOT/'shared/audio/raid'/c['file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),c['sha256'])
   for dest in ['pilots/gdevelop/assets','pilots/defold/audio']:self.assertEqual(raw,(ROOT/dest/c['file']).read_bytes())
   pcm=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(ROOT/'shared/audio/raid'/c['file']),'-ac','1','-ar','22050','-f','f32le','-'])
   samples=struct.unpack('<'+'f'*(len(pcm)//4),pcm);peak=max(abs(x)for x in samples)
   self.assertGreater(peak,.005);self.assertLess(peak*10**((c['playback_gain_db']-1)/20),.95)
   self.assertAlmostEqual(len(samples)/22050,c['seconds'],places=2)
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
