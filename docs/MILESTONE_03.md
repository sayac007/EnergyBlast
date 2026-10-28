# Meilenstein 03 — Defold 0.4, Aurora Hop

**28.10.2026.** Schwerpunkt nach dem Betreiber-Test: Defold. Beauftragt sind
klare Zeitsteuerung, synthetische Hintergrundmusik, größere Spielfelder und
animierte Zerstörung. [Aktueller Auftrag](PROJECT_BRIEF.md).
[0.3-Vergleich erhalten](MILESTONE_02.md), [0.2-Ausgangsvergleich](MILESTONE_01.md).

## Umsetzung und Bedienung

| Wunsch | Tatsächliche Änderung |
|---|---|
| Kurz drücken = laufen | Unter 0,30 s wird ausschließlich ein Laufziel gesetzt, auch auf Gegnern, Schaltern oder Wänden. Unbegehbare Stellen werden auf einen erreichbaren Ort abgebildet. |
| Länger drücken = zielen | Ab 0,30 s aktiviert sich an jeder Stelle freies Zielen; Bewegung hält an. Eine Füllanzeige zeigt den Übergang. Loslassen feuert einmal. Ein schneller Wischer löst keinen Schuss aus. |
| Keine dünne Wand treffen müssen | Der Finger gibt eine freie Richtung/Stelle vor. Die Wand bleibt physisch reflektierend. Keine Zieltyp-Heuristik und keine vorausberechnete Schussbahn. |
| Größeres Spielfeld | Alle drei Arenen von 14×10 auf **21×15** erweitert: **2,25-fache Fläche**. Wege, Deckungen, Schalter, Tore, Patrouille und Geheimnisse entsprechend versetzt. |
| Handy-taugliche Darstellung | Folgende Kamera statt winzig herausgezoomter Figuren; Miniübersicht im HUD. Eigener Spielausschnitt hält Weltmarkierungen von Bedienelementen fern. Warnungen für ladende Gegner außerhalb des Bildes erscheinen am Rand. |
| Hintergrundmusik | **Aurora Hop**, eigene mathematisch synthetisierte Chiptune-Komposition: 32 Takte, 128 BPM, 60 Sekunden, Schleife. Leiser während Ansagen; separat im Arsenal abschaltbar, Einstellung bleibt lokal gespeichert. TON schaltet auch Musik stumm. |
| Bessere animierte Grafik | Hellerer eigener Shader, differenzierte Bodenplatten, Leitungen, Dachdetails. Letzter Treffer: kurzer Lichtimpuls, expandierender Energiering, zehn räumlich fliegende/drehende Fragmente und schrumpfender Zielkörper. |

FEUER halten und DASH bleiben erhalten. Der Druckzeitmesser verwendet die volle
verstrichene Framezeit; langsames Rendern darf den Zielwechsel nicht künstlich
verzögern. Hintergrundwechsel, Menü und fremde Finger können keinen hängenden
Schuss auslösen. Kamera bleibt während eines anliegenden Feldkontakts ruhig.

Die bisherige Kurz-Tipp-auf-Gegner-/Reflektor-Schussregel wurde ausdrücklich
entfernt. Das ist eine beauftragte Änderung gegenüber 0.3.

## Spielumfang und Fortschritt

Weiterhin drei Sektoren: Prisma-Station, Neon-Zitadelle, Aurora-Dock. Aktive
Kanonen, Deckung, Abpraller, Patrouille, Fächersalve, zwei Schalter vor dem Boss,
Heilzelle, zeitgesteuerter Ausgang und versteckte Ausrüstung bleiben spielbar.
Die vollständigen Abschlüsse der erweiterten Arenen sind mit bewegten Geschossen
geprüft, einschließlich der beiden Dock-Abpraller.

Punkteökonomie unverändert: **600 Sterne** im frischen Profil; bis 925 mit
historischen 0.1-Sternen. Erhalt von Sternen, Ausrüstung und bezahlten Hinweisen
beim Prozessneustart geprüft. Gleiche Paketkennung und Entwicklungssignatur sind
für ein Update vorgesehen. Echte Geräte-Datenübernahme bleibt eine manuelle Prüfung.

Die Explosionsanimation läuft auch nach einem Sieg weiter. Erst nach 0,95 s
erscheint der Ergebnisdialog; sonst würde er die letzte Explosion sofort verdecken.
Effekte werden begrenzt, nach Ablauf gelöscht und beim Sektorwechsel aufgeräumt.
GDevelop 0.3 und Godot 0.2 wurden weder umgebaut noch neu paketiert.

## Tatsächliche Prüfungen am 28.10.2026

| Prüfung | Ergebnis | Grenze |
|---|---|---|
| Defold native Laufzeit | **76** Kampf-/Eingabe-/Kamera-/Effektprüfungen bestanden | Linux/OpenGL unter Xvfb, keine Gerätebildrate |
| Beibehaltene Regression (Teil der 76) | 42 bisherige Fälle an ursprünglicher Arenageometrie, mit der neuen Zeitsteuerung | Alte Tipp-Schuss-Erwartung bewusst angepasst |
| Neue Fälle | 34 zusätzliche Prüfungen: Druckschwelle, stehender Hold, schnelle Wischbewegung, Zielfreiheit, Finger/Abbruch, langsame Frames, große Welt, Kamera, alle drei Abschlüsse, Effekte und verzögerter Ergebnisdialog | Simulierte Ereignisse/Zeitschritte im echten Engine-Prozess |
| Tatsächliche UI-Eingabe | Menü per XTest gewählt, **derselbe Feldpunkt** kurz und lang gedrückt: erst Bewegung ohne Schuss, dann genau ein Schuss; FEUER anschließend geprüft | Native Mausereignisse, kein physischer Android-Touch |
| Native Audioausgabe | Tatsächlichen Defold/OpenAL-Ausgang als WAVE aufgezeichnet: Musik an hörbares Signal, Musik aus Nullsignal; Sprach-/Effektmischung auf Pegel geprüft | Technischer Signalnachweis, keine menschliche Klangabnahme |
| Speicher | Getrennte Schreib-/Lesestarts mit alten/neuen Sternen, Ausrüstung, Hinweisen und ausgeschalteter Musik bestanden | Kein physischer Update-Test |
| Gemeinsame Konsistenz | Sieben Testgruppen: Daten/Hashwerte/Modelle/Medien, 30 Sprachaufnahmen sowie Musik und Explosionsklang decodiert; Dauer/Pegel/Schleifenübergang geprüft | Keine vollständige Geräte-/Hörzertifizierung |
| Neue Bedienansage | 6,52 s, unabhängiger Whisper-small-Screen **1/1** normalisiert exakt | ASR ersetzt keine menschliche Hörabnahme |
| Sichtprüfung | Arena und zeitlich verschiedene Explosionsbilder in nativer Laufzeit selbst angesehen | Softwaregrafik, kontrollierter letzter Treffer für die Aufnahme |

Die Musikprüfung fand eine doppelte Absenkung: statischer Sound-Gain 0,28 wurde
nochmals mit dem Laufzeit-Gain multipliziert. Der statische Gain ist jetzt 1;
die Lautstärke wird an einer Stelle geregelt. Ein Regressionstest kontrolliert
Sound-Konfiguration und tatsächliches Ausgangssignal. Muting wird am Signal,
nicht bloß an einem UI-Schalter geprüft.

[Befehle/Voraussetzungen](BUILD_AND_TEST.md), [aktueller Qualitätsüberblick](QUALITY.md).
Quellstand, Paketprüfung, Dateigröße und Hash stehen bei den [Downloads](../downloads/README.md).
APKs werden vom sauberen Quellcommit erzeugt und separat versioniert.

## Tatsächliche Laufzeitbilder

![Erweiterte Defold-Arena](images/04-defold-arena.png)

![Animierter endgültiger Treffer](images/04-defold-explosion.gif)

Native Softwaregrafik, keine Konzeptbilder. Für die Explosionsaufnahme wurde ein
letzter Treffer kontrolliert im selben Spielcode ausgelöst; keine behauptete
Handy-Spielrunde. Die folgenden Frames zeigen echte Fragmentbewegung.

## Noch offen

Auf dem Handy über die vorhandene Defold-App installieren, ohne sie vorher zu
löschen. Sterne und Musikpräferenz vergleichen. Besonders testen: kurze Tipps
auch auf Gegner, ruhiges längeres Drücken, Zielen an beliebigen Stellen, Loslassen,
Kamera beim Erkunden, Musiklautstärke gegen Ansagen, Musikschalter und Rotation.

**Keine neue physische Android-Installation/-Spielrunde durch uns verifiziert.**
Kein Hardwarebenchmark, keine empirisch bewiesene Lernwirkung, keine Play-Freigabe.
Es wurden keine PRs, Merges, Actions-Workflows oder GitHub-Releases angelegt.

```text
Gerät / Android:
Update von 0.3: Sterne erhalten?
Kurz drücken / lang drücken jetzt eindeutig?
Musik gut hörbar, Ansagen verständlich?
Kamera und Explosionen angenehm?
Nächste wichtigste Verbesserung:
```
