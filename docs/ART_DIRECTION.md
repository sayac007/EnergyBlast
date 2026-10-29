# EnergyBlast — visuelle Richtung nach Brawl-Stars-Recherche

**28.10.2026.** Der Betreiber hat die Grafik von 0.5 ausdrücklich abgelehnt.
Ein Funktions-/Testzuwachs und kräftigere Farben genügen nicht. Maßstab ist eine
überzeugende, sorgfältig gestaltete Spielerfahrung. Die folgende Recherche
unterscheidet tatsächliche Beobachtung, veröffentlichte Produktionsangaben und
die daraus abgeleiteten Entscheidungen für EnergyBlast.

## Tatsächlich eingesehene Quellen

1. [Supercell: Brawl Stars](https://supercell.com/en/games/brawlstars/): offizielle
   Produktseite, Beschreibung und Bilder. Kurze Arena-Kämpfe, verschiedene
   Spielmodi, Charakterfokus; kein Beleg für eine pädagogische Wirksamkeit.
2. [Offizieller Google-Play-Eintrag](https://play.google.com/store/apps/details?id=com.supercell.brawlstars&hl=en)
   und [App Store](https://apps.apple.com/us/app/brawl-stars/id1229016807):
   veröffentlichte Spielbeschreibung und Store-Bilder. Sechs große offizielle
   Store-Abbildungen abgerufen; die Gameplay-Ausschnitte und die davon getrennten
   Werbe-/Figurenillustrationen selbst angesehen. Store-Illustrationen sind nicht
   automatisch die Grafikqualität jedes einzelnen Gameplay-Frames.
3. [Supercell: GDC 2025](https://supercell.com/en/news/gdc-2025/): bestätigt den
   Vortrag „Making of a Brawler: Character Creation for Brawl Stars“ von Fernanda
   Oliveira. Die Ankündigung wurde gelesen; kein vorgetäuschtes Anschauen des
   vollständigen GDC-Videos oder Zugriff auf interne Produktionsunterlagen.
4. [Sephy/Ocellus: Brawl-Stars-Illustrationen](https://sephyka.com/supercell-brawl-stars-illustrations/):
   Primärbericht des beteiligten Art Directors über Konzept-, Illustrations-,
   Layout-, Farb- und Compositing-Arbeit. Die Seite trennt Ingame-/Profilbilder,
   Ladebilder und Marketingarbeit. Diese Unterscheidung ist für den Vergleich wichtig.
5. [Modma Studios: Brawl Stars Case Study](https://www.modmastudios.com/casestudybrawlstars):
   Produktionspartner beschreibt stilisierte 3D-Assets, Rigging/Animation,
   Implementierung, technische Integration und Qualitätssicherung. Das stützt
   einen durchgängigen Asset-/Animations-/Laufzeitprozess, keine Behauptung,
   EnergyBlast verwende Supercells interne Rendertechnik.

Referenzbilder und Webseiten liegen nur temporär im Rechercheverzeichnis;
keine Supercell-Figur, Grafik, Textur, Aufnahme oder heruntergeladene Spielmodelle
werden ins Projekt oder APK übernommen. Suchtreffer wurden als Wegweiser benutzt,
nicht als verifizierter Volltext eines unbekannten Artikels.

## Beobachtung und konkrete Konsequenz

| An den offiziellen Gameplay-Bildern erkennbar | Problem der 0.5-Fassung | Konsequenz für die nächste Laufzeitfassung |
|---|---|---|
| Hohe Lesbarkeit in einer gestalteten Landschaft | Große, gleichförmige Bodenquadrate und austauschbare Farbflächen | Wirklich texturierte Sandstein-/Gartenböden, gegliederte Mauerteile, erkennbare Außenwelt, Schattierung |
| Überzeichnete, klar unterscheidbare Figuren | Starre Körper, Grundkörperoptik, kaum sichtbare Persönlichkeit | Eigenständige detailliertere Entdecker-/Drachen-/Fuchsmodelle; getrennte bewegliche Arme, Beine, Flügel und Schwanz |
| Materialien und Kontakt zum Boden statt flacher Farben | Blender-Porträts sahen besser aus als die tatsächliche Shader-Ausgabe | In der App gebundene AO-Texturen, korrigierte Licht-/Farbraumbehandlung und weich auslaufender Kontaktschatten |
| Sofort verständliche Aktion/Rückmeldung | Rotation/Bob ersetzte eine Laufanimation | Gegensinnige Arm-/Beinbewegung, Leerlaufatmung, weiche Drehung, Rückstoß und Trefferstauchung |
| Querformat und klare Blickrichtung | Portrait-Brett mit gedrehten Weltachsen und breiten leeren UI-Zonen | Festes Querformat, normale X-/Z-Orientierung, größere zusammenhängende Spielfläche mit eigenen Bedienrändern |
| Charakterinszenierung auch außerhalb des Kampfes | Statisches Bild vor einer flachen Menüfläche | Dieselbe animierte 3D-Figur auf einer eigenen Bühne, jederzeit mit Auswahl vergleichbar |
| Wenige große visuelle Schwerpunkte, plastische Bedienelemente | Flache Pillen mit viel Text, kaum Piktogrammen | Eigene mehrschichtige UI-Grafiken, klarer Gold-/Blau-/Grün-Code, Stern-/Herz-/Ziel-/Funk-Symbole |
| Sichtbare Abgrenzung von Weltkörpern und Effekten | Frühere GUI-Schüsse konnten über Mauern erscheinen | Native Tiefenprüfung bleibt verpflichtend; neue Materialien dürfen Kollisionen nicht verändern |

Das sind gestalterische Ableitungen aus den Bildern, keine Behauptung über die
unveröffentlichten Shader, Polygonbudgets, Animationsraten oder andere Interna
von Brawl Stars. Neue Bodenillustrationen wurden eigens mit dem Bildgenerator
erstellt; 3D-Geometrie, AO-Bakes und UI werden aus den versionierten eigenen
Generatoren erzeugt. Es gibt keine Kopie der Marken-/Figurenidentität.

## Sichtabnahme vor Auslieferung

Die nächste Fassung wird nicht wegen einer hohen Testzahl als optisch gelungen
erklärt. Vor dem APK-Bau müssen echte Laufzeitbilder von Menü, Figurenauswahl,
Kampf und mindestens einer neuen Mission angesehen werden. Eine tatsächliche
Bewegungs-/Angriffssequenz muss aufgenommen werden. Dabei prüfen:

- Gelangen die Texturen und die Modellschattierung wirklich bis zum Renderer?
- Sind Figuren vollständig zusammengesetzt, klar erkennbar und tatsächlich bewegt?
- Hat der Boden Materialcharakter, ohne Schüsse und Ziele zu verschlucken?
- Sind Wände und Wege räumlich unterscheidbar und alle Bedienelemente außerhalb?
- Bleibt die Richtung eines kurzen Tipps korrekt, auch nach Kamera-/Formatwechsel?
- Bleibt der Tiefenpuffer-Test verdeckter Schüsse mit sichtbarem Kontrollfall grün?

Die persönliche ästhetische Abnahme liegt beim Betreiber. Ein technischer
Regressionstest kann sie nicht ersetzen. Ebenso wenig wird eine Gleichwertigkeit
mit einer jahrelang entwickelten kommerziellen Gesamtproduktion behauptet.


## Neuer Auftrag nach Ablehnung auch von 0.6 — Neon Frontier 0.7

Die technische 0.6-Abnahme war keine visuelle Abnahme. Erneute Sichtprüfung:
Grundkörperfiguren, winzige Kugelkanonen, unruhiger Fotoboden und sechs ähnliche
Textknöpfe ergeben keinen überzeugenden kommerziellen Spielcharakter.

Zusätzlich tatsächlich eingesehen:

- [Pedro Jones: Brawl Stars Environment Design](https://pedrojonesart.myportfolio.com/brawl-stars-environment-design):
  Künstlerbericht und vier Konzeptbilder. Thematische Eingänge und lebendige
  Arenaränder erhalten eine lesbare zentrale Kampffläche. Konzept, kein Laufzeitbeleg.
- [Modma-Animationssequenz](https://framerusercontent.com/assets/dsMm7LmhcE4FyCXCeSqpMlVYYhs.mp4):
  4,949s lange öffentlich zugängliche Studio-Präsentation; zehn zeitlich verteilte
  Frames angesehen. Sprung, Drehung, Landestauchung und Erholung ändern die Silhouette.
  Kein Gameplayvideo und keine Behauptung, die gesamte Produktion angesehen zu haben.
- [Vom Betreiber zugesandtes Instagram-Reel](https://www.instagram.com/reel/DcZNsZyTveA/):
  öffentliches Cover und Metadaten geprüft. Ruhiger Boden, kräftige Deckungen,
  deutliche Figuren und große kontrastierende Effekte. Das eigentliche Video war
  ohne Anmeldung nicht abrufbar; keine Videoansicht behauptet.

0.7 setzt originale Illustrationsanimation auf native tiefengeprüfte Weltflächen,
markante Gegner, ruhigen futuristischen Deckboden, gepanzerte Lichtarchitektur,
illustrierte Missionskarten und echte mehrphasige Explosionen um. Das sind bewusst
2,5D-Figuren, keine vollwertigen Skelettmodelle. Originalquellen und Ableitungen:
[PROVENANCE.json](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/shared/assets/defold07/PROVENANCE.json). Keine Referenzgrafik
wird übernommen. Neue Bedienausnahme auf Betreiberwunsch: der pausierte
Fallenkatalog liegt direkt im Feld; normale HUD-Flächen bleiben außerhalb.

[Reale korrigierte Laufzeitbilder und Prüfgrenzen](MILESTONE_06.md). Die persönliche
Abnahme bleibt beim Betreiber, unabhängig von bestandenen technischen Prüfungen.

## 0.9 — tatsächliche Kampfansichten weiter ausbauen

Dem Betreiber ist die Grafik von 0.8 weiterhin zu einfach. Diese Iteration ändert
die laufenden Arenen: sechs eigene Bodenbilder in voller Auflösung, plastische
Deckungstypen je Bereich mit echten 1024-AO-Texturen, weiche Kontaktschatten,
animierte tiefengeprüfte Energieschilde, dünne Figurenkonturen und nähere Kamera.
Die ursprünglichen 2,5D-Figuren bleiben erhalten; keine Behauptung vollständig
skelettanimierter 3D-Figuren. [Echte Bilder und Gestenbelege](MILESTONE_08.md),
[neue Bildherkunft](https://github.com/sayac007/EnergyBlast/blob/a2fef82fb2c12d5a4b7b56cdd3735c50c6060f89/shared/assets/defold09/PROVENANCE.json). Technische Prüfungen
ersetzen weder persönliche grafische Abnahme noch einen physischen Gerätebenchmark.
