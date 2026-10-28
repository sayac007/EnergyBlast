class Shooter extends Pilot {
  constructor(scene) {
    super(scene);
    this.sound = true;
    window.addEventListener(
      "pointermove",
      (e) =>
        (this.pointerId === undefined || e.pointerId === this.pointerId) &&
        this.drag(e.clientX, e.clientY),
    );
    window.addEventListener("pointercancel", () => this.cancelControls());
    window.addEventListener("pointerup", (e) => {
      if (e.pointerId === this.firePointerId) {
        this.held = false;
        this.firePointerId = undefined;
      }
      if (this.pointerId === undefined || e.pointerId === this.pointerId)
        this.release(e.clientX, e.clientY);
    });
  }
  cancelControls() {
    this.held = false;
    this.pointer = false;
    this.aiming = false;
    this.pointerId = undefined;
    this.firePointerId = undefined;
  }
  setBackground(value) {
    super.setBackground(value);
    if (value) this.cancelControls();
  }
  ui() {
    super.ui();
    let style = document.createElement("style");
    style.textContent =
      "@font-face{font-family:EnergyBlast;src:url(LilitaOne-Regular.ttf)}#eb{font-family:EnergyBlast,system-ui}#eb button{font-family:EnergyBlast,system-ui}#eb button{background:#20314b;border-radius:24px;font-weight:750}#eb .top{flex-wrap:wrap}#eb-stars{font-size:26px}#eb .bottom{bottom:max(12px,env(safe-area-inset-bottom))}#eb-modes{gap:14px;margin-bottom:10px}#eb-modes button{height:76px;font-size:20px}#eb-modes button b{display:none}#eb-extra button{min-height:42px;font-size:12px}#eb-extra button b{display:inline;font-size:18px;margin-right:6px}#eb-status{font-size:12px;min-height:28px;margin-bottom:0;color:#b8e5ed}#eb .dialog{background:#18253e;border:1px solid #45627c;border-radius:28px}#eb .dialog button{min-height:70px;font-size:16px}#eb .top{background:linear-gradient(135deg,#14243ee8,#202e4bd9);padding:12px;border-radius:22px;border:1px solid #486378;box-shadow:0 8px 20px #050d2140}#eb-stars{color:#ffe299;text-shadow:0 2px 8px #f9b34b66}#eb-modes button{box-shadow:0 5px 0 #0a152c,0 8px 18px #040e2b77}#eb .dialog{box-shadow:0 25px 80px #020921cc;background:linear-gradient(145deg,#20344d,#172038)}#eb .dialog button{border:1px solid #536c86}#eb .dialog button:nth-of-type(3){background:#715337;color:#ffde9b}#eb-objective{font-size:12px;color:#ffdf8c}#eb-health{color:#ff7394;width:100%;font-weight:800;font-size:22px}#eb-mission{color:#9db5ce;font-size:12px;width:100%}";
    document.head.append(style);
    let row = this.hud.querySelector("#eb-modes");
    row.replaceChildren();
    this.dashButton = this.button("» DASH", "", row, () => this.dash());
    this.fireButton = this.button("ϟ FEUER", "", row, () => {});
    this.fireButton.style.background = "#d63969";
    this.fireButton.onpointerdown = (e) => {
      e.stopPropagation();
      this.firePointerId = e.pointerId;
      this.held = true;
      this.fireButton.setPointerCapture(e.pointerId);
      this.fire();
    };
    this.fireButton.onpointerup = (e) => {
      e.stopPropagation();
      if (e.pointerId === this.firePointerId) {
        this.held = false;
        this.firePointerId = undefined;
      }
    };
    this.fireButton.onpointercancel = () => (this.held = false);
    row = this.hud.querySelector("#eb-extra");
    row.replaceChildren();
    this.button("Hinweis", "?", row, () => this.hint());
    this.button("Funk", "♫", row, () => {
      this.say(this.m.id === "dock" ? "raid_dock" : "combat_" + this.m.id);
      this.next = "combat_controls";
    });
    this.button("Arsenal", "◇", row, () => this.gear());
    let h = document.createElement("div");
    h.id = "eb-health";
    this.hud.querySelector(".top").append(h);
    h = document.createElement("div");
    h.id = "eb-mission";
    this.hud.querySelector(".top").append(h);
    h = document.createElement("div");
    h.id = "eb-objective";
    this.hud.querySelector(".top").append(h);
  }
  model(name, p, width, height, depth) {
    const dimensions = /*ENERGYBLAST_DIMENSIONS*/ {};
    if (dimensions[name.toLowerCase()])
      [width, height, depth] = dimensions[name.toLowerCase()].map(
        (n) => n * 100,
      );
    let o = this.scene.createObject(name);
    o.setWidth(width);
    o.setHeight(height);
    o.setDepth(depth);
    o.setPosition(p[0] * 100, p[1] * 100);
    o.setZ(0);
    this.models.push(o);
    o.get3DRendererObject().scale.y =
      (["Reactor", "Citadel", "Dock"].includes(name) ? 1 : -1) *
      Math.abs(o.get3DRendererObject().scale.y);
    return o;
  }
  load(index) {
    for (const o of this.models) o.deleteFromScene(this.scene);
    this.models = [];
    this.m = DEF.missions[index];
    this.index = index;
    this.p = [...this.m.spawn];
    this.clock = 0;
    this.mode = "move";
    this.path = [];
    this.aim = this.norm([8.5, -11.9]);
    this.paused = false;
    this.solved = false;
    this.over = false;
    this.invulnerable = 0;
    this.damage = 0;
    this.cooldown = 0;
    this.dashCooldown = 0;
    this.dashTime = 0;
    this.held = false;
    this.pointer = false;
    this.aiming = false;
    this.clueTime = 0;
    this.hintDebounce = 0;
    this.healUsed = false;
    this.target = null;
    this.feedback = 0;
    this.bullets = [];
    this.shotsFired = 0;
    this.fx = [];
    this.hp = 3 + (this.total() >= 160 ? 1 : 0);
    this.maxHp = this.hp;
    this.model(["Reactor", "Citadel", "Dock"][index], [0, 0], 1620, 1190, 305);
    this.hero = this.model("Hero", this.p, 134, 110, 190);
    this.radar = this.model("Radar", this.m.radar, 110, 100, 120);
    this.radar.setZ(117);
    this.walls = [
      { r: [-7, -5, 14, 0.3], type: "border" },
      { r: [-7, 4.7, 14, 0.3], type: "border" },
      { r: [-7, -5, 0.3, 10], type: "border" },
      { r: [6.7, -5, 0.3, 10], type: "border" },
      ...this.m.covers.map((r) => ({ r, type: "cover" })),
      ...this.m.reflectors.map((r) => ({ r, type: "reflector" })),
    ];
    this.enemies = this.m.turrets.map((t) => ({
      ...t,
      p: [...t.position],
      hp: t.hp || 2,
      timer: t.phase + 0.7,
      warning: 0,
      direction: [-1, 0],
      node: this.model("Cannon", t.position, 110, 152, 120),
      maxHp: t.hp || 2,
      burst: t.burst || 1,
      waypoint: 1,
    }));
    for (const t of this.m.relays || [])
      this.enemies.push({
        ...t,
        p: [...t.position],
        hp: 1,
        maxHp: 1,
        shield: true,
        kind: "relay",
        warning: 0,
        direction: [0, 1],
        node: this.model("Relay", t.position, 97, 85, 142),
      });
    this.secret = this.cube(
      this.m.secret.position[0] - 0.35,
      this.m.secret.position[1] - 0.25,
      0.7,
      0.5,
      0.5,
      "157;99;233",
    );
    this.secret.hide(true);
    this.heal = this.m.heal
      ? this.cube(
          this.m.heal[0] - 0.2,
          this.m.heal[1] - 0.2,
          0.4,
          0.4,
          0.25,
          "116;255;210",
        )
      : null;
    this.gate = null;
    this.lights = [];
    if (this.m.gate_rect) {
      this.gate = this.cube(...this.m.gate_rect, 1, "243;163;108");
      for (let i = 0; i < 3; i++)
        this.lights.push(
          this.cube(4.2 + i * 0.6, -1, 0.25, 0.2, 0.22, "60;85;100", 1.5),
        );
      this.cube(
        this.m.goal[0] - 0.3,
        this.m.goal[1] - 0.3,
        0.6,
        0.6,
        0.6,
        "82;246;213",
      );
    }
    this.layer.setCameraX(1800);
    this.layer.setCameraY(0);
    this.layer.setCameraZ(2400);
    this.layer.setCameraRotationX(0);
    this.layer.setCameraRotationY(36.87);
    this.layer.setCameraZoom(720 / 1170);
    let camera = this.layer.getRenderer().getThreeCamera();
    camera.up.set(0, 0, 1);
    camera.lookAt(0, 0, 0);
    this.status("Tippen: laufen · Ziehen und loslassen: schießen");
    this.hud.querySelector("#eb-mission").textContent = this.m.title;
    this.score();
  }
  cluesEarned() {
    return (
      (DEF.hint_completion_keys || []).filter((k) => this.saved.earned[k])
        .length * 2
    );
  }
  score() {
    super.score();
    if (this.hud.querySelector("#eb-health"))
      this.hud.querySelector("#eb-health").textContent =
        "♥ ".repeat(Math.max(0, this.hp || 0)) +
        "♡ ".repeat(Math.max(0, (this.maxHp || 0) - (this.hp || 0)));
  }
  menu() {
    this.cancelControls();
    this.modal(
      "ENERGYBLAST · AURORA RAID 0.3",
      DEF.missions
        .map((m, i) => [
          String(i + 1).padStart(2, "0") + " · " + m.title,
          "ϟ",
          () => {
            this.load(i);
            this.close();
            if (this.audio) this.audio.pause();
            this.next = "combat_controls";
            this.important = [];
            this.say(m.id === "dock" ? "raid_dock" : "combat_" + m.id);
          },
        ])
        .concat([["▶ WEITER", "", () => this.close()]]),
    );
  }
  stats() {
    let s = super.stats();
    s.speed += 1.2;
    s.lens ||= !!this.saved.earned["secret:reactor"];
    s.quiet ||= !!this.saved.earned["secret:citadel"];
    return s;
  }
  tap(x, y, id) {
    if (this.pointer) return;
    this.pointerId = id;
    this.pointer = true;
    this.start = [x, y];
    this.current = [x, y];
    this.aiming = false;
  }
  world(x, y) {
    let r = this.canvas.getBoundingClientRect(),
      ray = new THREE.Raycaster(),
      p = new THREE.Vector3();
    ray.setFromCamera(
      new THREE.Vector2(
        ((x - r.left) / r.width) * 2 - 1,
        1 - ((y - r.top) / r.height) * 2,
      ),
      this.layer.getRenderer().getThreeCamera(),
    );
    if (
      !ray.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 0, 1), 0), p)
    )
      return this.p;
    return [
      Math.max(-6.4, Math.min(6.4, p.x / 100)),
      Math.max(-4.3, Math.min(4.3, -p.y / 100)),
    ];
  }
  drag(x, y) {
    if (!this.pointer || this.paused) return;
    this.current = [x, y];
    if (this.distance(this.start, this.current) > 12) {
      this.aiming = true;
      this.path = [];
      let q = this.world(x, y);
      this.aim = this.norm([q[0] - this.p[0], q[1] - this.p[1]]);
      this.target = q;
    }
  }
  release(x, y) {
    if (!this.pointer || this.paused) return;
    // A release can cross the drag threshold even when the last move was coalesced.
    if (this.distance(this.start, [x, y]) > 12) this.drag(x, y);
    this.pointer = false;
    if (this.aiming) this.fire();
    else {
      let q = this.world(x, y),
        target = null,
        nearest = 26;
      for (const t of this.enemies)
        if (t.hp > 0) {
          const p = this.project(t.p, 80),
            d = Math.hypot(p[0] - x, p[1] - y);
          if (d < nearest) {
            target = t.p;
            nearest = d;
          }
        }
      const reflector = this.walls.some(
        (w) =>
          w.type === "reflector" &&
          q[0] > w.r[0] - 0.2 &&
          q[0] < w.r[0] + w.r[2] + 0.2 &&
          q[1] > w.r[1] - 0.2 &&
          q[1] < w.r[1] + w.r[3] + 0.2,
      );
      this.target = target || q;
      if (target || reflector) {
        this.path = [];
        this.aim = this.norm([
          this.target[0] - this.p[0],
          this.target[1] - this.p[1],
        ]);
        this.fire();
      } else this.navigate(q);
    }
    this.pointerId = undefined;
    this.aiming = false;
  }
  fire() {
    if (this.over || this.paused || this.cooldown > 0) return;
    this.cooldown = DEF.combat.fire_cooldown;
    this.shotsFired++;
    this.bullets.push({
      points: this.shot(),
      segment: 0,
      p: [this.p[0] + this.aim[0] * 0.35, this.p[1] + this.aim[1] * 0.35],
      enemy: false,
      speed: DEF.combat.player_bullet_speed,
    });
    this.beep(740, 0.07);
  }
  beep(hz, seconds) {
    if (!this.sound) return;
    try {
      this.context ||= new (window.AudioContext || window.webkitAudioContext)();
      this.context.resume();
      let o = this.context.createOscillator(),
        g = this.context.createGain();
      o.frequency.value = hz;
      o.connect(g);
      g.connect(this.context.destination);
      g.gain.setValueAtTime(0.08, this.context.currentTime);
      g.gain.exponentialRampToValueAtTime(
        0.001,
        this.context.currentTime + seconds,
      );
      o.start();
      o.stop(this.context.currentTime + seconds);
    } catch (e) {}
  }
  dash() {
    if (this.paused || this.over || this.dashCooldown > 0) return;
    if (!this.path.length)
      this.navigate([this.p[0] + this.aim[0] * 2, this.p[1] + this.aim[1] * 2]);
    this.dashTime = DEF.player.dash_seconds;
    this.dashCooldown =
      DEF.player.dash_cooldown * (this.saved.earned["secret:dock"] ? 0.8 : 1);
    this.invulnerable = Math.max(this.invulnerable, this.dashTime);
    this.beep(400, 0.08);
  }
  damagePlayer() {
    if (this.invulnerable > 0 || this.over) return;
    this.hp--;
    this.damage++;
    this.invulnerable = DEF.combat.hit_invulnerability;
    this.feedback = 0.35;
    this.score();
    this.beep(130, 0.15);
    if (this.hp <= 0) {
      this.over = true;
      this.held = false;
      this.path = [];
      this.say("combat_retry");
      this.modal("ENERGIE LEER", [
        [
          "↻ NEUER ANLAUF",
          "",
          () => {
            this.load(this.index);
            this.close();
            this.say(
              this.m.id === "dock" ? "raid_dock" : "combat_" + this.m.id,
            );
          },
        ],
        ["≡ SEKTOREN", "", () => this.menu()],
      ]);
    }
  }
  locked(t) {
    return t.boss && this.enemies.some((e) => e.kind === "relay" && e.hp > 0);
  }
  hit(t, bounces) {
    if (this.locked(t)) {
      this.status("RELAIS ZUERST");
      this.say("raid_relays");
      return;
    }
    if (t.shield && !bounces) {
      this.status("SCHILD · Triff über die leuchtende Wand.");
      this.say(t.kind === "relay" ? "raid_relays" : "combat_shield");
      return;
    }
    t.hp--;
    this.fx.push({ p: [...t.p], life: 0.45 });
    this.beep(250, 0.1);
    if (t.hp <= 0) {
      t.node.hide(true);
      if (this.enemies.every((e) => e.hp <= 0)) {
        if (!this.m.exit_required) this.finish();
        else this.status("KANONEN AUS · Erreiche den Energiekern.");
      }
    }
  }
  finish() {
    if (this.solved) return;
    this.solved = true;
    this.over = true;
    this.held = false;
    this.path = [];
    let n = this.award("mission:" + this.m.id);
    if (!this.damage) n += this.award("skill:" + this.m.id);
    this.say("combat_win");
    this.modal("SEKTOR GESICHERT · + " + n + " ★", [
      [
        "◇ BEUTE SUCHEN",
        "",
        () => {
          this.over = false;
          this.close();
        },
      ],
      ["▶ SEKTOREN", "", () => this.menu()],
      [
        "↻ NOCH EINMAL",
        "",
        () => {
          this.load(this.index);
          this.close();
        },
      ],
    ]);
  }
  hint() {
    if (this.hintDebounce > 0) return;
    this.hintDebounce = 1.2;
    let level = this.clueLevel();
    if (level < 2) {
      if (this.hints() <= 0) {
        this.say("hints_empty");
        return;
      }
      this.saved.clues.push(this.m.id + ":" + (level + 1));
      this.save();
    }
    this.clueTime = 8;
    this.say(
      this.m.id === "dock"
        ? "raid_hint"
        : this.m.id === "reactor"
          ? "hint_bank"
          : "hint_guardian",
    );
    this.score();
  }
  gear() {
    this.cancelControls();
    this.modal(
      "ARSENAL",
      DEF.unlocks
        .map((u) => [
          (this.total() >= u.stars ? "✓ " : u.stars + " ★ ") +
            {
              prism: "PRISMA · 2 ABPRALLER",
              armor: "RÜSTUNG · +1 ENERGIE",
              boots: "STIEFEL · MEHR TEMPO",
              cloak: "TARNUNG · KÜRZERE REICHWEITE",
            }[u.id],
          "",
          () => {
            if (u.id === "prism" && this.total() >= 100) {
              this.saved.weapon =
                this.saved.weapon === "prism" ? "pulse" : "prism";
              this.save();
            }
          },
        ])
        .concat([["WEITER", "▶", () => this.close()]]),
    );
  }
  project(p, height = 75) {
    const v = new THREE.Vector3(p[0] * 100, -p[1] * 100, height).project(
        this.layer.getRenderer().getThreeCamera(),
      ),
      r = this.canvas.getBoundingClientRect();
    return [
      r.left + ((v.x + 1) * r.width) / 2,
      r.top + ((1 - v.y) * r.height) / 2,
    ];
  }
  dot(p, color, r = 6, height = 75) {
    const v = this.project(p, height),
      o = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    o.setAttribute("cx", v[0]);
    o.setAttribute("cy", v[1]);
    o.setAttribute("r", r);
    o.setAttribute("fill", color);
    this.svg.append(o);
    return o;
  }
  ring(p, color, r = 12, height = 0) {
    const o = this.dot(p, "none", r, height);
    o.setAttribute("stroke", color);
    o.setAttribute("stroke-width", 2);
    return o;
  }
  update(dt) {
    if (this.paused || this.background || this.over) return;
    this.clock += dt;
    this.svg.replaceChildren();
    this.feedback = Math.max(0, this.feedback - dt);
    this.cooldown = Math.max(0, this.cooldown - dt);
    this.invulnerable = Math.max(0, this.invulnerable - dt);
    this.dashTime = Math.max(0, this.dashTime - dt);
    this.dashCooldown = Math.max(0, this.dashCooldown - dt);
    this.clueTime = Math.max(0, this.clueTime - dt);
    this.hintDebounce = Math.max(0, this.hintDebounce - dt);
    if (this.held) this.fire();
    if (this.path.length) {
      let t = this.path[0],
        step =
          (this.dashTime > 0 ? DEF.player.dash_speed : this.stats().speed) * dt,
        d = this.distance(t, this.p),
        n = this.norm([t[0] - this.p[0], t[1] - this.p[1]]),
        q = d < step ? t : [this.p[0] + n[0] * step, this.p[1] + n[1] * step];
      if (!this.blocked(q)) this.p = q;
      else this.path = [];
      if (this.path.length && this.distance(this.path[0], this.p) < 0.04)
        this.path.shift();
      if (!this.held && !this.aiming)
        this.hero.setAngle((Math.atan2(n[1], n[0]) * 180) / Math.PI);
    }
    this.dot(this.p, "#050d2155", 18, 3);
    this.radar.setAngle(this.clock * 26);
    this.hero.setPosition(this.p[0] * 100, this.p[1] * 100);
    this.hero.hide(this.invulnerable > 0 && this.clock % 0.13 < 0.05);
    if (this.aiming || this.held)
      this.hero.setAngle(
        (Math.atan2(this.aim[1], this.aim[0]) * 180) / Math.PI,
      );
    const model = this.hero.get3DRendererObject();
    if (model)
      for (const name of ["Leg_L", "Leg_R", "Arm_L", "Arm_R"]) {
        let node = model.getObjectByName(name);
        if (node)
          node.rotation.x =
            Math.sin(this.clock * 11) *
            (this.path.length ? 0.5 : 0.04) *
            (name.endsWith("L") ? 1 : -1);
      }
    for (const t of this.enemies) {
      if (t.hp <= 0) continue;
      if (t.kind === "relay") {
        t.node.setZ(8 * Math.sin(this.clock * 2));
        this.ring(t.p, "#ffd674", 20, 10);
        continue;
      }
      if (t.patrol && t.warning <= 0) {
        const q = t.patrol[t.waypoint],
          d = this.distance(t.p, q),
          step = (t.speed || 1) * dt;
        if (d < step) {
          t.p = [...q];
          t.waypoint = (t.waypoint + 1) % t.patrol.length;
        } else {
          const n = this.norm([q[0] - t.p[0], q[1] - t.p[1]]);
          t.p = [t.p[0] + n[0] * step, t.p[1] + n[1] * step];
        }
        t.node.setPosition(t.p[0] * 100, t.p[1] * 100);
      }

      if (t.warning > 0) {
        t.warning -= dt;
        if (t.warning <= 0) {
          for (let j = 0; j < t.burst; j++) {
            const a = (j - (t.burst - 1) / 2) * 0.16,
              d = [
                t.direction[0] * Math.cos(a) - t.direction[1] * Math.sin(a),
                t.direction[0] * Math.sin(a) + t.direction[1] * Math.cos(a),
              ],
              start = [...t.p],
              hit = this.ray(start, d, 20, this.activeWalls());
            this.bullets.push({
              points: [
                start,
                hit ? hit.p : [start[0] + d[0] * 20, start[1] + d[1] * 20],
              ],
              segment: 0,
              p: [...start],
              enemy: true,
              speed: DEF.combat.enemy_bullet_speed,
            });
          }
          t.timer = DEF.combat.enemy_interval;
          this.beep(190, 0.08);
        }
      } else {
        t.timer -= dt;
        if (
          t.timer <= 0 &&
          this.distance(t.p, this.p) <
            13 * (1 - this.stats().cloak * 0.5) * (this.stats().quiet ? 0.9 : 1)
        ) {
          t.warning = DEF.combat.enemy_warning;
          t.direction = this.norm([this.p[0] - t.p[0], this.p[1] - t.p[1]]);
        }
      }
      t.node.setAngle(
        (Math.atan2(t.direction[1], t.direction[0]) * 180) / Math.PI,
      );
      if (t.shield || this.locked(t)) {
        this.ring(t.p, "#b688ff", 26, 65);
        this.dot(t.p, "#b688ff22", 26, 65);
      }
      for (let i = 0; i < t.hp; i++)
        this.dot([t.p[0] - 0.15 + i * 0.3, t.p[1]], "#ff7394", 4, 145);
      if (t.warning > 0) {
        this.ring(t.p, "#ffb47b", 12 + 4 * Math.sin(this.clock * 28) ** 2, 100);
        this.dot(t.p, "#ffd674", 5, 100);
      }
    }
    for (const b of [...this.bullets]) {
      let distance = b.speed * dt,
        removed = false;
      while (distance > 0 && b.segment < b.points.length - 1) {
        let t = b.points[b.segment + 1],
          d = this.distance(t, b.p),
          step = Math.min(distance, d),
          n = this.norm([t[0] - b.p[0], t[1] - b.p[1]]),
          q = [b.p[0] + n[0] * step, b.p[1] + n[1] * step];
        if (b.enemy) {
          if (this.segment(this.p, b.p, q) < 0.36) {
            this.damagePlayer();
            removed = true;
          }
        } else
          for (const e of this.enemies)
            if (
              e.hp > 0 &&
              this.segment(e.p, b.p, q) < (this.stats().lens ? 0.56 : 0.48)
            ) {
              this.hit(e, b.segment);
              removed = true;
              break;
            }
        b.p = q;
        distance -= step;
        if (removed) break;
        if (this.distance(q, t) < 0.001) {
          b.segment++;
          this.fx.push({ p: [...q], life: 0.22 });
        }
        if (step < 0.00001) break;
      }
      this.dot(b.p, b.enemy ? "#ff6b8e" : "#a1fff0", 5);
      this.dot(b.p, b.enemy ? "#ff6b8e22" : "#a1fff022", 10);
      if (removed || b.segment >= b.points.length - 1)
        this.bullets.splice(this.bullets.indexOf(b), 1);
    }
    this.fx = this.fx.filter((f) => (f.life -= dt) > 0);
    for (const f of this.fx) this.dot(f.p, "#ffd77988", 12 * (1 - f.life));
    if (this.aiming && this.target) {
      this.ring(this.target, "#b6ffeb", 13, 0);
      this.dot(this.target, "#b6ffeb", 3, 0);
    }
    if (this.path.length) this.ring(this.path.at(-1), "#74efcc", 10, 0);
    const sp = this.m.secret.position,
      dist = this.distance(sp, this.p);
    this.secret.hide(
      !!this.saved.earned["secret:" + this.m.id] ||
        dist > 2 ||
        !!this.ray(
          this.p,
          this.norm([sp[0] - this.p[0], sp[1] - this.p[1]]),
          dist - 0.05,
          this.walls,
        ),
    );
    if (this.secret.isVisible() && dist < 0.7) {
      this.award("secret:" + this.m.id);
      this.say("combat_loot");
      this.secret.hide(true);
    }
    if (this.clueTime > 0)
      this.line(
        [this.p, this.clueLevel() > 1 ? sp : this.m.secret.hint_landmark],
        "#ffe090",
      );
    if (this.gate) {
      this.gate.setDepth(this.open() ? 10 : 100);
      for (let i = 0; i < 3; i++)
        this.lights[i].setColor(
          this.clock % 8 >= 3 + i ? "104;246;198" : "60;85;100",
        );
    }
    if (
      this.m.exit_required &&
      this.open() &&
      this.enemies.every((t) => t.hp <= 0) &&
      this.distance(this.p, this.m.goal) < 0.8
    )
      this.finish();
    if (
      this.heal &&
      !this.healUsed &&
      this.hp < this.maxHp &&
      this.distance(this.p, this.m.heal) < 0.65
    ) {
      this.hp++;
      this.healUsed = true;
      this.heal.hide(true);
      this.score();
      this.beep(600, 0.15);
    }
    if (this.heal && !this.healUsed)
      this.heal.setZ(15 + 8 * Math.sin(this.clock * 3));
    const relays = this.enemies.filter(
        (e) => e.kind === "relay" && e.hp > 0,
      ).length,
      alive = this.enemies.filter((e) => e.kind !== "relay" && e.hp > 0).length;
    this.hud.querySelector("#eb-objective").textContent =
      (this.m.id === "dock" ? `RELAIS ${2 - relays}/2 · ` : "") +
      `KANONEN ${alive}` +
      (this.m.exit_required
        ? ` · TOR ${this.open() ? "OFFEN" : Math.ceil(5 - (this.clock % 8)) + " s"}`
        : "");
    this.hud.querySelector(".top").style.borderColor =
      this.feedback > 0 ? "#ff6b8e" : "#486378";
    this.dashButton.textContent =
      this.dashCooldown > 0 ? "» " + this.dashCooldown.toFixed(1) : "» DASH";
  }
}
