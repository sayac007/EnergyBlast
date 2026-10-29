# Fallen direkt auf dem Spielfeld

**Aktuelle Regeln ab Defold 0.12.** Die Fallenwahl ist eine ausdrücklich gestartete
taktische Aktion im **Magnetwerk**, in der **Echo-Kammer** und bei der
**Drohnen-Rettung**.
Es gibt keinen Fallenknopf unter dem Spielfeld. Kurzes Tippen auf normalen Boden
bleibt Laufen; Bodenhalten ab 0,14 Sekunden feuert, Gegnertipp schießt sofort und Ziehen der
eigenen Figur bewegt sie. Loslassen erzeugt keinen weiteren Schuss.
Ein langes Drücken öffnet deshalb keinen konkurrierenden Fallenkatalog.

1. Auf das **Fallenbild direkt neben der Spielfigur** tippen. Die Handlung hält an;
   der Katalog mit drei illustrierten Geräten erscheint auf dem Spielfeld.
2. **Magnet, Eis oder Impuls** antippen. Die Stimme nennt das Gerät und seine Wirkung.
   Der größere helle Kreis zeigt die Reichweite; helle Punkte markieren gültigen
   freien Boden. Die Vorschau zeigt den vorgesehenen Platz.
3. Innerhalb des Kreises auf freien Boden tippen und loslassen. Das gewählte Gerät
   liegt dort. Die Handlung läuft weiter. Den Wächter hineinlocken und beim offenen
   Schild treffen. Das Kreuz bricht Wahl oder Platzierung ohne Schuss ab.

| Gerät | Wirkung zu Beginn | Nachladen | Auslöseradius |
|---|---|---:|---:|
| Magnet | Gegner und Schild 18 Sekunden deaktiviert | 4 Sekunden | 0,85 Welteinheiten |
| Eis | Gegner und Schild 27 Sekunden deaktiviert | 7 Sekunden | 1,00 Welteinheiten |
| Impuls | Zwei Energiepunkte Schaden; 15 Sekunden deaktiviert | 8 Sekunden | 1,15 Welteinheiten |

Der Wächter hat drei Energiepunkte. Ein Impuls allein gewinnt die Mission nicht.
Alle drei Geräte sind frei wählbar; keine Sternkosten und keine neuen Währungen.
Maximal zwei vorbereitete Geräte existieren gleichzeitig. Das älteste weicht dem
dritten. Zu Beginn bleiben unbenutzte Geräte **36 Sekunden** liegen. Sowohl diese
Bereitschaftszeit als auch die Wirkung sind damit gegenüber 0.11 verdreifacht.
Die Platzierungsreichweite beträgt **5,25 statt 3,5 Welteinheiten**, also 50 Prozent
mehr Radius. Darstellung und Prüfung verwenden dieselbe Reichweite. Wände,
Plätze hinter einer Wand und zu weit entfernte Punkte werden abgelehnt, ohne ein
Gerät zu verbrauchen. Auch die Auslösung reicht nicht durch eine Wand. Eine zweite
Falle verkürzt eine bereits längere Schildöffnung nicht.

## Behutsam kürzere Zeiten nach erfolgreicher Anwendung

Die Zeiten werden nur dann schrittweise kürzer, wenn in einer früheren Mission
eine Falle tatsächlich einen Gegner gefangen **und** dieselbe Runde anschließend
erfolgreich abgeschlossen wurde. Ein alter Abschlussstern, bloßes Platzieren,
Scheitern oder wiederholtes Laden zählen nicht als Übungserfolg. Dieselbe Mission
zählt nur einmal. Ohne solche früheren Erfolge bleiben die langen Anfangszeiten
auch in späteren Missionen erhalten.

| Frühere erfolgreiche Fallenmissionen | Magnet | Eis | Impuls | Unbenutzt bereit |
|---|---:|---:|---:|---:|
| Keine | 18 s | 27 s | 15 s | 36 s |
| Eine | 15 s | 22,5 s | 12,5 s | 30 s |
| Zwei | 12 s | 18 s | 10 s | 24 s |

Die Stufe wird beim Missionsstart festgelegt. Laufende Fallen werden durch einen
neuen Erfolg nicht plötzlich kürzer. Beim erneuten Spielen einer früheren Mission
bleibt deren großzügigere Stufe erhalten. Der Katalog zeigt die aktuelle Wirkzeit;
an gelegten Fallen und gefangenen Gegnern steht die verbleibende Zeit.

Während Auswahl und Vorschau bleiben Gegner, Geschosse, Abklingzeiten und Kamera
stehen. Auch FEUER erzeugt in dieser Phase keinen Schuss. Menüwechsel, Verlust des
Fensterfokus oder Missionswechsel beenden den Modus. Die generösen Wirkungszeiten
lassen Raum, den gesprochenen Hinweis zu hören und anschließend zu reagieren.

Die Zeiten und Reichweite stehen in [defold04.json](../shared/defold04.json),
die Regeln in [objectives.lua](../pilots/defold/main/objectives.lua),
Gesten und Validierung in [trap_controls.lua](../pilots/defold/main/trap_controls.lua).
[trap_checks.lua](../pilots/defold/main/trap_checks.lua) prüft die echte Simulation;
[trap_training_checks.lua](../pilots/defold/main/trap_training_checks.lua) prüft
die längeren Zeiten, Grenzen, Lernstufen und gespeicherte Übungserfolge.
[check_defold_traps.py](../tools/check_defold_traps.py) betätigt den nativen Katalog
über XTest und prüft alle drei Varianten einschließlich Abbruch, Koordinaten und
ausbleibenden versehentlichen Schüssen. Diese Dateien sind Prüfverfahren; ihre
Existenz allein belegt keinen bestandenen Testlauf. Tatsächlich ausgeführte Läufe
und die weiterhin nötige Android-/Kind-Bedienprobe stehen im zentralen
[Qualitätsüberblick](QUALITY.md).
