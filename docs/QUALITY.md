# Aktueller Prüfstand — Defold 0.8

**28.10.2026.** [Änderungen/Ursachen](MILESTONE_07.md), [Testbefehle](BUILD_AND_TEST.md),
[APK-/Quellmetadaten](../downloads/README.md).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regeln/Darstellung | **347 PASS**: 231 erhaltene Prüfungen, 47 Spielflussfälle, 69 Bonusprüfungen |
| Gemeinsame Tests | **13 Gruppen PASS**: Daten/Medien/Hashes, unveränderte Vergleichs-Engines, Belohnungen, native Soundkapazität, echte Wandpuffer und Geometrie-Batching |
| Tatsächliche UI-Eingaben | **PASS**, Drachen-/Figurenwahl, zwei Käufe, Kurz-/Langdruck, FEUER und TON bei 1280×720 sowie 1280×800 |
| Neue echte Touch-Abläufe | **3 Szenarien PASS**: direkte Heldenwahl/Käufe/fehlende Sterne; Nachfolger trotz offenem Schatz; freiwillige sichere Suche und anschließendes Weiter |
| Getrennte Speicherprozesse | **PASS**, Gesamtsterne, Guthaben, Käufe, Figur, Hinweise, Musik; Missionswiederherstellung zusätzlich simuliert |
| Geschossverdeckung | **PASS**, verdeckt 0 Pixel verändert, sichtbarer Kontrollfall 250 Pixel |
| Tatsächliche Audioausgabe | **PASS**, Musik an RMS 0,01148, aus 0, Mischung 0,03704; kein Überlauf im geprüften Ausgang |
| Sprachdateien | **26/26 technisch bestanden**: Hash, Dauer, Decodierung, Pegel;12 bisherige unverändert |
| Unabhängiger ASR-Screen | **25/26 wörtlich normalisiert exakt**; einmal gültiges „Geh jetzt“ statt „Gehe jetzt“, keine Bedeutungsabweichung behauptet |
| Eigene Sichtprüfung | Menü, Drachenwahl, Kaufen/Guthaben, Sieg/Weiter, Schatz-/Bonusführung und neue Missionsanzeige in echter nativer Laufzeit angesehen |
| Android-Artefakt | Abschlussnachweis folgt in den Download-Metadaten; vor Prüfung kein neues APK behauptet |

Die bisherigen Spieltests laufen mit unveränderter0.7-Regelfixture weiter.
Neue Prüfungen kontrollieren echte reflektierte Geschosse, Reihenfolge, ein grünes
Zeitfenster statt Dauerfeuer, erreichbare Bonuspositionen aller sechs Missionen,
einmalige Belohnungen und nicht blockierende optionale Ziele. Die Zähler führen
nicht zur nächsten richtigen Antwort einer Lichterfolge.

Der ursprüngliche Übergangsfehler war `over=true` nach geschlossenem Siegdaten-
dialog sowie ein fehlender direkter Nachfolger. Beide Wege werden durch echte
GUI-Eingaben geprüft. Schätze und Boni bleiben freiwillig; sichere Nachsuche
setzt das Spiel fort und kann jederzeit zur nächsten Mission verlassen werden.

Beim ersten Lauf wurde die native Grenze von 32 Soundkomponenten überschritten.
Jetzt explizit 64; der Konsistenztest vergleicht sie mit 45 tatsächlich gebundenen
Komponenten. Ein Speichertest konnte nach angefordertem Exit noch auf nicht
gezeichnete Objekte zugreifen; sein Abschluss stoppt weitere Updates. Beides
wurde vor Auslieferung korrigiert und im Gesamtlauf erneut geprüft.

**Offen:** neue APK auf Handy/Tablet installieren bzw. aktualisieren, reale
Spielstandübernahme, kindliches Verständnis, Klang, Schwierigkeit, längere Runden
und Geräteleistung. Keine neue grüne CI, Store-Reife oder pädagogische Wirksamkeit.
Die Sieg-UI-Prüfung verwendet kontrolliert den echten Abschlussweg; sie ist kein
behaupteter manuell bestandener Android-Level.

## Historische Nachweise

- [0.7: versionierter Qualitätsnachweis](https://github.com/sayac007/EnergyBlast/blob/e7564ba/docs/QUALITY.md),
  [Meilenstein 06](MILESTONE_06.md):231 native / 12 gemeinsame Prüfgruppen, ursprüngliche Grafiküberarbeitung.
- [0.6](MILESTONE_05.md), [0.5](MILESTONE_04.md), [0.4](MILESTONE_03.md),
  [0.3](MILESTONE_02.md), [Ausgangsvergleich](MILESTONE_01.md).

Historische Ergebnisse gehören zu ihren dort genannten Quell-/APK-Snapshots;
sie ersetzen keinen neuen Gerätetest. Laufzeitlogs verbleiben außerhalb von Git.
