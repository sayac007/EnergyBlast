# EnergyBlast — Defold 0.8

Ein Offline-Touch-Shooter mit Deckung, Abprall-Schüssen und drei wählbaren Helden.
Die neue Fassung macht Fortschritt, Schatzsuche, Käufe und Bonusziele sichtbar.
Die Grafik von 0.7 bleibt erhalten; Defold ist der Schwerpunkt.

| Einstieg | Weiterlesen |
|---|---|
| Installierbare APK / Update | [Download und geprüfte Metadaten](downloads/README.md) |
| Was sich nach dem Spieltest geändert hat | [Meilenstein 07](docs/MILESTONE_07.md) |
| Tatsächliche Prüfungen / offene Geräteprobe | [Qualitätsstatus](docs/QUALITY.md) |
| Bauen / Auftrag / Recherche | [Befehle](docs/BUILD_AND_TEST.md), [Projektauftrag](docs/PROJECT_BRIEF.md), [Art Direction](docs/ART_DIRECTION.md) |

**[EnergyBlast 0.8 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/5c8e1ca956e99abd805cc29f90f9ee6620a7a5ce/downloads/energyblast-defold-debug.apk) — 44,1 MB.**
Android 7/API 24+, ARM64. Über die bisherige Defold-App installieren; **nicht vorher
deinstallieren**, damit lokale Sterne und Käufe erhalten bleiben. Entwicklungssignatur,
Paketkennung und Speicherort sind unverändert. [Hash/Metadaten](downloads/README.md).

## Wo finde ich was?

- **Drache wählen:** Auf der Startseite direkt das Bild **Drache Flammi** antippen.
  Alle drei Helden bleiben sichtbar. Auch das Heldenbild im Spiel öffnet die Wahl.
- **Sterne ausgeben:** Goldene Schaltfläche auf der Startseite → Bild/Effekt ansehen
  → **Kaufen**. Prisma-Waffe, mehr Gesundheit, Tempo und Tarnung. Gesundheitskauf
  wirkt sofort; Gesamtsterne bleiben, nur das verfügbare Guthaben sinkt.
- **Offene Schätze:** Oben steht **Schatz 0/1** oder **1/1**. Antippen aktiviert
  einen kostenlosen goldenen Wegweiser zum Suchgebiet. Bei Annäherung wird die
  Truhe sichtbar. Nach Missionsabschluss führt er direkt zum verbliebenen Schatz.
- **Nächste Mission:** Nach dem Sieg ausdrücklich **Nächste Mission** antippen.
  Der Schatz und die Bonusziele sind freiwillig. Wer weitersucht, kann jederzeit
  über **Weiter** wechseln. Die aktuelle Mission bleibt beim Neustart gespeichert.
- **Neue Aufgaben:** Magnetfallen, Lichterfolge und Drohnenrettung sind deutlich
  markiert. Außerdem enthält **jede Mission zwei Bonusziele direkt im Spielfeld**.

## Mehr Sterne und integrierte Boni

| Erfolg | Einmalige Sterne |
|---|---:|
| Mission geschafft | 300 |
| Ohne Schaden / Drohne unbeschädigt | 100 |
| Schatz gefunden | 75 |
| Goldenen Kristall durch einen echten Abpraller treffen | 100 |
| Lichterfolge oder grünes Zeitfenster lösen | 150 |
| Maximum pro Mission | **725** |

Sechs Missionen ergeben bis **4.350 Sterne**, mit alten 0.1-Erfolgen bis 4.675.
Vorhandene Erfolge werden mit den erhöhten Werten bewertet; Käufe, Figur, Hinweise
und Musik bleiben erhalten. Wiederholen erzeugt keine doppelten Belohnungen.

Die Boni sind tatsächliche Schussaufgaben in der normalen Arena, keine zusätzliche
Bonusmission und kein vorgeschalteter Fragebogen. Die Lichterfolge wird beobachtet
und nachgespielt. Beim Zeitfenster muss das Kind auf Grün warten; Dauerfeuer startet
nur die Wartephase neu. Kein Verlust von Gesundheit oder schon verdienten Punkten.
Auch nach dem Sieg können die offenen Boni in Ruhe gelöst werden.

## Tatsächliche neue Laufzeit

![Direkte Heldenwahl und Missionen](docs/images/08-defold-menu.png)
![Klare Käufe](docs/images/08-defold-shop.png)
![Nächste Mission trotz offenem Schatz](docs/images/08-defold-win.png)

Native Linux-/OpenGL-/XTest-Aufnahmen, keine behaupteten Handyaufnahmen.
[Bonusziele](docs/images/08-defold-bonus.png), [Schatzsuche](docs/images/08-defold-treasure.png).

## Bedienung bleibt

Kurz antippen läuft, mindestens **0,30 Sekunden halten** zielt, Loslassen feuert.
FEUER und DASH bleiben. Fallen werden im Magnetwerk vollständig auf dem Spielfeld
gewählt und platziert. [Fallenbedienung](docs/TRAPS.md). Kein Joystick und keine
berechnete Flugbahn. Gegner-/Relais-/Ausgangsziele, Schatz und Boni haben getrennte
Zähler und Richtungszeichen. Angetippte Zähler erklären ihr aktuelles Ziel.

## Prüfstand und Grenzen

Die bisherigen Spieltests bleiben mit unveränderter 0.7-Regelfixture erhalten;
zusätzliche Prüfungen decken den neuen Spielfluss und die Bonusaufgaben ab.
Tatsächlich ausgeführte Tests und Artefaktprüfung: [Qualitätsstatus](docs/QUALITY.md).
Die neue Handy-/Tablet-Probe, Hörverständnis, Schwierigkeit und Geräteleistung
bleiben offen. Keine behauptete Store-Reife oder empirische Lernwirkung.

Spielcode: `feat/touch-shooter-v2`; `main` bleibt Dokumentationsstartseite.
Keine PRs, Spielmerges, neuen Actions oder Releases. Kinderwelt, Godot-0.2- und
GDevelop-0.3-Vergleichsfassungen bleiben unverändert. Keine privaten Familienbilder,
Konten, Werbung oder Telemetrie. Lokale Daten, keine Android-Berechtigungen, Backup aus.

[Regeln](https://github.com/sayac007/EnergyBlast/blob/952a5639c69267cb8d9a78a8e168d33886ef7a3b/shared/defold04.json), [Spielfluss](https://github.com/sayac007/EnergyBlast/blob/952a5639c69267cb8d9a78a8e168d33886ef7a3b/pilots/defold/main/mission_flow.lua),
[Boni](https://github.com/sayac007/EnergyBlast/blob/952a5639c69267cb8d9a78a8e168d33886ef7a3b/pilots/defold/main/bonus.lua), [Bildherkunft](https://github.com/sayac007/EnergyBlast/blob/952a5639c69267cb8d9a78a8e168d33886ef7a3b/shared/assets/defold07/PROVENANCE.json),
[Lizenzen](THIRD_PARTY.md), [Dokumentationsstandard](docs/DOCUMENTATION_STANDARD.md),
[vorheriger Stand](docs/MILESTONE_06.md).
