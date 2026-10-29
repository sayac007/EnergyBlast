# Bauen und prüfen — Defold 0.13.0

Vom Repository-Hauptverzeichnis ausführen. Ausgaben außerhalb des Checkouts;
keine Schlüssel in Git. Aktuell wird Defold weiterentwickelt. Die unveränderten
GDevelop-0.3-/Godot-0.2-Anleitungen bleiben über [Meilenstein 02](MILESTONE_02.md)
und dessen feste Quell-/APK-Referenzen erreichbar.

## Werkzeuge und Vorbereitung

- Python 3.12, FFmpeg und NumPy für Geometrie-/Medienprüfungen und optionale Synthese.
- Defold **1.14.0**, Bob und native Engine; Java **25** aus dessen offizieller
  Linux-Distribution. SDK-Dateien sind in `tools/defold-sdk.json` per Hash gepinnt.
- Android SDK platform **36**, build-tools **36.1.0**, JDK 17 für die APK-Prüfwerkzeuge.
  Standardverzeichnis `/workspace/tools`, über `--tools` anpassbar.
- Pillow für echte native Screenshots und die Pixelprüfung; Blender/Cycles mit
  deaktiviertem Denoising für die optionalen Originalporträts.
- Native Linux-Tests: Xvfb/OpenGL, `libX11.so.6`, `libXtst.so.6`, OpenAL Soft mit
  Null- und WAVE-Backend. Die Audioausgabe wird tatsächlich aufgezeichnet.

```bash
python3 tools/setup_defold.py --output /tmp/energyblast-defold-tools
python3 tools/sync_defold.py
```

Defold konsumiert `shared/defold04.json`, Weltgeometrie aus `shared/assets/defold06` und originale Animationsbilder aus `shared/assets/defold07`. Die alte
`shared/raid.json` wird zusätzlich als unveränderte Arenageometrie für Kampf-
Regressionsfixtures mitgeliefert. GDevelop-/Godot-Projekte und Exporte für diese
Iteration nicht neu erzeugen; ihre aktuellen Vergleichsdateien bleiben unverändert.

Optionale Neuerzeugung der eigenen Modelle und Töne:

```bash
blender -b -t 4 --python tools/make_defold06_models.py
python3 tools/make_defold_ui.py
python3 tools/update_defold06_provenance.py
python3 tools/make_defold_music.py
python3 tools/sync_defold.py
```

Der neue passierbare Schutzort wird durch `blender -b --python tools/make_sanctuary.py`
aus eigener Geometrie erzeugt und unter `shared/assets/defold10` versioniert.
Für reguläre Builds ist auch hier keine Neuerzeugung nötig.

Zusätzlich aktiv: `shared/assets/defold09` mit sechs neuen Original-Bodenbildern
und analytischen Effektquads. Reimport: `python3 tools/import_defold09_art.py
--sources /tmp/sources.json` mit einer JSON-Zuordnung der sechs Missions-IDs zu
ihren versionierten Original-PNGs. Keine Bildgenerierung für den Build nötig.

Die ursprünglichen zehn generierten Illustrations-/Animationsquellen liegen in
`shared/assets/defold07/*-original.png`; `PROVENANCE.json` enthält ihre Hashes.
Für einen normalen Build ist kein Bildgenerator nötig. Der optionale technische
Import lässt sich mit einer JSON-Zuordnung der IDs hero/dragon/fox/enemies/icons/
cards/floor/lobby/explosion/props zu diesen Dateien wiederholen:
`python3 tools/import_defold07_art.py --sources /tmp/sources.json`.
Das ist eine Atlas-Aufbereitung, keine Zusicherung identischer neuer KI-Erzeugung.
Weltgeometrie separat erneuern: Blender-Befehl mit `-- --world-only` ergänzen.
Die aktuelle HD-2,5D-Darstellung verwendet Front-/Rückansicht mit jeweils vier
Laufphasen und Spiegelung. Gegner haben vier Zustandsbilder. Alle sind native
Weltmodelle mit Alpha-Ausschnitt und Tiefenprüfung; keine GUI-Projektilbilder.

Aktiv sind außerdem die drei HD-Figuren unter `shared/assets/defold11`.
`tools/import_defold11_art.py --sources /tmp/sources.json` erwartet je hero/dragon/fox
ein Objekt mit `source` und `intermediate` als Pfade auf die versionierten Originale.
Es isoliert die Alpha-Silhouetten und erzeugt 1536×1024-Laufatlanten ohne Vergrößern
der generierten Laufbildpixel. Keine kreative Neuerzeugung im regulären Build nötig.

Danach Herkunftshashes in `shared/asset-origins.json` aktualisieren und prüfen.
Blender **4.3.2** wurde hier verwendet. Keine Bilder-/Modell-/Musikdownloads nötig.
Schrift und Engine-/Modellhinweise bleiben mit ihren Fremdlizenzen enthalten.

## Aktuelle Prüfungen

Die exakten Shop-/Erholungswerte aus 0.12 bleiben zusätzlich als unveränderte
Regeldaten unter `shared/defold12-regression.json` erhalten. Nur deren strikte
15–35-HP-/1–4-Schaden-Prüfungen und die historische Shop-GUI-Fixture verwenden
diese alten Werte; die übrigen Regel-/GUI-Prüfungen und neuen Machtprüfungen
laufen mit den aktuellen Bonus-Macht-Regeln.


```bash
python3 tools/check_shared.py
python3 tools/check_defold.py
```

- **check_shared:** fünfzehn Testgruppen. Daten/Modelle/Provenienz, unveränderte
  andere Engine-Kopien, Hashwerte, tatsächliche FFmpeg-Decodierung von 61 Sprach-
  aufnahmen und Musik/Explosion, Pegel/Dauer/Schleifenübergang, begrenzte Sterne,
  Offline-Manifeste und kein berechneter Vorschaupfad in der GUI.
- **check_defold:** baut zuerst; bei Fehlern läuft niemals eine alte Binärdatei.
  Native Regelsuite einschließlich der unveränderten 0.7-Fixture, neuer Spielfluss- und Bonusprüfungen; aktuelle tatsächlich ausgeführte Anzahl in QUALITY.md. Sechs
  Sektoren werden mit bewegten Geschossen abgeschlossen. Kamera, aktive 0,14-s-Schwelle und historische 0,30-s-Fixtures,
  langsame Frames, schnelle Wischbewegungen, Abbruch/Finger und Effekte geprüft.
- Danach getrennte Speicherprozesse für Sterne, Ausrüstung, Hinweise und
  Musikpräferenz, gekaufte Ausrüstung, Guthaben und Figur. Echte XTest-Eingaben prüfen Figurenwahl/Käufe, Menü, kurzen Tipp und langen Hold
  am selben Punkt, FEUER sowie TON aus/an mit angehaltenem Ansagetimer. Die volle
  UI-Eingabefolge läuft bei 1280×720 und nach echter Fensteränderung auf 1280×800.
- `check_defold_power_ui.py` verdient mit echten Schüssen die Machtstufen 1, 8 und 12, prüft sichtbares Wachstum und Tarnmaterial, lesbare Millionengesundheit, Schutzschild, POWER-Menü, Prozessneustart und Wiederholung ohne Zusatzgewinn.
- `check_defold_replay_ui.py` lädt einen vollständig belohnten Spielstand, löst alle sechs Lichter-/Timingboni mit echten Schüssen, sammelt die wiederhergestellten Truhen per Laufweg und prüft Wiederbesuch/Prozessneustart ohne zusätzliche Sterne.
- `check_defold_polish_ui.py` prüft echte Zoomtasten, geänderte Weltpixel/Figurengröße sowie echte Hinweise und Sammlung aller sechs Schätze.
- `check_defold_hero_glow.py` prüft den tatsächlichen Figurenschimmer mit einem positiven Pixelvergleich an/aus.
- `check_defold_resilience_ui.py` prüft tatsächliche Heilung ohne Doppelabbuchung, Waffen-/Rüstungsstufen, alle drei Shopkategorien sowie den echten Weg in den Schutzort mit gezählten Geschossabsorptionen und Erholung.
- `check_defold_direct_touch.py` prüft fünf neue echte Gesten, ausdrücklich vor dem Loslassen. `check_defold_energy.py` vergleicht tatsächliche Pixel mit Schild an/aus.
- `check_defold_flow_ui.py` prüft zusätzlich drei reale GUI-Abläufe für Heldenwahl/Käufe, Weiter trotz offenem Schatz und freiwillige Suche mit anschließendem Weiter.
- `check_defold_traps.py` prüft zusätzlich echte Bildschirmtaps für alle drei Fallen und Abbruch, vollständig innerhalb der Arena, zusätzlich bei 175% Zoom; die tatsächlichen Taps platzieren 4,4 Welteinheiten entfernt, außerhalb der früheren Grenze.
- `check_defold_audio.py` zeichnet drei echte native Ausgaben mit OpenALs
  WAVE-Backend auf: Musik an, Musik aus und Musik/Sprache/Explosion gemischt.
  Signal/RMS und Pegel werden geprüft. Das ist keine menschliche Klangabnahme.

- `check_defold_depth.py` prüft tatsächlich gerenderte verdeckte Geschosse mit
  einem sichtbaren Kontrollgeschoss. `check_shared.py` liest die echten glTF-
  Positionspuffer aller Wandkörper und prüft deren Kollisionsflächen sowie
  Stereomischung und Abschnittsdynamik. Beide laufen in den obigen Befehlen.

Optionale native Spiel-/Menübilder (vorher `check_defold.py` zum Bauen):

```bash
xvfb-run -a -s '-screen 0 1600x1600x24' python3 tools/capture_defold.py --output /tmp/energyblast11-images
```

Bewegungs-/Schusssequenz mit tatsächlichen XTest-Eingaben aufnehmen:

```bash
xvfb-run -a -s '-screen 0 1600x1600x24' python3 tools/capture_defold_motion.py --output /tmp/energyblast11-motion
```

Das schreibt echte Laufzeitbilder/GIF außerhalb des Repositories, keine
Konzeptanimation. Quellen und Sichtabnahme: [ART_DIRECTION.md](ART_DIRECTION.md).

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
erhalten. Für 0.13 werden diese unveränderten Apps nicht erneut gebaut.

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
80 Sekunden, 32 Takte bei 96 BPM in D-Moll/modal, vollständig eigene Synthese. Statischer
Musik-Gain **1**; Laufzeitpegel 0,28 im Spiel, 0,24 im Menü, 0,065 unter Ansagen.
Im Schutzort ohne Ansage 0,20. Master-Gain 0,75, SFX separat gedämpft. Musikpräferenz wird lokal gespeichert.
Keine Schauspieleraufnahme, Silbenmontage oder kopierte Referenzmelodie.

## Android-APK

```bash
python3 tools/build_defold_android.py --output /tmp/energyblast-defold11-build
```

Ausgabeverzeichnis muss neu sein. Native ARM64-App, **0.12.0 / Code 13**,
`org.example.energyblast.defold`, minSdk 24, targetSdk 36. Derselbe ausschließlich
für Entwicklung angelegte Schlüssel außerhalb des Repositories:
`<tools>/energyblast-pilot-signing/debug.keystore`. Keine Release-/Play-Identität.
Die temporäre bekannte Debug-Passwortdatei wird nach dem Export gelöscht.

Ausgabe: APK, Build-/Signatur-/Manifestauszüge und `verification.json` mit Quell-
commit, sauberem/dirty Status, Buildzeit, Größe, Hash, Paket/Version, Signatur und
ZIP-Ausrichtung. Zusätzlich vor Veröffentlichung: ZIP-CRC, keine Schlüsseldateien,
Zertifikatsgleichheit mit der vorherigen 0.10 und Hash der veröffentlichten Download-Datei prüfen.

Abschlussexport vom sauberen Quellcommit, anschließend APK/Metadaten separat
versionieren. Das ist ein nachvollziehbarer Bauweg, keine Zusicherung bitidentischer
Ausgaben oder einer bereits bestandenen physischen Android-Installation.
Keine Actions-Artefaktflut, PRs, Merges oder automatischen Releases.
