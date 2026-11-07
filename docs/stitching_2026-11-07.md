# Plane stitching regeneration

Based on the latest user placement (GitHub 2c391741). Plane outlines and
component positions retained. Removed 265 plane-only vias: GND 131, VDC 52,
MPPT_MINUS 61, SHUNT_RETURN 21. Four GND vias touching routed tracks retained;
signal transition vias retained. Three obsolete plane vias intersecting the
new feedback route had already been removed in the feedback commit.

Generated 386 vias inside the common filled copper area:

| Net | Added vias | Pitch | Diameter / drill | Required connected layers |
|---|---:|---:|---:|---|
| GND | 117 | 5 mm | 0.6 / 0.3 mm | F.Cu, In1.Cu, B.Cu |
| VDC | 168 | 3 mm | 0.8 / 0.4 mm | all four |
| MPPT_MINUS | 70 | 3 mm | 0.8 / 0.4 mm | all four |
| SHUNT_RETURN | 31 | 3 mm | 0.8 / 0.4 mm | all four |

Generator excludes pads, holes, other-net tracks, existing vias, copper
boundaries and antenna area. Solder-mask settings are inherited from the board defaults.
The signal layer has no blanket GND plane; power islands remain on all four
layers as requested. This geometry is not a verified current/thermal rating.

After native zone refill, all 386 new vias retain their assigned net and have
same-net filled copper at their centre on every required layer. KiCad DRC:
no new electrical violations, zero schematic parity issues, unchanged 43
open connections. The 97 remaining rule findings are silk (including new reference labels), four existing library
footprint mismatches and the existing Q1/R9 courtyard overlap. The 43 opens
must be routed before manufacture. Five baseline ERC findings remain.

See review_2026-11-07/stitching.json and DRC_step4.json for exact UUIDs/counts.
Reproduction: tools/regenerate_stitching.py requires KiCad 10 pcbnew + shapely;
refill zones and run native DRC after any regeneration.
