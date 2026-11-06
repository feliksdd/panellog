# PanelLog C6 / LM5163 cost revision — 2026-11-06

Reconstructed against GitHub main d8d0a7136e705900ffed0bd6bce364b5b91faa7e. This revision updates both schematic and four-layer PCB. It is a prototype revision, not a production release.

## Implemented scope

- U3: E73 replaced with ESP32-C6-MINI-1-N4 (LCSC C5736265). Official Espressif symbol, pad geometry and original STEP model; license included. Module antenna at top board edge, copper/track/via keepout on all four layers, with 15 mm lateral clearance. Final enclosure/solar-module RF tests remain necessary.
- U1: LM5163DDAR (C2873264), pin-compatible DDA package with existing thermal pad. Supply means **3.3 V / 500 mA**, not 500 mV. R4=174 kΩ / R5=100 kΩ gives nominal 3.288 V using 1.2 V reference. 1% resistor tolerance contributes approximately ±1.27% output variation before reference tolerance. RON=27.4 kΩ, L1=68 µH and the 150 kΩ / 3.3 nF / 150 pF ripple network retained. Around 300 kHz: estimated ripple 152 mA at 60 V and peak 576 mA at 500 mA output. Verify current-limit margin, stability, minimum on-time, thermal performance and RF load steps on hardware.
- EN: R17=10 kΩ / C24=1 µF. GPIO8 and GPIO9 have 10 kΩ pull-ups (R26/R25). UART/EN/BOOT replaces SWD at J4. See firmware pin map.
- R20/R24=100 kΩ each protects the rail-monitor ADC range; 100 nF filter gives 5 ms nominal time constant. ADC acquisition and calibration require measurement; old Nordic SAADC accuracy estimates are superseded.
- C15 enlarged to 22 µF / 25 V 0805. C5/C6/C15 use the same Samsung X5R part. X5R operating temperature must remain ≤85 °C; characterize effective capacitance under bias.
- Removed Y1/C16/C17: use the C6 internal LP clock. Verify sleep timing and Zigbee power consumption.
- Selected lower-cost exact MPNs for general capacitors and resistors. Keep precision R18, C0G ripple C9, 100 V ratings, input damping capacitor C3 and qualified inductor L1. No reduction of input capacitor count.
- INA228, BVB-M-R0007-1.0 0.7 mΩ shunt and IPT015N10N5 unchanged. Their positions/pad nets and the twelve VDC/MPPT_MINUS/SHUNT_RETURN copper-zone outlines are preserved. Existing stitching retained. Signals use In2.Cu with short top-layer escapes; power supply routes use F.Cu. GND planes remain In1.Cu and B.Cu, with the existing high-current copper regions.

## Procurement and savings

See `bom/panellog_rev0_selection.csv` for exact MPN/LCSC assignments and `bom/panellog_c6_procurement_4boards.csv` for grouped four-board quantities. These are procurement candidates, not a supplier quotation. Check stock, price breaks, minimum quantities and JLCPCB extended-component handling fees at order time.

Prior research indexed ESP32-C6-MINI-1-N4 at about US$3.92 and LM5163DDAR at about US$1.53 singly. Those observations are not current guaranteed quotes or reserved stock. The old E73 quote and many old passive MPNs were unspecified, so an exact total BOM saving cannot be substantiated.

C1/C21/C22: FH 1210B475K101NT / C2840282 instead of TDK CNA6P1X7R2A475KT000A / C22877898. Prior indexed single-unit prices were US$0.519 versus US$0.6872, an indicative saving of US$0.50 per board (US$2.02 for four), before quantity tiers/assembly fees. FH parts do not inherit TDK's soft-termination or DC-bias characterization. Require aggregate effective capacitance ≥2.2 µF at maximum 60 V including tolerance/temperature; test hot-plug and ringing. Do not apply the old TDK curve to FH. If that condition fails, retain the qualified input capacitors despite cost.

Further cuts considered: replacing Q2, input damping C3, high-voltage L1 or precision R18 would require new leakage, transient, insulation or accuracy qualification. No speculative substitutions made. Small-volume assembly fees may outweigh unit-price savings; quote the grouped BOM for four boards.

## Validation

Native KiCad 10.0.8 ERC/DRC and schematic parity results are stored in `hardware/kicad/review_2026-11-06/`. Final checks: ERC 0 errors / 0 warnings; PCB 0 unconnected; schematic parity 0; no copper clearance, shorting or keepout violations. Remaining DRC: 3 inherited courtyard overlaps (D1/J1, J1/C21, Q1/R9), 35 silk-over-copper warnings, 22 silk-overlap warnings, 4 silk-edge warnings and 2 dangling track warnings. They are reported, not suppressed. Native baseline has 38 unconnected items. No claim of production release is made; existing mechanical/silkscreen issues and all electrical qualification gates must be reviewed before ordering.

## Sources

- TI LM5163 datasheet: https://www.ti.com/lit/ds/symlink/lm5163.pdf
- Espressif module datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_datasheet_en.pdf
- Espressif KiCad library and license: https://github.com/espressif/kicad-libraries
- ESP32-C6 hardware guidance: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/
- LCSC part pages are identified by the exact C-number in the BOM. Recheck availability and pricing before purchase.
