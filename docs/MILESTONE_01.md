# Meilenstein 01 — erster Drei-Engine-Shooter-Vergleich

**Fassung 0.2, gebaut am 27.10.2026; dokumentiert und Dateiprüfung erneuert am
28.10.2026.** Status: Testfassungen zur Bewertung bereit, finale Engine- und
Spielqualitätsabnahme offen. Grundlage: [konsolidierter Auftrag](PROJECT_BRIEF.md).

## Eingefrorene Referenzen

| Bestandteil | Unveränderlicher Stand |
|---|---|
| Ursprüngliches Briefing | [`b0f344f`](https://github.com/sayac007/EnergyBlast/blob/b0f344f/docs/pilot-brief.md) |
| Alter Geometriepilot 0.1 | Quellcommit [`46c1fec`](https://github.com/sayac007/EnergyBlast/commit/46c1fec); APK-Commit [`c29acbe`](https://github.com/sayac007/EnergyBlast/commit/c29acbe) |
| Aktueller Shooter-Quellstand | [`1006cde8595b4249d0375ddf8bc4ea60fd2a93c9`](https://github.com/sayac007/EnergyBlast/tree/1006cde8595b4249d0375ddf8bc4ea60fd2a93c9) |
| Drei ausgelieferte APKs und Metadaten | [`defd791bd94809045cf5a8ed9429ead92c8bd959`](https://github.com/sayac007/EnergyBlast/tree/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads) |
| Arbeitsbranch | [`feat/touch-shooter-v2`](https://github.com/sayac007/EnergyBlast/tree/feat/touch-shooter-v2) |

Die folgenden Downloadlinks sind auf den APK-Commit festgelegt. Spätere Änderungen
am Branch können dadurch diesen ersten Vergleich nicht stillschweigend ersetzen.
Die Dokumentationsänderung vom 28.10. verändert weder Spielcode noch APK-Dateien.

## Testdateien

| Engine | Direkter APK-Download | Größe | Paketkennung |
|---|---|---:|---|
| Godot 4.7.2 | [Godot](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-godot-debug.apk) | 30.317.360 Bytes | `org.example.energyblast.pilot` |
| GDevelop 5.6.269 | [GDevelop](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-gdevelop-debug.apk) | 1.720.558 Bytes | `org.example.energyblast.gdevelop` |
| Defold 1.14.0 | [Defold](https://raw.githubusercontent.com/sayac007/EnergyBlast/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads/energyblast-defold-debug.apk) | 8.737.978 Bytes | `org.example.energyblast.defold` |

Alle drei sind Debug-Builds mit Version **0.2.0 / Code 2**, minSdk 24 und targetSdk
36. Godot und Defold sind native ARM64-Builds; GDevelop läuft als echte GDJS/WebGL-
Implementierung in einer Offline-Android-WebView. Die System-WebView steckt nicht
in der APK-Größenangabe. Die Apps können nebeneinander installiert werden; ihre
Spielstände sind unabhängig. Kein Play-Release und keine Produktionssignierung.

Dateihashes, Builddatum, Signaturart, deaktiviertes Backup, fehlende angeforderte
Berechtigungen und sauberer Quellstand sind je Engine im zugehörigen
[`*-verification.json`](https://github.com/sayac007/EnergyBlast/tree/defd791bd94809045cf5a8ed9429ead92c8bd959/downloads)
festgehalten. Die Binärdateien sind versionierte Repository-Dateien und hängen
nicht von der Ablaufzeit eines Actions-Artefakts ab.

## Abgleich mit dem Auftrag

| Anforderung | Belegter Stand | Offene Grenze |
|---|---|---|
| Drei ausführbare Engine-Versuche | Drei erzeugte APKs; native Godot-/Defold-Läufe und GDevelop-WebGL-Lauf ausgeführt | Kein gemeinsamer echter Android-Benchmark |
| Echter Shooter | Kanonen laden, feuern und verursachen Energieverlust; Deckung blockt Geschosse; Schild verlangt Abpraller | Kleine Arenen mit stationären Kanonen auf Sockeln, noch keine große Gegnerwelt |
| Verbesserte Grafik | Gemeinsame neue 3D-Figur, Kanonen, zwei Arenen, größere Spielfeldansicht und reduzierte Aktionsleiste | Ästhetische Abnahme offen; Material-/Animationsunterschiede zwischen Engines |
| Touch ohne Joystick | Boden antippen, ziehen/loslassen, FEUER halten, DASH | Echte Handy-/Tablet-Gesten und Rotation noch offen |
| Punkte/Ausrüstung/Beute | Lokaler Fortschritt, vier Freischaltschwellen, versteckte Funde, verdiente Hinweise | Zwei Sektoren mit endlichen Belohnungen, keine langfristige Kampagne |
| Ohne sicheres Lesen bedienbar | Symbole, sichtbare Lade-/Trefferreaktionen, kurze deutsche Funkansagen | Verständnis und Hörtest durch Kind/Begleitung noch nicht abgenommen |
| Geometrie und Timing im Spiel | Abpraller, Deckung, Ausweichen und wiederkehrendes Torfenster | Lerntransfer und allgemeine Impulskontrolle nicht empirisch geprüft |
| Reproduzierbarer Vergleich | Gemeinsame Daten/Modelle, getrennte Implementierungen und Build-/Testskripte | Kein zugesicherter bitidentischer Build; keine gemessenen Entwicklungsstunden |

## Spielumfang

- **Prisma-Station:** Eine Schildkanone; zwei wirksame Treffer über die reflektierende
  Wand sichern den Sektor. Direkte Schüsse überwinden ihren Schild nicht.
- **Neon-Zitadelle:** Zwei unabhängig angreifende Kanonen und anschließend ein
  Energiekern hinter einem Tor. Drei Lichter kündigen das wiederkehrende Fenster an.
- Drei Energieeinheiten zu Beginn, kurze Treffer-Unverwundbarkeit, direkter
  Neustart bei Niederlage, gespeicherte Sterne bleiben erhalten.
- Einmalige Belohnungen für Abschluss, schadensfreien Abschluss und Geheimfund.
  Frisch gestartete 0.2-Profile können **325 Sterne** erreichen. Mit übernommenen
  0.1-Belohnungen sind insgesamt bis zu **650** möglich; die alte Arena ist kein
  normaler Startbereich der aktuellen App. Wiederholungen erzeugen keine Doppelzahlung.
- Zwei Hinweisguthaben je unterschiedlichem Missionsabschluss; zwei dauerhaft
  bezahlbare Hinweisstufen je Geheimnis. Funk und Bedienhinweise kosten nichts.
- Prisma ab 100, zusätzliche Energie beim Sektorstart ab 160, höheres Tempo ab
  230 und verringerte gegnerische Erfassungsreichweite ab 300 Sternen. Letzteres
  ist eine Regelwirkung, noch kein visueller Tarnshader. Linse/leise Stiefel sind
  zusätzliche versteckte Ausrüstung.
- Eine Roboterfigur, deutsche Ansagen und synthetisierte Toneffekte. Kein aktuelles
  Charakter-/Kostümauswahl- oder Hintergrundmusiksystem.

## Unterschiede, die beim Vergleich zu berücksichtigen sind

Godot und GDevelop bewegen benannte Körperteile der Figur. Defold verwendet bisher
Gesamtdrehung und Lauf-Bob; das ist keine gleichwertige vollständige Körperanimation.
Schatten, Materialien, UI-Details und Laufzeitbasis unterscheiden sich. Die
GDevelop-Downloadgröße lässt keinen direkten Rückschluss auf Speicherverbrauch,
Bildrate oder Akkuverbrauch auf dem Gerät zu.

Unity ist lediglich ein historischer, unkompilierter Importkit und zählt nicht
als vierter ausgeführter Prototyp. BRUTAL wurde anhand von README, Plattformcode
und NuGet-Paketen geprüft: Framework ohne fertigen Renderer/Editor und ohne
belegten vollständigen Android-Bauweg. Nach dieser Prüfung wurde die aktuelle
Dreierauswahl ausdrücklich vom Betreiber bestätigt. Kein BRUTAL-Leistungsurteil
oder dort ausgeführter Android-Test wird behauptet.

In `shared/combat.json` stehen noch einzelne Beobachtungs-/Effektbeschreibungen
aus 0.1, etwa zur Vorhersage oder alten Rüstungswirkung. Sie sind kein Beleg für
einen aktuellen Abfragemodus: maßgeblich sind die ausgeführten 0.2-Implementierungen
und die oben beschriebenen Wirkungen. Eine funktionale Datenbereinigung gehört
nicht zu dieser Dokumentationsänderung.

## Tatsächliche Prüfungen und Datum

**Am 27.10.2026 ausgeführt:**

| Bereich | Ergebnis |
|---|---|
| Godot-Shooter | 24 Prüfungen bestanden |
| GDevelop-Shooter | 28 Prüfungen im Chromium/WebGL-Lauf bestanden |
| Defold-Shooter | 17 Prüfungen in der nativen Linux/OpenGL-Laufzeit bestanden |
| Alte Regression | 43 Godot- und 32 GDevelop-Prüfungen bestanden |
| Speicher | Godot-/Defold-Prozessneustart, GDevelop-Neuladen sowie Godot-/GDevelop-Formatmigration geprüft |
| Gemeinsame Medien/Regeln/Manifeste | Vier Testgruppen bestanden; 26 Ogg-Dateien decodiert und gegen Manifest geprüft |
| Spracherkennungs-Screen | 25/26 Texte exakt nach Normalisierung; neue Kampfansagen 6/7; kein menschlicher Hörnachweis |
| Grafik | Alle drei Laufzeiten tatsächlich gerendert und Bilder visuell geprüft |
| Pakete | Paket/Version, Signatur, keine angeforderten Berechtigungen, Backup aus und ZIP-Ausrichtung geprüft |

[Ausführlicher technischer Prüfbericht](https://github.com/sayac007/EnergyBlast/blob/defd791bd94809045cf5a8ed9429ead92c8bd959/docs/QUALITY.md).
Ein Vergleich auf demselben physischen Android-Gerät wurde nicht ausgeführt.
Es gibt keinen GitHub-Actions-Workflow in diesem Stand und deshalb keinen
zusätzlich belegten grünen CI-Lauf. Die genannten Prüfungen sind lokal ausgeführte
Cloud-/Desktop-Tests, keine manuelle Android-Abnahme.

**Am 28.10.2026 für diese Veröffentlichung geprüft:** Referenzen auf Quell-/APK-
Commits, SHA-256/Größe/ZIP-Integrität der gespeicherten APKs und Konsistenz der
Build-Metadaten. Die lokalen Dokumentationslinks wurden geprüft und alle drei
auf Commit festgelegten öffentlichen APKs erneut heruntergeladen und per
SHA-256 mit den Metadaten verglichen. Keine
neuen Builds, Spieltests oder Signaturschlüssel für die Dokumentationsänderung.

## Offene Abnahme und nächste Anweisung

Zuerst dieselben zwei Sektoren in allen drei Apps auf demselben Gerät spielen.
Vergleichen: Ziel-/Laufbedienung, Lesen ohne Hilfe, Ton, Orientierung/Rotation,
Trefferverständnis, Flüssigkeit und der Wunsch weiterzuspielen. Erhalt lokaler
Daten beim echten Android-Update bleibt gesondert zu prüfen. Eine Deinstallation
löscht Spielstände und ist dafür ungeeignet.

Danach sind vor allem folgende Entscheidungen hilfreich: Welche Engine fühlt
sich am besten an? Was stört am stärksten? Soll als Nächstes Steuerung, Grafik,
Gegnerverhalten oder mehr Inhalt ausgebaut werden? Die folgende Anweisung sollte
möglichst die Engine, den betroffenen Sektor und höchstens drei Prioritäten nennen.
Eine endgültige Engine-Auswahl oder Freigabe für eine größere Kampagne wurde
bisher nicht erteilt.
