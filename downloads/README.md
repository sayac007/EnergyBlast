# EnergyBlast — Defold 0.5 herunterladen

**[Defold 0.5 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/4315cf73fe6fd5b8688e7d397766394010fe2e5d/downloads/energyblast-defold-debug.apk)**

Sechs Sektoren, drei wählbare Originalfiguren, tatsächliche Käufe, klare freie
Bedienflächen und neues Ensemble-Arrangement. [Umfang/Bilder/Tests](../docs/MILESTONE_04.md).

| Merkmal | Tatsächlicher Wert |
|---|---|
| Engine / Laufzeit | Defold 1.14.0, native ARM64-App |
| Paket | `org.example.energyblast.defold` |
| Version / Code | **0.5.0 / 6** |
| Größe | **10.474.682 Bytes** — rund 10,5 MB |
| Android | minSdk 24, targetSdk 36 |
| Quellcommit | [`321d5cf`](https://github.com/sayac007/EnergyBlast/commit/321d5cf6f50f7b038a2f7f8189ac421770af9013) |
| Gebaut | 28.10.2026 vom sauberen Quellstand, 16:59 MEZ |
| Physischer Gerätetest der neuen APK | **NOT VERIFIED** |

```text
SHA-256 1dd5d3372f759f55f4c3f04229040874fcad88f46b0971a03a5d36f5cd8aaa66
```

[Maschinenlesbare Metadaten](defold-verification.json) nennen Buildzeit, Größe,
Hash, Version, Paket, APIs, Signaturstatus und Quellstand mit `source_dirty: false`.

## Installation und Update

Android 7 / API 24 oder neuer, ARM64. **Über die bisherige Defold-App installieren,
nicht vorher deinstallieren**, wenn der lokale Spielstand erhalten bleiben soll.
Gleiche Paketkennung und tatsächlich verglichenes Entwicklungssignatur-Zertifikat
wie 0.4.1. Android kann die Freigabe der Downloadquelle verlangen; Play Protect
oder Geräteverwaltung können die Installation weiterhin blockieren.

Getrennte Speicherprozesse erhalten Gesamtsterne, Guthaben, Käufe, Figur, bezahlte
Hinweise und Musikpräferenz. Alte automatische Verbesserungen bleiben bei der
einmaligen Migration kostenlos erhalten. Echte Datenübernahme auf dem Gerät bleibt
für die neue APK offen. Debug-Testfassung, keine Google-Play-Upload-Datei.
Keine Release-Schlüssel oder zusätzlichen App-Berechtigungen, Backup aus.

## Tatsächliche technische Prüfungen

Android-Build, Paket/Version/Code, minSdk/targetSdk, gültige v2-Entwicklungssignatur,
identisches Zertifikat zu 0.4.1, keine Berechtigungen, Backup deaktiviert,
ZIP-CRC und ZIP-Ausrichtung mit 16-KB-Seiten bestanden. Keine Schlüsseldateien
im APK. Der vollständige externe Projektabzug wurde gegen den Quellstand verglichen.
ZIP-Ausrichtung allein ist keine vollständige 16-KB-/Play-Zertifizierung.

**187 native Prüfungen**, getrennte Speicherstarts, tatsächliche Menü-/Kauf-/Figur-
und Touch-Eingaben, aufgezeichnete Audiomischung, native Pixelprüfung verdeckter
Geschosse und neun gemeinsame Testgruppen bestanden. Fünf komplette Defold-
Ansagen unabhängig per ASR erkannt. [Ergebnisse/Grenzen](../docs/QUALITY.md).
Kein neuer physischer Android-Test und keine grüne CI behauptet.

## Dauerhaft erhaltener Ausgangsstand

[Defold 0.4.1 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/bd3d6f1374a7aca4e79fe4b9ba512ff67244e78f/downloads/energyblast-defold-debug.apk)
— 9.540.794 Bytes,
[Metadaten](https://github.com/sayac007/EnergyBlast/blob/bd3d6f1374a7aca4e79fe4b9ba512ff67244e78f/downloads/defold-verification.json).
[0.4.0-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/4539cdf739582e22046c36aa76e20d7750584fce/downloads/energyblast-defold-debug.apk).

## Erhaltene Vergleichsfassungen

Diese Apps wurden für 0.5 nicht verändert oder neu gebaut:

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
