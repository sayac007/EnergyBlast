# Bauen und prüfen — Aurora Raid 0.3

Vom Repository-Hauptverzeichnis ausführen. Build-Ausgaben außerhalb des Checkouts
oder unter ignoriertem `build/`; keine Schlüssel in Git. Die bisherigen 0.1-
Tests bleiben separat ausführbar, sind aber keine Tests der neuen Startszenen.

## Werkzeuge

- Python 3.12, FFmpeg, Node.js >=18; hier Node 24.
- Godot **4.7.2 official** mit exakt passenden Android-Vorlagen; Compatibility /
  OpenGL ES 3, ARM64, ETC2/ASTC-Import aktiviert.
- Android SDK platform **36**, build-tools **36.1.0**, platform-tools; JDK 17 für
  Godot/GDevelop. Standard-Toolverzeichnis `/workspace/tools`, via `--tools` änderbar.
- GDevelop: `gdcore-tools` **2.0.0-gd-v5.6.269-autobuild**, `gdexporter`
  **4.0.0-beta7**, exakt im Lockfile. Tatsächliche GDJS-3D-Laufzeit.
- GDevelop Android: Gradle **8.11.1**, AGP **8.6.1**. compileSdk-36-Warnung dieses
  älteren Plugins ausdrücklich unterdrückt; keine daraus abgeleitete Play-Freigabe.
- Defold **1.14.0**: Bob und native Engine sowie Java **25** aus derselben offiziellen
  Linux-Distribution. `tools/setup_defold.py` lädt gepinnte Dateien nach `/tmp`.
- Browserprüfung: Python-Paket `playwright`, Chromium unter `/usr/bin/chromium`.
  Native Render-/Defold-Prüfungen brauchen Xvfb und OpenGL; hier Software-Mesa.

## Vorbereitung

```bash
npm ci --prefix tools/gdevelop-tools --ignore-scripts
export ENERGYBLAST_GD_TOOLS="$PWD/tools/gdevelop-tools"
python3 tools/setup_defold.py --output /tmp/energyblast-defold-tools
python3 tools/sync_defold.py
node tools/gdevelop_export.mjs
```

Der Standardpfad des Exportskripts ist `/tmp/energyblast-gd-tools`. Dieser
temporäre Cache kann nach einem Umgebungsneustart fehlen. Die obigen Befehle
installieren das gepinnte Werkzeug im Checkout und setzen den passenden
`ENERGYBLAST_GD_TOOLS`-Pfad.
`ENERGYBLAST_GD_OUTPUT` ändert den HTML5-Ausgabepfad; die Browserprüfung nutzt
standardmäßig `/tmp/energyblast-gdevelop-web`.

Die beiden aktiven Versuche konsumieren `shared/raid.json` und
`shared/assets/raid/`. Godot bleibt mit `shared/combat.json` und dem alten
`shared/assets/shooter/` unverändert. `sync_assets.py` und `sync_unity.py` gehören
zum älteren Vergleich; für diese Runde nicht ausführen. Die GDevelop-/Defold-
Kopien werden durch ihren Export beziehungsweise `sync_defold.py` aktualisiert.

Optionale Neuerzeugung der Originalmodelle/Töne:

```bash
blender -b --python tools/make_raid_models.py
```

Danach synchronisieren, neu exportieren und die Herkunftshashes aktualisieren.
Kein Bilder-/Assetdownload ist zur Erzeugung der eigenen 3D-Modelle erforderlich.
Die unveränderte zusätzliche Lilita-One-Schrift wird mit OFL-Hinweis mitgeliefert.

## Aktuelle Tests

```bash
python3 tools/check_shared.py
python3 tools/check_godot.py
python3 tools/check_gdevelop_combat.py
python3 tools/check_defold.py
```

- `check_shared`: Regeln/Modellkopien, Herkunft/Audiohashes, 26 bestehende und drei neue Ogg-Dateien mit
  FFmpeg decodiert, Dauer/Pegel/Verstärkung, begrenzte Belohnungen, Android-Manifeste
  und der tatsächlich verwendete Defold-Render-Einstieg.
- `check_godot`: 43 alte Kern- und 24 neue Kampfprüfungen, Touch-/Weltprojektion,
  wirkliche Schüsse/Schild/Treffer/Deckung/Dash, Sterne/Hint-Migration und getrennte
  Speicherprozesse. `--godot /pfad/zu/godot` überschreibt den Cloud-Pfad.
- `check_gdevelop_combat`: 51 Prüfungen der realen exportierten WebGL-Laufzeit, echter Touch-Drag über
  Chromium/CDP, sichtbare Deckung gegen Kollisionskoordinaten, Kampf, gespeicherte
  Sterne/alte Hinweise, Neustartfläche, keine JS-Seitenfehler/externe Requests.
- `check_defold`: baut zuerst und stoppt bei Fehlern, startet dann die native Engine
  in Xvfb. 42 Prüfungen einschließlich Eingabeprojektion, Kampf und neuem Relais-/Boss-Sektor, anschließend
  getrennte Prozesse für Speichern/Neustart und echter nativer Menü-/FEUER-Klick via XTest. Benötigt `libXtst.so.6` / `libX11.so.6`. Sound nutzt ein Nullgerät; keine
  menschliche Audioabnahme. `--sdk` überschreibt das externe SDK-Verzeichnis.

Zusätzliche unveränderte GDevelop-Regression (separater Export, anschließend den
aktuellen Export wiederherstellen):

```bash
ENERGYBLAST_GD_LEGACY=1 ENERGYBLAST_GD_OUTPUT=/tmp/energyblast-gdevelop-legacy node tools/gdevelop_export.mjs
ENERGYBLAST_GD_OUTPUT=/tmp/energyblast-gdevelop-legacy python3 tools/check_gdevelop.py
node tools/gdevelop_export.mjs
```

Der Community-Exporter setzte einen WASM-Decoder fälschlich als JavaScript-Script
in HTML ein. Nur dieser ungültige Script-Verweis wird entfernt; der Decoder bleibt.
GDevelop braucht außerdem die explizite glTF-Achsenanpassung für sichtbare Deckung.
Defold braucht `bootstrap.render`, nicht einen unbeachteten `render.render`-Eintrag.

## Sprachausgabe

Die drei neuen Raid-Aufnahmen liegen separat unter `shared/audio/raid`, damit
Godots 0.2-Assets unverändert bleiben. Optionale Erzeugung:

```bash
/workspace/tools/qwen-env/bin/python tools/prepare_raid_audio.py --model /workspace/tools/qwen-female
```

Für deren unabhängigen ASR-Screen beim folgenden Befehl zusätzlich
`--manifest shared/audio/raid/manifest.json` angeben; standardmäßig werden die
26 erhaltenen Aufnahmen geprüft.


Bereits enthaltene Aufnahmen reichen für Builds. Vier genehmigte alte Clips,
15 ältere Pilotansagen und sieben neue Kampfansagen stehen mit Text/Hash/Quelle
im Manifest. Im neuen Spiel werden die kurzen Kampfansagen verwendet. Es werden
keine Silben zusammengeschnitten und keine Schauspielerstimmen nachgeahmt.

Optionaler unabhängiger ASR-Screen mit lokalem Whisper-small-int8:

```bash
/workspace/tools/piper-env/bin/python tools/screen_voice.py \
  --model /workspace/tools/asr/sherpa-onnx-whisper-small \
  --output /tmp/energyblast-asr.json
```

`tools/prepare_audio.py --help` beschreibt die optionale Offline-Erzeugung mit
gepinntem Qwen-Modell/Serena. Keine Modellgewichte oder privaten Aufnahmen im Repo.
ASR ist kein menschlicher Verständlichkeits-/Betonungsnachweis.

## Die zwei aktuellen Android-APKs

```bash
python3 tools/build_gdevelop_android.py --output /tmp/energyblast-gdevelop-build
python3 tools/build_defold_android.py --output /tmp/energyblast-defold-build
```

Ausgabeverzeichnisse müssen neu sein. Godot verwendet einen für diese Piloten
angelegten Entwicklungsschlüssel außerhalb des Repositories unter
`<tools>/energyblast-pilot-signing/debug.keystore`; die beiden anderen verwenden
denselben Debug-Schlüssel. Keine Play-Upload-Identität und keine Release-Secrets.
Defolds bekannte Debug-Passwortdatei liegt temporär nur im externen Buildordner
und wird nach dem Aufruf entfernt.

GDevelop verpackt die echte GDJS/WebGL-Laufzeit in eine eigene lokale Android-
WebView-Hülle. Keine Internet-/Medienberechtigung, keine JavaScript-Native-Bridge,
keine externen Navigationsziele. Die System-WebView bleibt eine Geräteabhängigkeit.
Defold und Godot verwenden native ARM64-Engines. Alle Spielstände bleiben im
privaten App-Speicher, Backup ist deaktiviert.

GDevelop unterstützt nach Auflösung seiner Abhängigkeiten `--offline` und bei
Cloud-Proxys `--trust-store /lokaler/pfad/cacerts`. Zertifikatsprüfung bleibt an.
Die Android-/Java-Benutzerverzeichnisse sind isoliert; `$HOME` wird nicht umgebogen.

Die Skripte erzeugen APK, technische Auszüge und `verification.json`: Paket,
Version 0.3.0 / Code 3, fehlende Berechtigungen, deaktiviertes Backup, gültige
Entwicklungssignatur, ZIP-Ausrichtung mit 16-KB-Seiten, Größe, SHA-256 und Quellcommit.
Das sind nachvollziehbare Befehle, keine zugesicherte Bit-für-Bit-Reproduktion.
Keine Aussage über eine auf echter Hardware bereits bestandene Installation.

Abschlussdateien entstehen vom sauberen Quellcommit; anschließend kommen APKs und
Provenienz in einen eigenen Download-Commit. Laufzeitlogs bleiben außerhalb von
Git, keine CI-Artefaktflut und kein automatisches Release/PR/Merge.
