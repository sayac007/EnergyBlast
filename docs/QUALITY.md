# EnergyBlast: aktueller Qualitätsstand

Stand **27.10.2026**, erster Touch-Pilot mit zwei Missionen. Zweck: spielbare
Versuche vergleichen und Bedienung ausprobieren. Die Version ist kein fertiges
pädagogisch evaluiertes Produkt. Der Quellcommit der ausgelieferten Builds und
Dateihashes stehen unter [downloads](../downloads/README.md). Ergebnisse beziehen
sich auf diesen Pilotstand, nicht automatisch auf `main` oder spätere Änderungen.

## Ausgeführt

| Prüfung | Ergebnis | Praktische Grenze |
|---|---|---|
| Godot 4.7.2, echte Szenen-/Geometrietests | **43 Prüfungen, 0 Fehler** | Headless/Dummy-Audio, kein Android-Gerät |
| Godot Schreiben → Prozess beenden → neuer Prozess | **bestanden**: 100 Sterne, Prisma, ein gekaufter Hinweis, Wiederholung ohne Doppelvergütung | künstlicher Testspielstand, kein Geräte-Update-Test |
| GDevelop 5.6.269, echte exportierte Runtime in Chromium | **32 Prüfungen bestanden**, keine JS-Seitenfehler, keine externen Requests im geprüften Ablauf | Desktop-Touch-Emulation und Software-WebGL |
| Gemeinsame Regeln/Assets/Audio/Android-Konfiguration | **4 Testgruppen bestanden**, darunter alle 19 Ogg-Dateien mit FFmpeg decodiert | Laufzeit-/Sprachverständlichkeit nicht allein aus Dateiformat ableitbar |
| Unabhängiger Whisper-small-Screen aller Ansagen | **19/19 nach Normalisierung wortgetreu erkannt** | kein menschlicher Hörtest, keine Zertifizierung von Akzent/Betonung oder Verständlichkeit für Kinder |
| Echter Godot-OpenGL-Start/Render | Menü und beide Arenen gerendert und visuell geprüft | Cloud-Linux, keine gemessene Android-Bildrate |
| Android-Debug-APKs | Godot und GDevelop tatsächlich erzeugt; siehe Build-Metadaten | keine physische Installation/Spielrunde hier durchgeführt |
| Unity-Importkit | 3 C#-Dateien ohne Tree-sitter-Syntaxfehler | **nicht kompiliert**, kein Editor/Android-Lauf |

APK-Prüfungen: ZIP/APK lesbar, erwartete Paketkennung, Version 0.1.0 / Code 1,
minSdk 24, targetSdk 36, keine angeforderten Berechtigungen, `allowBackup=false`
im kompilierten Manifest, gültige Entwicklungssignatur, ZIP-Ausrichtung auch für
16-KB-Seiten. Das allein belegt keine vollständige 16-KB-/Play-Kompatibilität der
nativen Bibliotheken oder Google-Play-Uploadbereitschaft.

Godots Vorlage meldet beim `aapt2`-Ressourcenlesen einen fehlenden Verweis auf
`themed_icon.xml`. Das ist im Pilot-Manifestprotokoll sichtbar; Signatur/Export
bestehen trotzdem. Das Launcher-Icon muss auf dem Gerät geprüft werden. Das
Originalmodell ist unverändert in GLB/FBX vorhanden; Animationen bewegen dessen
benannte Einzelteile, noch kein professioneller Skeletal-Animation-Workflow.

## Was die Regression konkret absichert

- Einfalls-/Ausfallswinkel und analytischer Bank-Schuss. Normale Deckung absorbiert
  Schüsse, die leuchtende Wand reflektiert. Touch-Strahl und Tippmarker treffen die
  beabsichtigten Weltkoordinaten.
- Sichtkegel, Deckung und Fangfeld; das sichtbare Kegelfeld wird an Wänden begrenzt.
  Entdecken löst einen kurzen Neustart aus, keinen Punkteverlust.
- Tor 8-Sekunden-Zyklus mit 3-Sekunden-Fenster und drei Vorwarnlichtern. Vorzeitiges
  Antippen führt zur Warteposition, ohne später automatisch zu überqueren.
  Das offene Fenster ist mit Grundtempo durchquerbar. Der Zyklus wiederholt sich.
- Einmalige Ziele/Geheimnisse, Obergrenze 325 Sterne. Keine Belohnungen für bloßes
  Warten, wiederholte Abschlüsse oder erneute Auszahlung derselben Fertigkeitsboni.
- Zwei Hinweisguthaben je unterschiedlicher abgeschlossener Mission. Hinweisstufen
  sind dauerhaft gekauft und gegen Doppeltippen geschützt; Hauptanleitungen bleiben frei.
- Freischaltungen ändern echte Werte: Abprallerbudget, Entdeckungs-Reaktionszeit,
  Tempo, teilweise Sichtweitenreduktion. Versteckte Linse vergrößert die Treffer-
  toleranz, versteckte leise Stiefel senken zusätzlich die Wächter-Reichweite um 10 %.
- Chromium: Sprachdatei läuft vollständig aus, bevor eine nachfolgende Ansage beginnt;
  Hintergrundpause und Stummschaltung bleiben beim Fortsetzen erhalten. Dieser
  Wiedergabefortschritt ist kein Nachweis dafür, wie sich das Gerät anhört.

## Kleiner Engine-Vergleich

| Aspekt | Godot | GDevelop | Unity |
|---|---|---|---|
| Gemeinsame Figur/Regeln | GLB + gemeinsame JSON | dieselbe GLB/JSON im nativen Projekt | FBX aus derselben Blender-Geometrie; generierte C#-Regeln |
| Tatsächliche Laufzeit | Godot 3D | GDJS 3D-Objekte, dessen Renderer und Kamera; DOM/SVG-HUD | nicht ausgeführt |
| Android | native ARM64-Debug-APK, ca. 29 MB | GDJS-WebGL in eigener Offline-WebView-Hülle, ca. 1–2 MB; System-WebView nicht eingerechnet | kein Build |
| Konkrete behobene Hürden | ETC2/ASTC-Exportflag; isolierter Android-Pfad | falscher WASM-Script-Verweis im Community-Exporter; Kamera-/Touch-Achsen; lokale Gradle-/Proxy-/SDK-Konfiguration | Editor/Module/Aktivierung fehlen |
| Bedienung/Leistung auf demselben Handy | offen | offen | offen |

Die Arbeit wurde nicht zuverlässig engineweise gestoppt; erfundene Stundenangaben
wären irreführend. Die beobachteten Hürden ersetzen keine Aufwandsmessung. Godot
ist derzeit die direkt nativ testbare Fassung; die kleinere GDevelop-Datei ist
kein Beweis für schnellere oder bessere Ausführung. Vor einer endgültigen Wahl
müssen beide auf demselben Gerät ausprobiert und Unity separat importiert werden.

## Gemeinsames Geräte-Testprotokoll — offen

1. APKs aus demselben Quellcommit auf demselben Android-Handy/Tablet installieren.
   Modell, Android-/WebView-Version und Build-SHA lokal notieren, keine Namen des
   Kindes erfassen. Beide Apps können parallel installiert werden.
2. Jeweils Mission 1 ohne Lesestütze starten: Erklärung vollständig anhören,
   laufen/zielen/Tipp/Schuss anhand der Symbole finden. Verständlichkeit und
   vollständige Satzanfänge/-enden beobachten; „Erklären“ wiederholen, Ton umschalten.
3. Wächterdeckungen, Fangfeld und Lichtfolge ausprobieren. Früh/zu spät handeln,
   Retry und wiederkehrendes Fenster prüfen. Kann das Kind zeigen/erklären, weshalb
   es hier wartet und dort handelt? Kein globales „immer warten“ vorgeben.
4. Beide Geheimnisse ohne/mit verdientem Hinweis suchen, Ausrüstung testen.
   App vollständig beenden/neustarten: Sterne und verbrauchte Hinweise vergleichen.
   Noch einmal lösen: keine doppelten Punkte.
5. Hintergrund/Vordergrund, Drehen in beide Orientierungen, kleine/große Displays,
   System-Zurück, Launcher-Icon und Wiederinstallation als **Update** derselben
   Signatur prüfen. Ein Deinstallieren löscht den lokalen Spielstand.
6. Je Engine dieselbe fünfminütige Strecke spielen; Ruckeln, Reaktionsverzögerung,
   Erwärmung und Akkuverbrauch beobachten. Falls gemessen, Methode und Geräte-
   zustand mitnotieren. Cloud-Screenshots nicht als Android-Benchmark ausgeben.

Ein kurzer freiwilliger Kind-/Erwachsenen-Test kann Aufgabenverständnis und
Frustration zeigen. Alltags-Impulskontrolle oder Lerntransfer sind damit nicht
nachgewiesen. Dafür wären ein gesondertes Forschungsdesign, passende veränderte
Aufgaben und Schutz-/Einwilligungsentscheidungen nötig. Es werden hier keine
personenbezogenen Forschungsdaten oder Video-/Sprachaufnahmen erhoben.

## Aufbewahrung und nächste Schritte

Aktuelle Befehle: [BUILD_AND_TEST](BUILD_AND_TEST.md). Laufzeitlogs/ASR-Ausgaben
bleiben außerhalb des Git-Checkouts; keine neuen Einzelberichte pro Testlauf.
Die Download-Metadaten erhalten Quellcommit, Builddatum, Größe und SHA-256.
Entwicklungsschlüssel bleiben außerhalb von Git. Keine CI-Artefaktflut, keine
Release-Publikation, keine PRs oder automatischen Merges. Kinderwelt ist unverändert.

Offen bleiben echte Geräte-/Hörtests, Unity-Editorprüfung und eine darauf gestützte
Engine-Entscheidung. Erst nach Rückmeldung weitere Missionen, bessere Animationen
und eine größere Inhalts-/Belohnungsökonomie entwickeln.
