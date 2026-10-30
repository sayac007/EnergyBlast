# Bauen und prüfen — Defold 0.14.1

Vom Repository-Hauptverzeichnis ausführen. Ausgaben außerhalb des Checkouts;
keine Schlüssel in Git. Die aktuelle Fassung enthält 16 Missionen. Der jeweilige
[Qualitätsstatus](QUALITY.md) dokumentiert ausgeführte Ergebnisse; die Anleitung
allein ist kein Nachweis eines erfolgreichen Builds oder Gerätetests.

## Werkzeuge und Vorbereitung

- Python 3.12, FFmpeg, NumPy und Pillow für Regeln, Medien und Bildprüfungen.
- Defold **1.14.0**, Bob und native Engine; Java **25** aus dessen offizieller
  Linux-Distribution. SDK-Dateien sind in `tools/defold-sdk.json` per Hash gepinnt.
- Android SDK platform **36**, build-tools **36.1.0**, JDK 17 für APK-Prüfwerkzeuge.
  Standardverzeichnis `/workspace/tools`, per `--tools` anpassbar.
- Native Linux-Tests: Xvfb/OpenGL, `libX11.so.6`, `libXtst.so.6`, OpenAL Soft
  mit Null- und WAVE-Backend. Der Test zeichnet tatsächliche Audioausgabe auf.

```bash
python3 tools/setup_defold.py --output /tmp/energyblast-defold-tools
python3 tools/sync_defold.py
```

Aktive Regeln: `shared/defold04.json`. Die neuen originalen Arenen liegen unter
`shared/assets/defold14`, Gegner/Drohnen/Effekte unter `shared/assets/defold14_units`.
HD-Helden aus `shared/assets/defold11`, eigene ältere Texturen und Musik bleiben
enthalten. Für normale Builds sind keine neuen Bilder oder Modellsynthesen nötig.

## Eigene Geometrie bei Bedarf erneut erzeugen

```bash
python3 tools/make_defold14_worlds.py
python3 tools/make_defold14_units.py
python3 tools/sync_defold.py
python3 tools/make_defold14_worlds.py --check
```

Der Weltgenerator liest die aktuelle Regelfassung. Er erzeugt sichtbare Geometrie,
Kollisionsmetadaten, Batches und Herkunftshashes für dieselben 16 Arenen. Die
Prüfung liest die exportierten Positionspuffer und kontrolliert auch Dekorationen
innerhalb der tatsächlichen Kollisionsflächen. Bestehende eigene Bodenbilder
werden wiederverwendet. Die neuen Einheiten und Piktogramme entstehen aus eigener
prozeduraler Geometrie; keine externe Spielgrafik wird heruntergeladen.

Optionale ältere Blender-/Atlas-Importanleitungen bleiben im
[festen 0.13-Dokumentationsstand](https://github.com/sayac007/EnergyBlast/blob/e557d936dac49f64b602239ace33379b490d3b2e/docs/BUILD_AND_TEST.md)
erhalten. Blender 4.3.2 wurde für diese älteren Quellen verwendet. Eine neue
Bildgenerierung ist für die aktuelle APK nicht nötig.

## Vollständige Prüfung

```bash
python3 tools/check_shared.py
python3 tools/check_defold.py
```

- **check_shared:** Gruppenanzahl im aktuellen Qualitätsstatus. Datenkopien, Regeln, unveränderte frühere Engine-
  Quellen, Herkunft und Hashes, tatsächliche FFmpeg-Decodierung von **72 Sprach-
  aufnahmen** (43 Defold, 3 Raid, 26 DE), Musik/Explosion, Pegel und Dauer,
  Offline-Manifeste sowie Exportgeometrie. Die 1.686 Geometrieprüfungen sind Teil
  dieser Suite, keine zusätzlichen nativen Regelprüfungen.
- **check_defold:** baut zuerst. Ein fehlgeschlagener Build darf niemals eine
  alte Binärdatei ausführen. Die native Suite meldet historische und aktive
  Regeln getrennt: 1.311 mit eingefrorenen 0.13-Fixtures plus aktive
  Kampagnenprüfungen einschließlich freier Relaistreffer und langsamer Lichter.
  Tatsächlich ausgeführte aktuelle Anzahl in [QUALITY.md](QUALITY.md). Danach
  folgen getrennte native GUI-/Speicher-/Audio-Prozesse.
- Die bisherige Oberfläche, direkte Touch-Gesten, Käufe, Speicherneustart,
  Verdeckung, Schimmer, Fallen und frühere Missionsabläufe bleiben als historische
  Regressionen erhalten. Dabei bedeuten damalige Bonus-/Schatz-/Millionenprüfungen
  nicht, dass diese Inhalte in der aktuellen Kampagne vorhanden sind.
- Die neuen Kampagnen- und Drohnenprüfungen laden ausdrücklich die aktuelle
  Regelfassung und prüfen alle 16 Missionen, drei Seiten, sichere Startpunkte,
  obere Bedienelemente, Gesundheitsbegrenzung, Migration und echte Angriffsdrohnen.
- Echte XTest-Taps und Ziehgesten prüfen das Zielantippen sowie das Ziehen der
  gewählten Drohne, echte Flugzeit/Blitzwirkung und Mission→Weiter. Ungültige Ziele
  und Abbruch dürfen keine Munition verbrauchen oder normale Schüsse auslösen.
- Die temporäre Kartenübersicht muss den gespeicherten Zoom unverändert lassen.
  Eine eigene Zoomänderung während des Fluges bleibt erhalten; sonst kehrt die
  vorherige Ansicht nach Flug oder Abbruch zurück.
- Die Kampagnentour läuft bei 1280 × 720 und nach tatsächlicher Fensteränderung
  auf 1280 × 800. Eine native Szene prüft 50 Gegner und zusätzliche echte Teilung.
  Das ist keine Messung der Bildrate auf einem physischen Android-Gerät.
- Der Starter isoliert Zustandsverzeichnisse, beendet bei Timeout die ganze
  Prozessgruppe und hält Laufzeitberichte außerhalb von Git.

Der Teststarter setzt für alte Prozesse `ENERGYBLAST_REGRESSION_RULES=013`.
Das ist eine ausdrückliche historische Fixture-Auswahl. Aktuelle Kampagnen-GUI-
Prozesse entfernen die Variable. Der normale App-Start ohne diese Testumgebung
verwendet immer die aktuelle Kampagnen-Regelfassung.

Die zusätzliche Taktikprüfung verwendet alle elf tatsächlichen Relais mit echten
Direktprojektilen und einen reflektierten Schuss an einer normalen Deckung.
Ein XTest-Tipp schaltet das Relais im Dock aus; der Kern bleibt bis zum letzten
Relais geschützt. Sechs Pixelzustände beobachten den laufenden langsameren
Lichttakt. Die tatsächliche Sprachsteuerung ersetzt eine ältere Ansage und lässt
die neue Erklärung bei wiederholten abgewiesenen Bosstreffern zu Ende laufen.

## Gezielte aktuelle GUI-Prüfungen und Bilder

Nach einem erfolgreichen nativen Build:

```bash
xvfb-run -a -s '-screen 0 1600x1600x24' python3 tools/check_defold_campaign_ui.py --output /tmp/energyblast14-campaign
xvfb-run -a -s '-screen 0 1600x1600x24' python3 tools/check_defold_drone_ui.py --output /tmp/energyblast14-drones
xvfb-run -a -s '-screen 0 1600x1600x24' python3 tools/check_defold_tactics_ui.py --output /tmp/energyblast141-tactics
xvfb-run -a -s '-screen 0 1600x1600x24' python3 tools/check_defold_campaign_ui.py --scenario tour --resize 1280 800 --output /tmp/energyblast14-resized
```

`--engine` ändert den Engine-Pfad. Die Prüfungen speichern auf Wunsch echte
Linux/OpenGL-Aufnahmen in den Ausgabepfad. Sie nutzen kontrollierte frühere
Spielstände und ruhige KI für einzelne Eingaben; Flug, Kontakte, Belohnungen,
Kollision und Speicher bleiben Produktionsregeln. Keine behauptete echte
Handyaufnahme oder unbegleitete Kinderspielrunde.

Die eingefrorenen Godot-/GDevelop-Vergleichsfassungen bleiben erhalten. Ihre
Anleitungen stehen im [0.3-Snapshot](https://github.com/sayac007/EnergyBlast/blob/cd9dc64/docs/BUILD_AND_TEST.md).
Diese Apps werden für die 0.14.1-Korrektur nicht neu gebaut.

## Bedienansagen und Musik

Die versionierten Aufnahmen genügen für Builds. Optionale Offline-Neuerzeugung
mit derselben synthetischen Serena-Stimme:

```bash
/workspace/tools/qwen-env/bin/python tools/prepare_defold_voice.py --model /workspace/tools/qwen-female
```

Unabhängiger Whisper-Screen ohne Referenztext als Prompt:

```bash
/workspace/tools/piper-env/bin/python tools/screen_voice.py \
  --model /workspace/tools/asr/sherpa-onnx-whisper-small \
  --manifest shared/audio/defold04/manifest.json \
  --output /tmp/energyblast-defold14-asr.json
```

Acht neue vollständige Ansagen erläutern Drohnenvorrat, beide Zielgesten,
Flug und leeren Vorrat sowie Missions-, Schwarm-, Lichter- und Abschlussziele.
Alle 34 früheren Dateien bleiben unverändert; ihre alten Sammel-/Begleitansagen
werden in der aktiven Kampagne nicht als aktuelle Anweisung geroutet.
Für 0.14.1 kommt eine vollständige Ansage zur freien Schusswahl bei Relais hinzu:
„Erst die Schalter, dann der Kern. Du kannst direkt treffen oder die Wand nutzen.“
Die nun 43 Dateien und ihre Metadaten sind versioniert; alle bisherigen 42 bleiben
unverändert. Der neue Clip wurde technisch geprüft und unabhängig exakt erkannt.
Das ist kein menschlicher Hörtest. Der aktuelle Prüf- und ASR-Umfang steht in
[QUALITY.md](QUALITY.md).

Musikherkunft, Hashes und Messwerte: `shared/audio/defold04/music.json`.
80 Sekunden, 32 Takte bei 96 BPM in D-Moll/modal, vollständig eigene Synthese.
Musikpräferenz und Stummschaltung bleiben lokal gespeichert. 62 native
Soundkomponenten liegen unter dem bestehenden Limit von 64.

## Android-APK

```bash
python3 tools/build_defold_android.py --output /tmp/energyblast-defold141-build
```

Das Ausgabeverzeichnis muss neu sein. Native ARM64-App, **0.14.1 / Code 16**,
`org.example.energyblast.defold`, minSdk 24, targetSdk 36. Der bestehende Schlüssel
für Entwicklungsupdates bleibt außerhalb des Repositories unter
`<tools>/energyblast-pilot-signing/debug.keystore`. Die temporäre bekannte
Debug-Passwortdatei wird nach dem Export gelöscht.

Ausgabe: APK, Build-/Signatur-/Manifestprotokolle und `verification.json` mit
Quellcommit, sauberem/dirty Status, Buildzeit, Größe, Hash, Paket/Version, Signatur
und ZIP-Ausrichtung. Vor Veröffentlichung zusätzlich ZIP-CRC, fehlende private
Schlüsseldateien, gleiches Zertifikat zur vorherigen APK und Hash des tatsächlich
erreichbaren Downloads prüfen.

**0.14.1-Abschlussexport: PENDING.** Der abschließende Build erfolgt erst vom
sauberen neuen Quellcommit; Paket/Version, Signaturgleichheit, APK-Inhalt und
Download-Hash werden für die neue Datei erneut geprüft.

**Historischer 0.14-Abschlussexport: PASS.** Gebaut vom [sauberen Quellcommit](https://github.com/sayac007/EnergyBlast/commit/9eecbbe5efe88973c8e4a4f0e26bbaa4a5dfdfa4);
[fester APK-Snapshot](https://github.com/sayac007/EnergyBlast/tree/11248b5ef4215838cb08bd2c8164d9718d9efcae/downloads), 69.063.866 Bytes. Signaturgleichheit zur
vorherigen APK, v2/v3, Paket/Version/API, keine Berechtigungen, Backup aus,
ZIP-CRC, keine privaten Schlüsseldateien, 16-KB-ZIP-Ausrichtung und
1.220 bytegleiche Projektdateien tatsächlich geprüft.
Reale Handy-/Tablet-Abnahme bleibt offen; Details in [QUALITY.md](QUALITY.md).
