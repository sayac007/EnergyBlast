# Aktueller Prüfstand — Defold 0.14.1

**30.10.2026.** [Umsetzung, Missionen und Laufzeitbilder](MILESTONE_13.md) ·
[Testkommandos](BUILD_AND_TEST.md) · [Download-Metadaten](../downloads/README.md).

## Aktuelle Korrektur 0.14.1 / Code 16

Branch `fix/free-relays-slower-patterns`: Passive Relais akzeptieren direkte und
reflektierte Treffer; die Boss-Sperre bis zum letzten Relais bleibt. Schild- und
Fallenregeln echter Gegner sowie Wandreflexionen bleiben erhalten. Die drei
Lichtermissionen verwenden gemeinsam 1,8 Sekunden je Schritt, davon 1,2 Sekunden
leuchtend, und 2,4 Sekunden Pause nach der Folge: insgesamt 7,8 Sekunden.

| Prüfung der Korrektur | Tatsächlicher Status |
|---|---|
| Neue Ansage `defold_relays_free` | **PASS**, 6,12 Sekunden, FFmpeg/Hash/Dauer/Pegel; unabhängiges Whisper ohne Referenzprompt **1/1 exakt** |
| Bisherige 42 Clips und Modelldaten | **PASS**, alle Datei-Hashes und individuellen/globalen Metadaten unverändert |
| Vollständige Regel-/GUI-/Medienregression | **PASS**, alle 22 Befehle; 4.674 native Prüfungen (1.311 historische + 3.363 aktuelle, davon 134 neu), 16 gemeinsame Gruppen mit 1.686 Geometrieprüfungen |
| Neuer sauberer Android-Build und Artefaktprüfung | **PASS**, 0.14.1/16, identisches Zertifikat, 1.225 bytegleiche Projektdateien, Paket/Manifest/v2/v3/ZIP geprüft |
| Feste neue Quell-/APK-Verweise | [Quelle](https://github.com/sayac007/EnergyBlast/commit/2fb77853b9018ac872c11a92c6fe6afb46317853) · [APK-Snapshot](https://github.com/sayac007/EnergyBlast/tree/387b8a7169d5b6a2a0b04dfaf4bfc12e03e929e7/downloads) |

Das Paket enthält nun 43 Defold-Sprachaufnahmen und 62 native Soundkomponenten.
Ein ASR-Screen ist kein menschlicher Hörtest. Die älteren grünen Ergebnisse unten
bleiben als historische Ergebnisse getrennt; die aktuelle vollständige Regression ist erneut bestanden.

Tatsächlich geprüft sind alle elf Relais über direkte fliegende Projektile,
ein echter Abpraller an normaler Deckung, verbleibende Boss-Sperren und alte
Schild-/Timingregeln. XTest bedient den echten Relaistreffer. Sechs Bildzustände
bei ungefähr 0,87/1,37/2,07/4,02/5,82/7,95 Sekunden prüfen die langsameren
Seitenkreise. Der laufende Spieltakt wird nicht manuell vorgerückt. Die tatsächliche
Sprachsteuerung ersetzt eine vorherige Ansage und bleibt nach vier erneuten
Bosstreffern bei derselben Restdauer; sie beginnt nicht erneut. Native Aufnahmen
wurden angesehen. Python-Syntax, Whitespace und 204 lokale Dokumentationsziele
sind geprüft. Physische Geräte-/Hörabnahme bleibt offen.

**APK 0.14.1 / Code 16: PASS.** 69.113.018 Bytes (49.152 Bytes mehr als 0.14),
gebaut 30.10.2026, 16:26 MEZ vom [sauberen Quellstand](https://github.com/sayac007/EnergyBlast/commit/2fb77853b9018ac872c11a92c6fe6afb46317853),
`source_dirty:false`. [Fester APK-Snapshot](https://github.com/sayac007/EnergyBlast/tree/387b8a7169d5b6a2a0b04dfaf4bfc12e03e929e7/downloads). Paket
`org.example.energyblast.defold`, API 24/target 36/ARM64, userLandscape, keine
Berechtigungen, Backup aus. Identisches Entwicklungszertifikat wie 0.14,
v2/v3-Signatur, ZIP-CRC, keine privaten Schlüsseldateien, 16-KB-ZIP-Ausrichtung
und **1225 bytegleiche Projektdateien** im Abzug bestanden.
ZIP-Ausrichtung allein ist keine Play-/16-KB-Zertifizierung.

```text
SHA-256 20451a92eac9aab78cfea4ae2e0b9258c2b77d2367ee1d473e24506b2560270d
```

## Historischer vollständig verifizierter Stand: 0.14

**Vollständige native Suite: PASS, alle 21 Prüfschritte erfolgreich.**
**APK 0.14: PASS**, [saubere Quelle](https://github.com/sayac007/EnergyBlast/commit/9eecbbe5efe88973c8e4a4f0e26bbaa4a5dfdfa4) · [APK-Snapshot](https://github.com/sayac007/EnergyBlast/tree/11248b5ef4215838cb08bd2c8164d9718d9efcae/downloads).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regelprüfungen insgesamt | **4.540 PASS**: 1.311 historische 0.13-Prüfungen und 3.229 Prüfungen mit aktiven 0.14-Regeln |
| Gemeinsame Suite | **16 Gruppen PASS**, einschließlich Medien, Regeln, Archividentität, Manifesten und Herkunft |
| Exportgeometrie | **1.686 PASS**, tatsächliche Positionspuffer, Kollisionsgrundrisse, unveränderte Material-Batches und Herkunftshashes; Teil der gemeinsamen Suite |
| Aktive Kampagne | **PASS**, genau 16 Missionen, keine Bonus-/Schatz-/Begleitaufträge, gültige Ziele und sichere Startpunkte |
| Gesundheit und Tarnung | **PASS**, höchstens 100 einschließlich Rüstung, begrenzter Schild/Schaden, wiederholte genaue Fernortung trotz stärkster Tarnung |
| Schwärme | **PASS**, endliche Familien, kontrollierte Teilungen, Kollisionsgrenzen und maximal 50 lebende Gegner |
| Tatsächliche Kampagnen-GUI | **PASS**, alle 16 Missionen, drei Auswahlseiten, obere Ziel-/Gegner-/Missionsaktionen, Schutzstart und Rückkehr zur Auswahl |
| Fensterformate | **PASS**, vollständige Missionstour bei 1280 × 720 und nach tatsächlicher Fensteränderung auf 1280 × 800 |
| Alte Spielstände | **PASS**, kontrollierter früherer Millionen-Spielstand behält 4.350 Gesamtsterne, 2.690 Guthaben und Käufe; neue Regeln ergeben in diesem Profil 70 Gesundheit, auch nach Prozessneustart |
| Angriffsdrohne tatsächlich bedient | **PASS**, Katalog wählen, Ziel antippen oder Vorschau ziehen, echter Flug, elektrischer Kontakt, kein versehentlicher normaler Schuss oder Laufweg |
| Auswahl abbrechen/ungültige Ziele | **PASS**, kein Vorratsverlust, keine HUD-Ziele und kein fremder Finger als gültige Bestätigung |
| Temporäre Zielübersicht | **PASS**, gesamte Karte aus echtem Zikkurat-Start erreichbar, gespeicherter Zoom unverändert; vorherige Ansicht nach Flug/Abbruch zurück, bewusste Zoomänderung bleibt |
| Echter Missionsabschluss/Weiter | **PASS**, tatsächlicher Drohnenkontakt beendet die erste Mission und die obere Folgeaktion startet die nächste |
| Native Belastungsszene | **PASS**, 50 tatsächliche native Gegner und echte zusätzliche Nachkommen gerendert; keine behauptete Handy-FPS-Messung |
| Bisherige Eingabe-/Darstellungsregression | **PASS**, direkte Gesten, Auswahl/Käufe, Archivspeicher, Fallen, Schimmer, Verdeckung und Audio |
| Tatsächliche Audioausgabe | **PASS**, Musik an RMS 0,01353, aus 0,00001, Mischung 0,04208; kein gemessener Überlauf |
| Sprachausgabe | **42/42 technisch PASS**, acht neue Ansagen unabhängig **8/8 ASR-exakt**; 34 frühere Dateien und Herkunftseinträge unverändert |

Ausgeführt wurden `python3 tools/check_shared.py` und die vollständige native
Suite `python3 tools/check_defold.py`. Die Geometrieprüfung liest die tatsächlichen
exportierten glTF-Positionspuffer; sie prüft nicht bloß Generator-Metadaten.

## Historische und aktive Regeln trennen

Die bisherigen 1.311 Regelprüfungen verwenden ausdrücklich eingefrorene
0.13-Regeln; noch ältere Shopwerte haben ihre eigenen unveränderten Fixtures.
Dazu gehören damalige Bonus-, Schatz- und Millionengesundheitsprüfungen. Ihr
Bestehen behauptet diese Funktionen nicht für 0.14. Die 3.229 aktuellen Prüfungen
laden die aktive 16-Missionen-Regelfassung. Der normale App-Start lädt ebenfalls
diese aktuelle Kampagne.

Der Teststarter setzt für historische Prozesse `ENERGYBLAST_REGRESSION_RULES=013`.
Die neuen Kampagnen- und Drohnen-GUI-Prozesse entfernen diesen Wert und starten
zusätzlich ihren ausdrücklich kontrollierten Testmodus. Aktuelle und historische
Ergebnisse werden im nativen Protokoll getrennt ausgegeben.

Die GUI-Prüfungen verwenden einen kontrollierten alten Spielstand und schalten für
isolierte Eingaben die gegnerische KI ruhig. Echte Eingaben, Flug, Treffer, Teilung,
Speicher und Produktionsregeln bleiben wirksam. Die Aufnahmen wurden angesehen.
Das ist keine unbegleitete Android-Spielrunde.

## Offene Freigaben

**Android-Abschlussexport: PASS.** Gebaut 30.10.2026, 15:10 MEZ von
[sauberer Quelle](https://github.com/sayac007/EnergyBlast/commit/9eecbbe5efe88973c8e4a4f0e26bbaa4a5dfdfa4), `source_dirty:false`.
69.063.866 Bytes, Version 0.14.0/Code 15, Paket `org.example.energyblast.defold`,
API 24/target 36/ARM64, userLandscape, keine Berechtigungen, Backup aus.
v2/v3-Signatur und dasselbe Entwicklungszertifikat wie 0.13, ZIP-CRC, keine
privaten Schlüsseldateien, 16-KB-ZIP-Ausrichtung und **1.220 bytegleiche
Projektdateien** im Buildabzug bestanden. ZIP-Ausrichtung allein ist keine
Play-/16-KB-Zertifizierung. [Fester APK-Snapshot](https://github.com/sayac007/EnergyBlast/tree/11248b5ef4215838cb08bd2c8164d9718d9efcae/downloads).

```text
SHA-256 d8a3206c2e45f48bdb9765ba73c4646ce62ca02738b86b1d5d3d0015b3cc7bfd
```

**Manuell offen:** Update und eigene Spielstände auf Handy/Tablet, reale
Mehrfingergesten und Drohnenziehen, kleine Displays, Klang, GPU-Leistung bei
50 Gegnern, längere Runden und Schwierigkeitsbalance. Keine neue grüne CI,
Store-Freigabe, kommerzielle Qualitätsgleichheit oder Lernwirkung behauptet.

[Früherer 0.13-Prüfstand](https://github.com/sayac007/EnergyBlast/blob/e557d936dac49f64b602239ace33379b490d3b2e/docs/QUALITY.md) ·
[Meilenstein 0.13](MILESTONE_12.md) · [aktueller Meilenstein](MILESTONE_13.md).

## Repository-Integration nach main — 30.10.2026

Die vollständige geprüfte 0.14-Fassung `425dd3c` wurde mit einem echten Merge und
erhaltener Historie übernommen. Der einzige Konflikt betraf die README-Ankündigung.
Der gesamte Nicht-Dokumentationsbaum einschließlich Spiel, Regeln, Assets,
Werkzeugen und Downloads bleibt bytegleich. APK-Größe, SHA-256, ZIP-CRC und
fehlende private Schlüsseldateien wurden erneut geprüft. Alle **199 lokalen Dokumentationsziele**, Konfliktmarkierungen, die geplanten
Merge-Eltern und der Nicht-Dokumentationsbaum sind ebenfalls geprüft. Die oben genannten nativen Spieltests und
der APK-Build bleiben die zuvor ausgeführten Nachweise; für diese identische
Repository-Übernahme werden weder neue Spieltests noch ein neuer Build behauptet.
