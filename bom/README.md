# PanelLog BOM — Revision 0, Reviewstand 29.10.2026

**Keine Fertigungs- oder Beschaffungsfreigabe.** Die maschinenlesbare, direkt aus dem neuesten KiCad-Schaltplan abgeleitete [Referenzliste (`panellog_rev0_selection.csv`)](panellog_rev0_selection.csv) umfasst **62 reale Referenzen: 61 PCB-Bauteile plus RT1 als externen Pt1000**. Die Felder `Disposition` und `Selection_notes` grenzen eine elektrische Bauteilauswahl von einem vollständig qualifizierten Hersteller-Bestellteil ab.

Alle Schaltplanwerte und DNP-Flags stammen aus `hardware/kicad/panellog.kicad_sch`. MPN-/LCSC-Zuordnungen wurden soweit angegeben mit Hersteller/LCSC abgeglichen; Kandidaten wurden nicht ohne Landpattern- und Strom-/Temperaturfreigabe in die Schaltung übernommen.

## Vorläufig gewählte zentrale Komponenten

| Ref | MPN / Zweck | LCSC | BOM-Status |
| --- | --- | --- | --- |
| U1 | TI LM5164DDAR, 100-V-Input Buck, 3,3 V direkt | C477928 | Elektrisch festgelegt; DDA-PowerPAD/Landpattern/EP9 offen |
| U2 | TI INA228AIDGSR, Mess-ADC | C2887910 | Elektrisch festgelegt; Footprint DGS-10 verifizieren |
| U3 | Ebyte E73-2G4M08S1C/nRF52840 | projektlokal | Modul gewählt; RF-Pad-Geometrie und Antennenfreiraum offen |
| RSH1 | Isabellenhütte BVB-M-R0007-1.0, 0,7 mΩ | C5563922 | Widerstand gewählt; Force/Sense-Pads verifizieren |
| Q1 | Infineon IPT015N10N5ATMA1, 100 V TOLL | C108964 | Elektrisch gewählt; Pad-Geometrie und 20-A-Thermik offen |
| C1, C21, C22 | TDK CNA6P1X7R2A475KT000A, 4,7 µF 100 V X7R 1210 | C22877898 | Drei Stück im Eingang; Bias/Temperatur-Derating offen |
| R18 | Susumu RG1608N-1472-W-T1, 14,7 kΩ 0,05 %, 10 ppm/K | C1721340 | Präzisions-R für Pt1000 |
| D2 | JSCJ MMSZ4697, 10-V-Low-current-Zener | C2910058 | Test der tatsächlichen Q1-Gatespannung und Heißleckage notwendig |
| RT1 | Nexensos M222 Pt1000 F0.15/Class A | extern | Sensorelement gewählt, feuchtefeste cabled-Probe und Leitung noch offen |

## Neue überprüfte Kandidaten, noch nicht layoutfreigegeben

| Ref | Konkreter Kandidat | LCSC | Entscheidung/Restprüfung |
| --- | --- | --- | --- |
| L1 | Shun Xiang Nuo **SMMS1040-680MT**, 68 µH | **C286354** | 2 A Nennstrom, 3,8 A Isat, 220 mΩ DCR, 11,5×10 mm; das bisherige **10×10-mm-Draft-Footprint ist geometrisch unpassend**. Hersteller-Landpattern, Isat bei Hitze und DCR prüfen |
| C3 | Panasonic **EEEFN2A100P**, 10 µF 100 V, SMD-Alu | **C494873** | 8×10,2 mm, ESR 1,3 Ω bei 100 kHz, Ripple 130 mA (LCSC). **Polarisiert!** Der gegenwärtige 2-Pad-Draft ist nicht geeignet. Dämpfung, Temperatur/Lifetime und Polung prüfen |
| RT2 | TDK **NTCG163JF103FT1S**, 10 kΩ NTC | **C406719** | 0603, B25/50=3380 K; Firmware-Kennlinie und thermische Anbindung an Q1 prüfen |
| Q2 | onsemi **2N7002** | **C124475** | SOT-23, Worst-Case-Heißleckstrom/Fail-ON, G1/S2/D3 und VGS-Festigkeit freigeben |
| Y1 | Jauch **Q 0,032768-JTX310-12,5-10-T1-HMR-LF** | **C5848533** | 32,768 kHz / CL12,5 pF / 3215-2P; ESR und externe C16/C17 gegen nRF52840-LFCLK prüfen |
| R8 | VO **1206 ±5% 47K**, 250 mW / 200 V | **C2889758** | 47 kΩ Gate-Pull-up; elektrische/thermische Reserve im Worst Case und Toleranz prüfen |

Keine vorzeitige BOM-Festlegung: Die Katalogdaten von LCSC sind keine Garantie für Herstellerlandpattern, Qualifikation, gleichbleibenden Lieferbestand oder Heißkennwerte.

## Weiter offen: mechanisch und konstruktiv

- J1/J2: MC4-Leitungssatz, Leiterplatten-Anschlüsse, 20-A-Strompfad und mechanische Zugentlastung. Ein blankes Pigtail-Lötpad genügt nicht.
- J3: externes Pt1000-Kabel und dessen wetterfeste Kabeleinführung.
- J4: SWD-Pogo-Adapter (Spannungstrennung im verbauten System).
- U1/U3/RSH1/Q1 und L1/C3: endgültige Original-Hersteller-Footprints, Assemblierung/Lötpaste und DRC.
- Generische R/C: **38 spezifizierte Werte**, aber noch ohne endgültige Herstellernummern, Spannungstoleranz-/Temperatur-Derating und teils LCSC-Bestellnummer; für eine platzierte JLCPCB-BOM sind diese Positionen nicht fertig.

**Nicht bestücken (DNP):** D1 TVS, R23/C23 Q1-Snubber. Die Entscheidung ist bewusst provisorisch; Oszilloskopprüfung der PV-Überspannung und des Schaltverhaltens bleibt Pflicht.

## Aktuelle CAD-Prüfung

Der native ERC des Nutzers vom 29.10.2026 22:47:52 lautet **0 Fehler, 0 Warnungen**. Das PCB hat laut DRC um 22:48:04 **39 Bibliotheksabweichungen und 131 offene Verbindungen**. Davon wurden 18 Standard-Footprints durch bekannte KiCad-10-kompatible Gegenstücke auf der Platine ersetzt; das Ergebnis muss erneut mit KiCad 10 geprüft werden.

Details: [`hardware/kicad/FOOTPRINT_BOM_REVIEW_2026-10-29.md`](../hardware/kicad/FOOTPRINT_BOM_REVIEW_2026-10-29.md).

Erst wenn der revidierte BOM-Typ mechanisch, elektrisch und thermisch freigegeben ist und KiCad-ERC/DRC ohne nicht akzeptierte Verstöße besteht, darf ein PCB-Auftrag vorbereitet werden.


**Update 23:09 Uhr:** Der neue native KiCad-10-DRC bestätigte **21 statt 39 Footprint-Bibliothekswarnungen** und unverändert **131 unverbundene Verbindungen**. Danach wurden auch die letzten **zehn Standard-Footprints** aus KiCad-10-Bibliotheksdefinitionen aktualisiert (SOT-23, D_SMB, 0805/1206/1210 und Y1). Die verbleibenden **11 projektlokalen Spezialfootprints** sind mechanisch noch zu validieren; ein weiterer nativer DRC nach diesem Update steht aus. Siehe [Footprint-Review](../hardware/kicad/FOOTPRINT_BOM_REVIEW_2026-10-29.md).
