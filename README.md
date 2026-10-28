# EnergyBlast — Defold 0.6, Prism Frontier

Ein echter Offline-Touch-Shooter für Kinder etwa von 7 bis 10 Jahren:
aktive Kanonen, Deckung, Ausweichen und klug eingeschätzte Abpraller.
**Sechs Sektoren, drei wählbare Helden und tatsächlich kaufbare Ausrüstung.**
Brawl Stars ist die visuelle Referenz; sämtliche Spielmodelle und die Musik
sind eigenständig erstellt. Defold ist der Schwerpunkt. GDevelop 0.3 und
Godot 0.2 bleiben als eingefrorene Vergleiche erhalten.

| Einstieg | Hier weiterlesen |
|---|---|
| Installierbare Test-App | [APK mit Größe, Hash und Update-Hinweisen](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/downloads/README.md) |
| Abgleich mit euren sieben Testpunkten | [Meilenstein 05](docs/MILESTONE_05.md) |
| Was geprüft wurde und was offen ist | [Qualitätsüberblick](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/docs/QUALITY.md) |
| Ausgangsauftrag und aktuelle Entscheidungen | [Projektauftrag](docs/PROJECT_BRIEF.md), [unverändertes Original](docs/pilot-brief.md) |
| Selbst bauen und prüfen | [Build-/Testanleitung](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/docs/BUILD_AND_TEST.md) |
| Frühere Versionen | [0.5](docs/MILESTONE_04.md), [0.4](docs/MILESTONE_03.md), [0.3](docs/MILESTONE_02.md), [0.2](docs/MILESTONE_01.md) |

## Installieren

**[Defold 0.6 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/24b24dd23d08eb73ebd5fc113c318da3b1f45e7a/downloads/energyblast-defold-debug.apk)** — **28,4 MB**.
Android 7/API 24+, ARM64; Version 0.6.0/Code 7. Das fertige APK ist auf Querformat
festgelegt. Gleiche Paketkennung und Entwicklungssignatur wie 0.5: als Update
installieren, **vorher nicht deinstallieren**. [Hash/Metadaten](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/downloads/README.md).
Der physische Handytest und eure grafische Abnahme bleiben offen.

## Grafik neu aufbauen statt nur umfärben

Nach der Ablehnung von 0.5 wurden offizielle **Brawl-Stars-Spielbilder** und
Produktionsberichte recherchiert und die tatsächliche Laufzeit überarbeitet.
[Quellen, Beobachtungen und konkrete Entscheidungen](docs/ART_DIRECTION.md).

- **Gestaltete Landschaft:** eigene Sandstein-/Gartenmaterialien, gegliederte
  Mauern mit Steinlagen und Kappen, erkennbare Umgebung statt Kachelbrett.
- **Plastische Figuren:** neu modellierte Entdecker-, Drachen- und Fuchsfigur.
  Gebackene Kontaktschattierung und weichere Beleuchtung erreichen tatsächlich
  den nativen Renderer. Kein besseres Konzeptbild als Ersatz für das Spielmodell.
- **Tatsächliche Animation:** bewegliche Arme/Beine, Flügel und Schwanz, kleine
  Leerlaufbewegungen, geglättetes Drehen, Rückstoß und sichtbare Trefferreaktion.
- **Animiertes 3D-Menü:** dieselbe Spielfigur auf einer Bühne; eigene plastische
  Bedienelemente mit Stern-, Herz-, Ziel- und Funksymbolen.
- **Klares Querformat:** zusammenhängende 992×528-Spielfläche im 1280×720-Layout.
  Steuerung und HUD liegen außen. Die große Welt und folgende Kamera bleiben.
- **Räumliche Effekte:** Feuerbälle, Licht und kurze vergangene Spuren sind
  tiefengeprüft; keine darübergelegten GUI-Schüsse und kein vorhergesagter Weg.
- **Geprüfte Zusammenfassung der Geometrie:** pro Arena 8 statt rund 450–480
  statischer Batches; dieselben Positionen bleiben erhalten. Keine versprochene
  Handy-Bildrate ohne Gerätetest.

Alle sechs Missionen, Punkte, Käufe, Hinweise und Spielstände bleiben.
[Umsetzung und Grenzen](docs/MILESTONE_05.md). Die persönliche grafische Abnahme
ist offen; technische Prüfungen erklären eine Darstellung nicht automatisch für gelungen.

## Drei Helden und drei zusätzliche Kampfsituationen

**Nova**, **Drache Flammi** mit sichtbaren Feuerbällen und bewegten Flügeln sowie
**Fennek** sind frei wählbar. Gleiche Spielstärke, keine Figur gegen Echtgeld.
Die Auswahl wird lokal gespeichert.

| Sektor | Was tatsächlich gespielt wird |
|---|---|
| Prisma-Station | Schildkanone durch einen klugen Abpraller treffen |
| Neon-Zitadelle | Zwei Kanonen, Deckung und zeitweise geöffnetes Tor |
| Aurora-Dock | Patrouille, Fächersalven, zwei Abprall-Schalter und geschützter Boss |
| **Magnetwerk** | Falle vorbereiten, patrouillierenden Wächter hineinlocken und den vorübergehend ausgeschalteten Schild nutzen |
| **Echo-Kammer** | Lichterfolge beobachten und Kristalle in dieser Reihenfolge treffen; gleichzeitig eine Kanone ausschalten |
| **Drohnen-Rettung** | Eine verwundbare Drohne um Deckungen begleiten und ihren Weg schützen |

Ein frisches Profil erreicht bis **1.200 Gesamtsterne**; mit alten 0.1-Erfolgen
bis 1.525. Wiederholen und Warten erzeugen keine doppelten Belohnungen.
Bedienung und Missionsziel werden gesprochen; die Lichtfolge lässt sich kostenlos
wiederholen. Kein vorgeschalteter Fragebogen, kein Joystick, keine berechnete Flugbahn.

## Tatsächliche Laufzeit — keine Konzeptbilder

![Neue animierte Menüfigur](docs/images/06-defold-menu.png)

![Tatsächliche Lauf-, Ziel- und Schusssequenz](docs/images/06-defold-gameplay.gif)

Native Linux-/OpenGL-Laufzeit mit wirklichen XTest-Eingaben. Keine behauptete
Handyaufnahme. [Echo-Kammer](docs/images/06-defold-echo.png),
[Figurenwahl](docs/images/06-defold-characters.png).

## Bedienung

| Eingabe | Wirkung |
|---|---|
| Kurz drücken und loslassen | Laufen, unabhängig davon, welches Objekt angetippt wurde |
| Mindestens **0,30 s** halten | An beliebiger Stelle zielen |
| Nach dem Halten loslassen | Ein Schuss / Feuerball |
| FEUER halten | Wiederholt schießen |
| DASH | Kurz geschützt ausweichen |
| FALLE im Magnetwerk | Magnetfalle am aktuellen Standort vorbereiten |
| Funk | Mission/Bedienung wiederholen; in der Echo-Kammer Lichtfolge neu vorführen |
| Hinweis | Verdientes Guthaben für die optionale Schatzsuche einsetzen |

Manchmal muss man die Deckung verlassen. Warten allein ist keine Lösung.
Musik kann im Arsenal separat ausgeschaltet werden; TON schaltet alle Audios um.

## Tatsächliche Prüfungen und Grenzen

**28.10.2026:** **199 native Prüfungen** und **elf gemeinsame Testgruppen**
bestanden. Echte Menü-/Kauf-/Figuren-/Touch-Eingaben bei 1280×720 und nach
Fensteränderung auf 1280×800 geprüft. Wirklich bewegte Gliedmaßen und getrennte
Speicherneustarts geprüft. Wandverdeckung: 0 veränderte Pixel beim verdeckten
Geschoss, sichtbares Kontrollgeschoss einschließlich Licht vorhanden.

Exportierte Wandpositionen, AO-/Texturbindung und Erhaltung der statischen
Geometrie beim Batching geprüft. Native Musik-/Sprach-/Effektausgabe erneut
aufgezeichnet. Musik und Sprachdateien sind unverändert.
[Qualitätsüberblick](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/docs/QUALITY.md), [Befehle](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/docs/BUILD_AND_TEST.md).

**Offen für die neue APK:** physische Installation/Update und Spielstandübernahme,
Touch-/Klanggefühl, Geräte-Seitenverhältnisse, längere Runden und Geräteleistung.
Grafische Abnahme durch euch offen. Kein Hardwarebenchmark, keine empirisch
nachgewiesene Lernwirkung oder Store-Reife und keine grüne CI behauptet.

## Arbeitsweise und Herkunft

Spielcode: `feat/touch-shooter-v2`. `main` bleibt die Dokumentationsstartseite.
Keine PRs, automatischen Merges, Actions-Workflows oder GitHub-Releases.
Kinderwelt und andere Repositories bleiben unverändert. Keine privaten Bilder,
Konten, Werbung, Telemetrie oder neuen Berechtigungen. Lokale Daten, Backup aus.

[Regeln](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/shared/defold04.json), [Originalmodelle/Porträts](https://github.com/sayac007/EnergyBlast/tree/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/shared/assets/defold06),
[Blender-Generator](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/tools/make_defold06_models.py), [Musikgenerator](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/tools/make_defold_music.py),
[Kollision/Geschosse](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/pilots/defold/main/projectiles.lua),
[Käufe/Migration](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/pilots/defold/main/progression.lua),
[neue Ziele](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/pilots/defold/main/objectives.lua),
[Herkunft/Lizenzen](https://github.com/sayac007/EnergyBlast/blob/3485ac6a56431920c4b3b64d5f8b593cf283bc0c/THIRD_PARTY.md), [Dokumentationsstandard](docs/DOCUMENTATION_STANDARD.md).
