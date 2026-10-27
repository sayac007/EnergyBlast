# EnergyBlast 0.2 — drei Shooter-APKs

Zwei identische Kampfszenarien: Prisma-Station und Neon-Zitadelle. Keine Abfragen
mehr. Kanonen greifen an; Deckung, Dash und Abpraller helfen beim Gewinnen.

- **[Godot-APK herunterladen](https://github.com/sayac007/EnergyBlast/raw/refs/heads/feat/touch-shooter-v2/downloads/energyblast-godot-debug.apk)**
- **[GDevelop-APK herunterladen](https://github.com/sayac007/EnergyBlast/raw/refs/heads/feat/touch-shooter-v2/downloads/energyblast-gdevelop-debug.apk)**
- **[Defold-APK herunterladen](https://github.com/sayac007/EnergyBlast/raw/refs/heads/feat/touch-shooter-v2/downloads/energyblast-defold-debug.apk)**

Tippen: laufen. Ziehen und loslassen: zielen und feuern. FEUER halten: weiterfeuern.
DASH: kurz ausweichen. „Funk“ wiederholt die Ansage. Bei einer Niederlage direkt
neu starten; bisherige Sterne bleiben erhalten.

Android 7 / API 24 oder neuer. Godot und Defold benötigen ARM64; Godot OpenGL ES 3.
GDevelop benötigt eine funktionsfähige Android System WebView mit WebGL. Deren
installierte Größe steckt nicht in der GDevelop-APK-Größe.

Die drei Paketnamen `org.example.energyblast.pilot`, `.gdevelop` und `.defold`
erlauben parallele Installation. Die Spielstände sind unabhängig. Godot/GDevelop
können mit derselben Entwicklungssignatur als Version 0.2.0 / Code 2 über die
bisherige 0.1 installiert werden. Alte Sterne und bezahlte Hinweise bleiben dabei
im Format erhalten; der physische Update-Test ist offen. Deinstallation löscht Daten.

Es handelt sich um **Debug-Builds für den Engine-Vergleich**, keine Play-Upload-
Dateien. Keine Release-Schlüssel, keine angeforderten App-Berechtigungen, kein
Backup oder Datenupload. Installation aus dieser Downloadquelle ggf. in Android
erlauben. Die Apps selbst fordern dafür keine Medien-/Speicherberechtigung an.

`godot-verification.json`, `gdevelop-verification.json` und
`defold-verification.json` nennen den tatsächlichen sauberen Quellcommit,
Buildzeitpunkt, Größe und SHA-256. Nach dem Push werden die öffentlichen Downloads
mit diesen Hashes verglichen. Die APKs und Metadaten sind ein separater Commit
nach dem Quellstand. Keine GitHub-Releases, keine Pull Requests/automatischen Merges.

[Prüfergebnisse und offene echte Geräte-/Hörtests](../docs/QUALITY.md).

Ausgelieferter Quellstand: [`1006cde`](https://github.com/sayac007/EnergyBlast/commit/1006cde8595b4249d0375ddf8bc4ea60fd2a93c9).

| Datei | Bytes |
|---|---:|
| Godot | 30.317.360 |
| GDevelop | 1.720.558 |
| Defold | 8.737.978 |
