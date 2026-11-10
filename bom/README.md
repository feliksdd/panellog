# Bestückung und Fertigungsdateien

Die vorhandene Standardbestückung liegt unter [hardware/kicad/production](../hardware/kicad/production/):

| Datei | Verwendung |
|---|---|
| [bom.csv](../hardware/kicad/production/bom.csv) | Gruppierte BOM mit LCSC-Nummern |
| [positions.csv](../hardware/kicad/production/positions.csv) | Bestückungspositionen |
| [designators.csv](../hardware/kicad/production/designators.csv) | Referenz-/Bestückungsdaten |
| [panellog.zip](../hardware/kicad/production/panellog.zip) | Gerber- und Bohrdaten |
| [netlist.ipc](../hardware/kicad/production/netlist.ipc) | IPC-Netzliste |

## Hauptbauteile

| Referenz | Herstellerteil | LCSC |
|---|---|---|
| U1 | LM5163DDAR | C2873264 |
| U2 | INA237AIDGSR | C2864837 |
| U3 | ESP32-C6-WROOM-1-N4 | C6034714 |
| Q1 | IPT015N10N5 | C108964 |
| Q2 | 2N7002 | C8545 |
| RSH1 | HOVB4026-5W-1mR-1% | C481535 |
| L1 | CDRH127/LDNP-680MC, 68 µH | C2452974 |
| R18 | PTFR0603B14K7N9, 14,7 kΩ, 0,1 %, 10 ppm/K | C19680002 |
| RT2 | NTCG163JF103FT1S | C406719 |
| RT1, extern | M222 Pt1000 Klasse A, 32208572 | C17472362 |

Für Q1 ist C108964 aus der Produktions-BOM zu verwenden. Das LCSC-Feld des Q1-PCB-Footprints enthält C8545 und widerspricht dem Bauteil IPT015N10N5; daraus darf kein automatischer Bestellimport erfolgen.

D1, R23/C23 sowie U4, C26 und R34/R35 bleiben in der Standardbestückung unbestückt. R32/R33 und R36 sind 0-Ω-Brücken. Die alternative Pufferbestückung steht in der [POA-Beschreibung](../docs/poa_schnittstelle.md).

J2/J3/J4/J5/J6/J7/J8 sind PCB-Löt-/Serviceflächen, keine zu beschaffenden Steckverbinder. RT1 liegt außerhalb der Platine und ist zusätzlich zur SMD-BOM zu beschaffen. Gehäuse, passende Kunststoffschrauben, PV-Leitungen, Stecker, Sensorkabel und dichte Kabeldurchführungen ergänzen die Baugruppe.

Preise, Lagerbestand, Mindestmengen und JLCPCB-Bestückungsklasse sind lieferantenabhängig und bei der Bestellung zu ermitteln. Nach Hardwareänderungen BOM, Positionen und Gerber gemeinsam aus derselben Konstruktion exportieren.
