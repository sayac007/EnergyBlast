# Aktueller Prüfstand — Defold 0.13

**29.10.2026.** [Machtregeln, Bilder und Grenzen](MILESTONE_12.md),
[Testkommandos](BUILD_AND_TEST.md), [APK-Metadaten](../downloads/README.md).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regeln/Darstellung | **1.311 PASS**, 1.066 bisherige + 245 neue Machtprüfungen |
| Gemeinsame Tests | **15 Gruppen PASS**, Regeln, Medien, Herkunft, aktive Ressourcen und exportierte Wandgeometrie |
| Dauerhafte Macht | **PASS**, alle zwölf erstmaligen Erfolge erhöhen Werte sofort, ältere Boni werden angerechnet; unbekannte/falsche Schlüssel zählen nicht |
| Erhalt von Fortschritt | **PASS**, keine Doppelbelohnung, kein Nachfüllen durch Wiederholung; Käufe, Guthaben, Figur und Hinweise bleiben erhalten |
| Gesundheit/Schild/Feuerkraft | **PASS**, echte Projektilwirkung und Schildtreffer, erneute Aufladung, proportionale Erholung, gekaufte Ausrüstung wirkt zusätzlich |
| Tatsächliche Macht-GUI | **PASS**, echte Zeitfenster-Bonusschüsse erreichen 20 / 1.005 / 1.000.005 Gesundheit; die zusätzlichen fünf Punkte stammen aus vorhandener Rüstung |
| Native Darstellung | **PASS**, echte Modellskalen 1,0625 / 1,5 / 1,75, echter Schild, Millionentarnung mit Shaderdeckkraft 0,37; physische Laufgröße unverändert |
| Kameragrenzen | **PASS**, alle vier echten Modell-Eckpunkte innerhalb des Feldes, auch am Nordrand bei 175% Zoom; komplette Figur auf der Menübühne |
| Große Zahlen/Bedienung | **PASS**, „1.000.005“ misst 86,42 Pixel bei 126 Pixeln verfügbarem Platz; POWER-Seite öffnet/schließt zur selben Runde |
| Macht nach Prozessneustart | **PASS**, Bonusstand 12, Gesundheit 1.000.005, Größe 1,75, gekaufte Ausrüstung, Gesamtsterne 4.350 und Guthaben 4.090 erhalten; Wiederholung vergibt null |
| Bisherige tatsächliche GUI | **PASS**, fünf direkte Gesten, Helden, Shop, Wiederbesuch, sechs Schätze/Bonusabläufe, Fallen bei 100/175% Zoom, Heilung/Schutzort, zwei Fensterformate |
| Native Verdeckung/Schild | **PASS**, verdecktes Geschoss 0 geänderte Pixel, sichtbare Kontrolle 328; Gegnerschild 15.701 |
| Native Schimmerausgabe | **PASS**, bisheriger Kontrollfall unverändert 2.937 geänderte Pixel |
| Tatsächliche Audioausgabe | **PASS**, Musik an RMS 0,01354, aus 0, Mischung 0,04224; kein gemessener Überlauf |
| Sprache | **34/34 technisch PASS**, zwei neue vollständige Serena-Ansagen 2/2 unabhängig ASR-exakt; vorherige 32 Dateien und Herkunftseinträge unverändert |

Ausgeführt: `python3 tools/check_shared.py` und die vollständige native Suite
`python3 tools/check_defold.py`. Die neuen GUI-Prüfungen benutzen kontrollierte
frühere Bonusstände und deaktivierte Gegner-KI, verdienen den jeweils nächsten
Bonus aber über echte Eingaben, Projektile und Produktionsregeln. Keine behauptete
unbegleitete Android-Spielrunde. Die tatsächlichen Aufnahmen wurden angesehen.

Die alten exakten 15–35-HP-/1–4-Schaden-Shopprüfungen und deren GUI-Fixture laufen
zusätzlich mit den bytegenau erhaltenen 0.12-Regeldaten. Die übrigen alten Tests
und neuen Machtprüfungen laufen mit den aktuellen Regeln. Die bisherige Migration
und der neue dauerhafte Bonusfortschritt sind getrennt abgesichert.

Bei der Sichtprüfung wurde zunächst ein abgeschnittener Kopf gefunden. Weltkamera
und Menübühne berücksichtigen jetzt das gewachsene Modell; die neuen Grenzen
werden gegen seine tatsächliche Welttransformation geprüft. Sichtbare Verdeckung
durch eine reale Wand bleibt weiterhin zulässig.

**APK 0.13.0 / Code 14: PASS.** Gebaut 29.10.2026, 17:12 MEZ vom sauberen
Quellstand [`fda39e5`](https://github.com/sayac007/EnergyBlast/commit/fda39e50c0fa1166b0be2847eebaf86adf38d89a);
APK-Snapshot [`9e486f1`](https://github.com/sayac007/EnergyBlast/commit/9e486f1dec3b6ca67371f1491c8e7b5991885a14).
Paket/APIs/Querformat, Berechtigungsfreiheit, Backup aus, v2/v3-Signatur,
identisches Zertifikat zur vorherigen APK, ZIP-CRC, keine privaten Schlüsseldateien,
16-KB-ZIP-Ausrichtung, Android-Shaderexport und 845 per Hash identische Projektdateien
bestanden. 68.342.970 Bytes, 128 KiB mehr als 0.12. [SHA-256 und Download](../downloads/README.md).

**Manuell offen:** Android-Update und eigene Spielstände, echte Mehrfinger-Gesten,
kleine Displays, Klang, GPU-Leistung und Balance der bewusst übermächtigen Stufen.
Keine neue grüne CI, Store-Freigabe oder Lernwirkung behauptet.

Die 20 neuen Missionen und die FPV-Spiel-Drohne sind als nachfolgender Auftrag
erfasst; der Betreiber hat die Bonus-Macht zuerst gewünscht. Diese Erweiterungen
sind in 0.13 noch nicht enthalten.

[Vorheriger 0.12-Prüfstand](https://github.com/sayac007/EnergyBlast/blob/e76739a835a6e7aece62cbb900c80e58053b9ec1/docs/QUALITY.md),
[0.12-Meilenstein](MILESTONE_11.md), [0.11](MILESTONE_10.md).
