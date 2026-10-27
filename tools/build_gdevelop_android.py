"""Build the native GDevelop export inside a minimal offline Android WebView."""
import argparse, hashlib, json, os, shutil, subprocess, re
from datetime import datetime,timezone
from urllib.parse import urlsplit
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--trust-store',type=Path);p.add_argument('--offline',action='store_true');p.add_argument('--output',type=Path,required=True);p.add_argument('--web',type=Path,default=Path('/tmp/energyblast-gdevelop-web'));p.add_argument('--tools',type=Path,default=Path('/workspace/tools'));a=p.parse_args()
out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
project=out/'project';shutil.copytree(ROOT/'pilots/gdevelop/android',project,ignore=shutil.ignore_patterns('.gradle','build'))
tools=a.tools.resolve();sdk=tools/'android-sdk';java=tools/'android-jdk';key=tools/'energyblast-pilot-signing/debug.keystore'
assert key.is_file(), 'Run the Godot debug export first to create an outside-repository development key.'
assert not key.is_relative_to(ROOT)
assert (a.web/'index.html').is_file(), 'Export the pinned GDevelop project first.'
gradles=list((tools/'android-gradle-cache/wrapper/dists/gradle-8.11.1-bin').glob('*/gradle-8.11.1/bin/gradle'));assert len(gradles)==1
(project/'local.properties').write_text('sdk.dir='+str(sdk)+'\n')
(out/'.android').mkdir()
env=dict(os.environ,ANDROID_USER_HOME=str(out/'.android'),ANDROID_PREFS_ROOT=str(out),JAVA_HOME=str(java),ANDROID_HOME=str(sdk),GRADLE_USER_HOME=str(tools/'android-gradle-cache'),ENERGYBLAST_DEBUG_KEY=str(key),ENERGYBLAST_WEB_EXPORT=str(a.web.resolve()))
if a.trust_store:
 env['GRADLE_OPTS']=env.get('GRADLE_OPTS','')+' -Djavax.net.ssl.trustStore='+str(a.trust_store.resolve())
proxy=urlsplit(os.environ.get('HTTPS_PROXY',''))
if proxy.hostname and not proxy.username:
 env['GRADLE_OPTS']=env.get('GRADLE_OPTS','')+f' -Dhttps.proxyHost={proxy.hostname} -Dhttps.proxyPort={proxy.port or 80} -Dhttp.proxyHost={proxy.hostname} -Dhttp.proxyPort={proxy.port or 80}'
with (out/'build.log').open('w') as log:
 r=subprocess.run([str(gradles[0]),'--no-daemon','--stacktrace']+(['--offline'] if a.offline else [])+[':app:assembleDebug'],cwd=project,env=env,stdout=log,stderr=subprocess.STDOUT)
if r.returncode:
 print((out/'build.log').read_text()[-6000:]);raise SystemExit(r.returncode)
apk=out/'energyblast-gdevelop-debug.apk';shutil.copyfile(project/'app/build/outputs/apk/debug/app-debug.apk',apk)
def run(args):
 r=subprocess.run([str(x) for x in args],env=env,check=True,capture_output=True,text=True)
 return r.stdout+r.stderr
bt=sdk/'build-tools/36.1.0'
badging=run([bt/'aapt2','dump','badging',apk]);(out/'manifest.txt').write_text(badging)
assert "name='org.example.energyblast.gdevelop'" in badging
assert "versionCode='1'" in badging and "versionName='0.1.0'" in badging
assert 'uses-permission:' not in badging
assert re.search(r"^(?:minSdkVersion|sdkVersion):'24'$",badging,re.M) and "targetSdkVersion:'36'" in badging
xml=run([bt/'aapt2','dump','xmltree',apk,'--file','AndroidManifest.xml']);(out/'manifest-xml.txt').write_text(xml)
assert re.search(r':allowBackup\([^)]*\)=false',xml)
sig=run([bt/'apksigner','verify','--verbose','--print-certs',apk]);(out/'signature.txt').write_text(sig)
assert 'CN=EnergyBlast Pilot Debug' in sig and 'v2): true' in sig
run([bt/'zipalign','-c','-P','16','4',apk])
report={'built_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','variant':'GDevelop 5.6.269 WebGL in offline Android WebView','package':'org.example.energyblast.gdevelop','version':'0.1.0','version_code':1,'bytes':apk.stat().st_size,'sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'permissions':[],'min_sdk':24,'target_sdk':36,'allow_backup':False,'signature':'Development-only key; not a Play release identity','zip_alignment_16kb':'PASS','source_commit':run(['git','-C',ROOT,'rev-parse','HEAD']).strip(),'source_dirty':bool(run(['git','-C',ROOT,'status','--porcelain']).strip()),'manual_android_test':'NOT VERIFIED','key_in_repository':False}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
