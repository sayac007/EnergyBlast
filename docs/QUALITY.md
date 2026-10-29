# Aktueller Prüfstand — Defold 0.9

**29.10.2026.** [Auftrag/Umsetzung und Laufzeitbilder](MILESTONE_08.md),
[Testkommandos](BUILD_AND_TEST.md), [APK-Metadaten](../downloads/README.md).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regeln/Darstellung | **440 PASS**,347 erhaltene+93 neue direkte Gestenfälle |
| Gemeinsame Tests | **14 Gruppen PASS**, Daten/Medien/Hashes, sechs neue Materialien, tatsächliche AO-Bindung, Wandpuffer, Batch-Identität und Komponentenkapazitäten |
| Neue tatsächliche Gesten | **5 Szenarien PASS**: Bodentipp, wiederholte Schüsse VOR Loslassen, sofortiger gepolsterter Gegnertipp, gepufferte schnelle Tipps, Bewegung WÄHREND Ziehen |
| Bisherige tatsächliche GUI | **PASS**, Helden, Käufe, fehlende Sterne, Schatz-/Bonusführung, Nachfolger, sichere Suche, Fallen und zwei Fensterformate |
| Getrennte Speicherprozesse | **PASS**, Sterne/Guthaben/Käufe/Figur/Hinweise/Musik; Missionswiederherstellung zusätzlich simuliert |
| Native Geschossverdeckung | **PASS**, verdeckt 0 Pixel verändert; sichtbarer Kontrollfall 328 Pixel |
| Native Energieschild-Ausgabe | **PASS**, an/aus 15.701 unterschiedliche Pixel; echte Renderausgabe statt nur Materialdeklaration |
| Audioausgabe | **PASS**, Musik an RMS 0,01135, aus 0, Mischung 0,04234; kein gemessener Überlauf im Test |
| Sprachdateien | **27/27 technisch PASS**, zwei neue Gestenhinweise frisch ASR 2/2 exakt,25 andere samt Metadaten unverändert |
| Eigene Sichtprüfung | Menü und sechs Sektoren, Schüsse vor Loslassen, sofortiger Gegnertipp, Ziehen und 36 native Bewegungs-/Kampfframes angesehen |
| APK | Abschlussprüfung und sauberer Quellstand werden nach Export in den Download-Metadaten dokumentiert |

Eine Waffenpause von 0,24 Sekunden bleibt. Die Tests messen Eingabelogik und
beobachtete native Ausführung, keine physische Android-Touch-to-Photon-Latenz.
Die Antippzonen verändern weder Wände noch die berechnete Projektilbewegung.
Historische 0.7-Steuerung verbleibt ausschließlich bei archivierten Regelfixtures;
sie wird nicht als aktive 0.9-Steuerung getestet oder beworben.

**Offen:** physisches Update und Spielstandübernahme, Geräte-Latenz/Mehrfingergefühl,
Klang, Schwierigkeit, längere Runden, Geräteleistung und grafische Betreiberabnahme.
Keine neue grüne CI, Store-Reife, kommerzielle Gesamtgleichwertigkeit oder
empirische Lernwirkung behauptet. Der bestehende 26/27-ASR-Gesamtvergleich enthält
eine unveränderte zulässige Variante „Geh“ statt „Gehe“ aus 0.8; kein neuer Hörnachweis
für die 25 unveränderten Aufnahmen wird vorgetäuscht.

[Vorheriger 0.8-Prüfstand](https://github.com/sayac007/EnergyBlast/blob/952a563/docs/QUALITY.md),
[0.8-Meilenstein](MILESTONE_07.md), [0.7](MILESTONE_06.md).
