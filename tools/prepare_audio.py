"""Reuse only approved matching clips; synthesize missing complete sentences offline."""
import argparse,hashlib,json,math,os,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEXTS={
'intro_bank':'Triff den gelben Knopf über die Wand.',
'intro_guardian':'Der Wächter kommt. Bleibe im Versteck.',
'gate':'Drei Lichter. Dann öffnet sich das Tor.',
'move':'Tippe auf den Boden. Dein Roboter läuft dorthin.',
'aim':'Tippe auf die leuchtende Wand.',
'predict':'Wo landet der Schuss? Tippe auf die Stelle.',
'fire':'Jetzt schießen. Beobachte die Spur.',
'hints_empty':'Sammle Hinweise mit einer Mission.',
'hint_bank':'Suche hinter der blauen Kiste.',
'hint_guardian':'Suche hinter dem großen Versteck.',
'gate_closed':'Drei Lichter. Dann geht es los.',
'trap':'Tippe auf einen Platz für dein Fangfeld.',
'found':'Ein geheimer Fund! Sterne und Ausrüstung für dich.',
'upgrade':'Deine Ausrüstung ist stärker geworden.',
'seen':'Zurück ins Versteck. Ein neuer Versuch.'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--reuse',type=Path,required=True);p.add_argument('--model',type=Path,required=True);a=p.parse_args()
 out=ROOT/'shared/audio/de';out.mkdir(parents=True,exist_ok=True)
 old=json.loads((a.reuse/'manifest.json').read_text());rows=[]
 prior=json.loads((out/'manifest.json').read_text()) if (out/'manifest.json').exists() else {'clips':[]}

 for row in old['clips']:
  if row['id'] not in ['success','again','praise_1','praise_4']:continue
  source=a.reuse/row['file'];assert sha(source)==row['sha256']
  shutil.copyfile(source,out/(row['id']+'.ogg'))
  rows.append({'id':row['id'],'text':row['text'],'file':row['id']+'.ogg','sha256':sha(source),'seconds':row['seconds'],'playback_gain_db':row['playback_gain_db'],'source':'Kinderwelt exact approved reuse','source_file':row['file'],'source_manifest_sha256':sha(a.reuse/'manifest.json')})
 for row in prior['clips']:
  if row['id'] in TEXTS and row['text']==TEXTS[row['id']] and (out/row['file']).is_file() and sha(out/row['file'])==row['sha256']:rows.append(row)
 for name in ['LICENSE.txt','MODEL_CARD.txt']:shutil.copyfile(a.reuse/name,out/name)
 manifest={'schema':1,'language':'de','speaker':'Serena','model':old['model'],'model_source':old['model_source'],'model_sha256':old['model_sha256'],'dataset_license':old['dataset_license'],'human_listening_review':'OPEN for new mission clips','owner_reuse_permission':'Explicit operator instruction 2026-10-27; matching public audio only','clips':rows}
 def save():(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 save()
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',XDG_CACHE_HOME='/tmp/energyblast-cache',HF_HOME='/tmp/energyblast-hf')
 import numpy as np,torch,soundfile as sf
 from qwen_tts import Qwen3TTSModel
 assert sha(a.model/'model.safetensors')==old['model_sha256']
 torch.set_num_threads(4)
 model=Qwen3TTSModel.from_pretrained(str(a.model),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
 for id,text in TEXTS.items():
  target=out/(id+'.ogg')
  prior=next((x for x in manifest['clips'] if x['id']==id and x['text']==text),None)
  if prior and target.exists() and sha(target)==prior['sha256']:continue
  torch.manual_seed(int(hashlib.sha256(text.encode()).hexdigest()[:8],16))
  wavs,rate=model.generate_custom_voice(text=text,language='German',speaker='Serena',do_sample=True,subtalker_dosample=True,temperature=.65,top_p=.85,top_k=30,max_new_tokens=220)
  pcm=np.asarray(wavs[0],dtype=np.float32);duration=len(pcm)/rate
  if not 0.6<duration<16:raise ValueError(f'Incomplete or runaway audio: {id} {duration}')
  peak=float(np.max(np.abs(pcm)));assert peak>.005
  pcm=np.concatenate([np.zeros(round(rate*.2)),pcm*min(1.,.8/peak),np.zeros(round(rate*.4))])
  with tempfile.TemporaryDirectory(prefix='energyblast-voice-',dir='/tmp') as d:
   wave=Path(d)/'clip.wav';sf.write(wave,pcm,rate,subtype='PCM_16')
   subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(wave),'-ar','22050','-ac','1','-c:a','libvorbis','-q:a','4',str(target)],check=True)
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(target),'-f','f32le','-ac','1','-ar','22050','-'])
  decoded=np.frombuffer(raw,dtype='<f4');peak=float(np.max(np.abs(decoded)))
  assert .005<peak<.999
  manifest['clips'].append({'id':id,'text':text,'file':target.name,'sha256':sha(target),'seconds':len(decoded)/22050,'playback_gain_db':max(-6.,min(20.,20*math.log10(.65/peak))),'source':'New complete mission sentence; same local synthetic speaker','model_sha256':old['model_sha256']})
  save();print(id,round(duration,2),'seconds',flush=True)
if __name__=='__main__':main()
