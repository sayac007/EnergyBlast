# Bauen und prüfen — Defold 0.4

Vom Repository-Hauptverzeichnis ausführen. Ausgaben außerhalb des Checkouts;
keine Schlüssel in Git. Aktuell wird Defold weiterentwickelt. Die unveränderten
GDevelop-0.3-/Godot-0.2-Anleitungen bleiben über [Meilenstein 02](MILESTONE_02.md)
und dessen feste Quell-/APK-Referenzen erreichbar.

## Werkzeuge und Vorbereitung

- Python 3.12, FFmpeg; NumPy für die optionale eigene Audiosynthese.
- Defold **1.14.0**, Bob und native Engine; Java **25** aus dessen offizieller
  Linux-Distribution. SDK-Dateien sind in `tools/defold-sdk.json` per Hash gepinnt.
- Android SDK platform **36**, build-tools **36.1.0**, JDK 17 für die APK-Prüfwerkzeuge.
  Standardverzeichnis `/workspace/tools`, über `--tools` anpassbar.
- Native Linux-Tests: Xvfb/OpenGL, `libX11.so.6`, `libXtst.so.6`, OpenAL Soft mit
  Null- und WAVE-Backend. Die Audioausgabe wird tatsächlich aufgezeichnet.

```bash
python3 tools/setup_defold.py --output /tmp/energyblast-defold-tools
python3 tools/sync_defold.py
```

Defold konsumiert `shared/defold04.json` und `shared/assets/defold04`. Die alte
`shared/raid.json` wird zusätzlich als unveränderte Arenageometrie für Kampf-
Regressionsfixtures mitgeliefert. GDevelop-/Godot-Projekte und Exporte für diese
Iteration nicht neu erzeugen; ihre aktuellen Vergleichsdateien bleiben unverändert.

Optionale Neuerzeugung der eigenen Modelle und Töne:

```bash
blender -b --python tools/make_defold04_models.py
python3 tools/make_defold_music.py
python3 tools/sync_defold.py
```

Danach Herkunftshashes in `shared/asset-origins.json` aktualisieren und prüfen.
Blender **4.3.2** wurde hier verwendet. Keine Bilder-/Modell-/Musikdownloads nötig.
Schrift und Engine-/Modellhinweise bleiben mit ihren Fremdlizenzen enthalten.

## Aktuelle Prüfungen

```bash
python3 tools/check_shared.py
python3 tools/check_defold.py
```

- **check_shared:** sieben Testgruppen. Daten/Modelle/Provenienz, unveränderte
  andere Engine-Kopien, Hashwerte, tatsächliche FFmpeg-Decodierung von 30 Sprach-
  aufnahmen und Musik/Explosion, Pegel/Dauer/Schleifenübergang, begrenzte Sterne,
  Offline-Manifeste und kein berechneter Vorschaupfad in der GUI.
- **check_defold:** baut zuerst; bei Fehlern läuft niemals eine alte Binärdatei.
  Native **76** Prüfungen: 42 beibehaltene Fälle plus 34 neue. Drei erweiterte
  Sektoren werden mit bewegten Geschossen abgeschlossen. Kamera, 0,30-s-Schwelle,
  langsame Frames, schnelle Wischbewegungen, Abbruch/Finger und Effekte geprüft.
- Danach getrennte Speicherprozesse für Sterne, Ausrüstung, Hinweise und
  Musikpräferenz. Echte XTest-Eingaben prüfen Menü, kurzen Tipp und langen Hold
  am selben Punkt, FEUER sowie TON aus/an mit angehaltenem Ansagetimer.
- `check_defold_audio.py` zeichnet drei echte native Ausgaben mit OpenALs
  WAVE-Backend auf: Musik an, Musik aus und Musik/Sprache/Explosion gemischt.
  Signal/RMS und Pegel werden geprüft. Das ist keine menschliche Klangabnahme.

`--sdk` ändert den SDK-Pfad. Der Starter isoliert private Zustandsverzeichnisse
und beendet bei Timeout seine gesamte Prozessgruppe. Laufzeitberichte verbleiben
unter temporären Pfaden, keine Einzelprotokolle pro Testlauf in Git.

Die ältere reine GDevelop-/Godot-Regression ist weiterhin ausführbar:

```bash
python3 tools/check_godot.py
python3 tools/check_gdevelop_combat.py
```

GDevelop benötigt dafür den passenden gepinnten 0.3-Webexport; die bisherige
Anleitung ist im [0.3-Dokumentationssnapshot](https://github.com/sayac007/EnergyBlast/blob/cd9dc64/docs/BUILD_AND_TEST.md)
erhalten. Für 0.4 werden diese unveränderten Apps nicht erneut gebaut.

## Bedienansage und Musik

Bereits enthaltene Aufnahmen reichen für Builds. Die neue Ansage liegt separat
in `shared/audio/defold04/manifest.json`; alte Audioquellen bleiben unverändert.
Optionale Offline-Erzeugung derselben synthetischen Serena-Stimme:

```bash
/workspace/tools/qwen-env/bin/python tools/prepare_defold_voice.py --model /workspace/tools/qwen-female
```

Unabhängiger ASR-Screen, ohne Referenztext als Prompt:

```bash
/workspace/tools/piper-env/bin/python tools/screen_voice.py \
  --model /workspace/tools/asr/sherpa-onnx-whisper-small \
  --manifest shared/audio/defold04/manifest.json \
  --output /tmp/energyblast-defold04-asr.json
```

Musik-/Klangherkunft, Hash und Messwerte in `shared/audio/defold04/music.json`.
60 Sekunden, 32 Takte bei 128 BPM, vollständig eigene Synthese. Statischer
Musik-Gain **1**; Laufzeitpegel 0,28 im Spiel, 0,16 im Menü, 0,065 unter Ansagen.
Master-Gain 0,75, SFX separat gedämpft. Musikpräferenz wird lokal gespeichert.
Keine Schauspieleraufnahme, Silbenmontage oder kopierte Referenzmelodie.

## Android-APK

```bash
python3 tools/build_defold_android.py --output /tmp/energyblast-defold04-build
```

Ausgabeverzeichnis muss neu sein. Native ARM64-App, **0.4.0 / Code 4**,
`org.example.energyblast.defold`, minSdk 24, targetSdk 36. Derselbe ausschließlich
für Entwicklung angelegte Schlüssel außerhalb des Repositories:
`<tools>/energyblast-pilot-signing/debug.keystore`. Keine Release-/Play-Identität.
Die temporäre bekannte Debug-Passwortdatei wird nach dem Export gelöscht.

Ausgabe: APK, Build-/Signatur-/Manifestauszüge und `verification.json` mit Quell-
commit, sauberem/dirty Status, Buildzeit, Größe, Hash, Paket/Version, Signatur und
ZIP-Ausrichtung. Zusätzlich vor Veröffentlichung: ZIP-CRC, keine Schlüsseldateien,
Zertifikatsgleichheit mit 0.3 und Hash der veröffentlichten Download-Datei prüfen.

Abschlussexport vom sauberen Quellcommit, anschließend APK/Metadaten separat
versionieren. Das ist ein nachvollziehbarer Bauweg, keine Zusicherung bitidentischer
Ausgaben oder einer bereits bestandenen physischen Android-Installation.
Keine Actions-Artefaktflut, PRs, Merges oder automatischen Releases.
