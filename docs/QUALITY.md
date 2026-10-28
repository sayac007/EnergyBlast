# Aktueller Prüfstand — Defold 0.6, Prism Frontier

**28.10.2026.** [Sorgfältiger Grafikauftrag und Recherche](ART_DIRECTION.md),
[Umsetzung/Bilder](MILESTONE_05.md), [Kommandos](BUILD_AND_TEST.md),
[APK-/Quellmetadaten](../downloads/README.md).

| Tatsächlich geprüft | Ergebnis |
|---|---|
| Native Regeln und Darstellungshierarchie | **199 PASS**, bisherige 187 erhalten; echte Gelenkobjekte und gegenläufige Beine, Querformat/Bediengrenzen |
| Tatsächliche native UI-Eingaben | **PASS** bei 1280×720 und 1280×800; Figurenwechsel, zwei Käufe, kurze/lange Eingabe, FEUER, TON |
| Getrennte Speicherprozesse | **PASS**, Gesamtsterne, Guthaben/Käufe, Figur, Hinweise, Musik |
| Geschossverdeckung einschließlich Licht | **PASS**, verdeckt 0 veränderte Pixel, davor sichtbarer Kontrollfall |
| Gemeinsame Prüfungen | **11 Gruppen PASS**, Medien/Hashes/Privatsphäre, tatsächliche Wandgeometrie, AO-/Texturbindung, beidseitiger Vergleich vor/nach statischem Batching |
| Native Audioausgabe | **PASS**, Musik an/aus und Sprach-/Effektmischung aufgezeichnet; kein Überlauf im geprüften Fall |
| Eigene Sichtprüfung | Menü, Figurenwahl und sechs Sektoren in echter Laufzeit angesehen; 33 native Animationsframes mit wirklichen XTest-Eingaben aufgezeichnet |
| Grafische Abnahme durch Betreiber | **OFFEN**; 0.5 wurde ausdrücklich abgelehnt. Testzahlen ersetzen diese Entscheidung nicht. |

Die neue Shader-Ausgabe verwendet tatsächliche Texturen und gebackenes AO.
Statische Arena-Primitiven wurden von 447–481 auf jeweils 8 zusammengefasst;
Positionspuffer bleiben geometrisch gleich. Das ist keine gemessene Handy-Bildrate.
Die sechs Missionen, Punkteökonomie, Käufe und alten Spielstände bleiben erhalten.

**Manuell offen:** neue APK auf Handy aktualisieren/installieren, physische
Spielstandübernahme, Touch-/Klanggefühl, Geräteformat, längere Runden, Schwierigkeit
und Geräteleistung. Keine Store-Reife, empirische Lernwirkung oder grüne CI.
Andere Engines und Repositories unverändert. [Historie](MILESTONE_04.md).

Quellstand [`19856c1`](https://github.com/sayac007/EnergyBlast/commit/19856c195a8b51d1136ef8e7e8f57efd744caf05),
sauber gebautes APK **0.6.0 / Code 7**, **28.366.010 Bytes**.
Paket/APIs, Querformatmanifest, v2-Signatur/Zertifikatsgleichheit, keine
Berechtigungen/Schlüsseldateien, Backup aus, ZIP-CRC/-Ausrichtung und vollständiger
Projektabzug bestanden. [Metadaten](../downloads/defold-verification.json).

## Historische Nachweise

Die folgenden Ergebnisse gehören zu älteren Versionen und sind keine neuen
Tests der aktuellen Fassung. Quell-/APK-Referenzen bleiben unverändert erreichbar.

## Prüfstand 0.5, Toybox Raid

**28.10.2026.** [Meilenstein 04](MILESTONE_04.md),
[aktuelle Befehle](BUILD_AND_TEST.md), [Quell-/APK-Referenzen](../downloads/README.md).

| Tatsächlich geprüft | Ergebnis |
|---|---|
| Native Defold-Regeln | **187 PASS** = bisherige 107 + 80 neue Fälle; alle sechs Sektoren, neue Ziele, Kauf/Guthaben/Migration, Figuren, sichere HUD-Flächen |
| Getrennte Speicherstarts | **PASS**, Gesamtsterne, Restguthaben, Käufe, Figur, Hinweise, Musik |
| Wirkliche native UI-Eingaben | **PASS**, Figuren wechseln, zwei Käufe, Sektor wählen, kurzer/langer Druck, FEUER, TON-Pause/Fortsetzung |
| Wirklicher Tiefenpuffer | **PASS**, verdecktes Geschoss unsichtbar; sichtbares Kontrollgeschoss vorhanden |
| Gemeinsame Prüfungen | **9 Gruppen PASS**, Medien/Hashes, tatsächliche glTF-Wandpuffer vs. Kollision, Stereodynamik, eingefrorene andere Kopien, keine Berechtigungen/Backup |
| Native Audioaufnahme | **PASS**, Musik an Signal / aus Nullsignal, Sprach-/Effektmischung ohne Überlauf im geprüften Fall |
| Unabhängiges ASR | **5/5** vollständige Defold-Ansagen normalisiert exakt; kein menschlicher Hörnachweis |
| Sichtprüfung | Reale native Menü-, Figuren- und Sektorbilder angesehen; Linux/Xvfb, kein Gerätebenchmark |

Die Hauptursache für vermeintliche Schüsse über Wände war die Darstellung als
GUI über der 3D-Welt. Native Geschosse, genaue Wandkappen und der neue Bildtest
sichern die Korrektur ab. [Technische Details](MILESTONE_04.md).

**Manuell offen für die neue APK:** physisches Update/Spielstandübernahme,
Touchgefühl, Rotation/Seitenverhältnisse, Klang, längere Runden, Schwierigkeit und
Geräteleistung. Keine behauptete empirische Lernwirkung oder Store-Reife.
Kein Actions-Workflow und keine behauptete grüne CI. Andere Engines eingefroren.

Quellstand: [`321d5cf`](https://github.com/sayac007/EnergyBlast/commit/321d5cf6f50f7b038a2f7f8189ac421770af9013).
APK **0.5.0 / Code 6**, **10.474.682 Bytes** vom sauberen Quellstand gebaut.
Paket/APIs, v2-Signatur und gleiche Entwicklungssignatur wie 0.4.1, keine
Berechtigungen/Schlüsseldateien, Backup aus, ZIP-CRC/-Ausrichtung und kompletter
Projektabzug bestanden. [Metadaten](../downloads/defold-verification.json).
ZIP-Ausrichtung ersetzt keine vollständige 16-KB-/Store-Freigabe.

## Historische Nachweise

Die folgenden Ergebnisse gehören zu älteren Versionen; sie ersetzen keinen
neuen Test. Feste Quell-/APK-Referenzen in den jeweiligen Meilensteinen.

## Prüfstand 0.4.1

**28.10.2026:** 107 native Prüfungen bestanden: die bisherigen 76 plus 31 neue
Fälle für alle Wandarten, Winkel, Ecken, dünne Wände, nächstes Ziel, Prisma-
Grenze, gegnerische Abpraller, wechselnde Tore, Reichweite, Lebensdauer,
Verblassen und Neutralisation beider Geschossarten. Große Welt und Kamera bleiben.
Echte Kurz-/Langdruck-/Menüeingaben, getrennte Speicherstarts und aufgezeichnete
Musik-/Mute-/Sprach-/Effektmischung erneut bestanden. Sieben gemeinsame
Konsistenztestgruppen bestanden. Keine neue ASR-Erzeugung; Aufnahmen unverändert.

Manuell offen: neue APK physisch installieren/aktualisieren, Touchgefühl,
Rotation, Klang, Schwierigkeit mit gegnerischen Abprallern und Neutralisations-
feldern, längeres Spiel und Hardwareleistung. Keine grüne CI behauptet;
kein Actions-Workflow, PR, Merge oder GitHub-Release. [Testbefehle](BUILD_AND_TEST.md).

Die folgenden 0.4.0-Ergebnisse bleiben als Ausgangsstand dokumentiert.

# Ausgangsstand 0.4.0

**28.10.2026.** Aktive Weiterentwicklung: **Defold**. GDevelop 0.3 und Godot 0.2
bleiben eingefroren. [Meilenstein 03](MILESTONE_03.md) dokumentiert Auftrag,
Umsetzung und Grenzen. Frühere Nachweise: [0.3](MILESTONE_02.md), [0.2](MILESTONE_01.md).

## Ausgeführt und bestanden

| Prüfbereich | Ergebnis |
|---|---|
| Defold native Engine | **76** Prüfungen: 42 beibehaltene Kampf-/Regressionsfälle und 34 neue Zeitsteuerungs-/Welt-/Kamera-/Effektprüfungen |
| Tatsächliche native GUI | Menü, derselbe Punkt mit kurzem Tipp und langem Hold, anschließend FEUER per XTest; keine Script-Kontextfehler |
| Vollständige neue Arenen | Abpraller, zwei Schalter/Boss und Abschluss aller drei vergrößerten Sektoren mit real bewegten Geschossen |
| Speicher | Getrennte Prozesse erhalten Sterne, Ausrüstung, bezahlte Hinweise und Musikpräferenz |
| Tatsächlicher Audioausgang | OpenAL-WAVE-Aufzeichnung: Musik an Signal, aus Nullsignal; Mischung aus Musik/Sprache/Explosion ohne gemessenes Clipping |
| Gemeinsame Daten/Medien/Provenienz | Sieben Testgruppen; Modellkopien/Hashes, 30 Sprachaufnahmen, 60-s-Musik und Explosionsklang tatsächlich decodiert |
| Bedienansage | Whisper-small: 1/1 normalisiert exakt erkannt |
| Native Sichtprüfung | Größere Arena und unterschiedliche Explosionsframes selbst angesehen |

Die Druckdauer steuert die Aktion. Ein kurzer Tipp auf Gegner oder Wand darf
keinen Schuss auslösen; ein ruhiger Hold auf gewöhnlichem Boden muss zielen.
Schnelle Wischbewegungen, fremde Finger, Pause/Hintergrund und langsame Frames
werden ausdrücklich geprüft. Rendering und Unprojektion nutzen dasselbe Kameramodul.
Effekte laufen nach dem Sieg weiter und verschwinden vor dem Ergebnisdialog.

Die Musikprüfung wurde am tatsächlichen Engine-Ausgang durchgeführt und fand
zunächst eine doppelte Gain-Absenkung. Statischer Musik-Gain jetzt 1, Lautstärke
nur zur Laufzeit; Hintergrundmusik, Sprach-Ducking und Gesamtmischung getrennt.
Musik und Klang sind originale mathematische Synthese, keine übernommenen Songs.

Die früheren 51 GDevelop- und 43+24 Godot-Ergebnisse gehören zum dokumentierten
0.3-Vergleich. Für die 0.4-Änderung wurden diese Apps nicht verändert oder neu gebaut;
die historischen Ergebnisse werden nicht als frisch ausgeführte Tests ausgegeben.
Die alte Arenageometrie bleibt als Defold-Regressionsfixture erhalten.

## Builds und Grenzen

APK-Metadaten und SHA-256 bei den [Downloads](../downloads/README.md) ordnen die
Datei ihrem Quellcommit zu. Paket/Version/APIs, Entwicklungssignatur, fehlende
Berechtigungen, deaktiviertes Backup, ZIP-Integrität und Ausrichtung werden geprüft.
Keine Release-Schlüssel und kein GitHub-Actions-Workflow; keine behauptete grüne CI.

**Manuell offen:** neue APK physisch installieren/aktualisieren, Touch mit mehreren
Fingern, Rotation, tatsächliche Lautstärke/Sprachklarheit, längere Spielrunde,
Handy-/Tablet-Bildrate und Akkuverbrauch. Die Audioaufzeichnung ist ein technischer
Nachweis für ein ausgegebenes Signal, keine menschliche Klang- oder Geräteabnahme.
Die kontrollierte Explosionsaufnahme ist keine manuell bestandene Mission.

Keine Lernwirksamkeit/Übertragung in den Alltag oder Store-Reife behauptet. Keine
privaten Familien-Assets, Konten, Werbung oder Telemetrie. Spielstände/Musikpräferenz
bleiben lokal, Android-Backup ist aus; keine neuen Berechtigungen.

Kommandos zentral in [BUILD_AND_TEST.md](BUILD_AND_TEST.md). Laufzeitlogs bleiben
außerhalb von Git; nur der aktuelle Überblick und wesentliche Meilensteine werden gepflegt.

**APK-Abschlussprüfung:** Defold 0.4 vom sauberen Quellcommit
`d070a6021ac1ecfd84556da40cb1e852bbc2e593`, 9.540.794 Bytes, Version 0.4.0 / Code 4.
Paket/APIs, Signatur/v2, Zertifikatsgleichheit zu 0.3, keine Berechtigungen,
Backup aus, ZIP-CRC/Ausrichtung und Abwesenheit von Schlüsseldateien bestanden.
Hash und Download werden gegen die veröffentlichte Datei geprüft. Die
installierten Vergleichsdateien der anderen Engines bleiben unverändert.

0.4.1-APK vom sauberen Quellcommit `02a2b409830600bdaa85b10f6accc58f18a5f085` gebaut: 9540794 Bytes, Version 0.4.1 / Code 5. Paket/APIs, Signatur/v2 und Zertifikatsgleichheit, fehlende Berechtigungen, Backup aus, ZIP-CRC/Ausrichtung und fehlende Schlüsseldateien bestanden. SHA-256: `4d2b60a32d53af1c4e2f94b4806dd4fc23261925d88c19fd377594166f728bc5`.
