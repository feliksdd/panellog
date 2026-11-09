# PanelLog — JLCPCB BOM / CPL export (engineering, not released)

Source: `feliksdd/panellog` main commit `7f1c67f20ceba1060a6349fc031e52ae3023f9c8`, schematic `a408df4acd5e40a6a7586b292318d23f13ea2572`, PCB `657b2ee9d28ddcb54a6383ef21333cb1be80b309`, reference BOM `25e5232f15d614587bb242e07819c4caceb778f0`.

BOM columns: Comment, Designator, Footprint, LCSC Part #. CPL columns: Designator, Mid X, Mid Y, Layer, Rotation. Units in mm. Coordinates are literal KiCad PCB footprint anchors (positive board X/Y), raw KiCad rotations normalized to 0..359; **these are not transformed JLC library pick-and-place origins/rotations**. Compare EVERY polarized/IC part and the entire placement overlay with the Gerbers in the JLCPCB upload preview. This connector-based export is not the native KiCad 10 POS exporter or Fabrication Toolkit.

Counts: 0 fitted surface-mount components, 0 grouped BOM lines, 0 unique LCSC codes, 0 CPL lines. BOM/CPL expanded designator sets verified equal. Board-only solder pads (J2...J8), mounting holes and external Pt1000 RT1 excluded; all PCB/schematic DNP excluded, including U4 P82B715 and snubber/TVS optional placements.

## Procurement and release blockers

- R18 marked OUT_OF_STOCK in source reviewed selection, LCSC `C19680002`. **Do not place assembly order until stocked suitable alternative confirmed and schematic/BOM updated.**
- CANDIDATE_REVIEW components  require engineering confirmation.
- R36 is a 0-ohm link in the prototype external POA 3V3 power line; system-level cable short protection still requires qualification.
- Exact rotation/centroid alignment not corrected for vendor library; **verify PCB+PCBA preview**, notably U1, U2, U3, Q1, Q2, C3 and D2/D3.
- No native KiCad 10 ERC/DRC or fabrication Gerber comparison performed by this export. Do not treat files as fabrication release.

Generated files:
- `panelLog_JLCPCB_BOM.csv`
- `panelLog_JLCPCB_CPL.csv`
