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
  self.assertIn(source.decode(),js)
 def test_all_audio_decodes_matches_manifest_and_will_not_clip(self):
  m=json.loads((ROOT/'shared/audio/de/manifest.json').read_text())
  self.assertEqual(len(m['clips']),19);self.assertEqual(len({c['id'] for c in m['clips']}),19)
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
 def test_unlocks_and_rewards_have_a_bounded_unique_economy(self):
  d=json.loads((ROOT/'shared/pilot.json').read_text())
  self.assertEqual(sum(d['rewards'].values()),325)
  self.assertEqual(len(d['missions']),2)
  for m in d['missions']:
   self.assertTrue(all(key+':'+m['id'] in d['rewards'] for key in ['mission','skill','secret']))
  self.assertEqual([u['stars'] for u in d['unlocks']],[100,160,230,300])
 def test_android_sources_do_not_request_permissions_or_backup(self):
  manifest=(ROOT/'pilots/gdevelop/android/app/src/main/AndroidManifest.xml').read_text()
  self.assertNotIn('<uses-permission',manifest);self.assertIn('android:allowBackup="false"',manifest)
  preset=(ROOT/'pilots/godot/export_presets.cfg').read_text()
  self.assertIn('permissions/internet=false',preset);self.assertIn('user_data_backup/allow=false',preset)
if __name__=='__main__':unittest.main(verbosity=2)
