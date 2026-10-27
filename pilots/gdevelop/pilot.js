// Native GDevelop scene/objects/renderer. Same JSON rules and original GLB as Godot.
if (!runtimeScene.energyblast) {
  runtimeScene.getGame().enableMetrics(false);
  const DEF = /*ENERGYBLAST_DEF*/ {};
  const AUDIO = /*ENERGYBLAST_AUDIO*/ {};
  class Pilot {
    constructor(scene) {
      this.scene = scene;
      this.layer = scene.getLayer("");
      this.models = [];
      this.meshes = [];
      this.saved = { earned: {}, clues: [], weapon: "pulse" };
      try {
        const v = JSON.parse(localStorage.getItem("energyblast-progress"));
        if (v && v.earned && Array.isArray(v.clues)) this.saved = v;
      } catch (e) {}
      this.saved.earned = Object.fromEntries(
        Object.entries(this.saved.earned).filter(
          ([k, v]) => v === true && DEF.rewards[k],
        ),
      );
      this.saved.clues = [...new Set(this.saved.clues)]
        .filter((x) => /^(bank|guardian):[12]$/.test(x))
        .slice(0, this.cluesEarned());
      this.layer.setCameraX(0);
      this.layer.setCameraY(1300);
      this.layer.setCameraZ(1900);
      this.layer.setCameraZoom(0.4556962);
      this.layer.setCameraRotationX(34.38);
      this.layer
        .get3DRendererObject()
        .add(new THREE.AmbientLight(0xffffff, 0.7));
      const light = new THREE.DirectionalLight(0xffffff, 0.7);
      light.position.set(-1000, 500, 1800);
      this.layer.get3DRendererObject().add(light);
      this.canvas = document.querySelector("canvas");
      this.ui();
      this.load(0);
      this.menu();
      this.sound = true;
      this.queue = [];
      this.important = [];
      window.addEventListener("pointerdown", (e) => {
        if (e.target.closest("[data-ebui]") || this.paused) return;
        this.tap(e.clientX, e.clientY);
      });
      document.addEventListener("energyblast-pause", () =>
        this.setBackground(true),
      );
      document.addEventListener("energyblast-resume", () =>
        this.setBackground(false),
      );
      document.addEventListener("visibilitychange", () =>
        this.setBackground(document.hidden),
      );
    }
    setBackground(value) {
      if (!!this.background === value) return;
      this.background = value;
      if (value) {
        this.resumeAudio =
          !!this.audio && !this.audio.paused && !this.audio.ended;
        if (this.audio) this.audio.pause();
      } else if (this.resumeAudio && this.sound && this.audio) {
        this.resumeAudio = false;
        this.audio.play().catch(() => {});
      }
    }
    total() {
      return Object.keys(this.saved.earned).reduce(
        (n, k) => n + (DEF.rewards[k] || 0),
        0,
      );
    }
    cluesEarned() {
      return (
        ["bank", "guardian"].filter((m) => this.saved.earned["mission:" + m])
          .length * 2
      );
    }
    hints() {
      return this.cluesEarned() - this.saved.clues.length;
    }
    clueLevel() {
      return this.saved.clues.filter((x) => x.startsWith(this.m.id + ":"))
        .length;
    }
    save() {
      try {
        localStorage.setItem(
          "energyblast-progress",
          JSON.stringify(this.saved),
        );
      } catch (e) {
        this.status("Speichern nicht möglich.");
      }
    }
    award(id) {
      if (this.saved.earned[id]) return 0;
      const before = this.total();
      this.saved.earned[id] = true;
      if (before < 100 && this.total() >= 100) this.saved.weapon = "prism";
      this.save();
      this.score();
      return DEF.rewards[id];
    }
    stats() {
      let n = this.total();
      return {
        speed: 3 + (n >= 230 ? Math.min(0.5, (n - 220) / 210) : 0),
        grace: n >= 160 ? 1.4 : 1,
        cloak: n >= 300 ? Math.min(0.35, (n - 280) / 180) : 0,
        bounces: n >= 100 && this.saved.weapon === "prism" ? 2 : 1,
        lens: !!this.saved.earned["secret:bank"],
        quiet: !!this.saved.earned["secret:guardian"],
      };
    }
    say(id) {
      if (!this.sound || !AUDIO[id]) return;
      if (this.audio && !this.audio.paused) {
        if (["success", "found", "upgrade"].includes(id)) {
          if (!this.important.includes(id)) this.important.push(id);
        } else this.next = id;
        return;
      }
      const row = AUDIO[id],
        res = gdjs.projectData.resources.resources.find(
          (r) => r.name === row.file,
        );
      this.audio = new Audio(res.file);
      this.context ||= new (window.AudioContext || window.webkitAudioContext)();
      this.context.resume();
      const source = this.context.createMediaElementSource(this.audio),
        gain = this.context.createGain();
      gain.gain.value = Math.pow(10, (row.playback_gain_db - 1) / 20);
      source.connect(gain);
      gain.connect(this.context.destination);
      this.audio.onended = () => {
        source.disconnect();
        gain.disconnect();
        const n = this.important.shift() || this.next;
        if (n === this.next) this.next = null;
        if (n) this.say(n);
      };
      this.audio.play().catch(() => {});
    }
    cube(x, y, w, h, depth, color, z = 0) {
      let o = this.scene.createObject("Cube");
      o.setPosition(x * 100, y * 100);
      o.setZ(z * 100);
      o.setWidth(w * 100);
      o.setHeight(h * 100);
      o.setDepth(depth * 100);
      o.setColor(color);
      this.models.push(o);
      return o;
    }
    robot(p, scale = 1) {
      let o = this.scene.createObject("Robot");
      o.setWidth(80 * scale);
      o.setHeight(50 * scale);
      o.setDepth(180 * scale);
      o.setPosition(p[0] * 100, p[1] * 100);
      o.setZ(0);
      this.models.push(o);
      return o;
    }
    load(index) {
      for (const o of this.models) o.deleteFromScene(this.scene);
      this.models = [];
      for (const o of this.meshes) {
        this.layer.get3DRendererObject().remove(o);
        o.geometry.dispose();
        o.material.dispose();
      }
      this.meshes = [];
      this.m = DEF.missions[index];
      this.index = index;
      this.p = [...this.m.spawn];
      this.g = [...(this.m.patrol?.[0] || [0, 0])];
      this.forward = [1, 0];
      this.patrol = 0;
      this.clock = 0;
      this.notice = 0;
      this.detected = 0;
      this.frozen = 0;
      this.retry = 0;
      this.solved = false;
      this.mode = "move";
      this.path = [];
      this.aim = [0.58, -0.81];
      this.prediction = null;
      this.trace = [];
      this.traceTime = 0;
      this.clueTime = 0;
      this.trap = null;
      this.trapUsed = false;
      this.pending = false;
      this.walls = [
        { r: [-7, -5, 14, 0.3], type: "border" },
        { r: [-7, 4.7, 14, 0.3], type: "border" },
        { r: [-7, -5, 0.3, 10], type: "border" },
        { r: [6.7, -5, 0.3, 10], type: "border" },
      ];
      this.cube(-7, -5, 14, 10, 0.15, "40;76;89", -0.2);
      for (const r of this.m.covers) this.walls.push({ r, type: "cover" });
      for (const r of this.m.reflectors)
        this.walls.push({ r, type: "reflector" });
      for (const w of this.walls)
        this.cube(
          ...w.r,
          w.type === "cover" ? 1.35 : 1,
          w.type === "reflector" ? "85;229;219" : "66;110;140",
        );
      this.hero = this.robot(this.p);
      this.target = this.cube(
        this.m.goal[0] - 0.4,
        this.m.goal[1] - 0.4,
        0.8,
        0.8,
        0.5,
        "255;200;94",
      );
      const sp = this.m.secret.position;
      this.secret = this.cube(
        sp[0] - 0.3,
        sp[1] - 0.25,
        0.6,
        0.5,
        0.5,
        "200;140;245",
      );
      this.secret.hide(true);
      if (this.m.patrol) {
        this.guard = this.robot(this.g, 1.35);
        const r = this.m.gate_rect;
        this.gate = this.cube(...r, 1.2, "225;150;135");
        this.lights = [];
        for (let i = 0; i < 3; i++)
          this.lights.push(
            this.cube(4 + i * 0.65, -1, 0.3, 0.2, 0.25, "70;90;110", 1.5),
          );
      }
      this.layer.setCameraRotationX(34.38);
      this.status("Tippe auf den Boden.");
      this.score();
    }
    activeWalls() {
      return this.walls.concat(
        this.m.gate_rect && !this.open()
          ? [{ r: this.m.gate_rect, type: "gate" }]
          : [],
      );
    }
    open() {
      return (
        this.clock % DEF.gate.period >= DEF.gate.period - DEF.gate.open_seconds
      );
    }
    distance(a, b) {
      return Math.hypot(a[0] - b[0], a[1] - b[1]);
    }
    blocked(p) {
      return (
        p[0] < -6.5 ||
        p[0] > 6.5 ||
        p[1] < -4.5 ||
        p[1] > 4.5 ||
        this.activeWalls().some(
          ({ r }) =>
            p[0] > r[0] - 0.28 &&
            p[0] < r[0] + r[2] + 0.28 &&
            p[1] > r[1] - 0.28 &&
            p[1] < r[1] + r[3] + 0.28,
        )
      );
    }
    ray(o, d, length, walls) {
      let best = null,
        tmax = length;
      for (const w of walls) {
        let r = w.r;
        for (const [value, axis, n] of [
          [r[0], 0, [-1, 0]],
          [r[0] + r[2], 0, [1, 0]],
          [r[1], 1, [0, -1]],
          [r[1] + r[3], 1, [0, 1]],
        ]) {
          if (Math.abs(d[axis]) < 1e-6) continue;
          let t = (value - o[axis]) / d[axis],
            k = 1 - axis,
            p = [o[0] + d[0] * t, o[1] + d[1] * t];
          if (
            t > 0.001 &&
            t < tmax &&
            p[k] >= r[k] - 0.0001 &&
            p[k] <= r[k] + r[k + 2] + 0.0001
          ) {
            tmax = t;
            best = { p, n, t, type: w.type };
          }
        }
      }
      return best;
    }
    norm(d) {
      let l = Math.hypot(...d) || 1;
      return d.map((v) => v / l);
    }
    segment(p, a, b) {
      let d = [b[0] - a[0], b[1] - a[1]],
        t = Math.max(
          0,
          Math.min(
            1,
            ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) /
              (d[0] * d[0] + d[1] * d[1] || 1),
          ),
        );
      return this.distance(p, [a[0] + t * d[0], a[1] + t * d[1]]);
    }
    shot() {
      let d = [...this.aim],
        o = [this.p[0] + d[0] * 0.35, this.p[1] + d[1] * 0.35],
        points = [o],
        length = 28;
      for (let b = 0; b < this.stats().bounces + 2; b++) {
        let hit = this.ray(o, d, length, this.activeWalls());
        if (!hit) {
          points.push([o[0] + d[0] * length, o[1] + d[1] * length]);
          break;
        }
        points.push(hit.p);
        length -= hit.t;
        if (hit.type !== "reflector" || b >= this.stats().bounces) break;
        let dot = d[0] * hit.n[0] + d[1] * hit.n[1];
        d = [d[0] - 2 * dot * hit.n[0], d[1] - 2 * dot * hit.n[1]];
        o = [hit.p[0] + d[0] * 0.003, hit.p[1] + d[1] * 0.003];
      }
      return points;
    }
    navigate(target) {
      const cell = (p) => [
          Math.max(0, Math.min(35, Math.round((p[0] + 6.8) / 0.4))),
          Math.max(0, Math.min(25, Math.round((p[1] + 4.8) / 0.4))),
        ],
        point = (c) => [c[0] * 0.4 - 6.8, c[1] * 0.4 - 4.8],
        key = (c) => c[1] * 36 + c[0];
      let start = cell(this.p),
        end = cell(target);
      if (this.blocked(point(end))) {
        let best = 1e9;
        for (let x = 0; x < 36; x++)
          for (let y = 0; y < 26; y++) {
            let p = point([x, y]),
              d = this.distance(p, target);
            if (!this.blocked(p) && d < best) {
              best = d;
              end = [x, y];
            }
          }
      }
      const queue = [start],
        parent = new Map([[key(start), null]]);
      let found = false;
      for (let i = 0; i < queue.length; i++) {
        let c = queue[i];
        if (key(c) === key(end)) {
          found = true;
          break;
        }
        for (const [dx, dy] of [
          [-1, 0],
          [1, 0],
          [0, -1],
          [0, 1],
          [-1, -1],
          [1, -1],
          [-1, 1],
          [1, 1],
        ]) {
          let n = [c[0] + dx, c[1] + dy];
          if (
            n[0] < 0 ||
            n[0] >= 36 ||
            n[1] < 0 ||
            n[1] >= 26 ||
            parent.has(key(n)) ||
            this.blocked(point(n))
          )
            continue;
          if (
            dx &&
            dy &&
            (this.blocked(point([c[0] + dx, c[1]])) ||
              this.blocked(point([c[0], c[1] + dy])))
          )
            continue;
          parent.set(key(n), c);
          queue.push(n);
        }
      }
      this.path = [];
      if (found) {
        for (let c = end; c; c = parent.get(key(c)))
          this.path.unshift(point(c));
      } else if (this.m.staging) {
        this.say("gate_closed");
        this.navigate(this.m.staging);
      }
    }
    tap(x, y) {
      let rect = this.canvas.getBoundingClientRect(),
        ray = new THREE.Raycaster();
      ray.setFromCamera(
        new THREE.Vector2(
          ((x - rect.left) / rect.width) * 2 - 1,
          -(((y - rect.top) / rect.height) * 2 - 1),
        ),
        this.layer.getRenderer().getThreeCamera(),
      );
      let p = new THREE.Vector3();
      if (
        !ray.ray.intersectPlane(
          new THREE.Plane(new THREE.Vector3(0, 0, 1), 0),
          p,
        )
      )
        return;
      let q = [
        Math.max(-6.4, Math.min(6.4, p.x / 100)),
        Math.max(-4.3, Math.min(4.3, -p.y / 100)),
      ];
      this.touch(q);
    }
    touch(p) {
      if (this.retry) return;
      if (this.mode === "move") this.navigate(p);
      else if (this.mode === "aim")
        this.aim = this.norm([p[0] - this.p[0], p[1] - this.p[1]]);
      else if (this.mode === "predict") this.prediction = p;
      else if (
        this.mode === "trap" &&
        !this.trapUsed &&
        this.distance(p, this.p) < 3.5 &&
        !this.blocked(p) &&
        !this.ray(
          this.p,
          this.norm([p[0] - this.p[0], p[1] - this.p[1]]),
          this.distance(p, this.p),
          this.activeWalls(),
        )
      ) {
        this.trap = p;
        this.trapTime = 12;
        this.trapUsed = true;
        this.mode = "move";
      }
    }
    fire() {
      if (this.pending) return;
      if (this.m.id === "bank" && !this.prediction) {
        this.mode = "predict";
        this.say("predict");
        return;
      }
      this.trace = this.shot();
      this.traceTime = 2.2;
      this.pending = true;
      this.win = false;
      if (this.m.id === "guardian")
        for (let i = 1; i < this.trace.length; i++)
          if (this.segment(this.g, this.trace[i - 1], this.trace[i]) < 0.7)
            this.frozen = Math.max(this.frozen, 0.5);
      for (let i = 1; i < this.trace.length - 1; i++)
        if (
          this.segment(this.m.goal, this.trace[i], this.trace[i + 1]) <
          (this.stats().lens ? 0.7 : 0.6)
        ) {
          this.win = true;
          this.trace = this.trace.slice(0, i + 2);
          this.trace[i + 1] = this.m.goal;
          break;
        }
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
      this.say("hint_" + this.m.id);
      this.score();
    }
    finish(skill) {
      if (this.solved) return;
      this.solved = true;
      let n = this.award("mission:" + this.m.id);
      if (skill) n += this.award("skill:" + this.m.id);
      this.say("success");
      this.path = [];
      this.modal("Geschafft! + " + n + " ★", [
        ["Geheimnisse suchen", "?", () => this.close()],
        ["Nächste Karte", "▶", () => this.menu()],
        [
          "Noch einmal",
          "↻",
          () => {
            this.load(this.index);
            this.close();
            this.say("intro_" + this.m.id);
          },
        ],
      ]);
    }
    ui() {
      const style = document.createElement("style");
      style.textContent =
        "html,body{margin:0;background:#102334!important;overflow:hidden}#eb{position:fixed;inset:0;color:#ecfff7;font:18px system-ui;pointer-events:none}#eb button{pointer-events:auto;color:#eafff5;background:#203f55;border:0;border-radius:14px;min-height:50px;font:14px system-ui;padding:6px;touch-action:manipulation}#eb button b{display:block;color:#61e6cd;font-size:25px}#eb .row{display:flex;gap:4px}#eb .row>*{flex:1}#eb .top{position:absolute;left:12px;right:12px;top:10px;display:flex;gap:8px;align-items:center}#eb .bottom{position:absolute;left:10px;right:10px;bottom:12px}#eb #eb-status{text-align:center;min-height:34px;font-size:14px}#eb .dialog{pointer-events:auto;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#19364a;padding:18px;border-radius:22px;width:min(82vw,440px);box-sizing:border-box;display:flex;flex-direction:column;gap:14px}";
      document.head.appendChild(style);
      this.hud = document.createElement("div");
      this.hud.id = "eb";
      this.hud.innerHTML =
        '<div data-ebui class="top"><strong id="eb-stars" style="color:#ffd56a;flex:1">★ 0</strong><span id="eb-hints">? 0</span><button id="eb-cards">▶ Karten</button><button id="eb-sound">♫ Ton</button></div><div data-ebui class="bottom"><div id="eb-status"></div><div class="row" id="eb-modes"></div><div class="row" id="eb-extra"></div></div><div data-ebui id="eb-dialog" class="dialog"></div>';
      document.body.appendChild(this.hud);
      const button = (text, icon, parent, fn) => {
        let b = document.createElement("button");
        b.innerHTML = "<b>" + icon + "</b>" + text;
        b.onclick = (e) => {
          e.stopPropagation();
          fn();
        };
        parent.appendChild(b);
        return b;
      };
      this.button = button;
      for (const [id, text, icon] of [
        ["move", "Laufen", "♧"],
        ["aim", "Zielen", "⌖"],
        ["predict", "Tipp", "⊙"],
        ["fire", "Schuss", "ϟ"],
        ["trap", "Fangfeld", "◎"],
      ])
        button(text, icon, this.hud.querySelector("#eb-modes"), () => {
          if (id === "trap" && this.m.id !== "guardian") return;
          if (id === "fire") this.fire();
          else {
            this.mode = id;
            this.path = [];
            this.say(id === "predict" ? "predict" : id);
          }
        });
      const row = this.hud.querySelector("#eb-extra");
      button("Hinweis", "?", row, () => this.hint());
      button("Erklären", "♫", row, () => this.say("intro_" + this.m.id));
      button("Ausrüstung", "◇", row, () => this.gear());
      this.hud.querySelector("#eb-cards").onclick = () => this.menu();
      this.hud.querySelector("#eb-sound").onclick = () => {
        this.sound = !this.sound;
        if (!this.sound) {
          if (this.audio) this.audio.pause();
          this.next = null;
          this.important = [];
        }
      };
      this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      this.svg.setAttribute(
        "style",
        "position:absolute;inset:0;width:100%;height:100%;pointer-events:none",
      );
      this.hud.prepend(this.svg);
    }
    score() {
      this.hud.querySelector("#eb-stars").textContent = "★ " + this.total();
      this.hud.querySelector("#eb-hints").textContent = "? " + this.hints();
    }
    status(text) {
      this.hud.querySelector("#eb-status").textContent = text;
    }
    modal(title, actions) {
      let d = this.hud.querySelector("#eb-dialog");
      d.replaceChildren();
      const h = document.createElement("strong");
      h.textContent = title;
      h.style.fontSize = "24px";
      d.appendChild(h);
      for (const [text, icon, fn] of actions) this.button(text, icon, d, fn);
      d.style.display = "flex";
      this.paused = true;
    }
    close() {
      this.hud.querySelector("#eb-dialog").style.display = "none";
      this.paused = false;
    }
    menu() {
      this.modal(
        "ENERGYBLAST",
        DEF.missions
          .map((m, i) => [
            m.title,
            i === 0 ? "↗" : "▣",
            () => {
              this.load(i);
              this.close();
              if (this.audio) this.audio.pause();
              this.next = null;
              this.important = [];
              this.say("intro_" + m.id);
            },
          ])
          .concat([["Weiter", "▶", () => this.close()]]),
      );
    }
    gear() {
      this.modal(
        "Deine Ausrüstung",
        DEF.unlocks
          .map((u) => [
            (this.total() >= u.stars ? "✓ " : u.stars + " ★ ") +
              {
                prism: "Prisma",
                armor: "Rüstung",
                boots: "Stiefel",
                cloak: "Tarnung",
              }[u.id],
            "◇",
            () => {
              if (u.id === "prism" && this.total() >= 100) {
                this.saved.weapon =
                  this.saved.weapon === "prism" ? "pulse" : "prism";
                this.save();
              }
              this.say("upgrade");
            },
          ])
          .concat([["Weiter", "▶", () => this.close()]]),
      );
    }
    line(points, color) {
      if (points.length < 2) return;
      let coords = points.map((p) => {
        let v = new THREE.Vector3(p[0] * 100, -p[1] * 100, 8).project(
          this.layer.getRenderer().getThreeCamera(),
        );
        let r = this.canvas.getBoundingClientRect();
        return (
          r.left +
          (v.x + 1) * 0.5 * r.width +
          "," +
          (r.top + (1 - v.y) * 0.5 * r.height)
        );
      });
      const line = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "polyline",
      );
      line.setAttribute("points", coords.join(" "));
      line.setAttribute("stroke", color);
      line.setAttribute("stroke-width", "3");
      line.setAttribute("fill", "none");
      this.svg.appendChild(line);
    }
    update(dt) {
      if (this.paused || this.background) return;
      this.clock += dt;
      this.traceTime -= dt;
      this.clueTime -= dt;
      this.hintDebounce = Math.max(0, (this.hintDebounce || 0) - dt);
      this.svg.replaceChildren();
      if (this.pending && this.traceTime < 1.45) {
        this.pending = false;
        if (this.win && this.m.id === "bank")
          this.finish(
            this.prediction && this.distance(this.prediction, this.m.goal) < 1,
          );
        else if (this.m.id === "bank") this.say("again");
      }
      if (this.retry > 0) {
        this.retry -= dt;
        if (this.retry <= 0) {
          this.p = [...this.m.spawn];
          this.notice = 0;
          this.trapUsed = false;
        }
      } else if (this.path.length) {
        let t = this.path[0],
          d = this.distance(t, this.p),
          step = this.stats().speed * dt;
        if (d < step) {
          this.p = t;
          this.path.shift();
        } else {
          let n = this.norm([t[0] - this.p[0], t[1] - this.p[1]]),
            q = [this.p[0] + n[0] * step, this.p[1] + n[1] * step];
          if (!this.blocked(q)) this.p = q;
          else this.path = [];
          this.hero.setAngle((Math.atan2(n[1], n[0]) * 180) / Math.PI);
        }
      }
      this.hero.setPosition(this.p[0] * 100, this.p[1] * 100);
      const fade = 1 - this.stats().cloak * 1.4;
      this.hero.get3DRendererObject().traverse((n) => {
        if (n.material) {
          n.material.transparent = true;
          n.material.opacity = fade;
        }
      });
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
      if (this.m.patrol) this.tickGuard(dt);
      const sp = this.m.secret.position,
        dist = this.distance(this.p, sp);
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
        this.say("found");
        this.secret.hide(true);
      }
      if (this.path.length) this.line([this.p, ...this.path], "#6beacf");
      if (this.mode === "aim" || this.mode === "predict")
        this.line(this.shot().slice(0, 2), "#6beacf");
      if (this.traceTime > 0) this.line(this.trace, "#ffd36c");
      if (this.prediction)
        this.line(
          [
            [this.prediction[0] - 0.3, this.prediction[1]],
            [this.prediction[0] + 0.3, this.prediction[1]],
          ],
          "#dcb1ff",
        );
      if (this.clueTime > 0)
        this.line(
          [this.p, this.clueLevel() >= 2 ? sp : this.m.secret.hint_landmark],
          "#ffe795",
        );
    }
    tickGuard(dt) {
      this.frozen = Math.max(0, this.frozen - dt);
      if (!this.frozen) {
        let target = this.m.patrol[(this.patrol + 1) % this.m.patrol.length],
          d = this.distance(this.g, target);
        this.forward = this.norm([
          target[0] - this.g[0],
          target[1] - this.g[1],
        ]);
        if (d < dt * 1.6) {
          this.g = [...target];
          this.patrol = (this.patrol + 1) % this.m.patrol.length;
        } else
          this.g = [
            this.g[0] + this.forward[0] * dt * 1.6,
            this.g[1] + this.forward[1] * dt * 1.6,
          ];
      }
      this.guard.setPosition(this.g[0] * 100, this.g[1] * 100);
      this.guard.setAngle(
        (Math.atan2(this.forward[1], this.forward[0]) * 180) / Math.PI,
      );
      if (this.trap) {
        this.trapTime -= dt;
        this.line(
          [
            [this.trap[0] - 0.7, this.trap[1]],
            [this.trap[0] + 0.7, this.trap[1]],
          ],
          "#a3f1ca",
        );
        if (this.distance(this.g, this.trap) < 1.05) {
          this.frozen = 3.5;
          this.trap = null;
        } else if (this.trapTime < 0) this.trap = null;
      }
      const distance =
          5.5 * (1 - this.stats().cloak) * (this.stats().quiet ? 0.9 : 1),
        v = this.norm([this.p[0] - this.g[0], this.p[1] - this.g[1]]),
        seen =
          !this.frozen &&
          this.distance(this.p, this.g) < distance &&
          v[0] * this.forward[0] + v[1] * this.forward[1] >
            Math.cos((35 * Math.PI) / 180) &&
          !this.ray(
            this.g,
            v,
            this.distance(this.p, this.g) - 0.02,
            this.walls,
          );
      this.notice = Math.max(0, this.notice + (seen ? dt : -dt * 2));
      if (this.notice >= this.stats().grace && !this.retry) {
        this.detected++;
        this.retry = 0.9;
        this.path = [];
        this.say("seen");
      }
      const angle = Math.atan2(this.forward[1], this.forward[0]);
      const fan = [this.g];
      for (let i = 0; i <= 20; i++) {
        let a = angle + ((-35 + i * 3.5) * Math.PI) / 180,
          d = [Math.cos(a), Math.sin(a)],
          hit = this.ray(this.g, d, distance, this.walls);
        fan.push(
          hit
            ? hit.p
            : [this.g[0] + d[0] * distance, this.g[1] + d[1] * distance],
        );
      }
      const polygon = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "polygon",
      );
      polygon.setAttribute(
        "points",
        fan
          .map((p) => {
            let v = new THREE.Vector3(p[0] * 100, -p[1] * 100, 4).project(
                this.layer.getRenderer().getThreeCamera(),
              ),
              r = this.canvas.getBoundingClientRect();
            return (
              r.left +
              (v.x + 1) * 0.5 * r.width +
              "," +
              (r.top + (1 - v.y) * 0.5 * r.height)
            );
          })
          .join(" "),
      );
      polygon.setAttribute("fill", "#eab06455");
      this.svg.appendChild(polygon);
      this.gate.setDepth(this.open() ? 12 : 120);
      for (let i = 0; i < 3; i++)
        this.lights[i].setColor(
          this.clock % 8 >= 3 + i ? "104;246;198" : "70;90;110",
        );
      if (
        !this.solved &&
        this.p[1] < -1.4 &&
        this.distance(this.p, this.m.goal) < 0.8
      )
        this.finish(this.detected === 0);
    }
  }
  runtimeScene.energyblast = new Pilot(runtimeScene);
  globalThis.__energyblast = runtimeScene.energyblast;
}
runtimeScene.energyblast.update(
  Math.min(0.05, runtimeScene.getElapsedTime() / 1000),
);
