"""Optional offline synthesis for the new press-duration control cue; no actor voice cloning."""
import argparse,hashlib,json,math,os,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
TEXTS={
 'defold_secret':'Suche die goldenen Pfeile und die dunklen Spuren. Dahinter liegt ein Schatz.',
 'defold_forge':'Tippe auf das Fallenbild neben deiner Figur. Wähle eine Falle. Tippe dann auf einen freien Platz in deiner Nähe.',
 'defold_echo':'Schau auf die Lichter. Triff sie in derselben Reihenfolge.',
 'defold_rescue':'Begleite die Drohne. Bleibe in ihrer Nähe und schütze sie vor den Kanonen.',
 'defold_controls':'Kurz tippen zum Laufen. Halte zum Zielen. Lass los zum Schießen.',
 'defold_trap_open':'Wähle eine Magnetfalle, eine Eisfalle oder eine Impulsfalle. Das Kreuz bricht ab.',
 'defold_trap_select':'Tippe auf freien Boden im hellen Kreis. Dort liegt gleich deine Falle.',
 'defold_trap_place':'Falle bereit. Locke den Wächter hinein.',
 'defold_trap_trigger':'Schild aus. Jetzt treffen!',
 'defold_trap_magnet':'Magnet. Hält den Wächter fest. Tippe zum Ablegen auf freien Boden im hellen Kreis.',
 'defold_trap_frost':'Eis. Hält länger fest. Tippe zum Ablegen auf freien Boden im hellen Kreis.',
 'defold_trap_pulse':'Der Wächter verliert zwei Energiepunkte. Tippe zum Ablegen auf freien Boden im hellen Kreis.',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True)
 p.add_argument('--regenerate',action='append',choices=TEXTS,default=[],help='Regenerate only this matching clip after a failed listening/transcription screen; repeatable.')
 p.add_argument('--seed-offset',type=int,default=0,help='Deterministic variation for targeted pronunciation retries.')
 a=p.parse_args()
 base=json.loads((R/'shared/audio/de/manifest.json').read_text())
 assert sha(a.model/'model.safetensors')==base['model_sha256']
 out=R/'shared/audio/defold04';out.mkdir(exist_ok=True)
 m={k:v for k,v in base.items()if k not in ['clips','owner_reuse_permission']};m['clips']=[]
 if(out/'manifest.json').exists():m['clips']=json.loads((out/'manifest.json').read_text())['clips']
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',XDG_CACHE_HOME='/tmp/energyblast-cache',HF_HOME='/tmp/energyblast-hf')
 import numpy as np,torch,soundfile as sf
 from qwen_tts import Qwen3TTSModel
 torch.set_num_threads(4)
 model=Qwen3TTSModel.from_pretrained(str(a.model),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
 for id,text in TEXTS.items():
  target=out/(id+'.ogg')
  if id not in a.regenerate and any(c['id']==id and c['text']==text and target.exists()and sha(target)==c['sha256'] for c in m['clips']):continue
  seed=(int(hashlib.sha256(text.encode()).hexdigest()[:8],16)+a.seed_offset)%2**32
  torch.manual_seed(seed)
  wavs,rate=model.generate_custom_voice(text=text,language='German',speaker='Serena',do_sample=True,subtalker_dosample=True,temperature=.65,top_p=.85,top_k=30,max_new_tokens=240)
  pcm=np.asarray(wavs[0],dtype=np.float32);assert 1<len(pcm)/rate<16
  peak=float(np.max(np.abs(pcm)));assert peak>.005
  if id=='defold_trap_trigger':
   # Preserve quiet consonants and 60 ms around words; remove only dead time.
   # No time-stretch or concatenation of independently generated syllables.
   block=max(1,round(rate*.01));n=len(pcm)//block
   levels=np.max(np.abs(pcm[:n*block].reshape(n,block)),axis=1)
   audible=np.flatnonzero(levels>peak*.004);assert len(audible)>0
   lo=max(0,audible[0]*block-round(rate*.06));hi=min(len(pcm),(audible[-1]+1)*block+round(rate*.06))
   pcm=pcm[lo:hi]
   quiet=np.max(np.abs(pcm[:len(pcm)//block*block].reshape(-1,block)),axis=1)<=peak*.004
   spans=[];start=None
   for i,is_quiet in enumerate(list(quiet)+[False]):
    if is_quiet and start is None:start=i
    elif not is_quiet and start is not None:
     if (i-start)*block>=round(rate*.25):spans.append((start*block,i*block))
     start=None
   for start,end in reversed(spans):
    keep=round(rate*.06);pcm=np.concatenate([pcm[:start+keep],pcm[end-keep:]])
  # Combat feedback must start promptly inside the short shield opening.
  lead,tail=(.05,.12)if id=='defold_trap_trigger'else(.2,.4)
  pcm=np.concatenate([np.zeros(round(rate*lead)),pcm*min(1.,.8/peak),np.zeros(round(rate*tail))])
  with tempfile.TemporaryDirectory(prefix='energyblast-raid-audio-',dir='/tmp')as d:
   wave=Path(d)/'clip.wav';sf.write(wave,pcm,rate,subtype='PCM_16')
   subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(wave),'-ar','22050','-ac','1','-c:a','libvorbis','-q:a','4',str(target)],check=True)
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(target),'-f','f32le','-ac','1','-ar','22050','-']);decoded=np.frombuffer(raw,dtype='<f4');peak=float(np.max(np.abs(decoded)));assert .005<peak<.999
  m['clips']=[c for c in m['clips']if c['id']!=id]
  m['clips'].append({'id':id,'text':text,'file':target.name,'sha256':sha(target),'seconds':len(decoded)/22050,'playback_gain_db':max(-6.,min(20.,20*math.log10(.65/peak))),'source':'New complete raid sentence; same local synthetic speaker','model_sha256':base['model_sha256'],'synthesis_seed':seed})
  (out/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(id,round(len(decoded)/22050,2),'seconds',flush=True)
if __name__=='__main__':main()
