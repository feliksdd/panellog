# Anschluss und Anwendung

## Verdrahtung

| Anschluss | Verbindung |
|---|---|
| J6, Pad 1 | PV-Modul + |
| J7, Pad 1 | PV-Modul − / lokales GND |
| J2, Pad 1 | MPPT + |
| J5, Pad 1 | MPPT − |
| J3, Pin 1 | Pt1000-Messleitung |
| J3, Pin 2 | Pt1000-Rückleitung / lokales GND |
| J8 | Optionaler [POA-Sensor](poa_schnittstelle.md) |
| J4 | [UART-/BOOT-Servicepads](../firmware/README.md) |

Die vier Leistungsanschlüsse sind einzelne Lötanschlüsse; J1 ist nicht vorhanden. PV-taugliche Leitungen mit passenden, untereinander kompatiblen Steckverbindern verwenden und mechanisch zugentlasten. Jeder Knoten gehört zu genau einem Modul und einem MPPT-Eingang. Keine Modulstrings anschließen und keine Masseverbindungen zwischen getrennten MPPTs herstellen.

MC4-Verbindungen nur stromlos trennen. Q1 ersetzt keine Wartungstrennstelle: Plus bleibt verbunden, Bodydiode und Diagnosepfad bleiben vorhanden. Ein geerdeter UART-Adapter, Oszilloskopanschluss oder POA-Schirm kann den Low-Side-Pfad überbrücken. Service am eingebauten Knoten erfordert galvanisch getrennte Geräte beziehungsweise einen vom Modul und Wechselrichter getrennten Aufbau.

## Gehäuse und Einbau

Kradex Z74JH ABS mit Deckeldichtung; PCB 118 × 90 × 1,6 mm. Die Platine liegt auf den inneren Kunststoffaufnahmen. Im aktuellen PCB sind H1, H3 und H4 als Befestigungslöcher vorhanden, jeweils Ø 3,2 mm; die freie vierte Gehäuseaufnahme ist bei der Montage zu berücksichtigen.

| Loch | Abstand von linker / oberer Platinenkante |
|---|---|
| H1 | 9,452 / 4,875 mm |
| H3 | 9,452 / 84,975 mm |
| H4 | 101,498 / 84,975 mm |

Passende Kunststoffschrauben verwenden; Einschraublänge am Gehäuse festlegen. Unterseitige Lötstellen und Drahtenden dürfen den Boden nicht berühren. Für vier einzelne PV-Adern sind passende Kabelverschraubungen, für Pt1000 und optional POA jeweils eigene dichte Durchführungen erforderlich. Bohrpositionen nach Leitung, Gegenmutter, Biegeradius und Deckeldichtung festlegen. Die Schutzart des Leergehäuses überträgt sich nicht automatisch auf den gebohrten Aufbau.

Unter dem Modul gegen direkte Sonne und stehendes Wasser geschützt montieren. Die WROOM-Antenne möglichst an einer Modulkante und mit Abstand zu Aluminiumprofilen platzieren. Funkverbindung in der tatsächlichen Einbaulage beurteilen. Herstellergeometrie liegt als [DXF](../hardware/mechanical/Z74_base_reference.dxf), [Unterteil-SAT](../hardware/mechanical/Z74_base.sat) und [Deckel-SAT](../hardware/mechanical/Z74_cover.sat) vor.

## Externer Pt1000

M222 Pt1000 Klasse A, 32208572 / C17472362, mit kurzer, fester Zweidrahtleitung (etwa 0,5–1 m) an J3 anschließen. Element, Leitung und ADC-Kanal gemeinsam kalibrieren. Der blanke Sensor benötigt Feuchteabdichtung und Zugentlastung.

Das Element an einer repräsentativen Zellfläche auf dem Rückseitenglas anbringen. Eine dünne elektrisch isolierende Klebeschicht sorgt für thermischen Kontakt; eine kleine wetterfeste Schutzabdeckung schützt Sensor und Anschlussstellen. Nur glas-, rückseiten- und leitungsverträgliche Materialien einsetzen. Die Messung erfasst die lokale Rückseitentemperatur; Abstand zur Zelltemperatur und Einfluss von Wind, Klebung und Abdeckung sind bei der Auswertung zu berücksichtigen.

## Inbetriebnahme und Kalibrierung

1. Polarität, Lötanschlüsse, Zugentlastung und Standardbestückung kontrollieren. Modul und MPPT zunächst getrennt halten.
2. Mit strombegrenzter Gleichspannungsquelle im vorgesehenen Eingangsbereich die 3,3-V-Versorgung und den passiven Q1-ON-Zustand erfassen. Temperatur und Funklast beim Versorgungsbudget berücksichtigen.
3. Eine an die [WROOM-Pinbelegung](../firmware/README.md) angepasste Firmware bereitstellen. Ein fertiges flashbares PanelLog-Image ist im Repository nicht enthalten.
4. Stromnullpunkt bei nachweislich stromlosem MPPT-Zweig aufnehmen; Verstärkung mit unabhängiger Referenz bei etwa 8–12 A kalibrieren. Modulspannung an zwei Punkten mit Referenzmessgerät abgleichen.
5. Pt1000 samt Leitung an bekannten Temperaturen abgleichen. Versorgungs- und NTC-Kanal auf plausible Werte, Leitungsbruch und Kurzschluss prüfen.
6. Mit dem realen MPPT langsame Schaltvorgänge, Drainrückmeldung, Transienten und erwärmten Betrieb beurteilen. Funk und optional POA mit den endgültigen Kabeln betreiben.

## Regelung und Messdaten

Die vorgesehene BatteryFlex-Regelung schaltet Module diskret ein oder aus, mit Hysterese, Mindestverweilzeit und MPPT-Einschwingzeit. Ein zeitlich begrenzter OFF-Auftrag muss erneuert werden; bei abgelaufener Frist soll die Firmware Q1 freigeben. Ein Firmware-Timeout kann einen dauerhaft hohen oder defekten GPIO nicht aufheben.

Zu übertragen sind Spannung, Strom, Leistung, integrierte Energie, Modul-/Platinentemperatur, INA-Die-Temperatur, Versorgung, angeforderter Schaltzustand und Abschaltplausibilität. Zeitstempel, Messgültigkeit, Kalibrierkennung und Resetgrund machen die Daten auswertbar. Fehlende Messungen dürfen nicht als Nullleistung oder Null-Einstrahlung erscheinen. Die BMS-/Speicherregelung bleibt unabhängig von der PanelLog-Abregelung.

Die Abschaltplausibilität kombiniert Drainspannung und Strom. Als zu parametrierender Ansatz: bei stabilen VDC ≥ 18 V nach dem OFF-Auftrag ≥100 ms warten und anschließend Vdrain ≥ 0,35 × VDC sowie |I| ≤ 0,15 A für 500 ms verlangen. Diese Schwellen sind keine nachgewiesene Schutzfunktion. Nacht, ungültige oder alte Messwerte ergeben „unbekannt“. Niedrige Drainspannung allein beweist keinen defekten MOSFET; der Wechselrichter kann den Knoten ebenfalls belasten.
