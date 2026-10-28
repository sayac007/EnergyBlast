# EnergyBlast — Defold 0.4.1 herunterladen

**[Defold 0.4.1 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/bd3d6f1374a7aca4e79fe4b9ba512ff67244e78f/downloads/energyblast-defold-debug.apk)**

Kurzer Feldkontakt läuft, längerer Kontakt zielt, Loslassen schießt. Neue eigene
Chiptune-Musik, 2,25-fache Arenenfläche mit folgender Kamera und animierte
Energieexplosionen. [Umfang, Bilder und Prüfungen](../docs/MILESTONE_03.md).

## Aktuelle Datei

| Merkmal | Tatsächlicher Wert |
|---|---|
| Engine / Laufzeit | Defold 1.14.0, native ARM64-App |
| Paket | `org.example.energyblast.defold` |
| Version / Code | **0.4.1 / 5** |
| Größe | **9.540.794 Bytes** — rund 9,5 MB |
| Android | minSdk 24, targetSdk 36 |
| Quellcommit | [`02a2b40`](https://github.com/sayac007/EnergyBlast/commit/02a2b409830600bdaa85b10f6accc58f18a5f085) |
| Gebaut | 28.10.2026 vom sauberen Quellstand |
| Gerätetest der neuen APK | **NOT VERIFIED** |

```text
SHA-256 4d2b60a32d53af1c4e2f94b4806dd4fc23261925d88c19fd377594166f728bc5
```

[Maschinenlesbare Metadaten](defold-verification.json) nennen Buildzeit, Größe,
Hash, Version, Paket, APIs, Signaturstatus und Quellstand mit `source_dirty: false`.

## Installation und Update

Android 7 / API 24 oder neuer, ARM64. **Über die bisherige Defold-App installieren,
nicht vorher deinstallieren**, wenn die Sterne erhalten bleiben sollen. Gleiches
Paket und gleiche Entwicklungssignatur wie 0.3 wurden tatsächlich geprüft.
Speicherneustart mit alten/neuen Sternen, Ausrüstung, bezahlten Hinweisen und
Musikpräferenz bestanden; physische Datenübernahme auf dem Gerät bleibt offen.

Debug-Testfassung, keine Google-Play-Upload-Datei. Keine Release-Schlüssel.
Android kann die Installation aus dieser Downloadquelle freigeben lassen; die App
verlangt selbst keine Medien-/Speicherberechtigung. Keine angeforderten App-
Berechtigungen, Backup aus, kein Upload von Spielständen.

## Technische Prüfungen

Tatsächlich bestanden: Android-Build, Paket/Version/Code, minSdk/targetSdk,
gültige v2-Entwicklungssignatur, identisches Zertifikat zu 0.3, keine Berechtigungen,
Backup deaktiviert, ZIP-CRC und ZIP-Ausrichtung mit 16-KB-Seiten, keine
Schlüsseldateien im APK. Der externe Buildprojekt-Abzug stimmt mit dem
committeten Hauptskript und den drei neuen Audio-Dateien überein.
ZIP-Ausrichtung allein ist keine vollständige 16-KB-/Play-Zertifizierung.

Die native Laufzeit wurde separat mit 107 Kampf-/Eingabe-/Kamera-/Effekttests,
echten Kurz-/Langdruck-Eingaben, Speicherneustarts und aufgezeichneter Audio-
ausgabe geprüft. [Ergebnisse und offene Handy-/Tablet-Prüfungen](../docs/QUALITY.md).

## Erhaltene Vergleichsfassungen

Diese Apps wurden für 0.4 nicht verändert oder neu gebaut:

- [GDevelop 0.3 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/943f9340ef78079ed60c7db068cd5b76f86d1b6a/downloads/energyblast-gdevelop-debug.apk) — 2.153.923 Bytes, GDJS/WebGL in lokaler Android-WebView.
- [Defold 0.3 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/943f9340ef78079ed60c7db068cd5b76f86d1b6a/downloads/energyblast-defold-debug.apk) — 9.065.658 Bytes, alter Vergleich.
- [Godot 0.2 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-godot-debug.apk) — 30.317.360 Bytes.

[0.3-Nachweise](https://github.com/sayac007/EnergyBlast/tree/943f9340ef78079ed60c7db068cd5b76f86d1b6a/downloads),
[0.2-Ausgangssnapshot](https://github.com/sayac007/EnergyBlast/tree/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads).
GDevelop benötigt eine funktionsfähige Android System WebView mit WebGL; deren
installierte Größe steckt nicht in der APK-Größe. Godot benötigt ARM64/OpenGL ES 3.
Verschiedene Engines lassen sich parallel installieren und speichern getrennt.

Dateien und Nachweise sind regulär versioniert; keine ablaufenden Actions-
Artefakte, kein automatisches Release/PR/Merge. Quellstand und APKs haben getrennte
Commits. Frühere Vergleichsdateien bleiben über ihre festen Referenzen erreichbar.

## Ergänzung 0.4.1

Alle Wandarten reflektieren, einschließlich gegnerischer Geschosse. Normale
Schüsse ein Abpraller, Prisma zwei, gegnerische ein Abpraller; Lebensdauer 3/6 s,
Reichweite und sichtbares Verblassen. Blaue, begehbare X-Felder neutralisieren.
Größe des Spielfelds, Kamera, Steuerung, Musik und Spielstände bleiben erhalten.
107 native Fälle, Speicher-/GUI-/Audio-Prüfungen und sieben gemeinsame Gruppen
bestanden. Neue physische Android-Spielrunde bleibt offen.

[Defold 0.4.0 als fester Ausgangsstand](https://raw.githubusercontent.com/sayac007/EnergyBlast/4539cdf739582e22046c36aa76e20d7750584fce/downloads/energyblast-defold-debug.apk).
