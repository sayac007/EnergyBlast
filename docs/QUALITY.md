# Aktueller Prüfstand — Shooter 0.2

**27.10.2026.** Die aktuellen Startszenen sind echte Kampfarenen. Der alte 0.1-
Geometriepilot ist eine zusätzliche Regression. Maßgeblich für die ausgelieferten
Dateien ist der Quellcommit in den [Download-Metadaten](../downloads/README.md).
Eine erfolgreiche alte Prüfung ersetzt keine Prüfung des neuen Shooters.

## Ausgeführt

| Prüfung | Tatsächliches Ergebnis | Grenze |
|---|---|---|
| Godot alter Geometriekern | 43 Prüfungen, 0 Fehler | archivierter Ablauf |
| Godot Shooter | 24 Prüfungen, 0 Fehler | echte Szene, simulierte Touch-Ereignisse/Zeitschritte, Testaudio ausgeschaltet |
| Godot lokaler Spielstand | getrennter Schreib-/Neustartprozess bestanden | kein physischer Android-Update-Test |
| GDevelop alter Ablauf | 32 Browserprüfungen bestanden | separater Legacy-Export |
| GDevelop Shooter | 28 Browserprüfungen bestanden | echte WebGL-Laufzeit mit Touch-Emulation, kein Android-Gerät |
| Defold Shooter | 17 Prüfungen in der nativen 1.14.0-Laufzeit bestanden | Linux/OpenGL unter Xvfb, Sound-Nullgerät |
| Defold lokaler Spielstand | Schreiben und neuer Prozess bestanden | tatsächlicher privater lokaler Dateipfad, keine Gerätemessung |
| Gemeinsame Daten/Assets/Medien/Manifeste | vier Testgruppen bestanden; alle 26 Ogg-Dateien decodiert, Hash/Dauer/Pegel geprüft | kein menschlicher Hörtest |
| Unabhängiger ASR-Screen | 25/26 Texte normalisiert exakt erkannt; neue Kampfansagen 6/7 | „Triff“ als „Trift“ erkannt; menschliche Artikulationsprüfung offen |
| Visueller Lauf | Godot, GDevelop und Defold tatsächlich gerendert und Bilder selbst geprüft | Software-Grafik/Cloud, keine gemessene Android-Bildrate |
| Android | drei Debug-APKs tatsächlich gebaut; technische Nachweise bei den Downloads | keine physische Installation/Spielrunde hier ausgeführt |

Die Abschlussexporte erfolgen vom committeten sauberen Quellstand. APK-Nachweise
enthalten Datum, SHA-256, Bytes, Version, Paket, Signaturart und Quellcommit.
Die Dateien werden nach dem Push zusätzlich heruntergeladen und gegen ihre
Hashes geprüft. Keine Schlüsseldateien in Repository oder APKs.

## Was die Kampfprüfungen absichern

- Kanonen laden sichtbar, fixieren die Schussrichtung und erzeugen bewegte
  Projektile. Ausweichen kann helfen; die Ladung verfolgt nicht unsichtbar jede Bewegung.
- Gegnergeschosse können Energie abziehen. Deckung stoppt sie. Kurze Treffer-
  Unverwundbarkeit verhindert sofortiges Leeren mehrerer Energieeinheiten.
- Direkte Treffer überwinden den ersten Schild nicht. Ein tatsächliches Projektil
  nach einem Abpraller beschädigt die Kanone; zwei Treffer sichern den ersten Sektor.
- Tap-to-move ohne Moduswahl; Ziehen/Loslassen mit Projektion in Weltkoordinaten.
  GDevelop verwendet dafür echte Chromium-Touch-Ereignisse. Sichtbare Deckung und
  Kollisionskoordinaten werden nach dem glTF-Achsenwechsel verglichen.
- Dash, Abklingzeit, Niederlage und direkte Neustartfläche; Sterne bleiben erhalten.
- Einmalige Zahlungen, verdiente Hinweise, kein Punktegewinn durch Warten und keine
  doppelte Siegesvergütung. Ein später gelungener schadensfreier Bonus bleibt möglich.
- Migration alter Godot-/GDevelop-Sterne und bereits bezahlter Hinweise, zusätzliche
  neue Missionsbelohnungen. Defold besitzt einen eigenen unabhängigen Spielstand.
- Geschlossenes Tor führt zur Warteposition; das wiederkehrende Fenster verlangt
  eine neue aktive Bewegung. Keine automatisch vorgemerkte Durchquerung.

Alte Kernprüfungen erhalten zusätzlich Reflexionsgesetz, Sichtlinien, Fangfeld,
Speicherökonomie und Torzyklus. Das Fangfeld gehört zum alten Pilotablauf; im
aktuellen Shooter ersetzt der direkte Dash die frühere Modusleiste.

## Konkrete behobene Darstellungsfehler

GDevelop dreht und normalisiert glTF-Modelle anders. Arenen und lokale Figuren
benötigen unterschiedliche Achsen-/Ursprungskonvertierung; die Deckung passt jetzt
auch sichtbar zur Kollision. Die Kamera verwendet dieselbe schräge Draufsicht wie
Godot/Defold. Ein sichtbarer Import allein hätte diesen Fehler nicht nachgewiesen.

Defold las zunächst seine Standard-2D-Renderkonfiguration, weil die Renderdatei
unter dem falschen Konfigurationsabschnitt stand. Die 3D-Datei gehört unter
`bootstrap.render`. Das wurde korrigiert und durch Konfigurationsprüfung plus
native gerenderte Bilder überprüft. Ein erfolgreicher Logiktest war dafür nicht genug.
Die Prüfskripte brechen vor dem Start ab, wenn der native Build fehlschlägt, damit
kein alter kompilierter Stand versehentlich als neuer Test gilt.

## APK-Technik und Grenzen

Erwartet sind Version 0.2.0 / Code 2, drei getrennte Paketkennungen, gültige
Entwicklungssignatur, keine angeforderten Berechtigungen, deaktiviertes Backup und
geprüfte ZIP-Ausrichtung mit 16-KB-Seiten. Das ist keine vollständige Play- oder
16-KB-Zertifizierung der nativen Bibliotheken. Release-Schlüssel werden nicht benutzt.

Die ursprüngliche Godot-Vorlage warnt bei `aapt2` über einen Verweis auf
`themed_icon.xml`. Das Launcher-Icon bleibt Bestandteil des manuellen Gerätechecks.
GDevelop ist eine echte GDJS/WebGL-Implementierung in einer lokalen Android-
WebView-Hülle; die APK-Größe enthält nicht die bereits installierte System-WebView.
Defold verwendet native Modelle, hat aber erst Lauf-Bob/Gesamtdrehung statt derselben
Einzelteilanimation. Keine erfundenen Entwicklungsstunden oder Leistungsranglisten.

## Gemeinsames Geräteprotokoll — offen

1. Die drei APKs auf demselben Handy/Tablet installieren. Geräte-/Android-/WebView-
   Version und Build-SHA lokal notieren; keine Namen oder Aufnahmen des Kindes.
2. Prisma-Station: Tippen, Ziehen/Loslassen, FEUER halten, Dash und Schild ausprobieren.
   Ist die Treffer-/Abprallerwirkung ohne Lesen verständlich? Start/Ende der Funk-
   Ansagen vollständig anhören und bei Bedarf wiederholen.
3. Neon-Zitadelle: Deckung, zwei Gegner und Lichtfolge testen. Auch falsches Timing,
   Niederlage und Neustart prüfen. Reaktion/Symbole/Touch-Abdeckung vergleichen.
4. Sterne/Hinweise erspielen, vollständig beenden und neu starten. Godot/GDevelop
   als Update über 0.1 installieren und vorhandene Sterne vergleichen. Deinstallation
   löscht lokale Daten; sie ist kein geeigneter Test für Erhalt beim Update.
5. Hintergrund/Vordergrund, Stummschaltung, Rotation, kleine/große Bildschirme,
   System-Zurück, Launcher-Icon und längere Spielrunde prüfen.
6. Dieselbe Strecke mit vergleichbarem Ausrüstungsstand spielen. Ruckeln, Touch-
   Verzögerung, Erwärmung und Akkuverbrauch beobachten; Messmethode mit angeben.

Die Engine-Wahl ist nach diesen echten Gerätetests zu treffen. Das Ziel ist ein
unterhaltsamer Shooter mit möglichem Lerneffekt durch Winkel, Deckung und Timing.
Lerntransfer oder Alltags-Impulskontrolle sind hier nicht empirisch nachgewiesen.
Keine personenbezogene Forschung, Telemetrie oder Fernübertragung ist eingebaut.

Befehle: [BUILD_AND_TEST](BUILD_AND_TEST.md). Laufzeitlogs/ASR-Ausgaben bleiben
außerhalb von Git; aktuell gepflegt werden Übersicht, Anleitung und Download-
Provenienz. Keine PRs, automatischen Merges oder Releases. Kinderwelt ist unverändert.
