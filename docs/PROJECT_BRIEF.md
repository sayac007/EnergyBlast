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
