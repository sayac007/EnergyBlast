"""Export the small Godot debug pilot with an outside-repository development key."""
import argparse,hashlib,json,os,re,subprocess,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(args,env=None,**kwargs):
 r=subprocess.run([str(x) for x in args],env=env,capture_output=True,text=True,**kwargs)
 if r.returncode:
  print((r.stdout+'\n'+r.stderr)[-5000:]);raise RuntimeError('Tool failed: '+str(args[0]))
 return r.stdout+r.stderr
p=argparse.ArgumentParser();p.add_argument('--tools',type=Path,default=Path('/workspace/tools'));p.add_argument('--output',type=Path,required=True);a=p.parse_args()
tools=a.tools.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
godot=tools/'godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64';java=tools/'android-jdk';sdk=tools/'android-sdk'
keydir=tools/'energyblast-pilot-signing';keydir.mkdir(exist_ok=True);key=keydir/'debug.keystore'
if not key.exists():
 run([java/'bin/keytool','-genkeypair','-storetype','JKS','-keystore',key,'-storepass','android','-keypass','android','-alias','androiddebugkey','-keyalg','RSA','-keysize','2048','-validity','10000','-dname','CN=EnergyBlast Pilot Debug'])
 key.chmod(0o600)
assert not key.is_relative_to(ROOT)
assert run([godot,'--version']).startswith('4.7.2.stable')
with tempfile.TemporaryDirectory(prefix='energyblast-export-',dir='/tmp') as d:
 state=Path(d);(state/'android-user').mkdir();data=state/'data/godot/export_templates';data.mkdir(parents=True)
 (data/'4.7.2.stable').symlink_to(tools/'android-tools/templates',target_is_directory=True)
 config=state/'config/godot';config.mkdir(parents=True)
 config.joinpath('editor_settings-4.7.tres').write_text('[gd_resource type="EditorSettings" format=3]\n[resource]\n'+''.join(f'{name} = {json.dumps(str(value))}\n' for name,value in {'export/android/android_sdk_path':sdk,'export/android/java_sdk_path':java,'export/android/debug_keystore':key,'export/android/debug_keystore_user':'androiddebugkey','export/android/debug_keystore_pass':'android'}.items()))
 env=dict(os.environ,XDG_DATA_HOME=str(state/'data'),XDG_CONFIG_HOME=str(state/'config'),XDG_CACHE_HOME=str(state/'cache'),JAVA_HOME=str(java),ANDROID_HOME=str(sdk),ANDROID_USER_HOME=str(state/'android-user'),ANDROID_PREFS_ROOT=str(state/'android-user'))
 log=run([godot,'--headless','--audio-driver','Dummy','--path',ROOT/'pilots/godot','--editor','--import','--quit'],env)
 out.joinpath('import.log').write_text(log)
 apk=out/'energyblast-godot-debug.apk'
 log=run([godot,'--headless','--audio-driver','Dummy','--path',ROOT/'pilots/godot','--export-debug','Android Pilot',apk],env)
 out.joinpath('export.log').write_text(log)
 bt=sdk/'build-tools/36.1.0'
 badging=run([bt/'aapt2','dump','badging',apk]);out.joinpath('manifest.txt').write_text(badging)
 assert "name='org.example.energyblast.pilot'" in badging
 assert "versionCode='1'" in badging and "versionName='0.1.0'" in badging
 assert 'uses-permission:' not in badging
 assert re.search(r"^(?:minSdkVersion|sdkVersion):'24'$",badging,re.M) and "targetSdkVersion:'36'" in badging
 xml=run([bt/'aapt2','dump','xmltree',apk,'--file','AndroidManifest.xml'])
 out.joinpath('manifest-xml.txt').write_text(xml)
 assert re.search(r':allowBackup\([^)]*\)=false',xml)
 signature=run([bt/'apksigner','verify','--verbose','--print-certs',apk],dict(os.environ,JAVA_HOME=str(java)))
 out.joinpath('signature.txt').write_text(signature)
 assert 'CN=EnergyBlast Pilot Debug' in signature and 'v2): true' in signature
 run([bt/'zipalign','-c','-P','16','4',apk])
 report={'built_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','variant':'Godot touch pilot','package':'org.example.energyblast.pilot','version':'0.1.0','version_code':1,'bytes':apk.stat().st_size,'sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'permissions':[],'min_sdk':24,'target_sdk':36,'allow_backup':False,'signature':'Development-only key; not a Play release identity','zip_alignment_16kb':'PASS','source_commit':run(['git','-C',ROOT,'rev-parse','HEAD']).strip(),'source_dirty':bool(run(['git','-C',ROOT,'status','--porcelain']).strip()),'manual_android_test':'NOT VERIFIED','key_in_repository':False}
 out.joinpath('verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
