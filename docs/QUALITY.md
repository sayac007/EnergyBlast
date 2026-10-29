# Aktueller Prüfstand — Defold 0.12

**29.10.2026.** [Ursache und Umsetzung](MILESTONE_11.md),
[Testkommandos](BUILD_AND_TEST.md), [APK-Metadaten](../downloads/README.md).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regeln/Darstellung | **1.066 PASS**, 820 bisherige + 167 Wiederholungs- + 79 Fallenprüfungen |
| Gemeinsame Tests | **15 Gruppen PASS**, Regeln, Medien, Herkunft, aktive Ressourcen und exportierte Wandgeometrie |
| Fehler reproduziert | Vollständig verdienter Spielstand: alle sechs Arenen ohne lebende Bonusziele, Truhe ausgeblendet und Fertigmeldung statt Bonusführung |
| Wiederhergestellte Boni | **PASS**, zwei aktuelle Rundenziele je Arena; sechs echte reflektierte Schüsse lösen Abprallboni gegen unveränderte Wände |
| Tatsächliche Wiederholungs-GUI | **PASS**, alle sechs Lichter-/Zeitfensterboni mit echten Bildschirmtaps/Projektilen gelöst, sechs Truhen durch Hinlaufen gesammelt und erneuter Besuch geprüft |
| Fortschritt/Speicher | **PASS**, 4.350 Gesamtsterne und 4.090 Guthaben unverändert; gekaufte Rüstung/Prisma erhalten, auch nach Prozessneustart; keine Doppelbelohnungen |
| Sinnvolle Hinweise | **PASS**, Info/Funk/Hinweis erklären die offene Bonusaufgabe wird erklärt, auch bei bereits verdienter Schatzbelohnung; direkte Schatzwahl bleibt möglich |
| Fallenreichweite | **PASS**, 5,25 statt 3,5; dieselbe Grenze für Anzeige/Controller/direkte Regel, Wände und Sichtlinie bleiben wirksam |
| Tatsächliche Fallen-GUI | **PASS**, alle drei Typen und Abbruch bei 100% und 175% Zoom; reale Platzierung 4,4 Welteinheiten entfernt, außerhalb des alten Kreises |
| Wirkzeit/Lernstufen | **PASS**, initial 18/27/15 Sekunden, unbenutzt 36; später 2,5×/2× nur nach erfolgreichem Fangen und Abschluss unterschiedlicher früherer Missionen; kein Fortschritt durch bloßes Laden |
| Alte GUI/Bedienung | **PASS**, Gesten, fünf direkte Eingaben, Helden, Käufe, zwei Fensterformate, Weiter, Schutzort und Heilung |
| Zoom/Schatz/HD | **PASS**, bisherige Zoom-/Eingaberegressionen, sechs erstmalige Schatzfunde mit +75, echte Zoomausgabe und HD-Atlanten; Schimmervergleich 2.937 Pixel |
| Native Verdeckung/Schild | **PASS**, verdecktes Geschoss 0 geänderte Pixel, sichtbare Kontrolle 328; Schild 15.701 |
| Tatsächliche Audioausgabe | **PASS**, Musik an RMS 0,01342, aus 0, Mischung 0,04214; kein gemessener Überlauf |
| Sprache/Medien | **PASS**, unveränderte 32 aktive Ansagen erneut technisch dekodiert und per Hash/Dauer/Pegel geprüft; keine neue Hör-/ASR-Prüfung |

Die native Suite wurde über `python3 tools/check_defold.py` vollständig ausgeführt,
die gemeinsame Suite über `python3 tools/check_shared.py`. XTest bedient die echte
Linux/OpenGL-Laufzeit. Der neue Wiederholungstest startet mit einem kontrollierten
alten Spielstand, stellt die Figur an erreichbare Positionen und deaktiviert die
feindliche KI. Aufgaben, Treffer, Wände und Belohnungsregeln bleiben echt.
Das ist keine unbegleitete Android-Spielrunde.

Die Aufnahmen der wiederhergestellten Ziele und des größeren Fallenkreises wurden
angesehen. Unveränderte eigene Figuren, Musik und Quellen bleiben erhalten.

**APK 0.12.0 / Code 13: PASS.** Gebaut 29.10.2026, 16:31 MEZ vom sauberen
Quellstand [`9554e66`](https://github.com/sayac007/EnergyBlast/commit/9554e66ba5ede774779857a0285b27e4d670d8c1);
APK-Snapshot [`8d0de93`](https://github.com/sayac007/EnergyBlast/commit/8d0de931d121f89e5ad8b6841c4124035a24c12b).
Paket/APIs/Querformat, Berechtigungsfreiheit, Backup aus, v2/v3-Signatur,
identisches Zertifikat zur vorherigen APK, ZIP-CRC, keine privaten Schlüsseldateien,
16-KB-ZIP-Ausrichtung und 831 per Hash identische Projektdateien bestanden.
68.211.898 Bytes, nur 16 KiB mehr als 0.11. [SHA-256 und Download](../downloads/README.md).

**Manuell offen:** Android-Update samt eigenem Spielstand, größerer Fallenkreis auf
Handy/Tablet, neuer Schwierigkeitsverlauf, echte Zwei-Finger-Geste, Klang, Leistung
und längere Spielrunden. Keine neue grüne CI, Store-Freigabe oder Lernwirkung behauptet.

[Vorheriger 0.11-Prüfstand](https://github.com/sayac007/EnergyBlast/blob/1cd1be18bfb8d316454279bbb756b128d373da3c/docs/QUALITY.md),
[0.11-Meilenstein](MILESTONE_10.md), [0.10](MILESTONE_09.md).
