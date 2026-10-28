"""Refresh hashes only for our versioned 0.6 generated art, preserving older evidence."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];p=R/'shared/asset-origins.json';d=json.loads(p.read_text());prefix='shared/assets/defold06/'
d['assets']=[row for row in d['assets']if not row['path'].startswith(prefix)]
for f in sorted((R/prefix).iterdir()):
 if not f.is_file():continue
 origin='Original detailed Blender 4.3.2 geometry, rigid-part rigs and AO bake from tools/make_defold06_models.py'
 if f.name.startswith(('ui_','button_'))or f.name=='panel.png':origin='Original layered UI/vector drawing from tools/make_defold_ui.py'
 elif f.name.startswith('ground-')or f.name=='TEXTURE_PROVENANCE.json':origin='Original OpenAI image-generation outputs 2026-10-28; flat ground materials; no reference-game image input; TEXTURE_PROVENANCE.json'
 d['assets'].append({'path':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'origin':origin})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
