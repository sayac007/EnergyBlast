# Bauen und prüfen

Vom Repository-Hauptverzeichnis ausführen. Build-Ausgaben gehören außerhalb des
Checkouts oder unter das ignorierte `build/`. Keine Schlüssel ins Repository.
Die Cloud-Vorgaben liegen unter `/workspace/tools`; die Python-Buildskripte nehmen
`--tools` entgegen. Andere Installationen müssen dieselbe beschriebene Struktur
bereitstellen. Vorbereitete Werkzeuge sind keine im Repository enthaltene SDKs.

## Voraussetzungen

- Python 3.12, FFmpeg, Node.js >=18; hier Node 24.
- Godot **4.7.2 official** und exakt passende Android-Exportvorlagen. GLES3 /
  Compatibility, ARM64; ETC2/ASTC-Import ist aktiviert.
- JDK 17, Android SDK platform 36, build-tools **36.1.0**, platform-tools.
- GDevelop: reale **5.6.269** Core/Runtime-Dateien aus dem nachstehenden gepinnten
  Community-Werkzeug, kein selbst geschriebener Ersatz-Renderer.
- GDevelop Android: Gradle **8.11.1**, Android Gradle Plugin **8.6.1**. Erstmaliges
  Auflösen benötigt Zugang zu Google Maven/Maven Central. Plugin 8.6.1 warnt
  normalerweise bei compileSdk 36; die Warnung wird ausdrücklich unterdrückt.
  Das ist ein gebauter Debug-Pilot, keine Zertifizierung dieser Toolchain für Play.
- Browserprüfung: `python3 -m pip install playwright`; Chromium, hier
  `/usr/bin/chromium`. Kein Browserdownload nötig, wenn dieser bereits installiert ist.

## Gemeinsame Dateien und GDevelop-Export

```bash
npm ci --prefix tools/gdevelop-tools --ignore-scripts
export ENERGYBLAST_GD_TOOLS="$PWD/tools/gdevelop-tools"
export ENERGYBLAST_GD_OUTPUT=/tmp/energyblast-gdevelop-web
python3 tools/sync_assets.py
python3 tools/sync_unity.py
node tools/gdevelop_export.mjs
```

Im aktuellen Cloud-Workspace ist dasselbe gepinnte Werkzeug bereits unter
`/tmp/energyblast-gd-tools` installiert, dem Standard des Exportskripts.
`pilots/gdevelop/game.json` ist das daraus erzeugte native GDevelop-Projekt.
Eine neue Godot-Importdatei darf anschließend vom Editor erzeugt werden.

Der Community-Exporter setzte irrtümlich den Draco-WASM-Decoder als JavaScript-
`<script>` ein. Das Exportskript entfernt **nur diesen ungültigen Script-Verweis**;
der Decoder selbst bleibt enthalten. Ein Browserstart mit JavaScript-Fehlern gilt
nicht als bestandener Export.

## Aktuelle Tests

```bash
python3 tools/check_shared.py
python3 tools/check_godot.py
python3 tools/check_gdevelop.py
```

- `check_shared`: Regeln/Modellkopien, Manifest-Hashes, alle 19 Ogg-Dateien tatsächlich
  mit FFmpeg decodieren, Dauer, nutzbare Pegel und Headroom nach Wiedergabeverstärkung;
  begrenzte Belohnungsökonomie und Android-Quellkonfiguration.
- `check_godot`: 43 Prüfungen im echten Godot, darunter Touch-Projektion, Abpraller,
  Deckung, Torfenster, Missionen/Belohnungen; getrennte Schreib-/Neustartprozesse für
  lokalen Fortschritt. Standardpfad mit `--godot /pfad/zu/godot` überschreiben.
  Testaudio ist hier ausgeschaltet: FFmpeg und der Browser prüfen Medien getrennt.
- `check_gdevelop`: echter exportierter Runtime im lokalen HTTP-Server, Chromium mit
  WebGL und Touch-Emulation, Missionen, Hinweise, Neustart, Ausrüstung, Hintergrund-
  Pause und vollständige Sprachwarteschlange. Fehler/externe Requests werden erfasst.
  Es wird kein Android-Touch-/Leistungsnachweis daraus abgeleitet.

Für den unabhängigen optionalen ASR-Screen sind `sherpa_onnx`, NumPy und lokal
bereitgestellte Whisper-small-int8-Dateien erforderlich:

```bash
/workspace/tools/piper-env/bin/python tools/screen_voice.py \
  --model /workspace/tools/asr/sherpa-onnx-whisper-small \
  --output /tmp/energyblast-asr.json
```

Spracherzeugung ist für Builds **nicht nötig**. `tools/prepare_audio.py --help`
beschreibt den optionalen Offline-Bau mit dem gepinnten Qwen-Modell. Dabei werden
nur erlaubte passende Ausgangsclips gelesen, vollständige Sätze erzeugt und
Modell-/Dateihashes geprüft. Niemals private Sprachmodelle/Schlüssel committen.

## Android-APKs

```bash
python3 tools/build_android.py --output /tmp/energyblast-godot-build
python3 tools/build_gdevelop_android.py --output /tmp/energyblast-gdevelop-build
```

Ausgabeverzeichnisse müssen neu sein. Godot erzeugt einmal einen ausschließlich
für diese Piloten verwendeten Entwicklungsschlüssel **außerhalb** des Repositories
unter `<tools>/energyblast-pilot-signing/debug.keystore`. Der GDevelop-Bau verwendet
denselben Debug-Schlüssel. Die bekannten Android-Debug-Parameter sind keine
Release-Zugangsdaten. Diese APKs sind nicht mit einer Play-Upload-Identität signiert.

GDevelop verpackt den **realen HTML5/WebGL-Export** in einer kleinen eigenen
Android-WebView-Hülle. Alle Dateien werden über einen abgefangenen lokalen HTTPS-
Ursprung aus APK-Assets gelesen; keine Internet-/Medienberechtigung, kein nativer
JavaScript-Bridge-Zugriff, keine externen Navigationsziele. Android System WebView
bleibt eine Geräteabhängigkeit. Lokal gespeicherte Sterne liegen im privaten
App-/WebView-Speicher; Backup ist deaktiviert.

Der GDevelop-Bau kann nach erfolgreicher Abhängigkeitsauflösung `--offline` nutzen.
Bei Unternehmens-/Cloud-Proxys liest der Java-Prozess nicht automatisch denselben
CA-Speicher wie Python. Optional `--trust-store /pfad/zum/lokalen/cacerts` nutzen;
HTTPS-Proxy ohne Zugangsdaten wird übernommen. Zertifikatsprüfung bleibt aktiv.
Die Android-Benutzerverzeichnisse sind pro Bau isoliert, ohne `$HOME` umzubiegen.

Die Befehle erzeugen funktional nachvollziehbare Builds, keine zugesicherte
Bit-für-Bit-Reproduktion (Zeitstempel/Signaturcontainer können abweichen).
Die Skripte schreiben APK, Export-/Build-Log, Manifestauszug, Signaturauszug und
`verification.json` mit Bytes, SHA-256, Commit und Dirty-Status. Sie prüfen Paket,
Version, fehlende Berechtigungen, Debug-Signatur und ZIP-Ausrichtung mit 16-KB-
Seiten. Ein erfolgreicher Bau beweist keinen Start auf einem echten Gerät.
Die abschließenden Downloads werden vom bereits committeten sauberen Quellstand
gebaut; ihre Metadaten nennen genau diesen Quellcommit.

## Unity

Siehe `pilots/unity/README.md`. Ein aktivierter Unity Editor mit Android-Modulen
ist nötig. Die mitgelieferten drei C#-Dateien wurden lediglich mit Tree-sitter auf
Syntaxfehler geprüft. Das ist **keine** Unity-API-/Compilerprüfung.
Keine Unity-APK oder Aktivierung wird vorgetäuscht.
