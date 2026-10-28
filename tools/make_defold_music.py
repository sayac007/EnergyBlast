"""Compose and synthesize original bouncy platform-game chiptune; no sampled songs."""
from pathlib import Path
import json,hashlib,subprocess,tempfile
import numpy as np
R=Path(__file__).resolve().parents[1];OUT=R/'shared/audio/defold04';OUT.mkdir(exist_ok=True)
RATE=32000;BPM=128;BEAT=60/BPM;BARS=32;SECONDS=BARS*4*BEAT
rng=np.random.default_rng(404);mix=np.zeros((round(SECONDS*RATE),2),np.float64)
def note(start,duration,midi,amp,pan,kind='lead'):
 n=round(duration*RATE);t=np.arange(n)/RATE;f=440*2**((midi-69)/12)
 if kind=='lead':wave=np.sin(2*np.pi*f*t)+.25*np.sin(6*np.pi*f*t)+.1*np.sin(10*np.pi*f*t)
 else:wave=np.sin(2*np.pi*f*t)+.15*np.sin(4*np.pi*f*t)
 envelope=np.minimum(1,t/.008)*np.minimum(1,(duration-t)/.018)
 sound=wave*envelope*amp;i=round(start*RATE);size=min(n,len(mix)-i)
 if size>0:mix[i:i+size]+=sound[:size,None]*np.array([1-pan,pan])[None,:]
# Newly authored score: two related eight-bar phrases, varied on each repeat.
chords=[(48,[0,4,7]),(45,[0,3,7]),(53,[0,4,7]),(55,[0,4,7]),(52,[0,3,7]),(53,[0,4,7]),(50,[0,3,7]),(55,[0,4,7])]
phrases=[[0,2,4,7,9,7,4,2],[4,7,11,9,7,4,2,0],[7,9,12,11,9,7,4,7],[4,2,0,4,7,4,2,7]]
for bar in range(BARS):
 root,intervals=chords[bar%8];base=bar*4*BEAT
 for beat in range(4):
  note(base+beat*BEAT,.72*BEAT,root+(12 if beat%2 else 0),.21,.48,'bass')
  note(base+(beat+.5)*BEAT,.23*BEAT,root+24+intervals[(beat+bar)%3],.10,.72,'arp')
 pattern=phrases[(bar//2+bar//8)%len(phrases)]
 for i,offset in enumerate(pattern):
  if (bar+i)%7==0:continue
  note(base+i*.5*BEAT,.40*BEAT,60+offset+(0 if bar%8<4 else 5),.19,.35)
 # Soft synthesized percussion, no external samples.
 for beat in [0,2]:
  dur=.12;t=np.arange(round(dur*RATE))/RATE;kick=np.sin(2*np.pi*(90*t-160*t*t))*np.exp(-30*t)*.13;i=round((base+beat*BEAT)*RATE);mix[i:i+len(t)]+=kick[:,None]
 for beat in np.arange(.5,4,.5):
  t=np.arange(round(.035*RATE))/RATE;hat=rng.uniform(-1,1,len(t))*np.exp(-120*t)*.022;i=round((base+beat*BEAT)*RATE);mix[i:i+len(t)]+=hat[:,None]
mix*=.72/max(abs(mix).max(),.001)
def encode(name,pcm,rate):
 with tempfile.TemporaryDirectory(prefix='energyblast-synth-',dir='/tmp')as folder:
  raw=Path(folder)/'pcm.f32';raw.write_bytes(np.asarray(pcm,dtype='<f4').tobytes())
  subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','f32le','-ar',str(rate),'-ac',str(pcm.shape[1]),'-i',str(raw),'-c:a','libvorbis','-q:a','3',str(OUT/name)],check=True)
encode('aurora-hop.ogg',mix,RATE)
t=np.arange(round(.65*RATE))/RATE
burst=(rng.uniform(-1,1,len(t))*.45+np.sin(2*np.pi*(420*t-220*t*t))*.4)*np.exp(-9*t)*np.minimum(1,t/.008)
encode('energy-burst.ogg',burst[:,None],RATE)
rows=[]
for file in ['aurora-hop.ogg','energy-burst.ogg']:
 p=OUT/file;pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(p),'-ar',str(RATE),'-ac','2','-f','f32le','-']),dtype='<f4')
 rows.append({'file':file,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':len(pcm)/RATE/2,'peak':float(abs(pcm).max()),'rms':float(np.sqrt(np.mean(pcm**2)))})
manifest={'schema':1,'origin':'Original deterministic composition and mathematical synthesis by tools/make_defold_music.py; no sampled or transcribed reference melody','title':'Aurora Hop','bpm':BPM,'bars':BARS,'music_gain':.28,'voice_duck_gain':.065,'model_or_external_recording':None,'files':rows}
(OUT/'music.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
