# Verbindlicher Dokumentationsstandard

Vom Betreiber am **28.10.2026** anhand des ersten EnergyBlast-Meilensteins bestätigt.
Dieser Standard gilt für die weiteren Arbeitsschritte im Repository. Referenz:
[Meilenstein 01](MILESTONE_01.md) und die aktuelle README-Startseite.

## Was zu einem nachvollziehbaren Ergebnis gehört

1. **Aktuelles README als Einstieg.** Projektziel, Zielgruppe, tatsächlich nutzbarer
   Umfang, Bedienung, Downloads und wichtigste Grenzen verständlich erklären.
   Ein Leser soll den Stand beurteilen und die nächste Anweisung formulieren können.
2. **Nachvollziehbarer Auftrag.** Originale und spätere Entscheidungen trennen.
   Ein ursprüngliches Auftragszitat unverändert erhalten; den aktuell maßgeblichen
   Auftrag konsolidiert und mit Datum verlinken. Abweichungen vom Auftrag benennen.
3. **Umsetzung, Prüfung und Planung unterscheiden.** Klar sagen, was implementiert,
   tatsächlich geprüft, noch offen oder lediglich vorgesehen ist. Ein Build,
   Screenshot oder Import ist kein Nachweis für eine erfolgreiche Geräte-Spielrunde.
4. **Wesentliche Meilensteine festhalten.** Quellcommit, Version, Artefaktcommit und
   Auftragsabgleich dokumentieren. Frühere Ausgangsstände durch feste Referenzen
   erhalten, damit ein späterer Branchstand sie nicht stillschweigend ersetzt.
5. **Testergebnisse präzise belegen.** Datum, zugehörigen Quellstand, ausgeführte
   Befehle beziehungsweise verlinkte Testanleitung, Ergebnis und praktische Grenzen
   angeben. Lokale Tests und CI trennen. Nicht ausgeführte Geräte-, Hör- oder
   Wirksamkeitsprüfungen ausdrücklich offenlassen. Eine Dokumentationsänderung
   macht alte Spieltests nicht zu neu ausgeführten Tests.
6. **Downloads überprüfbar machen.** Bei ausführbaren Dateien direkte Links,
   Plattformanforderungen, Version, Größe, SHA-256 und relevante Build-/Signatur-
   Metadaten bereitstellen. Ablaufende CI-Artefakte nicht als dauerhaften Nachweis
   behandeln. Links und Dateien soweit zugänglich vor Veröffentlichung prüfen;
   nicht prüfbare Zugriffe ehrlich kennzeichnen.
7. **Offene Entscheidungen konkret machen.** Bekannte Einschränkungen, notwendige
   manuelle Prüfungen und die noch benötigten Entscheidungen knapp aufführen.
   Für Rückmeldung einen einfachen Rahmen anbieten: Version/Engine, Situation,
   Beobachtung und nächste Prioritäten.
8. **Dokumentation pflegen statt anhäufen.** README, aktuellen Auftrag, zentrale
   Qualitätsübersicht und Testanleitung konsistent halten. Keine Einzelberichte
   für jeden Testlauf committen. Historie nicht ohne verifizierten Ersatz entfernen.
   Keine privaten Assets, Zugangsdaten oder Schlüsselmaterial veröffentlichen.

## Verhältnismäßige Anwendung

Bei wesentlichen Funktions- oder Versionsständen gehören README-/Statuspflege und
gegebenenfalls ein neuer Meilenstein zum Ergebnis. Kleine Korrekturen benötigen
keinen neuen Meilenstein und keine Wiederholung aller Spieltests; relevant sind
die tatsächlich betroffenen Angaben und angemessene Prüfungen. Bestehende
Freigabe-, Branch- und Veröffentlichungsgrenzen bleiben bestehen.

Die Abschlussmeldung verlinkt den veröffentlichten Stand und nennt knapp die
wichtigsten Änderungen, tatsächlich ausgeführte Prüfungen und verbleibende Grenzen.
