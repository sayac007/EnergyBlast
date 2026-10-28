# Meilenstein 02 — Aurora Raid, Version 0.3

**28.10.2026.** Zweite Spielrunde mit **Defold 1.14.0** und **GDevelop 5.6.269**.
Der Betreiber bevorzugt diese beiden nach seinem Test und lobt besonders
Defolds klare Eingabe. Godot 0.2 bleibt unverändert und separat herunterladbar.
[Auftrag und neue Entscheidung](PROJECT_BRIEF.md), [Ausgangsvergleich](MILESTONE_01.md).

## Was sich tatsächlich geändert hat

| Auftrag | Umgesetzt | Grenze |
|---|---|---|
| Mehr spielerische Komplexität | Dritter Sektor mit zwei Abprall-Relais, drei Kanonen, geschütztem Boss, Patrouille, Fächersalven und zeitgesteuertem Ausgang | Drei kompakte Arenen, noch keine große Kampagne |
| Ansprechendere Grafik | Neu modellierter Held mit Ionentanks/Antenne, eigene Arenenfarben, Landeringe, Bodenleitungen, Lüftungen, Servicetürme, rotierende Radarschüssel, schwebende Relais und Trefferpartikel | Stilisierte einfache 3D-Geometrie; Defolds Figur dreht/wippt als Ganzes, GDevelop bewegt zusätzlich Gliedmaßen |
| Keine berechnete Flugbahn | Nur Zielmarke, tatsächliche Geschosse und lokales Warnleuchten; keine Schuss-/Abpralllinie und keine vorgezeichnete gegnerische Schussbahn | Die Physik berechnet Kollisionen intern weiterhin; bezahlte Beutehinweise zeigen einen Suchort |
| Gehen und Schießen trennen | Boden-/Deckungstipp läuft; Tipp auf sichtbares Ziel oder Reflektor feuert; Ziehen/Loslassen feuert; Fingerzuordnung und Abbruch beim Hintergrundwechsel | Echtes Multi-Touch-/Rotationsgefühl braucht den erneuten Android-Test |
| Vergleichbar bleiben | Gemeinsame Regeln, Modelle, Missionen, Belohnungen und neue deutsche Ansagen in beiden Apps | Native Defold-Grafik und GDJS/WebView-Licht/Materialien unterscheiden sich |

Ein echter nativer Mausklick im Defold-Menü deckte einen Kontextfehler auf:
Die GUI rief eine Lua-Closure auf, die `go.delete`/`factory.create` ausführte.
Closures wechseln Defolds Script-Kontext nicht. Die Auswahl sendet jetzt eine
Nachricht an `main.script`, das die Objekte im richtigen Kontext ersetzt.
Ein neuer Test klickt tatsächlich den dritten Sektor und FEUER an.

## Die drei spielbaren Sektoren

1. **Prisma-Station:** Einstieg in Schild und Abpraller. Zwei wirksame Wandtreffer.
2. **Neon-Zitadelle:** Zwei Kanonen, Deckung und ein wiederkehrendes Torfenster.
3. **Aurora-Dock:** Zwei goldene Relais widerstehen direkten Schüssen. Beide müssen
   über reflektierende Wände getroffen werden. Ein Patrouillengegner kann die
   Schussroute kreuzen; während seiner Ladung steht er und hält die Zielrichtung.
   Eine weitere Kanone und der Boss verschießen je drei Geschosse als Fächer.
   Der Boss bleibt bis zum Ausfall beider Relais geschützt, auch gegen Abpraller.
   Nach allen Gegnern muss der Kern im offenen Torfenster erreicht werden.

Eine grüne Energiezelle heilt einmal pro Versuch einen Treffer; sie entfernt
keinen erlittenen Schaden aus der Wertung für einen fehlerfreien Abschluss.
Die verborgene Dock-Ausrüstung gibt 75 Sterne und verkürzt DASH dauerhaft von
2,8 auf 2,24 Sekunden. Hinweise müssen weiterhin verdient werden.

**Sterne:** Ein frisches Profil kann jetzt **600** sammeln: 150 + 175 + 275.
Zusätzlich erhaltene historische 0.1-Punkte erlauben bis zu 925. Alte 0.2-Sterne,
Ausrüstung und bereits bezahlte Hinweise bleiben in derselben lokalen Speicherung.
Warten und Wiederholungen zahlen keine zusätzlichen Abschlusssterne.

## Bedienung für den Vergleich

- Boden oder Deckung antippen: laufen beziehungsweise nächster erreichbarer Ort.
- Sichtbare Kanone/Relais oder leuchtenden Reflektor antippen: schießen.
- Ziehen und loslassen: frei zielen und feuern, ohne vorausberechnete Lösung.
- FEUER halten: wiederholte Schüsse. DASH: kurzer geschützter Ausweichschritt.
- Funk: kurze Ansage wiederholen. Hinweis: verdientes Guthaben für Beute einsetzen.

Die Missionswahl steht offen: Dock lässt sich direkt ausprobieren, ohne zunächst
Sterne zu sammeln. Mit einem frischen Profil ist der Abschluss technisch geprüft.

## Tatsächlich am 28.10. ausgeführt

| Prüfung | Ergebnis | Grenze |
|---|---|---|
| Defold, native Linux/OpenGL-Laufzeit | 42 Kampf-/Eingabeprüfungen bestanden | Cloud mit Softwaregrafik und Sound-Nullgerät |
| Defold GUI | Echter Menü- und FEUER-Klick bestanden; Objekte erfolgreich ersetzt | XTest-Mausereignisse unter Xvfb, kein physischer Android-Touch |
| Defold Speicher | Getrennte Schreib-/Lesestarts mit alten/neuen Sternen, Dock-Ausrüstung und bezahlten Hinweisen bestanden | Kein Geräte-Update-Test |
| GDevelop | 51 Prüfungen in echter Chromium/WebGL-Laufzeit bestanden, keine Seitenfehler/externe Requests | Touch-Emulation, kein Hardwarebenchmark |
| Gemeinsame Daten/Medien | Sechs Testgruppen bestanden; Hashes, Modellkopien, 29 Ogg-Dateien decodiert, Pegel/Dauer, Punkteökonomie und Offline-Manifeste | Kein menschlicher Hörnachweis |
| Erhaltene Regression | 43 alte und 24 Shooter-Godot-Prüfungen samt Speicherneustart; 32 alte GDevelop-Prüfungen bestanden | Godot bleibt inhaltlich 0.2 |
| Sichtprüfung | Beide 0.3-Laufzeiten gerendert, Menü und Dock selbst angesehen | Keine gemessene Gerätebildrate |

Die Kampfprüfungen spielen die neue Relais-/Boss-Abfolge mit tatsächlich bewegten
Geschossen durch, prüfen blockierte Direkt-/Boss-Treffer, Patrouille und Ladestopp,
Fächersalve, Heilungsgrenze, erreichbare Flanken, Ausgang und einmalige Belohnungen.
GDevelop prüft außerdem die tatsächlich gezeichneten SVG-Elemente beim Zielen:
Zielkreise vorhanden, keine vorausberechneten Linien.

Befehle/Voraussetzungen: [BUILD_AND_TEST.md](BUILD_AND_TEST.md). Aktueller
[Qualitätsüberblick](QUALITY.md). Quellcommit, endgültige APK-Hashwerte, Größen und
technische Paketprüfungen stehen bei den [Downloads](../downloads/README.md)
und in den zugehörigen `*-verification.json`-Dateien. Abschließende APKs werden
vom sauberen Quellcommit gebaut und gesondert versioniert. Kein Actions-Lauf,
PR, Merge oder GitHub-Release gehört zu dieser Veröffentlichung.

## Noch prüfen und rückmelden

Beide APKs auf demselben Handy installieren beziehungsweise über 0.2 aktualisieren,
ohne vorher zu deinstallieren. Sterne vor/nach dem Update vergleichen. Dann den
Dock-Sektor testen: Ziel-/Laufeingabe, Winkel ohne Vorschau, Verständlichkeit von
Relais/Boss-Schutz, Schwierigkeit, Ton, Drehung und Flüssigkeit.

Diese neuen APKs sind noch nicht auf einem echten Handy/Tablet von uns geprüft.
Der Betreiber-Test der vorherigen Fassung ist keine Abnahme von 0.3. Kein Nachweis
für Lerntransfer oder alltagsbezogene Impulskontrolle, keine Play-Freigabe.

```text
Engine / Gerät / Android:
Frisches Profil oder Update von 0.2; Sterne erhalten:
Zielen und Gehen klar getrennt:
Dock: Relais und Boss verständlich / zu leicht / zu schwer:
Welche Engine fühlt sich besser an:
Nächste wichtigste Verbesserung:
```

Der unabhängige Whisper-small-Screen der drei neuen Ansagen erkennt **2/3**
normalisiert exakt. Bei „Triff“ erkennt er „trifft“; Satz und Kerninhalt werden
sonst erkannt. Das ist kein bestätigter Aussprachefehler und keine menschliche
Hörabnahme. Der ältere 25/26-Screen bleibt ein historischer 0.2-Nachweis.

## Erzeugte Android-Dateien

Am 28.10.2026 vom sauberen Quellcommit
[`4352737`](https://github.com/sayac007/EnergyBlast/commit/43527374e1705a9608a9ddb11ccc8e4af31ef69e)
wirklich gebaut: **Defold 9.065.658 Bytes**, **GDevelop 2.153.923 Bytes**.
Version 0.3.0 / Code 3, API 24–36, Paketkennungen unverändert.
Paket-/Versionsprüfung, Entwicklungssignatur/v2, gleiches Zertifikat wie 0.2,
keine Berechtigungen, Backup aus, ZIP-CRC und Ausrichtung bestanden. GDevelop
enthält nachweislich die neuen Regeln und unveränderte Kopien der neuen Audios.
Hashes und Dateilinks: [Downloads](../downloads/README.md). Godot-APK unverändert.
Keine physische Installation oder Spielrunde mit den neuen APKs behauptet.
