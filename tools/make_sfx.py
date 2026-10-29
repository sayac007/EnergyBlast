"""Tiny original synthesized combat tones; no sampled commercial recordings."""
from pathlib import Path
import wave,math,struct
folder=Path(__file__).resolve().parents[1]/'shared/audio/sfx';folder.mkdir(exist_ok=True)
for name,hz,seconds in [('fire',740,.07),('hit',130,.15),('bounce',1000,.035),('dash',400,.08)]:
 with wave.open(str(folder/(name+'.wav')),'wb')as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(22050);n=round(seconds*22050)
  w.writeframes(b''.join(struct.pack('<h',round(math.sin(math.tau*hz*i/22050)*3500*(1-i/n)))for i in range(n)))
