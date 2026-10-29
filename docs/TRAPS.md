# Fallen direkt auf dem Spielfeld

Die Fallenwahl ist eine ausdrücklich gestartete taktische Aktion im **Magnetwerk**.
Es gibt keinen Fallenknopf unter dem Spielfeld. Kurzes Tippen auf normalen Boden
bleibt Laufen; Bodenhalten ab 0,14 Sekunden feuert, Gegnertipp schießt sofort und Ziehen der
eigenen Figur bewegt sie. Loslassen erzeugt keinen weiteren Schuss.
Ein langes Drücken öffnet deshalb keinen konkurrierenden Fallenkatalog.

1. Auf das **Fallenbild direkt neben der Spielfigur** tippen. Die Handlung hält an;
   der Katalog mit drei illustrierten Geräten erscheint auf dem Spielfeld.
2. **Magnet, Eis oder Impuls** antippen. Die Stimme nennt das Gerät und seine Wirkung.
   Der helle Kreis zeigt die erreichbare Umgebung; die Vorschau zeigt den Platz.
3. Innerhalb des Kreises auf freien Boden tippen und loslassen. Das gewählte Gerät
   liegt dort. Die Handlung läuft weiter. Den Wächter hineinlocken und beim offenen
   Schild treffen. Das Kreuz bricht Wahl oder Platzierung ohne Schuss ab.

| Gerät | Tatsächliche Wirkung | Nachladen | Auslöseradius |
|---|---|---:|---:|
| Magnet | Wächter und Schild 6 Sekunden deaktiviert | 4 Sekunden | 0,85 Welteinheiten |
| Eis | Wächter und Schild 9 Sekunden deaktiviert | 7 Sekunden | 1,00 Welteinheiten |
| Impuls | Zwei Energiepunkte Schaden; 5 Sekunden deaktiviert | 8 Sekunden | 1,15 Welteinheiten |

Der Wächter hat drei Energiepunkte. Ein Impuls allein gewinnt die Mission nicht.
Alle drei Geräte sind frei wählbar; keine Sternkosten und keine neuen Währungen.
Maximal zwei vorbereitete Geräte existieren gleichzeitig. Das älteste weicht dem
dritten; unbenutzte Geräte verschwinden nach 12 Sekunden. Die Platzierungsreichweite
beträgt 3,5 Welteinheiten. Wände, Plätze hinter einer Wand und zu weit entfernte
Punkte werden abgelehnt, ohne ein Gerät zu verbrauchen. Eine zweite Falle verkürzt
eine bereits längere Schildöffnung nicht.

Während Auswahl und Vorschau bleiben Gegner, Geschosse, Abklingzeiten und Kamera
stehen. Auch FEUER erzeugt in dieser Phase keinen Schuss. Menüwechsel, Verlust des
Fensterfokus oder Missionswechsel beenden den Modus. Die generösen Wirkungszeiten
lassen Raum, den gesprochenen Hinweis zu hören und anschließend zu reagieren.

Die Regeln liegen in [objectives.lua](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/pilots/defold/main/objectives.lua),
Gesten und Validierung in [trap_controls.lua](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/pilots/defold/main/trap_controls.lua).
[trap_checks.lua](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/pilots/defold/main/trap_checks.lua) prüft die echte Simulation;
[check_defold_traps.py](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/tools/check_defold_traps.py) betätigt den nativen Katalog
über XTest und prüft alle drei Varianten einschließlich Abbruch, Koordinaten und
ausbleibenden versehentlichen Schüssen. Diese Dateien sind Prüfverfahren; ihre
Existenz allein belegt keinen bestandenen Testlauf. Tatsächlich ausgeführte Läufe
und die weiterhin nötige Android-/Kind-Bedienprobe stehen im zentralen
[Qualitätsüberblick](QUALITY.md).
