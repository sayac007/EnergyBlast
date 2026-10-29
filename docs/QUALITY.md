# Aktueller Prüfstand — Defold 0.10

**29.10.2026.** [Auftrag, Umsetzung und Laufzeitbilder](MILESTONE_09.md),
[Testkommandos](BUILD_AND_TEST.md), [APK-Metadaten](../downloads/README.md).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regeln/Darstellung | **629 PASS**, 440 erhaltene + 189 neue Prüfungen für Erholung, Schutzort, Ausrüstung und Migration |
| Gemeinsame Tests | **14 Gruppen PASS**, Daten/Medien/Herkunft, Wandpuffer, Batch-Identität, Materialien und Komponentenkapazitäten |
| Gesundheit und Erholung | **PASS**, 15 Grundenergie, 20/25/30/35 mit Rüstung, Wartezeit, Zurücksetzen nach Treffer, Pause/Hintergrund und Obergrenze |
| Sechs Schutzorte | **PASS**, nutzbare Fläche frei, tatsächliche Wege unter 1,25 s, Absorption aus 16 Richtungen, nach Abprallern und bei innen erzeugten Geschossen; kein Feuern hinaus |
| Neuer tatsächlicher GUI-Test | **PASS**, Heilung/keine Doppelabbuchung, Waffen-/Rüstungsstufen, gesperrte Stufen, alle Shopkategorien, echter Weg zum Zikurrat, mindestens 10 gezählte Schutzabsorptionen/0 Schaden/20 Energie |
| Bisherige tatsächliche GUI | **PASS**, fünf direkte Gesten, Helden, Käufe, fehlende Sterne, Schatz-/Bonusführung, Nachfolger, sichere Suche, Fallen und zwei Fensterformate |
| Getrennte Speicherprozesse | **PASS**, Sterne/Guthaben/Käufe/Figur/Hinweise/Musik; neue wiederholte Heilungsbuchungen und Stufen zusätzlich rekonstruiert |
| Native Geschossverdeckung | **PASS**, verdeckt 0 Pixel verändert; sichtbarer Kontrollfall 328 Pixel |
| Native Energieschild-Ausgabe | **PASS**, an/aus 15.701 unterschiedliche Pixel |
| Tatsächliche Audioausgabe | **PASS**, Musik an RMS 0,01337, aus 0, Mischung 0,04183; kein gemessener Überlauf im Test |
| Sprachdateien | **30/30 technisch PASS**, drei neue Ansagen frisch ASR 3/3 exakt, 27 vorherige Dateien und Metadaten unverändert |
| Neue Musik | **PASS**, 80 s, 96 BPM, Stereo, Abschnitts-RMS-Verhältnis 2,42, geprüfter Schleifenübergang; keine daraus abgeleitete menschliche Klangabnahme |
| APK | Abschlussprüfung und sauberer Quellbezug werden nach Export in den Download-Metadaten dokumentiert |

Die XTest-Prüfungen laufen unter Linux/OpenGL mit klar benannten Testprofilen.
Der Schutzort-Test injiziert echte Geschosse; gezählt wird deren tatsächliche
Kollision mit dem Schutzfeld. Regeneration kann einen Fehler nicht über null
Schaden hinweg verschleiern. Die Tests belegen keine physische Android-Latenz.

**Offen:** physisches Update und Spielstandübernahme, Geräte-Latenz/Mehrfingergefühl,
Klang und musikalische Atmosphäre, langfristige Schwierigkeit/Motivation/Ökonomie,
Wahrnehmung des Schutzorts, mobile Leistung und grafische Betreiberabnahme.
Keine neue grüne CI, Store-Reife, kommerzielle Gesamtgleichwertigkeit oder
empirische Lernwirkung behauptet. Der ältere Sprachvergleich enthält eine
zulässige Variante „Geh“ statt „Gehe“; die 27 unveränderten Aufnahmen werden nicht
als neu gehörte oder neu ASR-geprüfte Aufnahmen ausgegeben.

[Vorheriger 0.9-Prüfstand](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/docs/QUALITY.md),
[0.9-Meilenstein](MILESTONE_08.md), [0.8](MILESTONE_07.md).
