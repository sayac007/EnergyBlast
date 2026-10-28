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
