# EnergyBlast — Defold 0.6 herunterladen

**[Defold 0.6 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/feat/touch-shooter-v2/downloads/energyblast-defold-debug.apk)** — rund **28,4 MB**.

Neue Grafik nach eingehender Brawl-Stars-Recherche: tatsächliche Landschafts-
materialien, modellierte und artikulierte Figuren, weicheres Licht/AO, animierte
3D-Menüfigur, freie Querformat-Spielfläche und native Lichtspuren. Alle sechs
Missionen, Sterne, Käufe und Spielstände bleiben. [Bilder/Bewegung](../docs/MILESTONE_05.md),
[Recherchequellen](../docs/ART_DIRECTION.md).

| Merkmal | Tatsächlicher Wert |
|---|---|
| Engine / Laufzeit | Defold 1.14.0, native ARM64-App |
| Paket | `org.example.energyblast.defold` |
| Version / Code | **0.6.0 / 7** |
| Größe | **28.366.010 Bytes** — rund 28,4 MB |
| Android | minSdk 24, targetSdk 36 |
| Ausrichtung | **userLandscape**, im fertigen Manifest tatsächlich geprüft |
| Quellcommit | [`19856c1`](https://github.com/sayac007/EnergyBlast/commit/19856c195a8b51d1136ef8e7e8f57efd744caf05) |
| Gebaut | 28.10.2026 vom sauberen Quellstand, 18:25 MEZ |
| Physischer Gerätetest / grafische Betreiberabnahme | **OFFEN** |

```text
SHA-256 8e65bc2c2391c7cceda5e0200dd2cfd7b7b5dfc3e5d50ac2d069bfe2167f31e2
```

[Maschinenlesbare Metadaten](defold-verification.json) enthalten Quellcommit,
`source_dirty: false`, Buildzeit, Paket/Version/APIs, Signatur, Hash und Größe.

## Installation und Update

Android 7/API 24 oder neuer, ARM64. **Über die vorhandene Defold-App installieren;
nicht vorher deinstallieren**, wenn Sterne, Käufe und Hinweise bleiben sollen.
Gleiche Paketkennung und tatsächlich verglichenes Entwicklungssignatur-Zertifikat
wie 0.5. Android kann die Freigabe der Downloadquelle verlangen. Debug-Testfassung,
keine Play-Upload-Datei; keine Release-Schlüssel verwendet.

Die bisherige einmalige Migration und alle Speicherfunktionen bleiben. Getrennte
Prozessstarts sind geprüft; echte Datenübernahme auf dem Handy bleibt offen.
Die neue Querformatfestlegung verhindert einen Wechsel zur gestauchten
Portrait-Szene. Zwei native Fensterformate wurden geprüft; Geräteleistung und
persönliches Touch-/Klang-/Grafikurteil werden dadurch nicht vorweggenommen.

## Tatsächliche technische Prüfungen

Android-Build, Paket/Version/Code, APIs, **userLandscape** im Manifest, gültige
v2-Signatur, identisches Zertifikat zu 0.5, keine Berechtigungen, Backup aus,
ZIP-CRC und ZIP-Ausrichtung mit 16-KB-Seiten bestanden. Keine Schlüsseldateien
im APK. Vollständiger Buildprojekt-Abzug gegen den Quellstand verglichen.
ZIP-Ausrichtung allein ist keine vollständige 16-KB-/Play-Zertifizierung.

**199 native Prüfungen und elf gemeinsame Testgruppen** bestanden. Echte
Eingaben bei 1280×720 und 1280×800, Käufe, Figurenauswahl, Speicherneustarts,
Audioaufnahme und verdeckte/sichtbare Kontrollgeschosse mit Licht erneut geprüft.
Quell-/Laufzeit-Geometrie vor/nach dem Batching beidseitig geprüft. Echte native
Spielbilder und eine Sequenz aus Bewegung, Zielen und Feuerbällen aufgenommen.
[Qualitätsstatus und Grenzen](../docs/QUALITY.md). Keine grüne CI behauptet.

## Vorheriger Stand 0.5 dauerhaft erhalten

[Defold 0.5 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/4315cf73fe6fd5b8688e7d397766394010fe2e5d/downloads/energyblast-defold-debug.apk)
— 10.474.682 Bytes,
[Metadaten](https://github.com/sayac007/EnergyBlast/blob/4315cf73fe6fd5b8688e7d397766394010fe2e5d/downloads/defold-verification.json).
Dieser grafische Stand wurde vom Betreiber abgelehnt; die technische Historie bleibt erhalten.

## Dauerhaft erhaltener Ausgangsstand

[Defold 0.4.1 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/bd3d6f1374a7aca4e79fe4b9ba512ff67244e78f/downloads/energyblast-defold-debug.apk)
— 9.540.794 Bytes,
[Metadaten](https://github.com/sayac007/EnergyBlast/blob/bd3d6f1374a7aca4e79fe4b9ba512ff67244e78f/downloads/defold-verification.json).
[0.4.0-APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/4539cdf739582e22046c36aa76e20d7750584fce/downloads/energyblast-defold-debug.apk).

## Erhaltene Vergleichsfassungen

Diese Apps wurden für 0.6 nicht verändert oder neu gebaut:

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
