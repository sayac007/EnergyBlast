# EnergyBlast — erster Shooter-Vergleich

**Stand 28.10.2026: Meilenstein 01, Testfassung 0.2.** Ein eigenständiger
Android-Touch-Shooter für Kinder etwa von 7 bis 10 Jahren: aktive Kanonen,
Deckung, Ausweichen und kluge Abpraller. Winkel und Timing werden beim Spielen
relevant. Die endgültige Engine und die Qualität des Spielgefühls sind noch
nicht abgenommen.

| Für deine Beurteilung | Einstieg |
|---|---|
| Was war beauftragt, was wurde später geändert? | [Ausgangsauftrag und aktuelle Entscheidungen](docs/PROJECT_BRIEF.md) |
| Was ist umgesetzt, was fehlt und welche Nachweise gibt es? | [Meilenstein 01 mit Auftragsabgleich](docs/MILESTONE_01.md) |
| Wo ist das unveränderte ursprüngliche Auftragszitat? | [Historisches Briefing](docs/pilot-brief.md) |
| Wie wird gebaut und geprüft? | [Build-/Testanleitung](docs/BUILD_AND_TEST.md) und [Qualitätsbericht](docs/QUALITY.md) |

## Die drei Apps ausprobieren

Die folgenden Downloads sind auf den ersten APK-Commit festgelegt; spätere
Branchänderungen ersetzen diesen dokumentierten Ausgangsstand nicht.

| Testfassung | Direkter Download | Größe | Laufzeit |
|---|---|---:|---|
| Godot 4.7.2 | [Godot-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-godot-debug.apk) | 30,3 MB | native ARM64-3D-Engine |
| GDevelop 5.6.269 | [GDevelop-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-gdevelop-debug.apk) | 1,7 MB | GDJS/WebGL in einer Offline-Android-WebView |
| Defold 1.14.0 | [Defold-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-defold-debug.apk) | 8,7 MB | native ARM64-3D-Engine |

Alle drei lassen sich nebeneinander installieren und haben getrennte lokale
Spielstände. Benötigt werden Android 7 / API 24 oder neuer, für Godot/Defold ARM64,
für Godot OpenGL ES 3 und für GDevelop eine funktionierende System-WebView mit
WebGL. Deren Größe steckt nicht in der GDevelop-APK-Größe. Es sind Debug-Builds
für den Vergleich, keine Play-Upload-Dateien. [Details und Dateinachweise](downloads/README.md).

## Was du tatsächlich spielen kannst

**Prisma-Station:** Eine stationäre Schildkanone lädt sichtbar und feuert auf
dich. Gerade Schüsse überwinden ihren Schild nicht; ein Treffer über die
leuchtende Wand wirkt. Zwei wirksame Treffer sichern den Sektor.

**Neon-Zitadelle:** Zwei unabhängig angreifende Kanonen, Deckungen und ein
Energiekern hinter einem angekündigten, wiederkehrenden Torfenster. Die Kanonen
stehen derzeit auf Sockeln; es ist noch keine große Gegnerwelt.

| Bedienung | Wirkung |
|---|---|
| Boden antippen | Figur läuft dorthin |
| Ziehen und loslassen | Zielen und schießen |
| Kanone oder leuchtende Wand antippen | Gezielt feuern |
| FEUER halten | Wiederholt schießen |
| DASH | Kurz ausweichen; anschließend Abklingzeit |
| Funk | Kurze deutsche Ansage wiederholen, ohne Hinweisguthaben zu verbrauchen |

Treffer ziehen sichtbare Energie ab, Deckung hält Geschosse auf. Bei einer
Niederlage ist ein direkter Neustart möglich; gespeicherte Sterne bleiben erhalten.
Es gibt keinen verpflichtenden Antwort-/Vorhersagemodus vor dem Schießen.

## Fortschritt und aktueller Umfang

- Zwei Sektoren, eine gemeinsame stilisierte Roboterfigur und selbst erstellte
  3D-Arenen/Kanonen. Godot/GDevelop animieren Körperteile; Defold bisher
  Gesamtdrehung und Lauf-Bob. Materialien, Schatten und UI-Details unterscheiden sich.
- Lokale Sterne für erstmaligen Abschluss, schadensfreien Abschluss und
  Geheimfunde. Ein frisches 0.2-Profil kann **325 Sterne** erreichen. Mit
  übernommenen 0.1-Punkten sind bis zu **650** möglich; Wiederholungen zahlen nicht doppelt.
- **100 Sterne:** Prisma mit zwei möglichen Abprallern. **160:** zusätzliche Energie
  beim Sektorstart. **230:** höheres Tempo. **300:** kürzere gegnerische Erfassungsreichweite;
  ein visueller Tarnshader ist noch nicht umgesetzt.
- Versteckte Linse/leise Stiefel und Sterne. Pro unterschiedlichem Missionsabschluss
  entstehen zwei Hinweisguthaben; gekaufte Hinweisstufen bleiben gespeichert.
- Deutsche synthetische Funkansagen und Toneffekte. Noch keine Charakter-/Kostümwahl,
  kein Musiksystem und keine längere Kampagne.

Der erste geometrische Pilot 0.1 wurde auf ausdrücklichen Wunsch zum aktiven
Shooter weiterentwickelt. Seine Tests sind weiterhin eine zusätzliche Regression,
seine alten Aufgaben sind nicht die normalen Startszenen von 0.2.

## Was belegt ist — und was noch offen ist

Die Spiel-/Buildprüfungen stammen vom **27.10.2026**. Für diese Dokumentations-
veröffentlichung am 28.10. wurden keine neuen Spieltests oder APKs erzeugt.

| Belegter Lauf | Ergebnis | Grenze |
|---|---|---|
| Godot-Shooter | 24 Prüfungen bestanden | echte Szene mit simulierten Touch-/Zeitschritten in der Cloud |
| GDevelop-Shooter | 28 Prüfungen bestanden | echter Chromium/WebGL-Lauf mit Touch-Emulation |
| Defold-Shooter | 17 Prüfungen bestanden | native Linux/OpenGL-Laufzeit, Sound-Nullgerät |
| Zusätzliche Regression | 43 Godot- und 32 GDevelop-Prüfungen bestanden | alter 0.1-Kern |
| Speicher, Regeln und Medien | Neustart-/Migrationsprüfungen und vier gemeinsame Testgruppen bestanden | kein physischer Android-Update-Test |
| APKs | Paket/Version, Entwicklungssignatur, fehlende Berechtigungen, Backup aus und ZIP-Ausrichtung geprüft | kein vollständiger Play-/Gerätenachweis |

Alle drei Szenen wurden tatsächlich gerendert und visuell geprüft. Der unabhängige
Spracherkennungs-Screen erkennt 25/26 Texte exakt nach Normalisierung; eine
menschliche Hörabnahme ersetzt das nicht. Es gibt in diesem Stand keinen
GitHub-Actions-Workflow und keinen behaupteten grünen CI-Lauf.

**Offen:** echtes Handy-/Tablet-Bediengefühl, Rotation, Ton, Launcher-Icon,
Datenübernahme beim Geräte-Update, längere Spielrunde und Leistung auf demselben
Gerät. Deshalb gibt es noch keinen belegten Engine-Sieger. Auch die gewünschte
Spielqualität ähnlich Kinderwelt und ein tatsächlicher Lerntransfer sind nicht
als erreicht abgenommen. [Einzelheiten und Testprotokoll](docs/QUALITY.md).

## Ausgangsauftrag, Auswahl und feste Referenzen

Ausgangspunkt war ein kleiner Drei-Engine-Vergleich für räumliche Orientierung,
Abpraller und situationsgerechtes Handeln. Der Betreiber entschied anschließend:
öffentliches eigenes Repository, Touch ohne Joystick, gespeicherte Sterne/
Ausrüstung, verdiente Beutehinweise und ein echter Shooter mit Lerneffekt.
Die bestätigte Auswahl ist **Godot, GDevelop und Defold**. Unity blieb ein
historischer unkompilierter Importkit. BRUTAL wurde als Framework geprüft und
nach der Desktop-/Android-Bauweg-Prüfung nicht in diese Dreierauswahl übernommen.

| Referenz | Commit |
|---|---|
| Shooter-Quellstand | [`1006cde`](https://github.com/sayac007/EnergyBlast/tree/1006cde8595b4249d0375ddf8bc4ea60fd2a93c9) |
| Drei APKs samt Metadaten | [`defd791`](https://github.com/sayac007/EnergyBlast/tree/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads) |
| Aktive Implementierung | [`feat/touch-shooter-v2`](https://github.com/sayac007/EnergyBlast/tree/feat/touch-shooter-v2) |

`main` dient derzeit als aktuelle Dokumentationsstartseite. Der Spielcode liegt
isoliert auf dem Arbeitsbranch; es wurde kein Spielcode automatisch gemergt,
kein PR erstellt und kein GitHub-Release veröffentlicht. Die auf Commit
festgelegten APK-Dateien sind regulär versioniert und laufen nicht wie Actions-
Artefakte nach einer Aufbewahrungsfrist ab.

## Eine ergänzende Anweisung formulieren

Nach einer Spielrunde helfen vor allem konkrete Beobachtungen und höchstens drei
Prioritäten. Beispielsweise:

```text
Getestete Engine(s) und Gerät/Android-Version:
Sektor und konkrete Situation:
Was gefällt / was stört:
Priorität 1:
Priorität 2:
Priorität 3:
Engine-Auswahl offen / bevorzugt:
```

## Wo die Implementierung liegt

| Bestandteil | Einstieg im Arbeitsbranch |
|---|---|
| Gemeinsame Arenen, Gegner, Punkte und Kampfparameter | [shared/combat.json](shared/combat.json) |
| Aktueller Godot-Shooter | [pilots/godot/shooter.gd](pilots/godot/shooter.gd) |
| Aktueller GDevelop-Shooter | [pilots/gdevelop/shooter.js](pilots/gdevelop/shooter.js) |
| Aktueller Defold-Kampf und Laufzeit | [combat.lua](pilots/defold/main/combat.lua), [main.script](pilots/defold/main/main.script) |
| Originale 3D-Modelle und Erzeugung | [gemeinsame Assets](shared/assets/shooter/), [Blender-Generator](tools/make_shooter_models.py) |
| Ausgelieferte Dateien und technische Herkunft | [downloads](downloads/) |

Die Entwicklungs-/Prüfbefehle und Voraussetzungen stehen zentral in
[BUILD_AND_TEST.md](docs/BUILD_AND_TEST.md). [Herkunft und Lizenzen](THIRD_PARTY.md)
dokumentieren die Originalmodelle, zusätzliche Schrift und genehmigten Audioquellen.
Kinderwelt bleibt unverändert. Die APKs enthalten keine Benutzerkonten, Werbung
oder Spiel-Telemetrie und fordern keine Berechtigungen an. Eigene neue Projekt-
inhalte haben noch keine gewählte Nutzungslizenz; Fremdlizenzen bleiben erhalten.
