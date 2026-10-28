# EnergyBlast — erster Shooter-Vergleich

**Stand 28.10.2026: Meilenstein 01, Testfassung 0.2.** Ein eigenständiger
Android-Touch-Shooter für Kinder etwa von 7 bis 10 Jahren: Kanonen greifen an,
Deckung schützt und kluge Abpraller überwinden einen Schild. Geometrie und Timing
werden beim Spielen relevant. Die endgültige Engine und das Spielgefühl sind
noch nicht abgenommen.

**[Ausführliches aktuelles README mit Umfang und offenen Punkten](https://github.com/sayac007/EnergyBlast/blob/feat/touch-shooter-v2/README.md)**

| Was du beurteilen möchtest | Dokumentation |
|---|---|
| Ausgangsauftrag und spätere Entscheidungen | [Konsolidierter Projektauftrag](docs/PROJECT_BRIEF.md) |
| Erster Schritt: umgesetzt, geprüft, offen | [Meilenstein 01 mit Auftragsabgleich](docs/MILESTONE_01.md) |
| Ursprüngliche vollständige Instruktion | [Historisches Auftragszitat](docs/pilot-brief.md) |
| Code und drei Engine-Implementierungen | [Arbeitsbranch `feat/touch-shooter-v2`](https://github.com/sayac007/EnergyBlast/tree/feat/touch-shooter-v2) |

## Die drei Test-APKs

| Engine | Direkter Download | Größe | Technik |
|---|---|---:|---|
| Godot 4.7.2 | [Godot-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-godot-debug.apk) | 30,3 MB | native ARM64-3D-Engine |
| GDevelop 5.6.269 | [GDevelop-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-gdevelop-debug.apk) | 1,7 MB | GDJS/WebGL in einer Offline-Android-WebView |
| Defold 1.14.0 | [Defold-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-defold-debug.apk) | 8,7 MB | native ARM64-3D-Engine |

Alle drei lassen sich parallel installieren; die Spielstände sind unabhängig.
Android 7 / API 24 oder neuer, für Godot/Defold ARM64, für Godot OpenGL ES 3 und
für GDevelop eine funktionierende System-WebView mit WebGL. Deren installierte
Größe steckt nicht in der GDevelop-APK-Größe. Es sind Debug-Testfassungen,
keine Play-Upload-Dateien. [Installationshinweise und Build-Metadaten](https://github.com/sayac007/EnergyBlast/blob/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/README.md).

## Was bereits spielbar ist

**Prisma-Station:** Eine stationäre Schildkanone lädt und feuert. Gerade Schüsse
überwinden ihren Schild nicht; ein Schuss über die leuchtende Wand trifft.

**Neon-Zitadelle:** Zwei unabhängig angreifende Kanonen, Deckungen und ein
Energiekern hinter einem angekündigten, wiederkehrenden Torfenster.

Boden antippen: laufen. Ziehen und loslassen: zielen und schießen. FEUER halten:
weiterfeuern. DASH: kurz ausweichen, dann Abklingzeit. „Funk“ wiederholt die kurze
deutsche Ansage kostenlos. Treffer ziehen sichtbare Energie ab; eine Niederlage
erlaubt direkten Neustart und löscht gespeicherte Sterne nicht.

- Neue gemeinsame 3D-Figur und zwei Arenen. Godot/GDevelop animieren Körperteile;
  Defold bisher Gesamtdrehung und Lauf-Bob. Darstellung und UI-Details unterscheiden sich.
- Sterne für erstmaligen Abschluss, schadensfreien Abschluss und versteckte Funde.
  **325 neue Sterne** sind erreichbar, mit übernommenen 0.1-Punkten bis zu **650**.
  Wiederholungen zahlen nicht doppelt.
- Freischaltungen bei **100/160/230/300** Sternen: Prisma, zusätzliche Energie beim
  Sektorstart, Tempo und kürzere gegnerische Erfassungsreichweite. Ein visueller
  Tarnshader fehlt noch. Versteckte Linse/Stiefel ergänzen die Ausrüstung.
- Beutehinweise werden durch Missionen verdient und bleiben nach Kauf verfügbar.
  Noch keine große Kampagne, Charakter-/Kostümwahl oder Hintergrundmusik.

## Was tatsächlich geprüft ist

Die Spiel-/Buildtests wurden am **27.10.2026** ausgeführt:

| Bereich | Ergebnis |
|---|---|
| Aktueller Shooter | Godot **24**, GDevelop **28**, Defold **17** Prüfungen bestanden |
| Alte Regression | Godot **43**, GDevelop **32** Prüfungen bestanden |
| Speicher/Medien | Neustart-/Formatmigration und vier gemeinsame Testgruppen bestanden |
| Grafik | Alle drei Laufzeiten tatsächlich gerendert und visuell geprüft |
| APK-Dateien | Paket/Version, Entwicklungssignatur, keine angeforderten Berechtigungen, Backup aus und ZIP-Ausrichtung geprüft |

Am 28.10. wurden Dokumentation, Referenzen und die vorhandenen Dateien geprüft;
alle drei auf Commit festgelegten öffentlichen APKs wurden erneut heruntergeladen
und per SHA-256 bestätigt. Keine neuen Spieltests oder APK-Builds. In diesem Stand gibt es keinen GitHub-
Actions-Workflow und keinen zusätzlich behaupteten grünen CI-Lauf.

**Offen:** Installation/Update, Ton, Rotation und Bediengefühl auf echten Handys/
Tablets sowie ein Leistungs-/Akkuvergleich auf demselben Gerät. Die gewünschte
Spielqualität ähnlich Kinderwelt und eine pädagogische Lernwirkung sind noch
nicht als erreicht abgenommen. Es gibt deshalb keinen belegten Engine-Sieger.
[Ausführlicher Prüfbericht und Geräteprotokoll](https://github.com/sayac007/EnergyBlast/blob/feat/touch-shooter-v2/docs/QUALITY.md).

## Auftrag und feste Ausgangsreferenz

Ausgangspunkt war ein kleiner Engine-Vergleich für Orientierung, Abprallwinkel
und situationsgerechtes Handeln. Der Betreiber entschied anschließend:
eigenes öffentliches Repository, Touch ohne Joystick, gespeicherte Sterne und
Ausrüstung, verdiente Beutehinweise sowie ein **echter Shooter mit Lerneffekt**.
Die bestätigte Auswahl ist **Godot, GDevelop und Defold**. Unity blieb ein
historischer unkompilierter Importkit; BRUTAL wurde geprüft und anschließend
nicht in die Dreierauswahl aufgenommen. [Vollständige Einordnung](docs/PROJECT_BRIEF.md).

- Shooter-Quellstand: [`1006cde`](https://github.com/sayac007/EnergyBlast/tree/1006cde8595b4249d0375ddf8bc4ea60fd2a93c9).
- Drei APKs samt SHA-256-/Buildnachweisen: [`defd791`](https://github.com/sayac007/EnergyBlast/tree/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads).
- Die direkten Downloads oben sind auf diesen Commit festgelegt. Sie laufen
  nicht wie zeitlich begrenzte Actions-Artefakte ab.

`main` veröffentlicht derzeit diesen Überblick und den Auftrag. Der Spielcode
bleibt auf dem verlinkten Arbeitsbranch. Kein Spielcode automatisch gemergt,
kein PR und kein GitHub-Release erstellt. Kinderwelt bleibt unverändert.
[Bauen/Testen](https://github.com/sayac007/EnergyBlast/blob/feat/touch-shooter-v2/docs/BUILD_AND_TEST.md)
· [Assetherkunft und Lizenzen](https://github.com/sayac007/EnergyBlast/blob/feat/touch-shooter-v2/THIRD_PARTY.md).
Eigene Projektinhalte haben noch keine gewählte Nutzungslizenz; Fremdlizenzen
bleiben erhalten.

## Ergänzende Instruktionen

Für die nächste Iteration helfen konkrete Beobachtungen und höchstens drei
Prioritäten. Diesen kurzen Rahmen kannst du als nächste Nachricht verwenden:

```text
Getestete Engine(s) und Gerät/Android-Version:
Sektor und konkrete Situation:
Was gefällt / was stört:
Priorität 1:
Priorität 2:
Priorität 3:
Engine-Auswahl offen / bevorzugt:
```
