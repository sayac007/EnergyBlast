// Pinned local tooling path; override with ENERGYBLAST_GD_TOOLS for another installation.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const base = process.env.ENERGYBLAST_GD_TOOLS || "/tmp/energyblast-gd-tools";
const { gd, exportProject } = await import(
  pathToFileURL(path.join(base, "node_modules/gdcore-tools/src/index.mjs"))
);
const p = gd.ProjectHelper.createNewGDJSProject();
p.setName("EnergyBlast Touch Pilot");
p.setVersion("0.1.0");
p.setPackageName("org.example.energyblast.gdevelop");
p.setGameResolutionSize(720, 1280);
p.setOrientation("default");
p.setProjectFile(path.join(root, "pilots/gdevelop/game.json"));
p.setPlayableWithMobile(true);
p.setPlayableWithKeyboard(false);
p.setPlayableWithGamepad(false);
p.setFirstLayout("Pilot");
fs.mkdirSync(path.join(root, "pilots/gdevelop/assets"), { recursive: true });
const scene = p.insertNewLayout("Pilot", 0);
const layer = scene.getLayer("");
layer.setRenderingType("3d");
layer.setCameraType("orthographic");
layer.setAmbientLightColor(200, 220, 230);
const objects = scene.getObjects();
objects.insertNewObject(p, "Scene3D::Cube3DObject", "Cube", 0);
objects.insertNewObject(p, "Scene3D::Model3DObject", "Robot", 1);
const raw = new gd.SerializerElement();
p.serializeTo(raw);
const data = JSON.parse(gd.Serializer.toJSON(raw));
data.firstLayout = "Pilot";
data.layouts[0].r = 16;
data.layouts[0].v = 35;
data.layouts[0].b = 52;
data.properties.disableRuntimeMetrics = true;
data.properties.showGDevelopSplash = false;
data.properties.loadingScreen.showGDevelopSplash = false;
data.properties.loadingScreen.minDuration = 0;
data.properties.watermark.showWatermark = false;
const cube = data.layouts[0].objects.find((x) => x.name === "Cube");
for (const face of ["front", "back", "left", "right", "top", "bottom"])
  cube.content[face + "FaceResourceName"] = "white.png";
const original = data.layouts[0].objects.find((x) => x.name === "Robot");
original.content.modelResourceName = "robot.glb";
original.content.width = 80;
original.content.height = 50;
original.content.depth = 180;
data.resources.resources = [
  {
    kind: "model3D",
    name: "robot.glb",
    file: "assets/robot.glb",
    userAdded: true,
  },
  {
    kind: "image",
    name: "white.png",
    file: "assets/white.png",
    userAdded: true,
  },
];
const manifest = JSON.parse(
  fs.readFileSync(path.join(root, "shared/audio/de/manifest.json"), "utf8"),
);
const audio = Object.fromEntries(manifest.clips.map((c) => [c.id, c]));
for (const c of manifest.clips) {
  fs.copyFileSync(
    path.join(root, "shared/audio/de", c.file),
    path.join(root, "pilots/gdevelop/assets", c.file),
  );
  data.resources.resources.push({
    kind: "audio",
    name: c.file,
    file: "assets/" + c.file,
    userAdded: true,
  });
}
const code = fs
  .readFileSync(path.join(root, "pilots/gdevelop/pilot.js"), "utf8")
  .replace(
    "/*ENERGYBLAST_DEF*/ {}",
    fs.readFileSync(path.join(root, "shared/pilot.json"), "utf8"),
  )
  .replace("/*ENERGYBLAST_AUDIO*/ {}", JSON.stringify(audio));
data.layouts[0].events = [
  {
    type: "BuiltinCommonInstructions::JsCode",
    inlineCode: code,
    parameterObjects: "",
    useStrict: true,
    eventsSheetExpanded: false,
  },
];
fs.copyFileSync(
  path.join(root, "shared/assets/robot.glb"),
  path.join(root, "pilots/gdevelop/assets/robot.glb"),
);
fs.writeFileSync(
  path.join(root, "pilots/gdevelop/game.json"),
  JSON.stringify(data, null, 2) + "\n",
);
const { loadProject } = await import(
  pathToFileURL(path.join(base, "node_modules/gdcore-tools/src/index.mjs"))
);
const loaded = await loadProject(path.join(root, "pilots/gdevelop/game.json"));
const out =
  process.env.ENERGYBLAST_GD_OUTPUT || "/tmp/energyblast-gdevelop-web";
exportProject(loaded, out);
const index = path.join(out, "index.html");
fs.writeFileSync(
  index,
  fs
    .readFileSync(index, "utf8")
    .replace(/<script[^>]+src="[^"]+\.wasm"[^>]*><\/script>/g, ""),
);
fs.mkdirSync(path.join(out, "licenses"), { recursive: true });
for (const name of fs.readdirSync(path.join(root, "shared/notices")))
  fs.copyFileSync(
    path.join(root, "shared/notices", name),
    path.join(out, "licenses", name),
  );
for (const name of ["LICENSE.txt", "MODEL_CARD.txt"])
  fs.copyFileSync(
    path.join(root, "shared/audio/de", name),
    path.join(out, "licenses", "AUDIO_" + name),
  );
console.log("Exported GDevelop 5.6.269 to", out); // Community exporter emitted a WASM file as a script; keep binary, remove only its invalid script tag.
