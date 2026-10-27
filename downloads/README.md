# EnergyBlast Touch-Pilot herunterladen

Zwei Entwicklungsversionen mit denselben zwei Missionen. Zunächst Godot testen;
GDevelop ist der kleine Vergleich im Android-System-WebView. Keine Unity-APK.

- [Godot-APK direkt laden](https://github.com/sayac007/EnergyBlast/raw/refs/heads/feat/touch-mission-pilot/downloads/energyblast-godot-debug.apk)
- [GDevelop-APK direkt laden](https://github.com/sayac007/EnergyBlast/raw/refs/heads/feat/touch-mission-pilot/downloads/energyblast-gdevelop-debug.apk)

Beide können nebeneinander installiert werden. Android 7 / API 24 oder neuer,
Godot zusätzlich ARM64 und OpenGL ES 3. Unterschiedliche Paketnamen, unabhängige
lokale Spielstände. Die GDevelop-Fassung benötigt eine funktionsfähige Android
System WebView mit WebGL. Downloads über den Browser gegebenenfalls bestätigen;
die Installation aus dieser Quelle muss Android gegebenenfalls einmal erlauben.
Die Apps selbst fordern keine Berechtigungen an.

Das sind ausschließlich Debug-Builds mit Entwicklungssignatur, keine Play-Upload-
Dateien. Keine Release-/Upload-Schlüssel verwendet. Deinstallieren löscht lokale
Sterne; Updates benötigen dieselbe Entwicklungssignatur.

Ausgelieferter Quellstand: [`46c1fec`](https://github.com/sayac007/EnergyBlast/commit/46c1fecc54356f9fecd8f6144ec00de2fd0df90d).
Godot: **28.854.983 Bytes**, GDevelop: **1.211.285 Bytes**.

Die nebenliegenden `godot-verification.json` und `gdevelop-verification.json`
nennen den tatsächlichen **Quellcommit**, Buildzeitpunkt, Dateigröße und SHA-256.
Die APKs werden erst nach dem sauberen Quellcommit erzeugt und anschließend in
einem getrennten Download-Commit abgelegt. Der Dirty-Status darin bezieht sich
auf den Quellstand während des Builds.

Prüfungen und offene Gerätetests: [Qualitätsübersicht](../docs/QUALITY.md).
