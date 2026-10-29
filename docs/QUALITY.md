# Aktueller Prüfstand — Defold 0.11

**29.10.2026.** [Auftrag, Ursache, Umsetzung und Bilder](MILESTONE_10.md),
[Testkommandos](BUILD_AND_TEST.md), [APK-Metadaten](../downloads/README.md).

| Tatsächlich ausgeführt | Ergebnis |
|---|---|
| Native Regeln/Darstellung | **820 PASS**, 629 bisherige + 72 Zoom + 117 Schatz + 2 native Materialprüfungen |
| Gemeinsame Tests | **15 Gruppen PASS**, Daten/Medien/Herkunft, echte Wandpuffer, Batch-Identität, HD-Atlanten und aktive Ressourcen |
| Zoom-Mathematik/Eingabe | **PASS**, gleiche Projektion/Rückprojektion, drei Größen und drei Fensterformate, Grenzen/Speicherung/Fokus, native Zwei-Finger-Pakete und Abbruch ohne Restgeste |
| Tatsächliche Zoom-Ausgabe | **PASS**, echte Plus-/Minus-Klicks, mehr als 5.000 veränderte Weltpixel und passende projizierte Figurengröße; feste HUD-Größe |
| Sechs Schatzfunde | **PASS**, echte Hinweise, echte Wege und Aufnahme je 75 Sterne, 0 Schüsse; im Testprofil Gesamtstand 2.400 → 2.850 |
| Schatzregeln | **PASS**, erreichbare Such-/Fundpunkte, Entdeckung/Speicherung, Sichtlinie, keine Aufnahme durch Wände/Tore, keine Doppelbelohnung oder erneute Hinweiskosten |
| Bisherige tatsächliche GUI | **PASS**, fünf direkte Gesten, Helden/Käufe/Missionen/Fallen/Schutzort/Heilung und beide Fensterformate |
| Getrennte Speicherprozesse | **PASS**, Sterne, Guthaben, Käufe, Figur, Hinweise, Musik; Zoom und Schatzentdeckung zusätzlich rekonstruiert |
| HD-Figuren | **PASS**, 3 Atlanten 1536×1024, 24 unterschiedliche transparente Zellen, alte Quellen erhalten, aktive Modell-/Shaderbindungen |
| Native Schimmerausgabe | **PASS**, an/aus 2.937 veränderte Pixel; sechs begrenzte native Lichtobjekte |
| Native Geschossverdeckung | **PASS**, verdeckt 0 Pixel; sichtbarer Kontrollfall 328 Pixel |
| Native Energieschild-Ausgabe | **PASS**, an/aus 15.701 veränderte Pixel |
| Tatsächliche Audioausgabe | **PASS**, Musik an RMS 0,01342, aus 0, Mischung 0,04256; kein gemessener Überlauf |
| Sprache | **32/32 technisch PASS**, 2 neue Ansagen frisch unabhängig ASR-exakt, 30 vorherige samt Metadaten unverändert |
| Eigene Sichtprüfung | Neue drei Atlanten, Figurenwahl, sechs Hinweisaufnahmen, Zoomvergleich und native Bewegungssequenz angesehen |
| APK 0.11.0 / Code 12 | **PASS**, sauberer Quellstand, Paket/APIs/Querformat, keine Berechtigungen, Backup aus, v2-Signatur und gleiches Zertifikat wie 0.10, ZIP-CRC, keine Schlüsseldateien, 16-KB-ZIP-Ausrichtung, 828 identische Projektdateien und Android-Shaderexport |

Geprüfter Quellstand [`59f1312`](https://github.com/sayac007/EnergyBlast/commit/59f13122e5840731d07c7a5c6b25a9ed18eea54c),
APK-Snapshot [`16dc606`](https://github.com/sayac007/EnergyBlast/commit/16dc606fa4b273887d20e6939539d39cd3b5439c),
gebaut 29.10.2026, 11:05 MEZ. [Dateigröße, SHA-256 und Download](../downloads/README.md).

Die echte Zwei-Finger-Geste wurde hier nicht auf Android ausgeführt. Native
Controllerpakete prüfen Verarbeitung und Abbruch; XTest klickt die Zoombuttons.
Ein Sofortschuss vor dem Hinzukommen eines zweiten Fingers kann nicht zurückgenommen
werden, ohne die bisherige unmittelbare Gegnerreaktion zu ändern. Freier Boden
ist deshalb der empfohlene Beginn für eine Zoomgeste.

Die Truhen bleiben native tiefengeprüfte Objekte. Eine Markierung zeigt bei
Verdeckung den Fundort; sie hebt die Wandkollision nicht auf. Welttext wird mit
vergrößert, das HUD bleibt konstant. Die neuen Figuren sind weiterhin 2,5D.

**Manuell offen:** Android-Update/Spielstände, echter Mehrfingerzoom, tatsächliche
Eingabelatenz, kleine/größere Displays, maximale Zoomleistung, Klang und grafische
Abnahme sowie langfristige Balance. Keine Store-Freigabe, neue grüne CI oder
empirische Lernwirkung behauptet. Keine zusätzlichen Hörprüfungen für die 30
unveränderten Aufnahmen vorgetäuscht.

[Vorheriger 0.10-Prüfstand](https://github.com/sayac007/EnergyBlast/blob/fb75f015ba31141b1658207b581e87bdffb2a279/docs/QUALITY.md),
[0.10-Meilenstein](MILESTONE_09.md), [0.9](MILESTONE_08.md).
