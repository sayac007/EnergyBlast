"""Download the pinned public Defold Linux SDK outside the checkout; no admin rights."""
import argparse,hashlib,json,stat,urllib.request,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('/tmp/energyblast-defold-tools'));a=p.parse_args();out=a.output.resolve();assert not out.is_relative_to(R);out.mkdir(parents=True,exist_ok=True)
m=json.loads((R/'tools/defold-sdk.json').read_text())
for row in m['assets']:
 f=out/row['file']
 if not f.exists():
  temporary=f.with_suffix(f.suffix+'.part')
  with urllib.request.urlopen(row['url'],timeout=45)as source,temporary.open('wb')as target:
   while chunk:=source.read(1024*1024):target.write(chunk)
  temporary.rename(f)
 assert f.stat().st_size==row['bytes']and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],f
 if f.suffix=='.zip':
  with zipfile.ZipFile(f)as z:
   for item in z.infolist():
    if '/jdk'not in item.filename.lower():continue
    target=(out/item.filename).resolve();assert target.is_relative_to(out)
    z.extract(item,out)
    if not item.is_dir():target.chmod((item.external_attr>>16)|stat.S_IRUSR|stat.S_IWUSR)
with zipfile.ZipFile(out/'bob.jar')as z:
 executable=out/'dmengine';executable.write_bytes(z.read('libexec/x86_64-linux/dmengine'));executable.chmod(0o755)
print('Defold',m['version'],'verified and prepared in',out)
