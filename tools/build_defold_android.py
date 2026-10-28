"""Native Defold/Bob ARM64 debug build; no editor service, no native extension server."""
import argparse,hashlib,json,os,re,shutil,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--sdk',type=Path,default=Path('/tmp/energyblast-defold-tools'));p.add_argument('--tools',type=Path,default=Path('/workspace/tools'));p.add_argument('--output',type=Path,required=True);a=p.parse_args()
out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);project=out/'project';shutil.copytree(ROOT/'pilots/defold',project,ignore=shutil.ignore_patterns('build','.internal','.editor_settings','.DS_Store'))
java=next(a.sdk.glob('Defold/packages/jdk-*/bin/java'));key=a.tools/'energyblast-pilot-signing/debug.keystore';assert key.exists() and not key.is_relative_to(ROOT)
password=out/'debug-password.txt';password.write_text('android\n');password.chmod(0o600)
cmd=[str(java),'-Duser.home='+str(out/'java-user'),'-jar',str(a.sdk/'bob.jar'),'--root',str(project),'--platform','arm64-android','--architectures','arm64-android','--variant','debug','--archive','--bundle-format','apk','--bundle-output',str(out/'bundle'),'--keystore',str(key),'--keystore-pass',str(password),'--keystore-alias','androiddebugkey','--max-cpu-threads','2','resolve','build','bundle']
env=dict(os.environ,JAVA_HOME=str(java.parent.parent),ANDROID_HOME=str(a.tools/'android-sdk'))
try:
 with(out/'build.log').open('w')as log:r=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT)
finally:password.unlink(missing_ok=True)
if r.returncode:print((out/'build.log').read_text()[-7000:]);raise SystemExit(r.returncode)
apks=list((out/'bundle').rglob('*.apk'));assert len(apks)==1,apks
apk=out/'energyblast-defold-debug.apk';shutil.copyfile(apks[0],apk)
def run(args):
 r=subprocess.run([str(x)for x in args],check=True,env=dict(env,JAVA_HOME=str(a.tools/'android-jdk')),capture_output=True,text=True);return r.stdout+r.stderr
bt=a.tools/'android-sdk/build-tools/36.1.0';badging=run([bt/'aapt2','dump','badging',apk]);(out/'manifest.txt').write_text(badging)
assert "name='org.example.energyblast.defold'" in badging and "versionCode='9'"in badging and "versionName='0.8.0'"in badging
assert not re.search(r'^uses-permission:',badging,re.M)
assert re.search(r"^(?:minSdkVersion|sdkVersion):'24'$",badging,re.M) and "targetSdkVersion:'36'" in badging
xml=run([bt/'aapt2','dump','xmltree',apk,'--file','AndroidManifest.xml']);(out/'manifest-xml.txt').write_text(xml);assert re.search(r':allowBackup\([^)]*\)=false',xml);assert re.search(r':screenOrientation\([^)]*\)=11(?:\s|$)',xml),xml
sig=run([bt/'apksigner','verify','--verbose','--print-certs',apk]);(out/'signature.txt').write_text(sig);assert 'CN=EnergyBlast Pilot Debug'in sig
run([bt/'zipalign','-c','-P','16','4',apk])
report={'status':'PASS','built_at_utc':datetime.now(timezone.utc).isoformat(),'variant':'Defold 1.14.0 native ARM64 shooter','package':'org.example.energyblast.defold','version':'0.8.0','version_code':9,'bytes':apk.stat().st_size,'sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'permissions':[],'min_sdk':24,'target_sdk':36,'allow_backup':False,'screen_orientation':'userLandscape','signature':'Development-only key; not a Play release identity','zip_alignment_16kb':'PASS','source_commit':run(['git','-C',ROOT,'rev-parse','HEAD']).strip(),'source_dirty':bool(run(['git','-C',ROOT,'status','--porcelain']).strip()),'manual_android_test':'NOT VERIFIED','key_in_repository':False}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
