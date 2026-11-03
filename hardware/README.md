> [Lokale STEP-Modelle und Gehäusevorschau](3dmodels/README.md) sind vollständig im Projekt hinterlegt.

> Gehäuserevision: [Spelsberg 12741501, Platine 150 × 104 mm und Kabelmontage](../docs/enclosure_2026-11-03.md).

> Latest routed prototype and actual KiCad 10.0.8 ERC/DRC: [review 2026-11-03](../docs/review_2026-11-03.md). Production release remains pending.

# Hardware

The root [README](../README.md) is the architecture, dimensioning, error-budget and calibration source of truth.

> **ERC-Warnung (29.10.2026):** Ein echter KiCad-10-ERC fand im ursprünglich erzeugten Schaltplan **35 Fehler und 65 Warnungen**, darunter sicherheitskritische Fehlzuordnungen an U1/U2/Q1/Q2/U3. Der Schaltplan wurde daraufhin in Commit `b1f31a81086f` anhand der tatsächlichen Pinpositionen korrigiert und auf 1,27-mm-Raster ausgerichtet. Die korrigierte Anschlussgeometrie wurde statisch geprüft; ein **erneuter nativer KiCad ERC** steht weiterhin aus. Das frühere allgemeine Strukturprüfergebnis war unzureichend. [Detaillierter ERC-Befund](kicad/VALIDATION_2026-10-29.md).

> **Aktualisierung 29.10.2026:** Die Schaltung nutzt jetzt bei allen 60 generischen Bauteilen KiCad-Standardsymbole (u.a. Device:R/C/L/D_Zener/Crystal/Thermistor_NTC, Transistor_FET:2N7002, Connector_Generic, power:PWR_FLAG). Nur die fünf speziellen Schaltungssymbole bleiben in der PanelLog-Projektbibliothek. Insgesamt sind 198 sichtbare Drahtsegmente und 20 Junctions eingezeichnet; 143 lokale Netlabels verbleiben für bereichsübergreifende Signale. Der automatische Netzvergleich gegen den Originalstand ergibt **193/193 identische Pin-Netzzuordnungen**. **Ein neuer nativer KiCad-10-ERC und eine optische Kontrolle sind noch erforderlich.** Siehe [Konvertierungs- und Validierungsbericht](kicad/STANDARD_SYMBOLS_WIRING_2026-10-29.md).

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
- 9.0 V on / 8.4 V off **typical** UVLO target from 1 MOhm / 200 kOhm (datasheet thresholds and component tolerances apply)
- ~300 kHz LM5164 RON setting with 27.4 kOhm
- 68 uH initial buck inductor value
- Type-3 LM5164 ripple network: 150 kOhm / 3.3 nF / 150 pF
- E73-2G4M08S1C / nRF52840 in normal-voltage mode with VDD and VDDH on 3.3 V; DCCH/USB VBUS are unused
- external two-wire Pt1000 module probe, measured ratiometrically with a 14.7 kOhm precision reference
- internal 10 kOhm NTC close to Q1 for hotspot/thermal protection
- passive normally-ON **intended** Q1 gate bias with **R8 47 kΩ**, **JSCJ MMSZ4697 10-V low-current zener (D2)** and **R9 2.2 kΩ**, with MCU-controlled 2N7002 pull-down; hot leakage, actual gate voltage, switching SOA and fault behavior remain unqualified
- SWD pogo interface

The TVS position D1 is intentionally present but DNP. Its actual part number and clamp voltage must not be frozen before the cold-Voc and transient envelope is checked for every deployed module type.

## Shunt / Kelvin representation

RSH1 is deliberately represented as a **two-pin / two-net** resistor in the schematic. The future four-terminal BVB footprint must implement the force and sense lands using duplicate pad numbers:

- both MPPT-side force/sense pads -> pad number 1
- both PV-side force/sense pads -> pad number 2

INA228 sense traces must leave directly from the dedicated Kelvin lands, not from the high-current copper. This preserves an electrically correct two-net model while enforcing true Kelvin routing on the PCB.

## PCB placement draft (2026-10-29)

A first native KiCad PCB now exists at [`kicad/panellog.kicad_pcb`](kicad/panellog.kicad_pcb): **61 placed components, 191 pads, 32 nets, 116×86-mm provisional outline, two pilot copper segments**. The external RT1 and ERC PWR_FLAGs remain off-board by design. An independent schematic-derived pad/net check found no mismatches or overlapping pads belonging to different nets. However, **this is NOT a routed, DRC-clean, 20-A/60-V-qualified or fabrication-ready board**. Nine local footprints are prototype candidates only, with major MPN/mechanical issues still open. Mandatory next step is the native KiCad 10 PCB DRC with schematic parity and completion of Kelvin sensing, return current path, buck/RF wiring, copper/via thermal design. See [PCB design status and footprint matrix](kicad/PCB_LAYOUT_REV0_DRAFT.md).

## Layout priorities

1. Treat the 15 A current path as power hardware, not ordinary PCB routing.
2. Use the exact BVB four-terminal land geometry and independent Kelvin pickup.
3. Keep the INA228 sense pair away from the LM5164 switching loop.
4. Keep Q1 source at local PV-/MCU ground.
5. Reserve large copper/thermal-via area for IPT015N10N5 and validate behind-module temperature experimentally.
6. Start with 2 oz copper; final widths/via count are released only after thermal/current-path review.
7. Keep the E73 antenna at a module/enclosure edge and out of the aluminium-rail shadow.
8. A grounded debugger can bypass the low-side measurement; installed-system SWD must be isolated or the PV/inverter circuit disconnected.

## Updated field-installation assumptions (2026-10-29)

The intended PV connection uses only **1–2 m MC4 cables** per single module and infrequent, slow Q1 switching. A continuously imposed >85-V PV-module voltage is not expected from the nominal cold `Voc`, but inductive switching peaks at **Q1 drain**, MPPT input-capacitor resonance, and unrelated induced surges cannot be excluded by `Voc`. Given the explicitly accepted modest surge-protection requirement, **retain D1 as DNP**, reserve Q1-snubber space if possible, and scope the actual transients before ordering a TVS. The provisional 20-A thermal/current case remains. The proposed capacitor/zener/gate value changes and actual LCSC numbers are in [short-lead PV decisions](../docs/design_decisions_short_pv_leads_2026-10-29.md). Native schematic **has now been modified**, see [pin/net static validation](kicad/VALIDATION_2026-10-29.md). D1 and the Q1 RC snubber are **DNP**, not fitted protection.

## Not yet release-frozen

- exact PV cable / MC4-pigtail mechanics and PCB termination
- TVS / surge-clamp part number
- exact 68 uH inductor MPN, hot Isat, input MLCC DC-bias derating (C1), input damping capacitor and regulator exposed-pad footprint
- footprints for BVB, IPT015N10N5 and PV cable interfaces
- enclosure
- verify exact JSCJ MMSZ4697 diode characteristics and qualified 2N7002 Q2 MPN; test gate voltage, hot leakage, R9 switching time/SOA and brownout
- exact Pt1000 probe encapsulation, cable and adhesive/protective patch stack

These depend on cold-Voc/transient validation, PCB geometry and the first thermal/RF prototype. The earlier 15-A power-path envelope is not generally sufficient for the bifacial Solarwatt model; perform a provisional 20-A thermal/current-path design check as described in [the detailed audit](../docs/electrical_audit_2026-10-29.md). The native schematic remains unchanged pending verified part choices.

## Validation status

The schematic file and project-local library have been generated in KiCad 10 syntax and structurally checked for balanced S-expressions, unique UUIDs, complete reference instances, and explicit no-connects on unused E73 pins.

A native `kicad-cli sch erc` run is still required after opening/saving with KiCad 10; the current execution environment does not provide KiCad 10. See [datasheet-based electrical audit (2026-10-29)](../docs/electrical_audit_2026-10-29.md) for recalculations, source links and blockers.

