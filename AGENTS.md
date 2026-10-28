# EnergyBlast repository instructions

- This is the independent public EnergyBlast project. Never modify or write to
  `sayac007/Kinderwelt` or another repository as part of this work.
- The operator's latest instruction overrides references to Kinderwelt in the
  original work order. Do not create pull/merge requests yet. Do not merge or
  publish a release automatically.
- Read README.md, docs/pilot-brief.md and docs/touch-pilot.md before implementation.
  Also read docs/PROJECT_BRIEF.md and docs/MILESTONE_01.md for the consolidated
  brief and frozen first comparison. Latest controls are tap-to-move and
  drag/release to aim/fire, plus FIRE hold and DASH; no joystick.
  Keep engine attempts small and comparable; use the same original arena/assets
  and an engine-neutral mission specification. Do not prebuild a general framework.
- Do not include family photos/artwork, private signing keys, passwords, tokens
  or proprietary reference-game assets in this public repository. The operator
  authorizes only matching finished public audio clips from Kinderwelt, read-only,
  with hashes/notices; no private audio/image pack or unrelated asset copying.
- Document actual execution/tests and blocked or manual checks separately. A
  project file, import or attractive screenshot is not a successful Android test.
- Use friendly robots and non-graphic effects. Keep rapid retries and respectful
  feedback. Reward suitable decisions, not maximum waiting. Do not infer general
  everyday impulse-control improvements from performance on these missions.

## Current shooter milestone (operator update, 27 October 2026)

- The operator explicitly selected **Godot, GDevelop and Defold**. All three need
  playable Android comparison builds. Unity is an archived unexecuted import kit;
  BRUTAL was assessed but not selected after its desktop/framework limitations.
- Build an actual touch shooter with indirect learning through play: hostile
  cannons, visible projectiles, energy/damage, cover, dash and reflected attacks.
  No compulsory answer/prediction mode and no classroom/retry coaching phrases.
- Current shared rules are `shared/combat.json`; `shared/pilot.json` describes the
  archived 0.1 regression. Do not confuse an old successful test/build with 0.2.
- Native Defold builds require Bob 1.14.0 / Java 25. Check build success before
  running the engine so a failed compile can never reuse a stale binary.
- Keep the new branch isolated, no PR, no automatic merge or release publication.

## Documentation publication (operator request, 28 October 2026)

- Publish the current milestone and original brief clearly on GitHub. The `main`
  README is the repository landing page and may link to the isolated implementation
  branch. Updating that documentation does not authorize merging the game branch.
- Preserve source commit `1006cde8595b4249d0375ddf8bc4ea60fd2a93c9` and APK snapshot
  `defd791bd94809045cf5a8ed9429ead92c8bd959` as the first shooter comparison.
- Distinguish the 27 October game/build test results from later documentation/link
  checks. Do not invent fresh game tests for a documentation-only update.

## Binding documentation standard (operator decision, 28 October 2026)

- Apply docs/DOCUMENTATION_STANDARD.md to future work. The operator explicitly
  requested the published milestone/readme quality as the standard.
- Maintain a useful README, traceable brief, honest test/limit reporting and
  immutable milestone/download provenance for substantial results.
- Scale documentation and verification to the change. No new milestone or full
  game-test rerun is required for every minor documentation correction.

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
