"""Compose and synthesize original bouncy platform-game chiptune; no sampled songs."""
from pathlib import Path
import json,hashlib,subprocess,tempfile
import numpy as np
R=Path(__file__).resolve().parents[1];OUT=R/'shared/audio/defold04';OUT.mkdir(exist_ok=True)
RATE=32000;BPM=128;BEAT=60/BPM;BARS=32;SECONDS=BARS*4*BEAT
rng=np.random.default_rng(404);mix=np.zeros((round(SECONDS*RATE),2),np.float64)
def note(start,duration,midi,amp,pan,kind='lead'):
 n=round(duration*RATE);t=np.arange(n)/RATE;f=440*2**((midi-69)/12);phase=2*np.pi*f*t
 if kind=='strings':
  wave=(np.sin(phase)+.25*np.sin(2*phase)+.12*np.sin(3*phase)+.25*np.sin(phase*1.003))*.62
  env=np.minimum(1,t/.12)*np.minimum(1,(duration-t)/.15)
 elif kind=='bell':
  wave=(np.sin(phase)+.27*np.sin(phase*2.01)+.12*np.sin(phase*3.97))*np.exp(-3*t)
  env=np.minimum(1,t/.003)*np.minimum(1,(duration-t)/.07)
 elif kind=='pluck':
  wave=(np.sin(phase)+.4*np.sin(2*phase)+.16*np.sin(3*phase))*np.exp(-6*t)
  env=np.minimum(1,t/.005)*np.minimum(1,(duration-t)/.04)
 elif kind=='brass':
  wave=(np.sin(phase)+.3*np.sin(2*phase)+.18*np.sin(3*phase)+.08*np.sin(4*phase))*.7
  env=np.minimum(1,t/.03)*np.minimum(1,(duration-t)/.09)
 elif kind=='bass':
  wave=np.sin(phase)+.18*np.sin(3*phase)
  env=np.minimum(1,t/.012)*np.minimum(1,(duration-t)/.04)
 else:
  wave=(np.sin(phase+.018*np.sin(2*np.pi*5*t))+.22*np.sin(3*phase))*.85
  env=np.minimum(1,t/.009)*np.minimum(1,(duration-t)/.04)
 sound=wave*env*amp;i=round(start*RATE);size=min(n,len(mix)-i)
 if size>0:mix[i:i+size]+=sound[:size,None]*np.array([np.sqrt(1-pan),np.sqrt(pan)])[None,:]
# Entirely newly authored 32-bar score: opening, energetic reply, quiet bridge,
# fuller final chorus. Pitched parts are intentionally independent, not doubled.
chords=[(48,[0,4,7]),(45,[0,3,7]),(53,[0,4,7]),(55,[0,4,7]),(52,[0,3,7]),(53,[0,4,7]),(50,[0,3,7]),(55,[0,4,7])]
phrases=[[0,4,7,9,7,4,2,4],[7,9,11,7,4,2,0,2],[4,7,12,9,7,4,7,11],[9,7,4,2,0,2,4,7]]
sections=[.62,.9,.48,1.0]
def drum(start,kind,amp):
 duration=.16 if kind=='kick'else .11;t=np.arange(round(duration*RATE))/RATE
 if kind=='kick':wave=np.sin(2*np.pi*(80*t-120*t*t))*np.exp(-28*t)
 elif kind=='snare':wave=(rng.uniform(-1,1,len(t))*.6+np.sin(2*np.pi*180*t)*.4)*np.exp(-36*t)
 else:
  noise=rng.uniform(-1,1,len(t));wave=(noise-np.roll(noise,1))*.5*np.exp(-90*t)
 i=round(start*RATE);size=min(len(wave),len(mix)-i)
 if size>0:mix[i:i+size]+=wave[:size,None]*amp
for bar in range(BARS):
 root,intervals=chords[bar%8];base=bar*4*BEAT;section=bar//8;dyn=sections[section]
 for j,interval in enumerate(intervals):note(base,3.9*BEAT,root+12+interval,.065*dyn,.2+j*.27,'strings')
 for beat in range(4):
  note(base+beat*BEAT,.70*BEAT,root+(7 if beat==3 else 0),.19*dyn,.5,'bass')
  note(base+(beat+.5)*BEAT,.65*BEAT,root+24+intervals[(beat+bar)%3],.12*dyn,.77,'pluck')
  if section!=2:drum(base+beat*BEAT,'kick',.12*dyn if beat%2==0 else .055*dyn)
  if beat%2==1 and section in [1,3]:drum(base+beat*BEAT,'snare',.08*dyn)
 for beat in np.arange(.5,4,.5):drum(base+beat*BEAT,'hat',.02*dyn)
 pattern=phrases[(bar//2+section)%len(phrases)]
 for i,offset in enumerate(pattern):
  if (bar+i)%7==0 or(section==2 and i%2):continue
  note(base+i*.5*BEAT,.44*BEAT,60+offset+(5 if bar%8>=4 else 0),.20*dyn,.35,'bell'if section==2 else'lead')
 if section in [1,3]:
  for i in [0,2]:note(base+(i+.25)*BEAT,1.25*BEAT,root+24+intervals[(i+1)%3],.09*dyn,.67,'brass')
 if bar%4==3:
  for j in range(4):note(base+(2+j*.5)*BEAT,.45*BEAT,root+36+intervals[j%3],.08*dyn,.15+j*.20,'bell')
# Short cross-channel ambience from the synthesized parts, no external recordings.
for delay,gain in [(round(RATE*.143),.08),(round(RATE*.231),.05)]:mix[delay:]+=mix[:-delay,::-1]*gain
fade=round(.025*RATE);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-fade:]*=np.linspace(1,0,fade)[:,None]
mix*=.62/max(abs(mix).max(),.001)
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
manifest={'schema':1,'origin':'Original deterministic composition and mathematical synthesis by tools/make_defold_music.py; no sampled or transcribed reference melody','title':'Aurora Hop — Toybox Ensemble','instruments':['lead','plucked strings','string pad','bells','brass reply','bass','kick','snare','hi-hat'],'section_dynamics':sections,'bpm':BPM,'bars':BARS,'music_gain':.28,'voice_duck_gain':.065,'model_or_external_recording':None,'files':rows}
(OUT/'music.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
