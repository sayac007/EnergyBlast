# Aktueller Prüfstand — Aurora Raid 0.3

**28.10.2026.** Aktive Weiterentwicklung: Defold und GDevelop. Godot bleibt im
unveränderten 0.2-Stand. Der [Meilenstein 02](MILESTONE_02.md) beschreibt Umfang,
Abgleich, Testergebnisse und offene Geräteabnahme. Der eingefrorene
[Meilenstein 01](MILESTONE_01.md) erhält die Nachweise des ersten Vergleichs.

## Ausgeführt und bestanden

| Prüfbereich | Ergebnis am 28.10.2026 |
|---|---|
| Defold native Engine | 42 Kampf-/Eingabeprüfungen in Linux/OpenGL |
| Defold tatsächliche GUI-Eingabe | Menüwahl Dock und FEUER per XTest bestanden; keine Script-Kontextfehler |
| Defold lokaler Spielstand | Neuer Prozess erhält alte/neue Sterne, Dock-Ausrüstung und bezahlte Hinweise |
| GDevelop tatsächliche WebGL-Laufzeit | 51 Prüfungen, Touch-Emulation, 0 Seitenfehler / 0 externe Requests |
| Gemeinsame Regeln/Modelle/Audios/Manifeste | Sechs Testgruppen; 26 bestehende + 3 neue Oggs tatsächlich decodiert; Hash/Pegel/Dauer geprüft |
| Erhaltenes Godot | 43 alte + 24 Shooter-Prüfungen; Prozessneustart bestanden |
| Alte GDevelop-Regression | 32 Prüfungen; separater Legacy-Export, danach aktuellen Export wiederhergestellt |
| Sichtprüfung | Gerenderte Menüs/Dock beider Apps selbst angesehen |

Die neuen Tests sichern reale Relais-Abpraller, geschützten Boss, beweglichen
Gegner mit Ladestopp, drei Geschosse pro Fächer, einmalige Heilung, erreichbare
Flanken, Torfenster, Ende des Sektors und begrenzte Belohnungen ab. Direkte
Treffer dürfen die Relais nicht umgehen. Die graphische Vorschau wird auch an
den tatsächlichen GDevelop-SVG-Elementen kontrolliert; Defolds GUI zeichnet die
ballistische Berechnung nicht mehr.

Der echte Defold-Menütest wurde ergänzt, weil die vorherige reine Kampfprüfung
den Wechsel in den falschen Script-Kontext nicht erfasste. Native Testfehler
beenden jetzt die Engine mit Fehlercode; der Teststarter räumt bei einem Timeout
die komplette eigene Prozessgruppe auf, damit keine verwaiste Engine Ports belegt.

## Builds und Aussagegrenzen

Die [Download-Nachweise](../downloads/README.md) und die maschinenlesbaren
`verification.json`-Dateien ordnen jedes APK dem Quellcommit zu. Geprüft werden
Paket, Version, Mindest-/Ziel-API, Entwicklungssignatur, fehlende Berechtigungen,
deaktiviertes Backup, ZIP-Integrität/Ausrichtung und Hash. Es gibt keinen
GitHub-Actions-Workflow; die genannten Prüfungen wurden lokal in der Cloud
wirklich ausgeführt. Keine behauptete grüne CI und keine Release-Schlüssel.

**Offen:** physische Installation/Update von 0.2, Touch mit mehreren Fingern,
Rotation, Ton/Hörverständlichkeit, Launcher, längeres Spiel, Gerätebildrate,
Akkuverbrauch und subjektives Spielgefühl. Native Audio-Prüfungen verwenden ein
Nullgerät. Die neuen Sätze sind komplett erzeugte synthetische Aufnahmen derselben
Stimme, keine Silbenmontage oder Schauspielerimitation. Ein automatischer
Spracherkennungs-Screen ersetzt keine menschliche Hörabnahme.

Die Arenen enthalten ausschließlich selbst erzeugte Geometrie; Herkunft und
Hashes stehen in `shared/asset-origins.json`. Kein Familienpaket, keine privaten
Bilder/Schlüssel und keine neue Drittanbieter-Grafik. Spielstände bleiben lokal,
Android-Backup ist aus, das Spiel verlangt keine Berechtigungen. Die GDevelop-
WebView akzeptiert nur lokale Inhalte; Netzwerk-Telemetrie ist abgeschaltet.

Keine pädagogische Wirksamkeit/Übertragung in den Alltag und keine Store-Reife
behauptet. Prüfkommandos zentral in [BUILD_AND_TEST.md](BUILD_AND_TEST.md).
Laufzeitlogs bleiben außerhalb von Git; keine neuen Einzelberichte pro Testlauf.

Der unabhängige Whisper-small-Screen der drei neuen Ansagen erkennt **2/3**
normalisiert exakt. Bei „Triff“ erkennt er „trifft“; Satz und Kerninhalt werden
sonst erkannt. Das ist kein bestätigter Aussprachefehler und keine menschliche
Hörabnahme. Der ältere 25/26-Screen bleibt ein historischer 0.2-Nachweis.

**Abschließende APK-Prüfung 28.10.2026:** Defold und GDevelop 0.3 vom sauberen
Quellcommit `43527374e1705a9608a9ddb11ccc8e4af31ef69e` gebaut. Alle technischen
Paketprüfungen bestanden, einschließlich Vergleich des Signaturzertifikats mit 0.2,
ZIP-CRC und Prüfung auf fehlende Schlüsseldateien. Die konkreten Größen und
SHA-256 stehen bei den Downloads. Godots APK bleibt bytegleich zu `defd791`.
