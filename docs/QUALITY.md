# Aktueller Prüfstand — Defold 0.4.1

**28.10.2026:** 106 native Prüfungen bestanden: die bisherigen 76 plus 30 neue
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
