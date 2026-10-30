# EnergyBlast repository instructions

## Latest operator request — repository integration, 29 October 2026

The operator explicitly requested integrating all completed work into the repository
and documenting the full history and current state in README. This authorizes the
0.10 integration from feat/touch-shooter-v2 into main with a real merge commit,
preserving both histories and the existing verified APK. The former documentation-
only main arrangement and earlier no-game-merge rule are superseded for this
requested integration. It does not authorize a Release/Play upload or unrelated
repository changes. Keep historical instructions below as a decision log.


- This is the independent public EnergyBlast project. Never modify or write to
  `sayac007/Kinderwelt` or another repository as part of this work.
- The operator's latest instruction overrides references to Kinderwelt in the
  original work order. Do not create pull/merge requests yet. Do not merge or
  publish a release automatically.
- Read README.md, docs/pilot-brief.md and docs/touch-pilot.md before implementation.
  Also read docs/PROJECT_BRIEF.md and docs/MILESTONE_01.md for the consolidated
  brief and frozen first comparison. Latest 0.9 controls are groundtap-to-move, groundhold-to-fire, own-actor drag
  to move and immediate padded enemy-press shooting; no joystick.
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

## Toybox Raid (operator playtest, 28 October 2026)

- Defold 0.5.0/code 6, six sectors, three selectable original characters. Brawl
  Stars is a visual direction, never an asset source. Preserve tap/hold controls.
- All shots must be native depth-tested models. Never restore GUI projectile
  circles. All solid arena meshes/caps must match collision footprints; verify
  actual exported POSITION buffers and the native occlusion image regression.
- Keep every interactive HUD element outside Layout.bottom..Layout.top. Menus
  replace the paused world entirely, rather than covering a playable scene.
- Free environmental treasure marks, optional earned clues. Real persistent
  purchases spend wallet balance, never lifetime score. One-time migration keeps
  pre-shop gear. New missions: magnetic trap, light sequence, escorted drone.
- Use MILESTONE_04.md, QUALITY.md and BUILD_AND_TEST.md for actual scope/results.
  Other engines stay frozen; no PR, merge, Actions or Release/store publication.

## Visual quality rejection and Prism Frontier 0.6 (operator update)

- The operator rejected the graphics of 0.5. Read docs/ART_DIRECTION.md and
  docs/MILESTONE_05.md. Research primary visuals and verify the actual runtime;
  passing functional tests is not an aesthetic acceptance.
- Active art is shared/assets/defold06, generated by make_defold06_models.py and
  make_defold_ui.py. Ground illustrations are original image-generation outputs.
  Source .gltf preserves semantic surfaces; .runtime.gltf batches identical static
  geometry by material. Verify exported positions, not just generator metadata.
- Actors use actual baked AO, rigid articulated parts and the same animated model
  on the menu stage. Projectiles/halos/trails must remain native and depth-tested.
- 0.6.0/code 7 is fixed landscape 1280x720, with the arena inside Layout's four
  boundaries and all HUD/control surfaces outside. Keep 0.30-second tap/hold input.
- Six missions, purchases, score and save migration stay. Other engines stay frozen.
  No PR, game merge, Actions or Release/store publication or other-repo writes.

## Neon Frontier 0.7 — latest operator instruction

- 0.6 graphics were rejected too. Use original illustrated directional animation
  on native depth-tested world quads, with actual futuristic 3D collision geometry;
  do not call these full skeletal 3D models. Active art adds shared/assets/defold07.
- Traps explicitly belong ON THE PLAYFIELD: badge near actor, catalogue, placement
  preview, floor tap, cancel. This overrides the old outside-HUD rule for these
  tactical controls only. Keep .30s hold-to-aim unchanged; no hidden hold shortcut.
- Catalogue/placement freezes combat and camera. Validate range, free floor and
  line of sight. Contextual speech replaces stale instructions immediately.
- 0.7.0/code8, same package/debug certificate/save location. Actual native render,
  input, occlusion, audio and Android artifact checks remain necessary.

## Clear mission flow 0.8 — operator playtest

- Preserve0.7art. Explicit next-mission flow, optional treasure and integrated
  in-arena bonuses; never block next on unfinished optional rewards. Persist the
  validated current mission. Solved missions resume as safe exploration.
- Main menu exposes all three illustrated heroes and explicit star spending;
  purchase controls say Kaufen and show wallet vs lifetime total.
- Active rules now define 300completion+100skill+75treasure+100/150two bonuses.
  Preserve the old0.7JSON under shared/defold07-regression.json for original tests.
- 0.8.0/code9, same package/certificate;64sound components for expanded speech.
  Test actual hero/shop/next/loot input in addition to the pure simulation.

## Current 0.9 operator instruction — 29 October 2026

- New direct gestures override historical release-to-fire requirements. A ground
  tap moves, ground hold fires after 0.14 s, enemy press fires without a hold
  threshold, and dragging the player moves. Release creates no additional shot.
- Keep old behavior only in touch_legacy.lua for historical fixtures. Actual UI
  tests must observe firing and movement BEFORE release, padded target selection,
  buffered presses, cancellation and pointer ownership.
- Active visuals add shared/assets/defold09 floors/effect quads, real baked AO and
  sculpted sector cover kits, depth-tested shields, floor shadows and an 8.8-unit
  camera. Surface heights come from actual exported geometry metadata.
- 0.9.0/code 10, same package/certificate. model.max_count=384 bounds the new effects
  and rapid fire. No PR, game merge, Actions, Release/Play or other-repository writes.

## Recovery and tiered equipment 0.10 — operator playtest

- Base health is now 15 (fivefold), armor tiers 20/25/30/35. Free recovery after
  four undamaged active seconds restores 0.5 HP/sec; sanctuary restores 2 HP/sec.
- Every mission has a reachable, labelled Zikurrat sanctuary. Swept collisions
  absorb both sides' projectiles at its boundary, including reflections and
  inside spawns. Do not permit firing outward from this invulnerable location.
- Shop keeps health refill visible/repeatable, charges only on actual healing,
  and offers sequential weapon/armor tiers with dimmed next prices. No new speed
  purchase; preserve legacy boots, ledgers, weapons, scores and save migration.
- New original 80-second,96-BPM minor/modal science-fiction score replaces the
  platform track. Historical aurora-hop.ogg path stays only for stable resources.
- 0.10.0/code11, same package/debug certificate. Other engines remain frozen.
  Preserve actual gesture/save/audio/depth tests and new sanctuary/shop UI test.
  No PR, game merge, Actions, Release/Play or other-repository changes.

## Zoom and visible treasure 0.11 — latest operator task, 29 October 2026

- Work on feat/zoom-treasure-polish; preserve main's integrated 0.10 and all history.
  No automatic game merge, PR, Release/Play publication or other-repository writes.
- Zoom the whole world from75–175%, with shared camera/unprojection/hit regions;
  fixed HUD controls, larger world text, persistent scale and focal-area anchoring.
  Pinch cancels ordinary input, including its remaining-finger tail. Keep immediate
  enemy presses; a shot emitted before a second finger exists cannot be undone.
- Current treasure guidance must link speech/compass/search area, use reachable
  landmarks and persistent discovery, enlarge/glow on approach, and require actual
  reachable LOS pickup. Never spend another clue for a collected/discovered chest.
- Current art adds shared/assets/defold11 HD redraws, native rim shimmer and six
  bounded orbit lights. Keep old source atlases and immutable provenance intact.
- 0.11.0/code12, same package/debug certificate. Real native UI tests must find all
  six treasures and compare rendered zoom/scaled actors; physical pinch stays open.

## Playable replay bonuses and forgiving traps 0.12 — 29 October 2026

- Continue feat/zoom-treasure-polish. The operator externally merged 0.11 into
  main through PR #1 (ffbdb91); preserve that history. No new automatic game merge,
  PR, Actions, Release/Play publication or other-repository writes.
- Keep one-time earned-star/purchase ledgers separate from current-visit optional
  objectives. Restore bonus targets and replay chests on mission load; resuming or
  focusing the same round must not respawn them. Label replay rewards honestly,
  preserve scores and purchases, and never award the same key twice.
- Hint/Info must lead to an unfinished bonus when the chest reward was earned;
  do not announce that everything is collected while playable objectives remain.
  Verify all six maps, reachable targets and actual reflected projectile hits.
- Current trap placement radius is 5.25 world units; renderer and validator share
  it. Reject walls, occluded floor and out-of-range points through either UI or
  direct gameplay calls. Enable the catalogue in forge, echo and rescue.
- Initially triple triggered durations (magnet18/frost27/pulse15 seconds) and
  armed lifetime (36 seconds). Later factors2.5/2 require an actual successful
  trap and completion in distinct earlier eligible missions; retries/old reward
  flags alone do not advance training. Snapshot timing at load, preserve longer
  active effects and keep repeat visits to earlier missions generous.
- 0.12.0/code13, same package/debug certificate. Extend native rule and actual GUI
  regressions using previously completed saves; report real Android checks separately.

## Bonus power first 0.13 — latest operator priority, 29 October 2026

- Work on feat/bonus-power. The latest instruction explicitly prioritizes bonus
  growth FIRST. Preserve the existing six missions; the additional20missions and
  first-person-view proposal remain the next planned work, not this iteration.
- Each distinct current bonus achievement permanently increases health, shield,
  firepower, concealment and the rendered hero's size. Derive power from the known
  once-earned bonus keys: the twelve existing achievements count immediately,
  unknown saved keys do not, and replays cannot farm stars or power.
- Preserve the requested extravagant health progression20/30/35/40/80/160/400/
  1000/10000/100000/400000/1000000, plus existing purchased armor bonuses. Five
  named milestones at1/2/4/8/12 bonuses complement growth at every earned bonus.
  Keep purchases and scores, apply gains in the current round, and do not revive
  a defeated hero or silently erase damage when increasing maximum health.
- Bigger visuals must remain bounded and playable: preserve collision/movement
  size, navigation, depth testing and the ability to use cover. Use real shield,
  weapon and detection effects, not only labels; preserve finite projectile
  lifetime/bounces and actual reflection/sequence/timing requirements. No new
  speed upgrade. Keep a bounded number of aura/shield objects.
- Explain current and next bonus power through an accessible illustrated page,
  visible health/shield totals, growth feedback and the existing synthetic voice.
  Long numbers must fit on the smallest tested HUD without scientific notation.
- 0.13.0/code14, same package/debug certificate. Preserve the0.12rules as a frozen
  regression fixture. Test fresh and previously completed saves, actual native
  growth/shield/cloak output and GUI input; separate physical Android checks.
  No automatic merge, PR, Actions, Release/Play or other-repository changes.

## Campaign revision 0.14 — latest operator request, 30 October 2026

- Work on `feat/campaign-16`, version 0.14.0 / code 15. The latest request replaces
  the former 20-mission plan with exactly 10 additional missions: 16 total. Remove
  active hidden bonus tasks and chests entirely. Preserve earlier earned stars,
  purchases and immutable historical assets/reports rather than deleting them.
- Progress now follows completed missions. Maximum health is 100 INCLUDING all
  purchased armor; shield capacity 20, projectile damage 8 and fire interval 0.16 s
  bound the earlier extravagant power model. Keep existing purchases useful and
  never mint a second completion reward on replay. Legacy 0.13 data remains frozen
  for explicit historical regressions; new campaign checks must use active rules.
- Camouflage is partial. Ordinary detection retains a 0.55 floor and enemies have
  repeated accurate long-distance sensor locks. Neither concealment nor cover
  permits bullets through walls. Do not restore permanently invisible players.
- Every mission starts the hero inside its Zikkurat. Use a reachable physical
  shelter plus swept projectile absorption; enemy shots cannot reach its interior,
  including reflections or an inside spawn. The exit remains walkable.
- More complex fields use individual mission arenas from 31.5x22.5 to 42x30 versus
  the former 21x15. Geometry, collision, navigation, projection and picking must
  consume those same bounds. Maximum zoom-out stops at the field boundary;
  neutral aspect-ratio margins contain no outside scenery or decorative cosmos.
- Add recognizable mini-drones, finite splitting families, crawlers, wisps and
  stronger guardians. Bound simultaneous living hostiles to 50, preserve finite
  family generations and clean dead render objects. Never create an endless
  replication wave that silently prevents completion.
- Attack drones are selected from a finite stock catalogue, like choosing a trap,
  but their targeting is different: after selecting, DRAG the ready drone onto an
  enemy OR hear "Waehle jetzt das Ziel" and TAP an enemy. Real flight precedes
  the electric contact destruction. Invalid targets, foreign fingers, cancellation
  and background/menu changes must not spend stock or leak walking/shooting.
  Keep relay locks on bosses; empty stock cannot make a mission impossible.
- Mission selection has 16 accessible cards across pages. The upper HUD must use
  real touch buttons for its advertised actions; remove obsolete bonus/chest
  controls and stale "already collected" or escort instructions.
- Retain the existing synthetic speaker; eight new complete cues are technically
  decoded/hash-checked and independently transcribed. Do not confuse those checks
  with a human hearing test. Report actual native/Android build results separately.
- No automatic game merge, PR, Actions, Release/Play upload, private family asset,
  signing-key publication or changes to another repository.
