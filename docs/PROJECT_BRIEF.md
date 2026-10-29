# EnergyBlast — Ausgangsauftrag und aktueller Arbeitsauftrag

**Konsolidiert am 28.10.2026.** Dieses Dokument fasst die ausdrücklichen
Betreiberentscheidungen für EnergyBlast zusammen. Es ist eine redaktionelle
Zusammenfassung; das [unveränderte ursprüngliche Auftragszitat](pilot-brief.md)
und das [ältere Entscheidungsprotokoll](touch-pilot.md) bleiben nachvollziehbar.
Der belegte Umsetzungsstand steht in [MILESTONE_01.md](MILESTONE_01.md).

## Ziel des Projekts

Ein eigenständiger, öffentlich entwickelter Android-Shooter für Kinder etwa von
7 bis 10 Jahren, mit stilisierter 3D-Draufsicht, lebendiger Figur, verständlichen
Effekten und direkter Touch-Bedienung. Der maßgebliche spätere Betreiberwunsch:

> „es soll keine Lernapp sein, sondern ein echter Shooter mit Lerneffekt“

Das Spiel soll durch aktive Gegner, Deckung, Timing und kluge Schüsse tragen.
Ein möglicher Lerneffekt entsteht beim Einschätzen von Wegen, Sichtlinien,
Wirkungsradien und Abprallwinkeln. Aufgabenformulare oder verpflichtende
Antwort-/Vorhersageschritte sollen den Kampf nicht unterbrechen.

„Beobachten → Planen → Handeln“ bedeutet situationsgerechtes Handeln: Manchmal
ist Deckung und Abwarten günstig, manchmal muss ein kurzes Zeitfenster genutzt
werden. Bloß möglichst lange zu warten ist kein Erfolgsziel. Eine allgemeine
Verbesserung der Impulskontrolle im Alltag ist nicht nachgewiesen.

## Entwicklung des Auftrags

| Ausgangspunkt | Spätere ausdrückliche Entscheidung | Heute maßgeblich |
|---|---|---|
| Ursprünglicher Repository-Verweis auf Kinderwelt | Eigenes öffentliches Repository mit dem Namen EnergyBlast | `sayac007/EnergyBlast`; Kinderwelt unverändert lassen |
| Godot, Unity und GDevelop als anfängliche Kandidaten | BRUTAL prüfen; anschließend Auswahl „Godot, GDevelop und Defold“ | Drei ausführbare Vergleichsprototypen dieser Engines |
| Ursprünglich Bewegungsstick als Vorschlag | Touchscreen-Steuerung ohne Joystick; noch kein vollwertiges PC-Spiel | Tippen/Touch-Gesten als Hauptbedienung |
| Erste Beobachtungs-/Geometrieaufgabe mit Wächter und Fangfeld | Echter Shooter, beispielsweise eine angreifende Kanone und ein klügerer Gegenschuss | Aktive Gegner, Treffer, Deckung und Abpraller |
| Technisch vergleichbarer kleiner Pilot | Grafik und Bedienung sollen von Beginn an überzeugender sein, ähnlich der Spielbarkeit von Kinderwelt | Überarbeitete Oberfläche und Grafik; Qualitätsurteil durch Spieltest noch offen |
| Allgemeine Missionsideen | Zunächst kleiner spielbarer Vergleich statt großer Welt | Zwei gemeinsame Szenarien als erster Schritt |

Der Bericht von Claude dient als Ideen-/Rechercheinput. Nicht jede dort genannte
Mechanik ist damit beauftragt oder schon umgesetzt. Der Joystick-Vorschlag wurde
vom Betreiber ausdrücklich verworfen. Battlelands Royale ist eine visuelle
Referenz; dessen Grafiken, Figuren oder Marken sollen nicht übernommen werden.

## Konkrete Anforderungen für den ersten Vergleich

1. **Drei echte Versuche:** Godot, GDevelop und Defold mit möglichst denselben
   Arenen, Originalassets, Missionsregeln und Touch-Anforderungen. Spielbare
   Android-Dateien bereitstellen. Ein Importkit oder Screenshot allein genügt nicht.
2. **Aktiver Kampf:** Freundlich stilisierte Roboter-/Energiewelt, sichtbare
   Gegnerangriffe, Wirkung von Treffern, Deckung und eine bessere Schussentscheidung.
3. **Geometrie im Spiel:** Winkel/Abpraller, Wege und Sichtlinien erfahrbar machen.
   Beobachten und Vorbereitung sollen helfen, ohne das Spiel zur Abfrageapp zu machen.
4. **Belohnungen:** Dauerhaft gespeicherte Sterne/Punkte; ab Schwellen neue Waffen
   beziehungsweise bessere Rüstung, höheres Tempo und Tarnung. Gut versteckte
   Bonusausrüstung und Sterne. Hinweise auf Beute durch Missionen verdienen.
5. **Bedienung ohne sichere Lesekenntnisse:** Deutliche Symbole, sichtbare Reaktionen
   und kurze gesprochene Missionsbeschreibungen. Passende fertige öffentliche
   Kinderwelt-Audios dürfen mit Nachweisen übernommen werden; keine privaten Assets.
6. **Vergleich und Nachweise:** Tatsächliche Starts/Tests, Import/Animation und
   Exportaufwand dokumentieren. Bediengefühl und Leistung auf demselben echten
   Android-Gerät vergleichen, bevor eine endgültige Engine gewählt wird.
7. **Arbeitsweise:** Isolierte Entwicklung; keine Pull Requests, automatischen
   Merges oder Release-Publikationen. Keine anderen Repositories verändern.

Die Veröffentlichung von README, Auftrag und Meilenstein wurde am 28.10.2026
zusätzlich beauftragt. Dafür erhält `main` eine aktuelle Dokumentationsstartseite;
der Spielcode bleibt bis zu einer gesonderten Entscheidung auf seinem Arbeitsbranch.

## Noch keine Entscheidung beziehungsweise kein aktueller Auftrag

Eine finale Engine ist noch nicht ausgewählt. Große Kampagne, Mehrspielerbetrieb,
ein eigenständiges PC-Spiel, Produktionssignierung und Store-Veröffentlichung
gehören nicht zu diesem ersten Vergleich. Auch die Zahl künftiger Sektoren,
weitere Sprachen und die nächste Grafik-/Animationsstufe sind noch festzulegen.

„Spielbar“ und „technisch geprüft“ ersetzen weder die persönliche Abnahme des
Spielgefühls noch eine pädagogische Evaluation. Die nächste Anweisung kann sich
auf die konkreten [Ergebnisse und offenen Punkte](MILESTONE_01.md) beziehen.

## Nächste Iteration nach dem Gerätetest — 28.10.2026

Der Betreiber bevorzugt **Defold und GDevelop**. Besonders Defolds Unterscheidung
zwischen Gehen und Zielen gefällt ihm; Godot verwechselt diese Absichten auf
seinem Gerät gelegentlich. Deshalb wird Godot vorerst eingefroren und nur als
bestehende Regression erhalten. Das ist eine Auswahl für die nächste Runde,
noch keine endgültige Entscheidung zwischen Defold und GDevelop.

Beauftragt sind komplexere, grafisch ansprechendere Prototypen dieser beiden
Engines. Die berechnete Schussbahn soll ausdrücklich verschwinden. Der Spieler
muss Abprallwinkel selbst einschätzen. Maßgeblich ist jetzt
[Meilenstein 02 — Aurora Raid](MILESTONE_02.md); die obigen Drei-Engine-Anforderungen
und Meilenstein 01 beschreiben den erhaltenen Ausgangsvergleich.

## Schwerpunkt Defold — Rückmeldung zur 0.3 am 28.10.2026

Der Betreiber bevorzugt Defold, erlebt aber auch dort noch eine unklare Trennung
zwischen Laufen und Zielen. Er legt deshalb eine neue, eindeutige Regel fest:
**kurzes Drücken bewegt, längeres Drücken zielt**. Ort/Richtung und die Art des
angetippten Objekts dürfen diese Entscheidung nicht beeinflussen. Ein präziser
Tipp auf eine dünne reflektierende Wand soll nicht erforderlich sein.

Zusätzlich beauftragt: synthetische Hintergrundmusik mit fröhlichem Retro-
Plattformspiel-Charakter, ein vergrößertes Spielfeld und bessere animierte Grafik,
insbesondere eine sichtbare Explosion bei endgültig besiegten Zielen. Die Musik
wird eigenständig komponiert und synthetisiert; keine Referenzmelodie übernehmen.
Aktueller Stand: [Meilenstein 03 — Defold 0.4](MILESTONE_03.md). GDevelop 0.3 und
Godot 0.2 bleiben erhaltene Vergleichsfassungen.

## Ergänzung: alle Wände und endliche Geschosse — 28.10.2026

Der Betreiber bestätigt das größere, über den Bildschirm hinausreichende Feld.
Alle Wände sollen reflektieren. Zusätzlich sollen Geschosse endlich bleiben und
Bereiche sie neutralisieren können. Umsetzung in 0.4.1: Abpraller an Deckungen,
Rändern und geschlossenen Toren für beide Seiten; begrenzte Zahl, Reichweite und
Lebensdauer sowie blau markierte, begehbare Neutralisationsfelder. Das sind
Spielregeln für Energiegeschosse, keine realistische Ballistiksimulation.

## Gemeinsamer Spieltest und Auftrag für 0.5 — 28.10.2026

Visuelle Referenz ist jetzt **Brawl Stars**: kräftige, übersichtliche eigene
Gestaltung, keine kopierten Assets. Deckung verlassen darf taktisch nötig sein.
Alle sichtbaren Wände müssen beide Geschossarten reflektieren oder klar absorbieren;
kein optisches Darüber-/Durchfliegen. HUD und Menüs dürfen keine spielbare Fläche
abdecken. Geheimnisse erhalten kostenlose Spuren/Pfeile als Umwelthinweise.
Ausrüstung wird ausdrücklich für Sterne gekauft; die Gesamtpunktzahl bleibt
motivierend erhalten. Neue, stärker instrumentierte Musik und drei weitere
Kampfsituationen sowie auswählbare nicht-robotische Figuren sind beauftragt.

Umsetzung und Grenzen: [Meilenstein 04 — Toybox Raid](MILESTONE_04.md).
Defold bleibt Schwerpunkt, die beiden Vergleichs-Engines bleiben eingefroren.

## Visuelle Abnahme abgelehnt — neuer Qualitätsauftrag für 0.6

Der Betreiber lehnt den visuellen Stand 0.5 ausdrücklich ab. Er fordert eine
sorgfältige Recherche zu Brawl Stars und einen grundlegenden grafischen Sprung
im tatsächlichen Spiel; zusätzliche Funktionen oder Dokumentation ersetzen dies
nicht. Ziel ist eine überzeugendere Spielerfahrung als der bisherige Kinderwelt-
Maßstab. Eine Gleichwertigkeit mit einer kommerziellen Gesamtproduktion wird
nicht allein aus Testergebnissen behauptet. [Recherche](ART_DIRECTION.md),
[nächste Laufzeitfassung](MILESTONE_05.md). Fokus bleiben Defold und die bereits
funktionierenden sechs Missionen. Keine Änderungen an anderen Repositories.

## 0.6 ebenfalls abgelehnt — Neon Frontier 0.7

Der Betreiber verlangt einen deutlich größeren visuellen Sprung: futuristische
Kulisse, ausdrucksstarke animierte Figuren/Gegner, bebilderte Missionen und
Menüs mit Piktogrammen. Zusätzlich muss das Fallenlegen durch passende Sprache
verständlich werden. Neueste Präzisierung: **Fallen vollständig auf dem Spielfeld
bedienen, kein Knopf unten.** Die bisherige Halten-/Schießen-Regel bleibt.

Umsetzung: Original-Animationsbilder auf tiefengeprüften Weltflächen, neue
Sci-Fi-Architektur, Gegnerzustände und Energieexplosion; Magnet-/Eis-/Impulsauswahl
neben der Figur, pausierte Platzierungsvorschau, Boden antippen, Abbruch.
[Bedienung](TRAPS.md), [aktueller Meilenstein](MILESTONE_06.md). Das zugesandte
Instagram-Reel lieferte öffentliche Metadaten und ein sichtbares Gameplay-Cover;
das Video selbst war nicht abrufbar. Keine vorgetäuschte Videoansicht.

## Verständlicher Fortschritt — 0.8

Der Betreiber akzeptiert die grafische Richtung zunehmend, vermisst aber auffindbare
Schätze, Restzähler, einen funktionierenden Nachfolger, sichtbare Drachenwahl und
verständliche Käufe. Boni sollen in normalen Missionen liegen und mehr Sterne
bringen. Umsetzung/Abnahme in [Meilenstein 07](MILESTONE_07.md): neue Spielfluss-APIs,
Ziel-/Schatz-/Bonusführung, direkte Heldenbilder, explizites Kaufen, zwei optionale
Schussaufgaben je Mission und erhöhte einmalige Belohnungen.

## Direktsteuerung und höhere Grafikqualität — 29.10.2026

Die neueste Anweisung ersetzt ausdrücklich die alte Zeit-/Loslassen-Regel:
kurzer Bodentipp läuft, Bodenhalten feuert, eigene Figur ziehen bewegt und
Gegnertipp feuert ohne vorherige Halteschwelle mit großzügiger Antippzone. Dazu
werden die tatsächlichen Kampfansichten weiter ausgebaut. [Umsetzung/Belege](MILESTONE_08.md).
