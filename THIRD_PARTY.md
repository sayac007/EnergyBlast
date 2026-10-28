# Assets and component notices

The robot, arena geometry, icons/feedback drawings and mission scripts are original
EnergyBlast work. `tools/make_models.py` produces both shared robot exports;
`shared/asset-origins.json` records their hashes. There are no Battlelands assets,
family pictures, character downloads or proprietary game recordings in the pilot.
Procedural animations move named parts of that original model.

The operator explicitly allowed **four matching public Kinderwelt speech clips**.
Their original file/manifest hashes, exact texts and the additional **15 newly
synthesized full German sentences** are in `shared/audio/de/manifest.json`.
New audio uses the same locally available synthetic **Serena** speaker from the
pinned Qwen3-TTS model. No celebrity recording, imitation or family voice is used.
The model is a build-time tool; the APKs contain only Ogg recordings. Preserve
`shared/audio/de/LICENSE.txt` and `MODEL_CARD.txt`. The publisher does not separately
specify the training-dataset licence; model licensing is not proof about every
training item. Human listening approval for these new sentences remains open.

Runtime/build component notices are preserved in `shared/notices/`:

| Component | Version/source used | Licence |
|---|---|---|
| Godot | 4.7.2 official, `ed1daf0bf` | MIT; bundled dependency notices exported by the actual engine |
| GDevelop GDJS | 5.6.269 from pinned `gdcore-tools` package | MIT, Florian Rival |
| PixiJS | 7.4.2, runtime header | MIT |
| Three.js + addons | r160, runtime header | MIT |
| Draco decoder | bundled GDevelop runtime | Apache-2.0; retained decoder header and Google licence |
| RBush | GDevelop runtime; historical 1.4.3 package notice retained | MIT, Vladimir Agafonkin |
| Howler | 2.2.3 with GDevelop patch, runtime header retained | MIT |
| Font Face Observer | 2.0.13, runtime header | BSD-3-Clause |
| gdcore-tools / gdexporter | exact npm versions in `tools/gdevelop-tools/package-lock.json` | MIT, Arthur Pacaud; build-time tools |

`jshashtable.js` in this runtime is GDevelop's own TypeScript map container
(source map: `GDJS/Runtime/libs/jshashtable.ts`), covered by the GDJS notice.
It is not the older external Tim Down implementation with the same filename.
GDevelop's name/logo are its owner's marks; the splash is disabled, with upstream
notices retained. Godot and GDevelop packages include the relevant notice text.
Unity is not distributed by this repository; using its Editor/Android modules
requires the operator's applicable Unity licence. Blender is a build-time tool,
not bundled into the games.

Public visibility is not a licence grant for the new project's own code/assets.
The operator has not selected that licence. Third-party notices and permissions
remain applicable independently. This inventory documents the components used;
it does not certify an unrestricted commercial release.

## Shooter 0.2 update

The current three-engine selection is **Godot / GDevelop / Defold**, explicitly
confirmed by the operator. BRUTAL is a reviewed candidate, not a bundled component.
Its README, `Brutal.Core/Platform.cs`, sample requirements and NuGet metadata
(net10.0; documented desktop platforms) were inspected. A few Android Vulkan types
do not provide a game renderer, touch stack or a complete Android export path.
Unity remains an archived, unexecuted input kit.

All models under `shared/assets/shooter/` are original Blender-generated geometry
from `tools/make_shooter_models.py`. No reference-game or internet character image
is used. `shared/asset-origins.json` records hashes. Seven new full tactical speech
sentences were added using the same synthetic speaker, bringing the manifest to
26 recordings. The combat tone WAVs are original mathematical synthesis from
`tools/make_sfx.py`; Godot/browser equivalents use the same simple tone approach.

The additional **Lilita One** font is unchanged from
https://github.com/google/fonts/tree/main/ofl/lilitaone and redistributed with
`shared/fonts/OFL.txt` (SIL OFL 1.1). It is not a Kinderwelt asset copy.

Defold **1.14.0**, engine revision `d295ed4`, uses the **Defold License 1.0**,
an Apache-derived licence with an additional restriction on commercialising the
engine as a Game Engine Product; do not describe it as plain MIT or Apache-2.0.
Preserved: `shared/notices/DEFOLD.txt`, `DEFOLD_NOTICE`, the upstream compliance
instructions and `shared/notices/defold/` dependency notices from release 1.14.0.
These files are included in the native package's custom resources. Android's
modified manifest prominently notes the offline/backup modifications. The Bob SDK
and its JDK are external build-time tools, not shipped inside these APKs.

Upstream notices may cover optional/editor/platform components as well; retaining
them does not assert every listed library executes on Android. The actual debug
APKs request no network permissions. Development-only runtime/profiler facilities
are not a Google Play production hardening claim.

## Aurora Raid 0.3 update

The operator shortlisted **Defold and GDevelop**; Godot remains at 0.2. New art in
`shared/assets/raid/` comes solely from `tools/make_raid_models.py`, an original
Blender geometry generator extending our own 0.2 kit. It adds the revised robot,
relay, rotating radar dish and three arena variants. Hashes and dimensions are
recorded in `shared/asset-origins.json`; there is no new downloaded game artwork.
Three complete German cues in `shared/audio/raid/manifest.json` use the same
pinned model/synthetic speaker and existing notices as above. Human listening
review remains open. No new runtime dependency or licence grant is implied.

## Defold 0.4 update

Defold is the current development focus; the other two app versions remain frozen.
`shared/assets/defold04` is original Blender geometry from
`tools/make_defold04_models.py`, extending our own kit: larger arenas, floor details
and angular energy fragments. `main/bright.fp` provides original lifted lighting
through Defold's standard model-shader interface. Hashes remain in the central
asset-origin manifest. No downloaded game graphics or animations.

**Aurora Hop** is an original deterministic 32-bar composition, mathematically
synthesized at 128 BPM by `tools/make_defold_music.py`, along with an energy-burst
sound. No external recording, sample or reference melody is used. Source/metrics/
hashes: `shared/audio/defold04/music.json`. One new complete synthetic control cue
uses the existing pinned model/Serena speaker and existing model notices; its
manifest is `shared/audio/defold04/manifest.json`. No new runtime dependency.

## Defold 0.5 — Toybox Raid

Brawl Stars is a visual reference only. No game art, character, soundtrack,
recording or melody was downloaded/copied from it. The dragon, fennec, wings,
portraits and revised arenas are original Blender geometry/renders in the same
`tools/make_defold04_models.py` generator. Native depth-tested projectiles and
original toon lighting use the standard Defold renderer. Provenance and SHA-256
cover the full `shared/assets/defold04` directory, including portraits/surfaces.

Aurora Hop — Toybox Ensemble is a new arrangement of our own composition, with
nine mathematically synthesized instruments, stereo ambience and four density/
dynamic sections. No external song, sample, performance or reference melody.
The updated music manifest records hashes/metrics. Four new complete mission/
secret cues use the existing pinned Qwen model and synthetic Serena speaker;
five Defold cues total. Existing model/font/engine notices remain applicable.
No new runtime dependency or project licence grant.

## Defold 0.6 — Prism Frontier

Research sources and observation limits are in `docs/ART_DIRECTION.md`. Official
Brawl Stars screenshots were viewed as references only; none is included in this
repository or APK. No reference-game model/texture/animation is downloaded for reuse.
Detailed new geometry, rigid-part joints, portraits, AO bakes and static batches
come from `tools/make_defold06_models.py`. UI graphics are original layered vector
and gradient drawings in `tools/make_defold_ui.py`. Two original ground material
images were generated with OpenAI image_gen in this session without input reference
images; `shared/assets/defold06/TEXTURE_PROVENANCE.json` records hashes/origin.
These are actual native game textures, not conceptual screenshots. Existing
engine/font/model/audio notices and project licence status remain unchanged.

## Defold 0.7 — Neon Frontier

Original AI-generated character walk sheets, three robot enemy state sheets,
equipment icons, mission illustrations, props, energy-burst frames, deck material
and orbital lobby live in `shared/assets/defold07`. `PROVENANCE.json` retains the
ten unmodified source images and SHA-256; `tools/import_defold07_art.py` performs
technical cropping/resampling and generates native camera-facing quad meshes.
These are runtime assets, not screenshots substituted for gameplay. No reference
game image, character model, video frame or animation is included. Brawl Stars
and the supplied Instagram cover were inspected only as references in temporary
storage. World geometry remains our own Blender generator, now a futuristic kit.

The Defold speech manifest now contains twelve complete synthetic Serena cues,
including the actual on-field trap gestures and differentiated trap effects.
Existing model/font/engine notices and licence status above remain applicable.
AI provenance alone does not establish every possible intellectual-property
clearance or imply a new licence grant.
