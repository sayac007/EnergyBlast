# EnergyBlast — Ricochet Raid 0.2

Ein **Touch-Shooter** für Android: Wandkanonen greifen an, sichtbare Geschosse
fliegen, Deckung schützt und geschickte Abpraller überwinden einen Schild.
Geometrie und Timing ergeben sich aus dem Spielen. Keine Abfrageaufgaben und
kein verpflichtendes „Tipp abgeben“ vor dem Schuss.

## Spielen

- **Tippen auf den Boden:** laufen. **Ziehen und loslassen:** zielen und schießen.
- Kanone oder leuchtende Wand antippen: gezielter Schuss. **FEUER halten:** weiterfeuern.
- **DASH:** kurz ausweichen; danach lädt die Fähigkeit wieder auf.
- Energie ist sichtbar. Bei einer Niederlage bleibt die Gesamtpunktzahl erhalten;
  der Sektor lässt sich direkt neu starten. „Funk“ wiederholt die kurze Ansage.

Die beiden ersten Sektoren verwenden dieselben selbst erstellten 3D-Arenen,
Figuren und Kampfregeln in **Godot, GDevelop und Defold**:

1. **Prisma-Station:** Eine geschützte Kanone feuert direkt auf dich. Gerade
   Schüsse prallen am Schild ab; ein Schuss über die leuchtende Wand trifft.
2. **Neon-Zitadelle:** Zwei unabhängig angreifende Kanonen, Deckungen und der
   Energiekern hinter einem angekündigten, wiederkehrenden Torfenster.

Sterne, Ausrüstung und bezahlte Hinweise bleiben lokal gespeichert. Einmalige
Ziele/Bonusfunde bringen bis zu **325 neue Sterne**. Die Sterne aus 0.1 bleiben
bei Updates der Godot-/GDevelop-App erhalten; zusammen sind derzeit 650 möglich.
Bei 100/160/230/300 Sternen werden Prisma, Rüstung, Tempo und Tarnung wirksam.
Versteckte Linse/Stiefel ergänzen die Ausrüstung. Hinweise auf Beute verdient man
mit Missionen; Bedienung und Funk kosten keine Hinweisguthaben.

**[Die drei Android-Test-APKs herunterladen](downloads/README.md)**

Die Apps besitzen unterschiedliche Paketnamen und können nebeneinander
installiert werden. Spielstände werden nicht zwischen Engines übertragen.
Debug-Signierung, keine Play-Release-Dateien und keine automatische Veröffentlichung.

## Tatsächlicher Stand

| Engine | Laufzeit und prüfbarer Build | Grenze |
|---|---|---|
| Godot 4.7.2 | native 3D-Laufzeit, Kampf-/Touch-/Speichertests, ARM64-APK | echtes Handy-/Tablet-Bediengefühl und Leistung noch offen |
| GDevelop 5.6.269 | reale GDJS-3D-Laufzeit, Touch-Gesten im Chromium-Browser, Offline-WebView-APK | zusätzlich vom Android-System-WebView abhängig |
| Defold 1.14.0 | native 3D-Laufzeit, Kampf-/Projektions-/Neustarttests, ARM64-APK | echte Android-Gesten, Ton und Leistung noch offen |

Alle drei Szenen wurden tatsächlich gerendert und visuell geprüft. Das ist noch
kein gemeinsamer Android-Benchmark. Godot/GDevelop animieren benannte Körperteile;
Defold nutzt zunächst die bewegte/gedrehte Gesamtfigur mit Lauf-Bob und Kanonen-
Drehung. Schatten/Materialdarstellung unterscheiden sich. Die endgültige Engine-
Entscheidung soll aus euren Tests entstehen.

BRUTAL wurde anhand von Dokumentation, Plattformcode und NuGet-Paketen geprüft:
ein C#/.NET-10-Framework ohne fertigen Renderer/Editor, mit dokumentierten Desktop-
Laufzeiten. Einzelne Android-Vulkan-Bindings sind kein fertiger Android-Export.
Anschließend hat der Betreiber Godot, GDevelop und Defold gewählt. Der alte Unity-
Importkit ist historisch vorhanden und zählt nicht als ausgeführter Prototyp.

[Qualität, konkrete Testergebnisse und offene Geräteprüfungen](docs/QUALITY.md)
· [Befehle und Werkzeugversionen](docs/BUILD_AND_TEST.md)
· [Herkunft und Lizenzen](THIRD_PARTY.md)

## Entwicklung

Regeln: `shared/combat.json`; Originalmodelle: `shared/assets/shooter/`.
Eigene Blender-Generatoren, gemeinsame Sprachclips/Schrift und getrennte Engine-
Implementierungen liegen im Repository. Der alte Geometriepilot bleibt als
Regression erhalten und ist nicht mehr der Startbildschirm.

```bash
python3 tools/sync_assets.py
python3 tools/sync_unity.py
python3 tools/sync_defold.py
node tools/gdevelop_export.mjs
python3 tools/check_shared.py
python3 tools/check_godot.py
python3 tools/check_gdevelop_combat.py
python3 tools/check_defold.py
```

Voraussetzungen und die zusätzliche alte GDevelop-Regression stehen in der
Buildanleitung. Keine Benutzerkonten, Werbung, Telemetrie oder Netzwerkverbindung
im Spiel; die APKs fordern keine Berechtigungen an. Kinderwelt bleibt unverändert.
Passende öffentliche Audioaufnahmen wurden ausdrücklich erlaubt übernommen.
Keine Familienbilder oder privaten Schlüssel im Repository. Keine empirisch
belegte Lernwirkung oder allgemeine Verbesserung der Impulskontrolle behauptet.
Eigene Projektinhalte haben noch keine gewählte Nutzungslizenz; Fremdlizenzen
bleiben erhalten.
