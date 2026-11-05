# PanelLog im Kradex Z74JH ABS

Mechanikstückliste: ein Z74JH ABS (graues ABS, Deckeldichtung, Standard-Deckelverschraubung) und vier zum Kunststoffdom passende Platinenschrauben. Die Platine liegt direkt auf den vier inneren Aufnahmen. Eine Montageplatte und separate Abstandhalter entfallen.

## Platine und Montage

Rechteckige FR4-Platine, 118 × 90 × 1,6 mm. In KiCad liegt die linke obere Ecke bei (15, 10) mm, die rechte untere bei (133, 100) mm. Alle vier Bohrungen sind unplattiert, Ø 3,2 mm, mit je 7 × 7 mm Kupfersperrfläche auf beiden Lagen. Das Lochbild folgt den Achsen der vier inneren Aufnahmen.

| Loch | KiCad X / Y (mm) | Ab linker oberer Platinenkante (mm) |
|---|---|---|
| H1 | 24,452 / 14,875 | 9,452 / 4,875 |
| H2 | 116,498 / 14,875 | 101,498 / 4,875 |
| H3 | 24,452 / 94,975 | 9,452 / 84,975 |
| H4 | 116,498 / 94,975 | 101,498 / 84,975 |

Die Domoberkanten liegen 4,8 mm über dem inneren Gehäuseboden. Jede Auflage hat Ø 6,05 mm. Im CAD ist die Schraubaufnahme innen annähernd quadratisch. Schraubentyp für Kunststoff, Einschraublänge, Anzugsmoment und Kopfauflage am Muster festlegen. Unterseitige Drahtenden der PV- und Sensorleitungen auf den verfügbaren Freiraum ablängen. Keine Schraube durch den Gehäuseboden führen.

Die Gehäuselage gegenüber der ersten zentrierten Überlagerung ist in PCB-X um −4,7 mm versetzt. Damit gewinnt die Deckseite Freiraum zwischen H2 und dem SWD-Anschluss J4. Q1, Shunt und Kelvin-Leitungen behalten ihre Positionen und ihr Routing. Vier GND-Stitching-Vias sind aus den Schraubfreiräumen versetzt.

## Kabelmontage

Je zwei M16-Verschraubungen für die einzelnen PV-Adern an den gegenüberliegenden Stirnwänden auf der Seite von J1 bzw. J2 vorsehen. J1 führt zum Modul, J2 zum Wechselrichter. Für das Pt1000-Kabel an J3 eine separate M12-Durchführung mit zum Leitungsdurchmesser passendem Dichteinsatz verwenden. Die Herstellerschutzart des geschlossenen Leergehäuses ist IP65. Für die bearbeitete Box sind Bohrungen, Gegenmuttern, Anschlussdichtungen und Zugentlastung separat zu prüfen.

Bohrmittelpunkte erst mit den gewählten Verschraubungen festlegen. Gegenmutter, Kabelbiegeradius, Platz für den Schlüssel, Deckeldichtung und E73-Antenne berücksichtigen. Unter dem Modul gegen direkte Sonne und stehendes Wasser geschützt montieren.

## CAD und Prüfumfang

[DXF-Draufsicht](../hardware/mechanical/Z74_base_reference.dxf), [Unterteil](../hardware/mechanical/Z74_base.sat) und [Deckel](../hardware/mechanical/Z74_cover.sat) stammen aus der Herstellerzeichnung Z74_2000.dwg. Die SAT-Dateien enthalten die beiden vollständigen ACIS-Körper im gemeinsamen ursprünglichen Koordinatensystem. Quell-DWG SHA256: 0fb30ad2446f30b14d21076ac3ea3a8dc7e6642db20b7acebb770bdac38b6124.

Für MCAD mit KiCad-Platinenoberseite als Z = 0, X nach rechts, Y nach oben und Ursprung entsprechend den KiCad-Boardkoordinaten gilt in mm:

- X = 70,3 + Z_SAT
- Y = −55 − X_SAT
- Z = 46,05 − Y_SAT

Die KiCad-Draufsicht auf User.Drawings zeigt Boden und Platinenauflagen. Bei direkter Auflage liegt die PCB-Unterseite auf Z = −1,6 mm. Die kleinste nominale Distanz des Platinenumrisses zur projizierten inneren Bodenkontur beträgt rund 5,8 mm. Die acht äußeren Platinenauflagen liegen außerhalb der Platine.

Geprüft wurden geschlossene Kontur, Übereinstimmung der vier Lochachsen mit der DXF, elektrische Pads, Leiterbahnen, Vias und Kupferfreiräume um die Schrauben. Native KiCad-10-Zonenfüllung und DRC mit Schaltplanabgleich sind für diese Revision noch auszuführen. Ein vollständiger Zusammenbau mit Kabeln, Schrauben und allen Bauteilen sowie eine Passprobe am Originalgehäuse stehen aus.
