# EnergyBlast repository instructions

- This is the independent public EnergyBlast project. Never modify or write to
  `sayac007/Kinderwelt` or another repository as part of this work.
- The operator's latest instruction overrides references to Kinderwelt in the
  original work order. Do not create pull/merge requests yet. Do not merge or
  publish a release automatically.
- Read README.md and docs/pilot-brief.md before implementing the first mission.
  Keep engine attempts small and comparable; use the same original arena/assets
  and an engine-neutral mission specification. Do not prebuild a general framework.
- Do not include family photos/artwork, private signing keys, passwords, tokens
  or proprietary reference-game assets in this public repository.
- Document actual execution/tests and blocked or manual checks separately. A
  project file, import or attractive screenshot is not a successful Android test.
- Use friendly robots and non-graphic effects. Keep rapid retries and respectful
  feedback. Reward suitable decisions, not maximum waiting. Do not infer general
  everyday impulse-control improvements from performance on these missions.

## Published milestone and current brief (28 October 2026)

- Read docs/PROJECT_BRIEF.md and docs/MILESTONE_01.md before planning new work.
  They consolidate the operator's later decisions; the original brief is historical.
- The selected comparison is Godot / GDevelop / Defold, with active cannon combat,
  tap-to-move, drag/release fire, FIRE hold and DASH. No joystick or compulsory quiz.
- `main` currently publishes the documentation/index. Current game implementation
  is on `feat/touch-shooter-v2`, source `1006cde`, APK snapshot `defd791`.
  Do not mistake the absence of game files on main for an unimplemented prototype.
- The operator authorized this README/brief/milestone publication on GitHub.
  No game branch merge, pull request or release publication is authorized by it.
- Matching finished public Kinderwelt audio was explicitly authorized read-only,
  with provenance/notices. Never copy private family assets or signing material.

## Binding documentation standard (operator decision, 28 October 2026)

- Follow docs/DOCUMENTATION_STANDARD.md for future work: useful README, traceable
  brief, honest test/limit reporting, stable milestone/download references.
- Keep scope proportional; minor changes need no new milestone or full game tests.

## Shortlist iteration (operator feedback, 28 October 2026)

- Continue **Defold and GDevelop** with a more complex, more attractive playable
  prototype. Godot stays at the frozen 0.2 comparison; do not update its app/assets.
- Remove computed player-shot trajectories. Show a reticle and actual projectiles,
  never the calculated reflected route. Enemy charge warnings remain local effects.
- Preserve the clear distinction between movement taps and shooting gestures;
  use visible target hit testing before projecting the floor behind a character.
- Current shortlist rules/assets: `shared/raid.json`, `shared/assets/raid`.
  Godot still consumes `shared/combat.json` and `shared/assets/shooter`.
- Current apps are 0.3.0/code 3; keep package IDs and the outside-repo development
  key stable for updates. No PR, merge, Release or Play publication is authorized.
- Native UI actions which create/delete game objects must send messages to the
  main script. Calling a captured Lua closure from a GUI script does not switch
  Defold's script context. Test real menu clicks as well as the pure combat loop.

## Defold focus and duration input (operator feedback, 28 October 2026)

- Continue **Defold**. GDevelop 0.3 and Godot 0.2 stay frozen as comparisons.
- A short field press ALWAYS moves, even on an enemy or reflector. Only elapsed
  press duration arms aim (0.30 s); holding anywhere aims, releasing fires once.
  Movement distance and target type must never decide between move and shoot.
  Preserve separate FIRE hold, DASH, cancellation and finger ownership.
- Current Defold rules/art: `shared/defold04.json`, `shared/assets/defold04`.
  Arenas are 21x15 with a following camera; rendering and unprojection share
  `main/view.lua`. Keep world overlays inside the play viewport, away from HUD.
- Add original synthetic upbeat platform-game music, not a copied song/melody.
  Test actual native audio output, mute, voice ducking and mix headroom. Avoid
  multiplying a baked music gain with the runtime gain a second time.
- Animate final-hit destruction, including during the short delay before the
  victory overlay. Expire fragments and clear them when switching sectors.
- Current Defold app is 0.4.0/code 4, same package and development certificate.
  No PR, merge, Release/store publication or writes to another repository.

## Wall reflections and finite energy (operator update, 28 October 2026)

- Defold 0.4.1/code 5: every solid wall type reflects both sides' shots; preserve
  the large scrolling world and timed touch controls. Closed gates reflect, open
  gates do not. Use live swept collisions, not a path frozen at firing time.
- Keep finite budgets: player 1 bounce / Prisma 2, enemy 1; player lifetime 3 s,
  enemy 6 s, plus range. Fade near expiration and dissipate visibly.
- Blue X neutralisation fields absorb either side's shots and remain walkable.
  These are explicit absorption areas; ordinary walls still reflect.

## Current Toybox Raid milestone (28 October 2026)

- Defold **0.5.0/code 6**, clean source `321d5cf`, APK snapshot `4315cf7`.
  Read docs/MILESTONE_04.md and the linked current quality/build documents.
- Six sectors: original three plus trap preparation, light sequence and escorted
  drone. Three original selectable characters, including dragon/fireballs.
- Use native depth-tested shots and matching visual/collision wall footprints.
  All interactive HUD stays outside the field; menus replace the paused scene.
  Real purchases spend wallet balance, never lifetime score. Migrate old gear.
- `main` remains documentation-only. GDevelop 0.3/Godot 0.2 stay frozen. No PR,
  game branch merge, Actions workflow, Release/store publication or other repo writes.

## Visual rejection and Prism Frontier 0.6 (28 October 2026)

- The operator explicitly rejected 0.5 graphics. Read docs/ART_DIRECTION.md and
  docs/MILESTONE_05.md; primary reference research and actual runtime visual review
  are required. Functional checks are not an aesthetic acceptance.
- Current clean source `19856c1`, APK snapshot `24b24dd`, Defold 0.6.0/code 7.
  Native textured arenas, AO-lit articulated original characters, animated 3D
  menu stage, fixed landscape and depth-tested light/trails. Six missions/saves stay.
- The implementation branch uses shared/assets/defold06, real source geometry
  and identical material-batched runtime geometry. Verify actual exported positions.
- Main remains documentation only. Other engines/repositories remain unchanged.
  No PR, game merge, Actions workflow or Release/store publication is authorized.
