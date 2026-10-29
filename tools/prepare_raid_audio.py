"""Optional offline synthesis for the three new raid cues; no actor voice cloning."""
import argparse,hashlib,json,math,os,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
TEXTS={'raid_dock':'Erst die Schalter. Nutze die leuchtende Wand. Dann zum Kern.',
       'raid_relays':'Erst die Schalter. Triff sie über die Wand.',
       'raid_hint':'Suche hinter der blauen Deckung.'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);a=p.parse_args()
 base=json.loads((R/'shared/audio/de/manifest.json').read_text())
 assert sha(a.model/'model.safetensors')==base['model_sha256']
 out=R/'shared/audio/raid';out.mkdir(exist_ok=True)
 m={k:v for k,v in base.items()if k not in ['clips','owner_reuse_permission']};m['clips']=[]
 if(out/'manifest.json').exists():m['clips']=json.loads((out/'manifest.json').read_text())['clips']
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',XDG_CACHE_HOME='/tmp/energyblast-cache',HF_HOME='/tmp/energyblast-hf')
 import numpy as np,torch,soundfile as sf
 from qwen_tts import Qwen3TTSModel
 torch.set_num_threads(4)
 model=Qwen3TTSModel.from_pretrained(str(a.model),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
 for id,text in TEXTS.items():
  target=out/(id+'.ogg')
  if any(c['id']==id and c['text']==text and target.exists()and sha(target)==c['sha256'] for c in m['clips']):continue
  torch.manual_seed(int(hashlib.sha256(text.encode()).hexdigest()[:8],16))
  wavs,rate=model.generate_custom_voice(text=text,language='German',speaker='Serena',do_sample=True,subtalker_dosample=True,temperature=.65,top_p=.85,top_k=30,max_new_tokens=240)
  pcm=np.asarray(wavs[0],dtype=np.float32);assert 1<len(pcm)/rate<16
  peak=float(np.max(np.abs(pcm)));assert peak>.005
  pcm=np.concatenate([np.zeros(round(rate*.2)),pcm*min(1.,.8/peak),np.zeros(round(rate*.4))])
  with tempfile.TemporaryDirectory(prefix='energyblast-raid-audio-',dir='/tmp')as d:
   wave=Path(d)/'clip.wav';sf.write(wave,pcm,rate,subtype='PCM_16')
   subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(wave),'-ar','22050','-ac','1','-c:a','libvorbis','-q:a','4',str(target)],check=True)
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(target),'-f','f32le','-ac','1','-ar','22050','-']);decoded=np.frombuffer(raw,dtype='<f4');peak=float(np.max(np.abs(decoded)));assert .005<peak<.999
  m['clips']=[c for c in m['clips']if c['id']!=id]
  m['clips'].append({'id':id,'text':text,'file':target.name,'sha256':sha(target),'seconds':len(decoded)/22050,'playback_gain_db':max(-6.,min(20.,20*math.log10(.65/peak))),'source':'New complete raid sentence; same local synthetic speaker','model_sha256':base['model_sha256']})
  (out/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(id,round(len(decoded)/22050,2),'seconds',flush=True)
if __name__=='__main__':main()
