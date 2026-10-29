# Hardware

The root [README](../README.md) is the architecture, dimensioning, error-budget and calibration source of truth.

## KiCad 10 schematic

The native KiCad 10 project is in `hardware/kicad/`:

- `panellog.kicad_sch` - KiCad 10 schematic, format version 20260306
- `panellog.kicad_pro` - project settings bootstrap
- `sym-lib-table` - project-local symbol-library mapping
- `../symbols/panellog.kicad_sym` - KiCad 10 project-local symbols

The native schematic is now the electrical source of truth. Open it with KiCad 10 and save once before the first ERC run so KiCad can normalize any local project defaults.

The schematic is intentionally flat and visually split into power, measurement/switch, and logic/temperature blocks.

## Revision 0 implemented baseline

One node per PV module with:

- PV+ pass-through and INA228 VBUS measurement
- PV- return path: MPPT- -> Isabellenhuette BVB 0.7 mOhm shunt -> IPT015N10N5 -> module PV-
- INA228 differential Kelvin pickup through 10 ohm / 100 nF input filtering
- LM5164 converting the PV module directly to 3.3 V
- 9.0 V on / 8.4 V off UVLO target from 1 MOhm / 200 kOhm
- ~300 kHz LM5164 RON setting with 27.4 kOhm
- 68 uH initial buck inductor value
- Type-3 LM5164 ripple network: 150 kOhm / 3.3 nF / 150 pF
- E73-2G4M08S1C / nRF52840 in normal-voltage mode with VDD and VDDH on 3.3 V; DCCH/USB VBUS are unused
- external two-wire Pt1000 module probe, measured ratiometrically with a 14.7 kOhm precision reference
- internal 10 kOhm NTC close to Q1 for hotspot/thermal protection
- passive normally-ON Q1 gate bias with 10 V VGS clamp and MCU-controlled 2N7002 pull-down
- SWD pogo interface

The TVS position D1 is intentionally present but DNP. Its actual part number and clamp voltage must not be frozen before the cold-Voc and transient envelope is checked for every deployed module type.

## Shunt / Kelvin representation

RSH1 is deliberately represented as a **two-pin / two-net** resistor in the schematic. The future four-terminal BVB footprint must implement the force and sense lands using duplicate pad numbers:

- both MPPT-side force/sense pads -> pad number 1
- both PV-side force/sense pads -> pad number 2

INA228 sense traces must leave directly from the dedicated Kelvin lands, not from the high-current copper. This preserves an electrically correct two-net model while enforcing true Kelvin routing on the PCB.

## Layout priorities

1. Treat the 15 A current path as power hardware, not ordinary PCB routing.
2. Use the exact BVB four-terminal land geometry and independent Kelvin pickup.
3. Keep the INA228 sense pair away from the LM5164 switching loop.
4. Keep Q1 source at local PV-/MCU ground.
5. Reserve large copper/thermal-via area for IPT015N10N5 and validate behind-module temperature experimentally.
6. Start with 2 oz copper; final widths/via count are released only after thermal/current-path review.
7. Keep the E73 antenna at a module/enclosure edge and out of the aluminium-rail shadow.
8. A grounded debugger can bypass the low-side measurement; installed-system SWD must be isolated or the PV/inverter circuit disconnected.

## Not yet release-frozen

- exact PV cable / MC4-pigtail mechanics and PCB termination
- TVS / surge-clamp part number
- exact 68 uH inductor MPN and input damping capacitor
- footprints for BVB, IPT015N10N5 and PV cable interfaces
- enclosure
- exact gate-clamp zener MPN
- exact Pt1000 probe encapsulation, cable and adhesive/protective patch stack

These depend on cold-Voc/transient validation, PCB geometry and the first thermal/RF prototype.

## Validation status

The schematic file and project-local library have been generated in KiCad 10 syntax and structurally checked for balanced S-expressions, unique UUIDs, complete reference instances, and explicit no-connects on unused E73 pins.

A native `kicad-cli sch erc` run is still required after opening/saving with KiCad 10; the current execution environment does not provide KiCad 10.
