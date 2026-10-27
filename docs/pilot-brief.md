# Engine pilot work order

**Operator update, 27 October 2026:** use the new **public** repository
`sayac007/EnergyBlast`. Do not change Kinderwelt or create pull/merge requests
at this stage. These updates override the repository/branch references in the
original request below. The earlier Kinderwelt status is historical context,
not evidence of any EnergyBlast test.

## Original request (preserved)

Bitte arbeite im Repository `sayac007/Kinderwelt`.

Wir haben eine neue Spielidee besprochen. Entwickle daraus einen kleinen, vergleichbaren Engine-Piloten und ein erstes pädagogisches Spielkonzept. Lies zunächst AGENTS.md, README und die vorhandene Projektstruktur. Das bestehende Kinderwelt-Spiel soll erhalten bleiben.

ZIEL UND ZIELGRUPPE

- Zielgruppe: Kinder von 7 bis 10 Jahren.
- Android-Spiel mit stilisierter 3D-Grafik aus der Draufsicht.
- Visuelle Referenz: „Battlelands Royale“ von Futureplay, App-ID `com.futureplay.battleground`.
- Gewünscht sind lebendige Figurenanimationen, direkte Steuerung und verständliche Effekte.
- Der Nutzer möchte drei Engines parallel anhand eines kurzen Piloten vergleichen und erst danach entscheiden.
- Vorgeschlagene Kandidaten: Godot 4, Unity und GDevelop. Diese Auswahl ist noch kein endgültiger Beschluss; prüfe ihre Eignung kurz. Unity ist der proprietäre Vergleichskandidat.

PÄDAGOGISCHER KERN

Beobachten → Planen → Handeln.

Drei Übungsziele:

1. Räumliche Orientierung:
   Wege, Deckung und Landmarken erkennen; eine Arena auch aus veränderter Kameraperspektive verstehen.

2. Geometrische Intuition:
   Sichtlinien, Winkel und Wirkungsradien einschätzen; später beispielsweise einen einfachen Abpraller vorhersagen.

3. Situationsgerechte Impulskontrolle:
   Eine vorschnelle Aktion zurückhalten, wenn Beobachten oder Vorbereiten günstiger ist. Andere Situationen verlangen schnelles Handeln. Es soll keine pauschale Regel „immer warten“ entstehen.

Die ursprünglichen Ideen des Nutzers:
- Einen großen, mächtigen Gegner beobachten und vorbeiziehen lassen.
- Das Spielfeld vorbereiten und Fallen beziehungsweise Minen platzieren.

Für die Altersgruppe wurde eine freundliche Roboterwelt vorgeschlagen. Die Fallen könnten Fangfelder, Klebefallen oder Energiefelder sein. Der taktische Reiz soll erhalten bleiben.

ERSTER PILOT: „RETTE DEN ENERGIEKERN“

- Eine kleine Arena mit zwei möglichen Wegen und geschützten Stellen.
- Ein großer Wächterroboter mit verständlichem Patrouillenverhalten.
- Anfangs sichtbarer Sichtbereich und erkennbare Laufwege.
- Ein spielbarer, animierter Charakter.
- Eine einfache Energiewaffe und ein platzierbarer Fallentyp.
- Eine Situation, in der Beobachten und Abwarten hilft.
- Eine Situation mit einem kurzen Handlungsfenster.
- Mehrere mögliche Lösungswege zum Energiekern.

Laufen, Zielen, Schießen und Reaktionen sollen sichtbar animiert sein. Noch kein vollständiges Spiel, keine große Welt und kein Online-Multiplayer.

STEUERUNG UND LERNHILFEN

- Zunächst ein Bewegungsstick und unterstütztes Zielen.
- Eine anspruchsvollere Zwei-Stick-Steuerung kann später geprüft werden.
- Kurze Hinweise mit Symbolen und vorgemachten Beispielen.
- Sichtbare Reichweiten, Laufwege und Vorschauen können schrittweise ausgeblendet werden.
- Hilfen nach Können abstufen, nicht allein nach Alter.
- Fehler sollen verständliches Feedback und eine schnelle neue Gelegenheit geben.
- Punkte für passende Entscheidungen, Vorbereitung und erreichte Ziele; keine Belohnung für möglichst langes Warten.

Wir wollen zunächst Lernen innerhalb dieser Aufgaben untersuchen. Eine Verbesserung allgemeiner Impulskontrolle im Alltag darf daraus nicht einfach behauptet werden.

ENGINE-VERGLEICH

Alle drei Piloten sollen möglichst dieselben Assets, Aufgaben, Kameraperspektiven und Steuerungsanforderungen verwenden.

Vergleiche:
- Tatsächlichen Entwicklungsaufwand.
- Figurenimport und Animation.
- Bediengefühl auf Android.
- Leistung auf demselben echten Testgerät.
- Build-/Export-Aufwand und relevante Lizenzbedingungen.

Ein spannendes Demo-Video allein genügt nicht als Entscheidungsgrundlage. Berichte tatsächliche Tests und erkennbare Grenzen.

PÄDAGOGISCHE BEOBACHTUNG

Später beim Ausprobieren beobachten:
- Verstehen Kinder die Hinweise?
- Können sie ihren Weg oder Fallenplatz erklären?
- Erkennen sie, wann Warten und wann schnelles Handeln sinnvoll ist?
- Nutzen sie das Gelernte in einer leicht veränderten Arena?

AKTUELLER STATUS

Für diese neue Spielidee wurde bisher kein Engine-Pilot implementiert oder getestet.

Frühere, erneut zu prüfende Kinderwelt-Statusmeldung:
- Repository erreichbar.
- 16 Packaging-Tests am Commit `d65ed9f` bestanden.
- Damals wurde Godot 4.7.2 benötigt, während 4.6.3 installiert war.
- Daraus wurde kein erfolgreicher vollständiger Spielstart nachgewiesen.

ARBEITSWEISE

Prüfe zuerst den aktuellen Stand und leite daraus den kleinsten spielbaren nächsten Schritt ab. Halte die drei Versuche überschaubar und vergleichbar. Keine neue Framework-Infrastruktur auf Vorrat.

Arbeite isoliert auf einem neuen Branch. Verändere keine anderen Repositories. Bewahre den funktionierenden Kinderwelt-Stand. Keine automatische Veröffentlichung und kein eigenständiger Merge.

Berichte Ergebnisse direkt im Chat: Was läuft tatsächlich, was wurde getestet, welche Probleme bestehen und welche Engine überzeugt anhand des Piloten?