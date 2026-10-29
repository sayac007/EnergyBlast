"""Original cinematic science-fiction score; deterministic synthesis, no samples.

The historical aurora-hop.ogg filename remains stable for installed resource paths.
The score itself is entirely new: slower pulse, minor/modal harmony, breathing
pads and a restrained tactical motif instead of a platform-game lead/arpeggio.
"""
from pathlib import Path
import json, hashlib, subprocess, tempfile
import numpy as np

R = Path(__file__).resolve().parents[1]
OUT = R / 'shared/audio/defold04'
OUT.mkdir(exist_ok=True)
RATE = 32000
BPM = 96
BEAT = 60 / BPM
BARS = 32
SECONDS = BARS * 4 * BEAT
rng = np.random.default_rng(1010)
mix = np.zeros((round(SECONDS * RATE), 2), np.float64)


def add(start, samples, amp=1, pan=.5):
    """Wrap release/reverb tails around the loop; do not truncate the last bar."""
    sound = np.asarray(samples, dtype=np.float64) * amp
    stereo = sound[:, None] * np.array([np.sqrt(1 - pan), np.sqrt(pan)])[None, :]
    start = round(start * RATE) % len(mix)
    end = start + len(stereo)
    if end <= len(mix):
        mix[start:end] += stereo
    else:
        size = len(mix) - start
        mix[start:] += stereo[:size]
        mix[:len(stereo) - size] += stereo[size:]


def note(start, duration, midi, amp, pan, kind='pad'):
    t = np.arange(round(duration * RATE)) / RATE
    f = 440 * 2 ** ((midi - 69) / 12)
    phase = 2 * np.pi * f * t
    if kind == 'pad':
        # Gentle detuning, no sawtooth buzz or shrill fairy bells.
        wave = (np.sin(phase) + .32 * np.sin(phase * 1.0021 + .3)
                + .16 * np.sin(2 * phase) + .07 * np.sin(3 * phase)) * .66
        env = np.minimum(1, t / .55) * np.minimum(1, (duration - t) / .85)
        env *= .91 + .09 * np.sin(2 * np.pi * .19 * t)
    elif kind == 'bass':
        wave = np.sin(phase) + .12 * np.sin(2 * phase) + .06 * np.sin(3 * phase)
        env = np.minimum(1, t / .025) * np.minimum(1, (duration - t) / .25)
        env *= np.exp(-.45 * t)
    elif kind == 'signal':
        wave = (np.sin(phase + .10 * np.sin(phase * .5))
                + .13 * np.sin(2 * phase) + .06 * np.sin(3 * phase)) * .82
        env = np.minimum(1, t / .06) * np.minimum(1, (duration - t) / .4)
        env *= np.exp(-.6 * t)
    elif kind == 'brass':
        wave = (np.sin(phase) + .24 * np.sin(2 * phase)
                + .10 * np.sin(3 * phase)) * .7
        env = np.minimum(1, t / .3) * np.minimum(1, (duration - t) / .5)
        env *= .88 + .12 * np.sin(2 * np.pi * 4 * t)
    else:
        raise ValueError(kind)
    add(start, wave * env, amp, pan)


def percussion(start, kind, amp, pan=.5):
    duration = {'pulse': .29, 'tom': .38, 'tick': .09, 'air': 1.1}[kind]
    t = np.arange(round(duration * RATE)) / RATE
    if kind == 'pulse':
        # Soft, deep electronic pulse rather than a marching/platform beat.
        wave = np.sin(2 * np.pi * (53 * t + 2.5 * (1 - np.exp(-18 * t))))
        wave *= np.exp(-15 * t) * np.minimum(1, t / .008)
    elif kind == 'tom':
        wave = (np.sin(2 * np.pi * (110 * t - 24 * t * t))
                + .16 * rng.uniform(-1, 1, len(t)))
        wave *= np.exp(-10 * t) * np.minimum(1, t / .008)
    elif kind == 'tick':
        noise = rng.uniform(-1, 1, len(t))
        # Band-limited/softened noise; no continuous high-hat machine-gun sound.
        wave = (noise + np.roll(noise, 1) + np.roll(noise, 2)) / 3
        wave *= np.exp(-70 * t) * np.minimum(1, t / .004)
    else:
        noise = rng.uniform(-1, 1, len(t))
        kernel = np.ones(18) / 18
        wave = np.convolve(noise, kernel, mode='same')
        wave *= np.sin(np.pi * t / duration) ** 2
    add(start, wave, amp, pan)


# D minor/modal palette: suspended/darker tensions resolve gently, not horror.
# One harmony per two bars, with 9ths/7ths carried in long pads.
harmonies = [
    (38, [0, 7, 14, 15]),       # Dm(add9)
    (34, [0, 7, 12, 16]),       # Bbmaj7 colour
    (43, [0, 7, 10, 14]),       # Gm9 colour
    (33, [0, 7, 10, 17]),       # A suspended / minor seventh
    (38, [0, 7, 14, 15]),
    (41, [0, 7, 12, 16]),       # Fmaj7
    (36, [0, 7, 12, 14]),       # C suspended
    (33, [0, 7, 10, 16]),       # dominant with a restrained major third
]
sections = [.64, .92, .42, 1.0]
# Sparse 4-bar call/response; never a stream of bright eighth notes.
motifs = [
    [(0, 62, 1.65), (2.5, 69, 1.2)],
    [(1, 65, 2.4)],
    [(0.5, 64, 1.5), (3, 62, 1.3)],
    [(1.5, 57, 2.5)],
]
for bar in range(BARS):
    section = bar // 8
    dyn = sections[section]
    base = bar * 4 * BEAT
    root, intervals = harmonies[(bar // 2) % len(harmonies)]
    if bar % 2 == 0:
        for j, interval in enumerate(intervals):
            note(base, 8.7 * BEAT, root + 12 + interval,
                 .085 * dyn, .15 + j * .23, 'pad')
        # Low octave bed is continuous enough to give the arena weight.
        note(base, 7.9 * BEAT, root - 12, .075 * dyn, .5, 'pad')
    note(base, 1.85 * BEAT, root, .21 * dyn, .48, 'bass')
    if section != 2 or bar % 2 == 0:
        note(base + 2.5 * BEAT, 1.15 * BEAT,
             root + (7 if bar % 4 == 3 else 0), .13 * dyn, .52, 'bass')
    percussion(base, 'pulse', .13 * dyn)
    if section in (1, 3):
        percussion(base + 2.5 * BEAT, 'pulse', .075 * dyn)
        if bar % 2:
            percussion(base + 3.25 * BEAT, 'tom', .065 * dyn, .65)
    for beat, pan in [(1.5, .25), (3, .74)]:
        if section != 2 or beat == 3:
            percussion(base + beat * BEAT, 'tick', .052 * dyn, pan)
    if bar % 4 == 3:
        percussion(base + 3 * BEAT, 'air', .06 * dyn, .7)
    # The middle eight bars are a recovery/sanctuary-like release.
    if section == 2:
        if bar % 2 == 0:
            note(base + BEAT, 3.6 * BEAT, root + 24 + 7, .065, .58, 'signal')
    else:
        for beat, pitch, length in motifs[bar % 4]:
            note(base + beat * BEAT, length * BEAT,
                 pitch + (0 if section != 3 else 0), .105 * dyn, .36, 'signal')
    if section == 3 and bar % 2 == 0:
        note(base + .5 * BEAT, 4.5 * BEAT, root + 12, .07, .68, 'brass')
        note(base + BEAT, 3.8 * BEAT, root + 19, .045, .24, 'brass')

# Circular stereo room response from our own synthesized score. Wrapped tails
# preserve atmosphere at the end/start boundary without an audible silence gap.
dry = mix.copy()
for delay, gain in [(round(RATE * .1875), .11), (round(RATE * .4375), .08),
                    (round(RATE * .8125), .055), (round(RATE * 1.1875), .035)]:
    mix += np.roll(dry[:, ::-1], delay, axis=0) * gain
mix *= .60 / max(abs(mix).max(), .001)


def encode(name, pcm, rate):
    with tempfile.TemporaryDirectory(prefix='energyblast-synth-', dir='/tmp') as folder:
        raw = Path(folder) / 'pcm.f32'
        raw.write_bytes(np.asarray(pcm, dtype='<f4').tobytes())
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'f32le',
                        '-ar', str(rate), '-ac', str(pcm.shape[1]), '-i', str(raw),
                        '-c:a', 'libvorbis', '-q:a', '3', str(OUT / name)], check=True)


encode('aurora-hop.ogg', mix, RATE)
# Preserve the established explosion SFX exactly. Only recover it when absent;
# its independent seed and formula do not depend on the score's random stream.
if not (OUT / 'energy-burst.ogg').exists():
    burst_rng = np.random.default_rng(404)
    # The archived 0.5 score consumed 224 hat + 32 snare noise windows before
    # this SFX. Skip those windows to retain that exact standalone recording.
    burst_rng.uniform(-1, 1, (224 + 32) * round(.11 * RATE))
    t = np.arange(round(.65 * RATE)) / RATE
    burst = (burst_rng.uniform(-1, 1, len(t)) * .45
             + np.sin(2 * np.pi * (420 * t - 220 * t * t)) * .4)
    burst *= np.exp(-9 * t) * np.minimum(1, t / .008)
    encode('energy-burst.ogg', burst[:, None], RATE)
rows = []
for filename in ['aurora-hop.ogg', 'energy-burst.ogg']:
    path = OUT / filename
    pcm = np.frombuffer(subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-i', str(path), '-ar', str(RATE),
        '-ac', '2', '-f', 'f32le', '-']), dtype='<f4').reshape(-1, 2)
    row = {'file': filename, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
           'seconds': len(pcm) / RATE, 'peak': float(abs(pcm).max()),
           'rms': float(np.sqrt(np.mean(pcm ** 2)))}
    if filename == 'aurora-hop.ogg':
        row['loop_boundary_delta'] = float(abs(pcm[0] - pcm[-1]).max())
        row['stereo_difference_rms'] = float(np.sqrt(np.mean((pcm[:, 0] - pcm[:, 1]) ** 2)))
        row['section_rms'] = [float(np.sqrt(np.mean(chunk ** 2)))
                              for chunk in np.array_split(pcm, 4)]
    rows.append(row)
manifest = {
    'schema': 2,
    'origin': 'Original deterministic composition and mathematical synthesis by tools/make_defold_music.py; no sampled or transcribed reference melody',
    'title': 'Zikurrat — Signal in the Dark',
    'runtime_filename_note': 'aurora-hop.ogg is retained solely as a stable resource path; the platform score has been replaced',
    'character': 'Restrained cinematic science fiction: tension, space, recovery; no cheerful platform arpeggio',
    'key': 'D minor / modal suspended harmony',
    'instruments': ['warm detuned pad', 'sub drone', 'deep synth bass',
                    'sparse tactical signal', 'soft brass swells', 'electronic pulse',
                    'low tom', 'filtered tick', 'air texture'],
    'section_dynamics': sections,
    'sections': ['quiet approach', 'threat / engagement', 'breathing / recovery',
                 'resolve / confrontation'],
    'bpm': BPM, 'bars': BARS, 'music_gain': .28, 'voice_duck_gain': .065,
    'model_or_external_recording': None, 'files': rows,
}
(OUT / 'music.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
