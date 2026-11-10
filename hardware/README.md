# Hardware

Das KiCad-10-Projekt liegt in [kicad/panellog.kicad_pro](kicad/panellog.kicad_pro). [Schaltplan](kicad/panellog.kicad_sch) und [PCB](kicad/panellog.kicad_pcb) sind die verbindlichen Konstruktionsdateien. Projektbibliotheken sind über `sym-lib-table` und `fp-lib-table` eingebunden.

| Verzeichnis | Inhalt |
|---|---|
| `kicad/` | Native Schaltung, Layout und Projekteinstellungen |
| `kicad/production/` | Gerber-/Bohrarchiv, BOM, Positionen und IPC-Netzliste |
| `symbols/` | Projektspezifische Symbole |
| `footprints/PanelLog.pretty/` | Projekt-Footprints |
| `3dmodels/` | Bauteil-/Gehäusemodelle und Lizenzen |
| `mechanical/` | Kradex-Gehäusegeometrie |

## Platine

118 × 90 × 1,6 mm, vier Kupferlagen. Der Umriss liegt in KiCad bei X = 81…199 mm und Y = 44,5…134,5 mm. Vorhandene Befestigungslöcher: H1, H3, H4; siehe [Montage](../docs/anwendung.md).

| Lage | Funktion |
|---|---|
| F.Cu | Bauteile, Versorgung, lokale Signale und Leistungskupfer |
| In1.Cu | GND-Bezug mit getrennten Leistungskupferbereichen |
| In2.Cu | Signalrouting und Leistungskupferbereiche |
| B.Cu | GND und Leistungskupferbereiche |

VDC, MPPT_MINUS, SHUNT_RETURN und GND führen den Modulstrom über getrennte Kupferbereiche mit Durchkontaktierungen. Die Kelvin-Leitungen gehören ausschließlich an die Sense-Anschlüsse des Shunts. Versorgungs-Schaltknoten, Q1-Gate und externe Digitalsignale benötigen Abstand zu diesen Messleitungen. Antennen-, Schrauben- und Spulensperrflächen sind beim Bearbeiten beizubehalten. Kupfergewicht und thermischer Betriebsstrom sind zusätzlich zur Lagenzahl bei der Fertigung festzulegen.

## Bearbeitung und Fertigung

KiCad 10 mit Standardbibliotheken und den lokalen Bibliothekstabellen verwenden. Nach Hardwareänderungen Zonen neu füllen, ERC/DRC mit Schaltplanabgleich ausführen und Fertigungsausgaben neu erzeugen. Die gespeicherten Ausgaben entsprechen keinem automatisch fortgeschriebenen Live-Export.

[Schaltung](../docs/schaltung.md), [Auslegung](../docs/auslegung.md), [Bestückung](../bom/README.md), [3D-Modelle](3dmodels/README.md).
