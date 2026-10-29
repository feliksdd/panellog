# PanelLog — Footprint-Abgleich und BOM-Freeze-Gates (29.10.2026)

## Native Ausgangsbasis

- Nutzerberichte: `panellog-erc-next.rpt`, 29.10.2026 22:47:52: **ERC 0 Fehler / 0 Warnungen**.
- `panellog-pcb-drc-next.rpt`, 29.10.2026 22:48:04: **39 `lib_footprint_mismatch`**, **131 `unconnected_items`**, **1 `footprint_symbol_field_mismatch`** (RSH1 Description). Keine gemeldeten Kurzschlüsse oder Lötmaskenbrücken.
- Referenzen im DRC: 39 einzelne Footprint-Instanzen. **Jede Änderung unten ist noch mit lokalem KiCad-10-DRC zu bestätigen.**

## 39 Footprint-Abweichungen: Bearbeitungsstand

| Klasse | Anzahl | Referenzen | Status |
| --- | ---: | --- | --- |
| KiCad-10-vorhandene, bereits DRC-konforme Referenz gleicher Bibliothek | **18** | R1,R2,R3,R4,R5,R9,R11,R12,R22,RT2 (R_0603); C4,C7,C12,C13,C18,C19,C20 (C_0603); R23 (R_1206) | **PCB-Datei aktualisiert** durch Übernahme der vollständigen Footprint-Geometrie samt Courtyard/Silk/3D-Modell und RoundRect-Pads aus den schon am Board vorhandenen, in diesem DRC **nicht** beanstandeten KiCad-10-Footprints R7, C8, R8. Alte individuelle Position, Rotation, UUID, Schaltplan-Pfad, Referenz, Wert, DNP und sämtliche Pin-Netze wurden erhalten; kein Schaltplansymbol wurde geändert. Ausstehend: nativer DRC |
| Weitere reguläre KiCad-10-Bibliotheken | **10** | C1,C21,C22 (C_1210), C2,C5,C6 (C_0805), C23 (C_1206), D1 (D_SMB), Q2 (SOT-23), Y1 (Crystal_3215) | Mit **installierter KiCad-10-Standardbibliothek** aktualisieren. Keine geeignete, bereits abgeglichene Instanz dieser Gehäuse in der PCB-Datei; nicht durch fremde Vorlagen ersetzen |
| PanelLog-Projektbibliothek | **11** | U1,C3,L1,J1,J2,RSH1,Q1,U2,U3,J3,J4 | **DRAFT / konstruktive Validierung erforderlich.** Bibliotheksmismatch nicht durch eine Kopie des möglicherweise fehlerhaften Footprints „beseitigen“. OEM-Zeichnungen und reale MPNs prüfen, dann nachführen |

**Rechnerisch 39 − 18 = 21 mögliche verbleibende `lib_footprint_mismatch`**. Keine Aussage, dass die neue DRC-Zahl tatsächlich 21 ist, bevor `kicad-cli pcb drc` ausgeführt wurde.

### KiCad 10: restliche Standardgehäuse synchronisieren

Im PCB-Editor (über `panellog.kicad_pro`) **Werkzeuge → Footprints aus Bibliothek aktualisieren…**. Als erste Filter nur die zehn obigen Referenzen, *nicht* alle PCB-Footprints. Pad-Netzzuordnung, Positionsänderungen, Pin 1 bzw. Polarität (D1, Q2, Y1) und Ergebnis der Aktualisierung kontrollieren. Aus 1210/0805-Datenblättern die zulässige Elektrodenform und Herstellertoleranzen prüfen. Nach dem Update native DRC mit Schaltplanvergleich ausführen.

### PanelLog-Spezialfootprints: physische Freigabe vor Bibliotheks-Synchronisierung

| Ref | Zwingender Nachweis |
| --- | --- |
| **U1** | TI LM5164 DDA-PowerPAD: Pins 1–8 und physikalisches Exposed Pad **9** (im Entwurf derzeit duplizierte Nummer 1 auf GND); Pad-, Pasten-, Wärmepfadgeometrie und Lötbrückenfreiheit. Vorläufige U1-Lands 1.55×0.60 mm ändern keine Pad-9-Diskussion |
| **RSH1** | BVB-M-R0007: vier getrennte Force/Sense-Lands und echtes Kelvin-Routing. OEM Layout-Proposal `a=2.9, c=2.0, e=0.9, f=0.8, g=5.6 mm` – erst Grafik/Zuordnung überprüfen, dann Geometrie freigeben |
| **Q1** | Infineon IPT015N10N5ATMA1 TOLL/PG-HSOF-8: Gate 1, Source 2–8, Drain-Tab; OEM-Padbelegung, Stencil und 20-A-Thermik |
| **U3** | E73-2G4M08S1C: **43** nummerierte Pads aus Drittanbieter-Vorlage, OEM-Pinplan und **2,4-GHz-Antennen- und Kupferfreihaltebereich** (alle Lagen) nachweisen; der gegenwärtige Rahmen auf Dwgs.User ist **kein** Keepout |
| **L1** | Vorläufiges 10×10-mm-Hüllmaß ist **nicht** das reale LCSC-Kandidatengehäuse (11,5×10 mm). Original-Hersteller-Landpattern, DCR, heißer Sättigungsstrom |
| **C3** | Der Platzhalter besitzt zwei **ungepolte** SMD-Pads; die ausgewählten 100-V-Aluminium-Elektrolytkandidaten sind **polarisiert**, benötigen Polaritätsmarkierung, D8-mm-Gehäuse und anderes Landpattern |
| **J1/J2** | MC4-Pigtail, Stromtragfähigkeit 20 A, mechanische Zugentlastung, Feuchtigkeit, Prüfspannung; Lötpads alleine genügen nicht |
| **J3/J4** | Pt1000-Kabel-/SWD-Pogo-Padmechanik und Schutz gegen äußere Einflüsse |
| **U2** | TI INA228 DGS VSSOP-10, Pitch 0,5 mm, DGS-Recommended-Landpattern und Kontaktlage |


### Zusätzlicher Feldabgleich

Die in diesem DRC gemeldete Abweichung `footprint_symbol_field_mismatch` von RSH1 betraf ausschließlich `Description` (PCB leer, Schaltplan nicht leer). Der RSH1-PCB-Footprint wurde auf das bestehende, unveränderte Schaltplan-Feld synchronisiert. Nicht mit einer mechanischen Freigabe verwechseln.

## BOM-Datei und freigegebene Entscheidungen

Maschinenlesbare komplette aktuelle Schaltplanliste: [`bom/panellog_rev0_selection.csv`](../../bom/panellog_rev0_selection.csv) – **62 Referenzen, davon 61 PCB und 1 externes Pt1000**. Dies ist ein Review-/Beschaffungsplan, **keine JLCPCB-Bestellfreigabe**.

- Bestehende **elektrisch selektierte** Hauptkomponenten bleiben INA228, LM5164, BVB, IPT015N10N5, E73, Susumu RTD-Referenz und drei TDK 1210 HV-MLCC.
- **Neu mit recherchierbarem Kandidaten (nicht mechanisch freigegeben):** L1 SMMS1040-680MT `C286354`: 68 µH, nominell 2 A, Isat 3,8 A, DCR 220 mΩ, **11,5×10 mm**, DCR-Verlust bei 1A ca. 0,22 W. Die LM5164-Ausgangsdrossel ist **nicht** der 20-A-PV-Strompfad.
- **C3** Panasonic EEEFN2A100P `C494873`: 10 µF, 100 V, 8×10,2 mm, Datenbank: ESR 1,3 Ω @100 kHz, Ripple 130 mA @100 kHz. Kandidat für Dämpfung; Ripple/Lebensdauer, Kaltstart und die gewünschte Dämpfung noch untersuchen. Schematic sollte bei Freigabe auf **polarisierten C** umgestellt werden.
- **RT2** TDK NTCG163JF103FT1S `C406719`: 10 kΩ, 0603, 3380 K B25/50; thermische Platzierung und Firmware-Kennlinie freigeben.
- **Q2** onsemi 2N7002 `C124475`: 60 V SOT-23. Bei der Fail-ON-Gate-Ansteuerung sind vor allem Worst-Case-Hot-Leckstrom und Q1-Gatespannung entscheidend; Pinout am konkreten Hersteller verifizieren.
- **R8** VO 47 kΩ 1206 250 mW 200 V `C2889758`: erste Kandidatur; bei 60-V-PV ca. 53 mW / bei 100 V ca. 172 mW bei idealen 10 V Zenerspannung. Temperatur-/Spannungsderating und 5-%-Toleranz prüfen.
- **Y1** Jauch `Q 0,032768-JTX310-12,5-10-T1-HMR-LF`, `C5848533`: 32,768 kHz, CL 12,5 pF, ESR 70 kΩ, 3215/2P. Crystal-Pin 1/2 sowie C16/C17 effektives CL und nRF52840 LFCLK-ESR-Freigabe erforderlich.
- **D1**, **R23**, **C23** bleiben DNP. Das ist eine bewusste Projektentscheidung, **keine fertige Überspannungsschutzlösung**.
- **Mechanische BOM weiterhin offen:** J1/J2/PV-Kabel, J3/Kabel und Wetterdichtung, J4/Pogo-Aufnahme, externes RT1-Probengehäuse.
- **Generische Passivpositionen:** Die Schaltplanwerte sind definiert, aber für 38 Positionen noch kein endgültiger Hersteller-MPN dokumentiert; für einen produktionsfähigen JLC/LCSC-Import müssen Strom-/Spannungs-/Temperatur-Derating, MPN und LCSC-Nummer ergänzt werden.

## Quellen zur Produktauswahl

- TI LM5164 https://www.ti.com/lit/ds/symlink/lm5164.pdf
- L1 https://www.lcsc.com/product-detail/Power-Inductors_SXN-Shun-Xiang-Nuo-Elec-SMMS1040-680MT_C286354.html
- C3 https://www.lcsc.com/product-detail/Aluminum-Electrolytic-Capacitors-SMD_PANASONIC-EEEFN2A100P_C494873.html
- RT2 https://www.lcsc.com/product-detail/C406719.html
- Q2 https://www.lcsc.com/product-detail/C124475.html
- R8 https://www.lcsc.com/product-detail/C2889758.html
- Y1 https://www.lcsc.com/product-detail/C5848533.html
- BVB https://www.isabellenhuette.com/de/fileadmin/Daten/Praezisionswiderstaende/Datenblaetter/BVB.PDF
- Q1 https://www.infineon.com/assets/row/public/documents/24/49/infineon-ipt015n10n5-datasheet-en.pdf
- E73 https://devzone.nordicsemi.com/cfs-file/__key/support-attachments/beef5d1b77644c448dabff31668f3a47-501ceb3d34d541b591f720b20ce1b1ba/E73_2D00_2G4M08S1C_5F00_Usermanual_5F00_v1.9.pdf

**Keine Fertigungsfreigabe:** ERC ist sauber, PCB noch weitgehend ungeroutet; die verbleibenden 21 Mismatches sind nicht nachweislich beseitigt. Reale Hersteller-Landpatterns und KiCad-10-DRC/Parität sind verpflichtend.
