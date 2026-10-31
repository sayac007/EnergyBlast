# EnergyBlast — Defold 0.14.1 herunterladen

**[EnergyBlast 0.14.1 APK herunterladen — 69,1 MB](https://raw.githubusercontent.com/sayac007/EnergyBlast/387b8a7169d5b6a2a0b04dfaf4bfc12e03e929e7/downloads/energyblast-defold-debug.apk)**

**Korrektur 0.14.1:** Passive Schalter direkt oder per Abpraller treffen, passende
Ansage und halb so schneller Wechsel der leuchtenden Kreise.

**16 Missionen, zehn davon neu**, größere Felder, geschützte Zikkurat-Starts,
keine versteckten Boni oder Schatztruhen. Gesundheit maximal **100 einschließlich
Rüstung**, begrenzte Tarnung und endliche Mini-Drohnen-Schwärme mit höchstens
50 lebenden Gegnern. Frühere Sterne und Käufe bleiben erhalten.
[Regeln, Bilder und Prüfungen](../docs/MILESTONE_13.md).

| Merkmal | Tatsächlicher Wert |
|---|---|
| Engine / App | Defold 1.14.0, native ARM64-Test-App |
| Paket | `org.example.energyblast.defold` |
| Version / Code | **0.14.1 / 16** |
| Größe | **69.113.018 Bytes**; 49.152 Bytes mehr als 0.14 |
| Android | API 24+, target 36, ARM64, userLandscape |
| Quelle | [2fb7785](https://github.com/sayac007/EnergyBlast/commit/2fb77853b9018ac872c11a92c6fe6afb46317853), `source_dirty:false` |
| APK-Snapshot | [387b8a7](https://github.com/sayac007/EnergyBlast/tree/387b8a7169d5b6a2a0b04dfaf4bfc12e03e929e7/downloads) |
| Gebaut | 30.10.2026, 16:26 MEZ |
| Signatur | v2/v3, identisches Entwicklungszertifikat wie 0.14 |
| Physischer Geräte-/Mehrfingertest | **OFFEN** |

```text
SHA-256 20451a92eac9aab78cfea4ae2e0b9258c2b77d2367ee1d473e24506b2560270d
```

[Maschinenlesbare Metadaten](defold-verification.json).

## Installation und Drohnenbedienung

Als Update über die vorhandene Defold-App installieren. **Nicht vorher deinstallieren**,
wenn Sterne, Käufe, Hinweise und Figur bleiben sollen. Android kann die Freigabe
der Downloadquelle verlangen. Debug-Testfassung, keine Release-/Play-Signatur.

Das Drohnenbild auf dem Feld öffnet den Vorrat. Eine Drohne auswählen; die Stimme
sagt **„Wähle jetzt das Ziel“**. Jetzt entweder die bereitstehende Drohne auf einen
Gegner ziehen und loslassen, oder den Gegner direkt antippen. Die vorübergehende
Kartenübersicht zeigt auch entfernte Gegner. Sie verändert die gespeicherte
Zoomstufe nicht. Nach Flug und Blitzeffekt kehrt der vorherige Ausschnitt zurück;
bewusstes Zoomen während des Flugs hat Vorrang. Abbrechen verbraucht keinen Vorrat.

Die Drohne fliegt tatsächlich über einen freien Weg zum Gegner und löst erst bei
Kontakt den elektrischen Treffer aus. Geschützte Bosse behalten ihre Relaisregel.
Pro Mission gibt es drei bis acht Drohnen. Waffe und Fallen bleiben verfügbar.

Die obere Leiste bietet anklickbare Schaltflächen für Ziel, Gegner und Mission;
die Sternanzeige öffnet die Ausrüstung. Alle 16 Missionen stehen auf drei Seiten.
[Gesamte Bedienung](../README.md).

## Tatsächliche Prüfung

**Vollständige Suite bestanden:** 4.674 native Prüfungen (1.311 historische,
3.363 aktive, davon 134 neu) plus tatsächliche GUI-/Speicher-/Audio-/Pixelabläufe, 16 gemeinsame
Testgruppen mit 1.686 Geometriepufferprüfungen. Alle 16 Missionen bei 720/800
Fensterhöhe, echter Drohnenflug vom Zikkurat bis Missionserfolg/WEITER, beide
Gesten, Abbruch, Bestand, Kamerarückkehr und bewusstes Zoomen sind geprüft.
Auch direkte Projektiltreffer an allen elf Relais, der freiwillige Abpraller,
sechs tatsächliche langsamere Lichtzustände und die Ansage ohne Neustart bei
wiederholten Bosstreffern sind geprüft.
APK: **PASS**, saubere Quelle, Paket/Version/API/Querformat, keine Berechtigungen,
Backup aus, v2/v3-Signatur, Zertifikatsgleichheit, ZIP-CRC, keine privaten Schlüssel,
16-KB-ZIP-Ausrichtung und 1.225 bytegleiche Projektdateien. Die ZIP-Prüfung allein
ist keine Play-/16-KB-Freigabe.
Physische Handy-/Tablet-Gesten, Android-Update mit eigenen Spielständen, Audio,
Leistung bei 50 Gegnern und Spielbalance bleiben separat manuell zu prüfen.
[Zentraler Qualitätsstatus](../docs/QUALITY.md).

## Vorherige 0.14 dauerhaft erhalten

[Defold 0.14 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/11248b5ef4215838cb08bd2c8164d9718d9efcae/downloads/energyblast-defold-debug.apk)
— 69.063.866 Bytes, [damaliger Stand](https://github.com/sayac007/EnergyBlast/blob/425dd3c29b7776864d0fcb0642f16d38db2f46d0/docs/MILESTONE_13.md).

## Vorherige 0.13 dauerhaft erhalten

[Defold 0.13 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/9e486f1dec3b6ca67371f1491c8e7b5991885a14/downloads/energyblast-defold-debug.apk)
— 68.342.970 Bytes, [damaliger Stand](../docs/MILESTONE_12.md).

## Vorherige 0.12 dauerhaft erhalten

[Defold 0.12 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/8d0de931d121f89e5ad8b6841c4124035a24c12b/downloads/energyblast-defold-debug.apk)
— 68.211.898 Bytes, [damaliger Stand](../docs/MILESTONE_11.md).

## Vorherige 0.11 dauerhaft erhalten

[Defold 0.11 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/284a94a0659ca9c0fd453977343053274bf214df/downloads/energyblast-defold-debug.apk)
— 68.195.514 Bytes, [damaliger Stand](../docs/MILESTONE_10.md).

## Vorherige 0.10 dauerhaft erhalten

[Defold 0.10 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/6ef588bd40f4a63e5f267f2fbf45e77b74aeca18/downloads/energyblast-defold-debug.apk)
— 64.033.978 Bytes, [damaliger Stand](../docs/MILESTONE_09.md).

## Vorherige 0.9 dauerhaft erhalten

[Defold 0.9 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/e49218e7015e365a0913961a0f1e005436c271f2/downloads/energyblast-defold-debug.apk)
— 63.853.754 Bytes, [damaliger Stand](../docs/MILESTONE_08.md).

## Vorherige 0.8 dauerhaft erhalten

[Defold 0.8 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/5c8e1ca956e99abd805cc29f90f9ee6620a7a5ce/downloads/energyblast-defold-debug.apk)
— 44.094.650 Bytes, [damaliger Stand](../docs/MILESTONE_07.md).

## Vorherige 0.7 dauerhaft erhalten

[Defold 0.7 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/f8e8542b30cf1691bedf8f28a2403936f9bafcb9/downloads/energyblast-defold-debug.apk)
— 43.340.986 Bytes, [damaliger Stand](../docs/MILESTONE_06.md).

## Vorherige 0.6 dauerhaft erhalten

[Defold 0.6 APK](https://raw.githubusercontent.com/sayac007/EnergyBlast/24b24dd23d08eb73ebd5fc113c318da3b1f45e7a/downloads/energyblast-defold-debug.apk)
— 28.366.010 Bytes. Grafischer Stand vom Betreiber abgelehnt;
[damalige Nachweise](../docs/MILESTONE_05.md) bleiben erhalten.

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

Diese Apps wurden für 0.14.1 nicht verändert oder neu gebaut:

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
