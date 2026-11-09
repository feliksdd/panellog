# PanelLog JLCPCB BOM and CPL — engineering export

**BOM update 2026-11-09, based on `159d9a1`:** C4 → C1604; C7/C10/C12/C14/C18/C19/C20/C25 → C14663; C13/C24 → C15849 (1uF 50V X5R); Q2 → C8545. MPNs and values match the native schematic; C25 board metadata was synchronized. Replacement stock/prices were not rechecked. The CPL retains the placement from the original export below and has not been regenerated against the current WROOM layout; it must be regenerated before use.

**Source pinned**: `7f1c67f20ceba1060a6349fc031e52ae3023f9c8` of `feliksdd/panellog` main, before these export files were added. Schematic blob `a408df4acd5e40a6a7586b292318d23f13ea2572`; board blob `657b2ee9d28ddcb54a6383ef21333cb1be80b309`; selection blob `25e5232f15d614587bb242e07819c4caceb778f0`.

Fitted SMD count: 65. Grouped BOM rows: 36. CPL rows: 65. BOM/CPL reference equality checked. LCSC codes come from the reviewed 2026-11-09 selection; actual footprints and positions come from native KiCad text. **No native KiCad CLI was available in the export runtime**.

JLC columns: BOM Comment, Designator, Footprint, LCSC Part #; CPL Designator, Mid X, Mid Y, Layer, Rotation (mm and degrees). Coordinates are literal KiCad drawing positions (board-space positive Y), not a native KiCad POS export and not corrected for JLC library centroids or orientation. **Overlay and orientation MUST be checked in the JLCPCB order preview against Gerbers**, and placement origin conventions reconciled if needed. A real Fabrication Toolkit / KiCad 10 native export is preferred for release.

DNP variants (e.g. U4 P82B715, C26, R34/R35) plus D1/C23/R23 were excluded; J2/J3/J4/J5/J6/J7/J8 solder pads, H1-H4 nylon holes, and external RT1 excluded from the PCBA files.

**Qualification/sourcing statuses:** C3:CANDIDATE_REVIEW:C494873; Q2:CANDIDATE_REVIEW:C8545 (user-selected; gate-path qualification remains open); R18:OUT_OF_STOCK:C19680002; RT2:CANDIDATE_REVIEW:C406719. These sourcing statuses, except Q2's updated selection, come from the original review and were not rechecked.

**Not a fabrication release**: Current, full native ERC/DRC, Gerber/centroid registration and JLCPCB placement preview not performed by this export. Do not order unvalidated PCBA. R36 is a 0R prototype supply link, not qualified cable short protection.
