# EnergyBlast

Ein kleiner Android-Spielpilot für Kinder von 7–10 Jahren:
**Beobachten → Planen → Handeln.** Freundliche Roboter, kurze Versuche und klare
Touch-Steuerung ohne Joystick. Das eigenständige öffentliche Projekt lässt
Kinderwelt unverändert.

## Jetzt spielbar

Zunächst **zwei Missionen**:

- **Bandenschalter:** Zielen, den Auftreffpunkt schätzen und einen Energieschuss
  über die leuchtende Wand zum gelben Knopf lenken.
- **Wächter und Energietor:** Deckung und Patrouille beobachten, ein Fangfeld
  vorbereiten und nach drei Lichtern das wiederkehrende Zeitfenster nutzen.

Boden antippen = laufen. Große Symbole wählen Zielen, Tipp, Schuss und Fangfeld.
Missionen und Hinweise werden gesprochen; „Erklären“ wiederholt die Erklärung.
Grundlegende Spielhilfen sind immer kostenlos.

Sterne bleiben nach dem Neustart erhalten. Bei **100 / 160 / 230 / 300 Sternen**
werden Prisma-Waffe, Rüstung, schnelleres Laufen und teilweise Tarnung wirksam.
Zwei versteckte Ausrüstungsfunde bringen zusätzliche Sterne. Hinweise darauf
verdient man durch Missionen; gekaufte Hinweisstufen bleiben gespeichert.
Warten, Fehlversuche und Wiederholungen erzeugen keine zusätzlichen Punkte.
Der Pilot bietet insgesamt höchstens **325 Sterne**, noch keinen langen Feldzug.

Die [Test-APKs und ihre Build-Nachweise](downloads/README.md) liegen auf
`feat/touch-mission-pilot`. Es sind Entwicklungsversionen für manuelle Tests,
keine Google-Play-Releases. Godot nutzt `org.example.energyblast.pilot`, der
GDevelop-Vergleich `org.example.energyblast.gdevelop`; beide können nebeneinander
installiert werden. Eigene Spielstände werden nicht zwischen ihnen übertragen.

## Was tatsächlich geprüft ist

| Versuch | Ausgeführt | Noch offen |
|---|---|---|
| Godot 4.7.2 | echter 3D-Start/Render, 43 Spielprüfungen, Speichern über Prozessneustart, Android-APK | Bediengefühl, Audio, Rotation und Leistung auf einem echten Android-Gerät |
| GDevelop 5.6.269 | echter WebGL-Export, Touch-/Spiel-/Speicher-/Sprachwarteschlangenprüfungen im Chromium-Browser, Android-WebView-APK | dieselben echten Gerätetests; Abhängigkeit von installierter Android System WebView |
| Unity | gemeinsamer Figuren-/Missions-Importkit und C#-Syntaxprüfung | aktivierter Editor fehlt: kein nachgewiesener Import, keine Kompilierung, kein Android-Build |

Es gibt **keinen abgeschlossenen Drei-Engine-Leistungstest** und noch keinen
belegten Engine-Sieger. Die [zentrale Qualitätsübersicht](docs/QUALITY.md)
trennt ausgeführte Prüfungen, Grenzen und das gemeinsame Geräte-Testprotokoll.
Verbesserungen von Geometrieverständnis oder allgemeiner Impulskontrolle sind
pädagogische Hypothesen, keine empirisch nachgewiesenen Wirkungen.

## Einstieg für die Entwicklung

Gemeinsame Regeln und Originalfigur: `shared/pilot.json`, `shared/assets/`.
Die Engine-Piloten liegen unter `pilots/`; Synchronisation/Export unter `tools/`.
[Reproduzierbare Befehle](docs/BUILD_AND_TEST.md) enthalten die Voraussetzungen
und dieselben aktuellen Testaufrufe:

```bash
python3 tools/sync_assets.py
python3 tools/sync_unity.py
node tools/gdevelop_export.mjs
python3 tools/check_shared.py
python3 tools/check_godot.py
python3 tools/check_gdevelop.py
```

Der Node-Export benötigt die zuvor installierten, gepinnten GDevelop-Werkzeuge;
Godot-/Chromium-Pfade können gemäß Anleitung angepasst werden.

Das [ursprüngliche Pilot-Briefing](docs/pilot-brief.md) und die
[aktuellen Touch-/Belohnungsentscheidungen](docs/touch-pilot.md) erklären den
Umfang. Keine Pull Requests, automatischen Merges oder Releases in dieser Phase.
Kinderwelt wird nur für ausdrücklich erlaubte passende Audioaufnahmen gelesen.
Keine Familien-Assets, Benutzerkonten, Telemetrie oder Online-Spielverbindungen.

## Herkunft und Rechte

Figur und Kulisse werden aus eigenem Code erzeugt. Vier passende Sprachclips
sind mit Zustimmung übernommen, 15 Missionssätze neu erzeugt. Quellen, Hashes,
Modell- und Engine-Hinweise: [THIRD_PARTY.md](THIRD_PARTY.md).
Für eigene neue Inhalte ist noch keine Projektlizenz gewählt; die Öffentlichkeit
des Repositories erteilt allein keine Nutzungslizenz. Fremdlizenzen bleiben erhalten.
