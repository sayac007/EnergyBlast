"""Independent offline transcription screen; never a human-listening certificate."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
import numpy as np,sherpa_onnx
root=Path(__file__).resolve().parents[1]/'shared/audio/de';m=json.loads((root/'manifest.json').read_text())
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(a.model/'small-encoder.int8.onnx'),decoder=str(a.model/'small-decoder.int8.onnx'),tokens=str(a.model/'small-tokens.txt'),language='de',num_threads=2)
rows=[]
for c in m['clips']:
 f=root/c['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==c['sha256']
 pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(f),'-ar','16000','-ac','1','-f','f32le','-']),np.float32)
 stream=r.create_stream();stream.accept_waveform(16000,pcm);r.decode_stream(stream)
 actual=stream.result.text.strip();normalize=lambda s:re.sub(r'[^\w]','',s.casefold()).replace('ß','ss')
 rows.append({'id':c['id'],'reference':c['text'],'recognized':actual,'normalized_exact':normalize(c['text'])==normalize(actual),'seconds':len(pcm)/16000})
 a.output.write_text(json.dumps({'scope':'Independent Whisper-small screen; no reference text prompts, no human intelligibility or heard stress certification','rows':rows},ensure_ascii=False,indent=2)+'\n')
 print(c['id'],repr(actual),flush=True)
print('EXACT',sum(x['normalized_exact'] for x in rows),'/',len(rows),flush=True)
