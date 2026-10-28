# Meilenstein 04 — Defold 0.5, Toybox Raid

**28.10.2026.** Umsetzung der sieben Rückmeldungen aus dem gemeinsamen Test
von 0.4.1. Brawl Stars dient als visuelle Referenz für kräftige Farben,
übersichtliche Silhouetten und unmittelbares Feedback. Keine übernommenen
Figuren, Modelle, Aufnahmen oder Melodien. Keine behauptete Gleichwertigkeit
mit dessen Produktionsumfang. [Aktueller Auftrag](PROJECT_BRIEF.md).

## Auftrag und tatsächlich spielbare Änderungen

| Rückmeldung | Umsetzung |
|---|---|
| Deckung verlassen darf nötig sein | Flankieren, gegnerische Zielbindung, Abpraller und DASH bleiben. Kein automatisches Zielen oder sicherer Treffer aus jeder Deckung. |
| Kein Schießen durch sichtbare Wände | Echte 3D-Geschosse mit derselben Tiefenprüfung wie die Wände. Sichtbare Wandkörper und Kappen liegen exakt in den Kollisionsflächen. Neue geschlossene Tore sind echte 3D-Körper; geöffnete Tore sind frei. |
| Kein HUD über dem Spielfeld | Einheitlicher Ausschnitt zwischen logischem y=260 und y=1100. Punkte, Gesundheit, Übersicht und alle Aktionstasten liegen außerhalb. Menü, Arsenal und Figurenwahl ersetzen die pausierte Szene vollständig. |
| Geheimnisse müssen auffindbar sein | Jeder Sektor besitzt kostenlose, in den Boden gemalte goldene Pfeile und dunkle Spuren/Luken nahe dem Versteck. Die Truhe wird in der Nähe sichtbar. Verdiente, bezahlte Richtungs-/Nähehinweise bleiben optional. |
| Ausrüstung wirklich kaufen | Vier funktionierende Käufe für 100/160/230/300 Sterne, dauerhaft gespeichert und ausgerüstet. Kumulierte Gesamtsterne und ausgebbares Guthaben sind getrennt. |
| Grafik und Musik verbessern | Sechs kräftig gefärbte Spielinseln, breitere klare Wandkronen, eigener Toon-Shader, Kontakt-Schatten, neue Figurenporträts, lebendige Flügel und native Energie-/Feuergeschosse. Neu arrangierte eigene Stereo-Musik mit neun synthetischen Instrumenten und vier unterschiedlich dichten Abschnitten. |
| Weitere Aufgabenarten und Figuren | Drei neue taktische Sektoren sowie Nova, Drache Flammi und Fennek frei wählbar. Auswahl und Käufe bleiben nach einem Neustart erhalten. |

## Die sechs Missionen

Die bisherigen **Prisma-Station**, **Neon-Zitadelle** und **Aurora-Dock** bleiben
mit Deckung, Winkel, Abprall-Schaltern, Boss, Heilzelle und Torfenster erhalten.
Dazu kommen drei tatsächliche Kampfsituationen, keine Aufgabenformulare:

- **Magnetwerk — vorbereiten und den Moment nutzen.** Lege eine Magnetfalle
  auf den Patrouillenweg. Der Wächter verliert beim Betreten für 3,5 Sekunden
  seinen Schild und hält an. In diesem Zeitfenster treffen. Bis zu zwei Fallen,
  vier Sekunden Abklingzeit, zwölf Sekunden Lebensdauer; kein Sternegewinn fürs Warten.
- **Echo-Kammer — beobachten und eine Reihenfolge behalten.** Drei nummerierte
  Kristalle blinken in einer wiederholten Folge. Dieselben Lichter erscheinen
  im reservierten HUD, auch wenn die Figur gerade woanders steht. Die Kristalle
  in der beobachteten Folge treffen; ein falscher Treffer setzt nur die Folge
  zurück. Die aktive Kanone muss ebenfalls ausgeschaltet werden. Funk wiederholt
  die Ansage und startet die kostenlose Lichtdemonstration neu.
- **Drohnen-Rettung — Wege und Schutz einschätzen.** Eine Drohne folgt ihrer
  Route nur, wenn die Figur höchstens 3,2 Einheiten entfernt ist. Gegnergeschosse
  können die Drohne treffen; sie hat drei Energiepunkte. Begleite sie um die
  Deckungen zum Ausgang. Allein zum Ausgang zu laufen reicht nicht. Gegner können
  ausgeschaltet oder umgangen werden; kein bloßer Zeitbonus. Der Bonus für perfekten Schutz erfordert unbeschädigte
  Figur und Drohne.

Kurzer Tipp bewegt weiterhin ausschließlich. Ab **0,30 Sekunden** wird frei
gezielt, Loslassen feuert. FEUER halten, DASH und Funk bleiben. Keine berechnete
Flugbahn, kein Joystick. Alle drei Figuren haben gleiche Trefferfläche und
Spielstärke; Flammi verschießt sichtbare Feuerbälle und bewegt seine Flügel.

## Kauf, Fortschritt und Updates

| Kauf | Preis | Tatsächlicher Effekt |
|---|---:|---|
| Prisma-Kanone | 100 | Zwei statt einem Abpraller; nach Kauf kostenlos an-/abschaltbar |
| Rüstung | 160 | Ein zusätzlicher maximaler Energiepunkt, auch sofort beim Kauf |
| Tempostiefel | 230 | Laufgeschwindigkeit +0,5 Einheiten/s |
| Tarnmodul | 300 | Gegnerische Erfassungsreichweite ×0,825; keine vollständige Unsichtbarkeit |

Gesamtsterne fallen beim Kauf nicht. Guthaben = Gesamtsterne minus die einmalig
bezahlten Kaufpreise. Ein frisches Profil kann **1.200 Sterne** in sechs Sektoren
erreichen; mit alten 0.1-Erfolgen maximal 1.525. Wiederholen und Warten zahlen nicht
doppelt. Eine vollständige Mission gibt weiterhin zwei Hinweisguthaben.

Vor 0.5 wurden die vier Verbesserungen automatisch ab Punktschwellen gewährt.
Die einmalige Spielstandmigration erhält diese bereits verdiente Ausrüstung
kostenlos, ohne alte Sterne abzuziehen. Neue Profile kaufen ausdrücklich im
Arsenal. Die Datenmigration und tatsächlich getrennte Schreib-/Lesestarts mit
Käufen, Restguthaben, Figur, Hinweisen und Musikpräferenz sind geprüft.

Gleiche Paketkennung und Entwicklungssignatur erlauben ein vorgesehenes Update;
den echten Geräte-Update-Test der neuen APK ersetzen die technischen Prüfungen
nicht. Vor dem Update nicht deinstallieren, wenn der lokale Spielstand bleiben soll.

## Nachgewiesene Fehlerursache und Absicherung

Die vorherigen Schüsse wurden als GUI-Kreise nach der gesamten 3D-Szene gezeichnet.
Damit konnten Schüsse optisch über einer davorliegenden Wand erscheinen, obwohl
die Physik sie korrekt dahinter hielt. Wandkappen und dekorative Eckpfeiler konnten
zusätzlich über die tatsächlichen Kollisionsflächen hinausreichen.

Jetzt sind Geschosse native Modelle mit Tiefenprüfung. Alle statischen Wandkörper
kommen aus derselben Flächenspezifikation; Kappen ragen nicht darüber hinaus.
Dekorative Wandpfeiler im begehbaren Bereich wurden entfernt. Geschlossene Tore
verwenden einen maßstäblichen, live geschalteten Körper. Bodenfarbe, flache
Spuren und blau gekennzeichnete Neutralisationsfelder sind erkennbar keine Wände.

Der neue Bild-Regressionstest vergleicht drei tatsächlich gerenderte Szenen:
ohne Geschoss, Geschoss hinter Deckung und sichtbares Kontrollgeschoss davor.
**Hinter Deckung: 0 veränderte Pixel; davor: 318 sichtbare Pixel** im ersten
verifizierten Lauf. Der sichtbare Kontrollfall verhindert einen falschen Erfolg,
falls gar keine Schüsse gezeichnet würden. Zusätzlich werden die tatsächlichen
exportierten glTF-POSITION-Puffer gegen sämtliche Kollisionsrechtecke geprüft.

Die bisherigen Grenzen bleiben: ein Abpraller, Prisma zwei, Gegner einer;
Reichweite und 3/6 Sekunden Lebensdauer. Energiegeschosse schrumpfen vor dem
Verpuffen; blaue X-Felder absorbieren beide Seiten. Keine echte Waffenballistik.

## Tatsächlich ausgeführt

Stand des Quellpakets; endgültige Quell-/APK-Referenzen stehen bei den
[Downloads](../downloads/README.md). Befehle: [Build-/Testanleitung](BUILD_AND_TEST.md).

- **187 native Prüfungen bestanden:** bisherige 107 und 80 neue Fälle für alle
  sechs Oberflächenbestände, begehbare Schatzspuren, HUD-Grenzen, Käufe, kein
  Doppelkauf/negative Salden, Migration, Figur/Feuerball, Falle, Lichtfolge,
  begleitete Route, Drohnenschaden und Wiederholungsbelohnungen.
- **Echte native Eingaben bestanden:** Menü, beide neuen Figuren gewählt,
  Prisma/Rüstung gekauft, Mission gestartet, kurzer Tipp, langer Hold, FEUER,
  TON aus/an. Kein GUI-/Gameobject-Kontextfehler. Laufende HUD-Tasten auf
  Überschneidung mit dem Spielfeld geprüft.
- **Getrennte Speicherprozesse bestanden:** 375 Gesamtsterne, 115 Restguthaben
  nach zwei Käufen, Drache, Rüstung/Prisma, Hinweise und Musik aus erhalten.
- **Tatsächliche Audioausgabe aufgezeichnet:** Musik an, aus und mit Sprache/
  Explosion. Nullsignal bei aus, Signal bei an, kein digitaler Überlauf der
  geprüften Mischung. Zusätzlich reale Abschnittsdynamik/Stereounterschiede
  der neuen Ogg-Aufnahme geprüft.
- **Unabhängige Spracherkennung:** 5/5 vollständige Sätze normalisiert exakt,
  ohne Referenztexte als Erkennungsprompt. Ein zuerst undeutlich erkannter
  Satz wurde neu formuliert und erzeugt. Keine menschliche Hörabnahme behauptet.
- **Neun gemeinsame Testgruppen bestanden:** alte Daten-/Modellkopien der
  eingefrorenen Engines, Medien/Hashes, neue Geometriepuffer, Musikdynamik,
  Berechtigungen/Backup und fehlende Schussbahn-Vorschau.
- Native Spiel-/Menübilder selbst angesehen. Keine Konzeptbilder; Screenshots
  entstehen in der Linux-/OpenGL-Laufzeit unter Xvfb. Kein Gerätebenchmark.

## Tatsächliche Laufzeitbilder

| Figurenwahl | Echo-Kammer |
|---|---|
| ![Originalfiguren](images/05-defold-cast.png) | ![Neue Lichtfolge-Mission](images/05-defold-echo.png) |

[Native Sektorauswahl](images/05-defold-menu.png). Direkt aus der Defold-Laufzeit
aufgenommen; kein Mock-up und keine neue Android-Geräteaufnahme.

## Grenzen und nächste Abnahme

Physische Installation/Update, Touchgefühl, Rotation und Seitenverhältnisse,
Klangabnahme, längere Runden, Schwierigkeit und Hardwareleistung der **0.5-APK**
bleiben manuell zu prüfen. Die Rückmeldungen zur Vorgängerversion sind
Betreiberbeobachtungen, keine von uns ausgeführte neue Android-Prüfung.

Die pädagogischen Bezüge sind **Designhypothesen** (Winkel, räumliche Wege,
Vorbereitung, Arbeitsgedächtnis und situationsgerechtes Handeln). Weder ein
Lerneffekt noch eine Übertragung der Impulskontrolle in den Alltag ist empirisch
nachgewiesen. Die App bleibt ein kleiner Offline-Shooter, kein Brawl-Stars-Klon,
kein Multiplayer-/Store-Release und keine ausgebaute Kampagne.

GDevelop 0.3 und Godot 0.2, deren Dateien und APKs bleiben unverändert. Keine PRs,
Merges, Actions-Workflows, GitHub-Releases oder Schreibzugriffe auf andere Repos.
Keine Konten, Werbung, Telemetrie, privaten Familienbilder oder neuen Berechtigungen.
