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
