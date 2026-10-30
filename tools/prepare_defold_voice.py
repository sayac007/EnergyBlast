"""Optional offline synthesis for touch, navigation and bonus cues; no actor voice cloning."""
import argparse,hashlib,json,math,os,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
TEXTS={
 'defold_secret':'Suche die goldenen Pfeile und die dunklen Spuren. Dahinter liegt ein Schatz.',
 'defold_forge':'Tippe auf das Fallenbild neben deiner Figur. Wähle eine Falle. Tippe dann auf einen freien Platz in deiner Nähe.',
 'defold_echo':'Schau auf die Lichter. Triff sie in derselben Reihenfolge.',
 'defold_rescue':'Begleite die Drohne. Bleibe in ihrer Nähe und schütze sie vor den Kanonen.',
 'defold_controls':'Kurz tippen zum Laufen. Halten zum Schießen. Ziehe deine Figur zum Bewegen.',
 'defold_enemy_tap':'Tippe auf einen Gegner. Deine Figur schießt sofort. Daneben tippen reicht auch.',
 'defold_trap_open':'Wähle eine Magnetfalle, eine Eisfalle oder eine Impulsfalle. Das Kreuz bricht ab.',
 'defold_trap_select':'Tippe auf freien Boden im hellen Kreis. Dort liegt gleich deine Falle.',
 'defold_trap_place':'Falle bereit. Locke den Wächter hinein.',
 'defold_trap_trigger':'Schild aus. Jetzt treffen!',
 'defold_trap_magnet':'Magnet. Hält den Wächter fest. Tippe zum Ablegen auf freien Boden im hellen Kreis.',
 'defold_trap_frost':'Eis. Hält länger fest. Tippe zum Ablegen auf freien Boden im hellen Kreis.',
 'defold_trap_pulse':'Der Wächter verliert zwei Energiepunkte. Tippe zum Ablegen auf freien Boden im hellen Kreis.',
 'flow_menu':'Wähle eine Mission. Links kannst du auch den Drachen wählen.',
 'flow_shop':'Hier gibst du Sterne aus. Tippe auf Kaufen. Deine Gesamtsterne bleiben.',
 'flow_dragon':'Dein Drache ist bereit. Er spuckt Feuer.',
 'flow_purchase':'Gekauft und ausgerüstet.',
 'flow_need_stars':'Dafür fehlen noch Sterne. Spiele eine Mission.',
 'flow_next':'Geschafft! Weiter geht es mit der nächsten Mission.',
 'flow_loot':'Der Schatz ist freiwillig. Folge den goldenen Spuren. Danach kannst du weitergehen.',
 'bonus_prism':'Dein Schuss trifft erst die Wand und dann den goldenen Kristall.',
 'bonus_sequence':'Bonus. Merke dir die Lichter. Triff die Kristalle in dieser Reihenfolge.',
 'bonus_wait':'Der Kristall muss grün leuchten. Dann kannst du schießen.',
 'flow_exit':'Alle Gegner sind weg. Gehe jetzt zum Ausgang.',
 'flow_treasure':'Hier ist noch ein Schatz. Er ist freiwillig. Suche bei den goldenen Spuren.',
 'flow_no_treasure':'Schatz gefunden. Du kannst die nächste Mission starten.',
 'flow_final':'Diese Mission ist geschafft. Du kannst noch offene Bonusziele sammeln.',
 'defold_sanctuary_intro':'Im leuchtenden Schutzort bist du sicher. Keine Schüsse treffen dich. Deine Energie erholt sich schnell.',
 'defold_shop_tiers':'Sterne kaufen stärkere Waffen und Rüstung. Die dunkle Karte zeigt die nächste Stufe und ihren Preis.',
 'defold_health_refill':'Hier kannst du deine Energie mit Sternen auffüllen. Sie erholt sich auch von selbst.',
 'defold_treasure_hint':'Folge dem goldenen Schatzzeichen. Wenn du näher kommst, leuchtet die Truhe. Geh zu ihr.',
 'defold_zoom_help':'Mit Plus siehst du alles größer. Mit Minus siehst du mehr vom Feld. Mit zwei Fingern kannst du auch zoomen.',
 'defold_power_up':'Bonus geschafft. Du bist jetzt größer und stärker. Deine neue Kraft bleibt gespeichert.',
 'defold_power_help':'Löse die Bonusaufgaben. So wachsen deine Gesundheit, dein Schild und deine Feuerkraft. Deine neue Kraft bleibt gespeichert.',
 'defold_drone_open':'Wähle eine Drohne aus deinem Vorrat.',
 'defold_drone_target':'Wähle jetzt das Ziel. Du kannst auf einen Gegner tippen oder die Drohne zu ihm ziehen.',
 'defold_drone_launch':'Die Drohne fliegt jetzt zu deinem Ziel.',
 'defold_drone_empty':'Keine Drohnen mehr. Nutze deine Waffe oder eine Falle.',
 'defold_campaign_mission':'Verlasse den Schutzort. Schalte die Gegner aus und nutze die Deckung.',
 'defold_campaign_swarm':'Kleine Drohnen voraus. Einige können sich teilen.',
 'defold_campaign_sequence':'Schalte die Gegner aus. Merke dir die Lichter und triff sie in der richtigen Reihenfolge.',
 'defold_campaign_clear':'Alle Gegner ausgeschaltet. Weiter zur nächsten Mission.',
 'defold_relays_free':'Erst die Schalter, dann der Kern. Du kannst direkt treffen oder die Wand nutzen.',
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
