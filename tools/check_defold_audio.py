"""Record the actual native Defold/OpenAL output through its WAVE backend."""
from pathlib import Path
import argparse,os,subprocess,tempfile,struct,math
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));a=p.parse_args()
levels={}
with tempfile.TemporaryDirectory(prefix='energyblast-audio-',dir='/tmp')as folder:
 root=Path(folder)
 for mode in ['on','off','mix']:
  state=root/mode;state.mkdir()
  for name in ['data','cache','config']:(state/name).mkdir()
  wave=state/'native-mix.wav';conf=state/'alsoft.conf';conf.write_text('[wave]\nfile = '+str(wave)+'\n')
  env=dict(os.environ,ALSOFT_DRIVERS='wave',ALSOFT_CONF=str(conf),XDG_DATA_HOME=str(state/'data'),XDG_CACHE_HOME=str(state/'cache'),XDG_CONFIG_HOME=str(state/'config'))
  proc=subprocess.run([str(a.engine),'--config=project.capture_music='+mode,str(R/'pilots/defold/build/default/game.projectc')],env=env,capture_output=True,text=True,timeout=15)
  log=proc.stdout+proc.stderr;assert proc.returncode==0 and 'ERROR:'not in log,log
  assert wave.is_file()and wave.stat().st_size>32000,log
  raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(wave),'-ac','2','-ar','22050','-f','f32le','-'])
  samples=struct.unpack('<'+'f'*(len(raw)//4),raw);assert len(samples)>22050
  peak=max(abs(x)for x in samples) # Include the initial explosion/voice transient.
  settled=samples[22050:];assert settled
  rms=math.sqrt(sum(x*x for x in settled)/len(settled));levels[mode]=rms
  assert peak<.99
 assert levels['on']>.01,levels
 assert levels['off']<.0001,levels
 assert levels['mix']>levels['on'],levels
 print('DEFOLD ACTUAL MUSIC OUTPUT / MUTE PASS; RMS on=%.5f off=%.5f mix=%.5f'%(levels['on'],levels['off'],levels['mix']))
