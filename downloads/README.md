# EnergyBlast — Aurora Raid 0.3 herunterladen

Aktuell weiterentwickelt: **Defold und GDevelop**, jeweils mit drei Sektoren.
Neue Grafik, beweglicher Gegner, Abprall-Schalter, geschützter Boss und
Fächersalven. Keine berechnete Schussbahn. [Umfang und Prüfungen](../docs/MILESTONE_02.md).

- **[Defold 0.3 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/943f9340ef78079ed60c7db068cd5b76f86d1b6a/downloads/energyblast-defold-debug.apk)**
- **[GDevelop 0.3 APK herunterladen](https://raw.githubusercontent.com/sayac007/EnergyBlast/943f9340ef78079ed60c7db068cd5b76f86d1b6a/downloads/energyblast-gdevelop-debug.apk)**
- [Godot 0.2, unverändert](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-godot-debug.apk).

## Anforderungen und Update

Android 7 / API 24 oder neuer. Defold benötigt ARM64. GDevelop benötigt eine
funktionierende Android System WebView mit WebGL; deren installierte Größe
steckt nicht in der kleinen APK-Größe. Godot 0.2 benötigt ARM64 und OpenGL ES 3.

| App | Paketkennung | Version / Code | Bytes |
|---|---|---|---:|
| Defold | `org.example.energyblast.defold` | 0.3.0 / 3 | 9.065.658 |
| GDevelop | `org.example.energyblast.gdevelop` | 0.3.0 / 3 | 2.153.923 |
| Godot, archivierter Vergleich | `org.example.energyblast.pilot` | 0.2.0 / 2 | 30.317.360 |

Beide neuen Pakete sind mit demselben extern gespeicherten Entwicklungsschlüssel
wie 0.2 signiert; Zertifikatsgleichheit und v2-Signatur wurden tatsächlich geprüft.
Sie können als Update angeboten werden. Vorher **nicht deinstallieren**, wenn
Sterne erhalten bleiben sollen. Die Speicherformate wurden mit alten/neuen Sternen
und bezahlten Hinweisen geprüft; ein physischer Geräte-Update-Test steht aus.
Apps verschiedener Engines lassen sich nebeneinander installieren und speichern getrennt.

Debug-Testfassungen, keine Play-Upload-Dateien. Keine Release-Schlüssel und keine
angeforderten App-Berechtigungen, kein Backup oder Datenupload. Android kann eine
Freigabe für die Installation aus dieser Downloadquelle verlangen; die Apps
fordern selbst keine Medien-/Speicherberechtigung an.

## Prüfsummen und Herkunft

```text
Defold 0.3
SHA-256 eb77c0e9248f29e4f3c9181555905dc02e03ae8d35ebf8b3f49365cc8cd859a6

GDevelop 0.3
SHA-256 5eb4a25ba88d88ebd853fb6d812cf012572d62f333936dd54406fb7a297f814f

Godot 0.2
SHA-256 5808ed6027c6d336acc223839d2127b9188966fe555c39fa6bac4c5a13b4b470
```

Neue APKs gebaut am **28.10.2026**, vom sauberen Quellcommit
[`4352737`](https://github.com/sayac007/EnergyBlast/commit/43527374e1705a9608a9ddb11ccc8e4af31ef69e).
[Defold-Metadaten](defold-verification.json) und
[GDevelop-Metadaten](gdevelop-verification.json) nennen Buildzeit, Quellstand,
Hash, Größe, Paket/Version, APIs, Signaturstatus und ausdrücklich
`manual_android_test: NOT VERIFIED`.

Tatsächlich bestanden: APK-Build, Paketkennung, Version/Code, minSdk 24,
targetSdk 36, gültige Entwicklungssignatur, identisches Zertifikat zu 0.2,
keine Berechtigungen, Backup deaktiviert, ZIP-CRC und ZIP-Ausrichtung mit
16-KB-Seiten. Keine Schlüsseldateien im APK. Der GDevelop-Inhalt wurde zusätzlich
auf die neue Regelversion und die Hashwerte der drei neuen Sprachdateien geprüft.
ZIP-Ausrichtung allein ist keine vollständige 16-KB-/Play-Konformitätszertifizierung.

Die Dateien sind regulär versioniert und laufen nicht wie CI-Artefakte ab.
Keine Actions-Speicherbelegung durch neue Workflow-Uploads und kein automatisches
GitHub-Release. Die ursprünglichen drei 0.2-APKs bleiben dauerhaft im
[festen Ausgangssnapshot](https://github.com/sayac007/EnergyBlast/tree/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads).
