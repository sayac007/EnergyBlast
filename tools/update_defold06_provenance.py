"""Refresh hashes for our active/retained original Defold art, preserving prior engines."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];p=R/'shared/asset-origins.json';d=json.loads(p.read_text());prefix='shared/assets/defold06/'
d['assets']=[row for row in d['assets']if not row['path'].startswith(prefix)]
d['assets']=[row for row in d['assets']if not row['path'].startswith(('shared/assets/defold07/','shared/assets/defold09/'))]
for f in sorted((R/prefix).iterdir()):
 if not f.is_file():continue
 origin='Original detailed Blender 4.3.2 geometry, rigid-part rigs and AO bake from tools/make_defold06_models.py'
 if f.name.startswith(('ui_','button_'))or f.name=='panel.png':origin='Original layered UI/vector drawing from tools/make_defold_ui.py'
 elif f.name.startswith('ground-')or f.name=='TEXTURE_PROVENANCE.json':origin='Original OpenAI image-generation outputs 2026-10-28; flat ground materials; no reference-game image input; TEXTURE_PROVENANCE.json'
 d['assets'].append({'path':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'origin':origin})
for f in sorted((R/'shared/assets/defold07').iterdir()):
 if not f.is_file():continue
 d['assets'].append({'path':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'origin':'Original OpenAI-generated EnergyBlast illustration/animation sheet, no reference-game asset input; technical import/quad geometry tools/import_defold07_art.py; PROVENANCE.json retains original-sheet hashes'})
for f in sorted((R/'shared/assets/defold09').iterdir()):
 if not f.is_file():continue
 d['assets'].append({'path':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'origin':'Original OpenAI-generated per-sector floor paintings 2026-10-29, no external game inputs; technical import/analytic effect geometry tools/import_defold09_art.py; PROVENANCE.json'})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
