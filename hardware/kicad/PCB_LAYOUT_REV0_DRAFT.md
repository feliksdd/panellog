# PanelLog PCB Rev0 — footprint review and placement draft (2026-10-29)

**STATUS: ENGINEERING DRAFT — DO NOT FABRICATE, ORDER PCBA, OR CONNECT TO A LIVE PV SYSTEM.**

Native file: `hardware/kicad/panellog.kicad_pcb` (opens in KiCad 10; initially written using KiCad 9-compatible PCB serial format 20241229). The file must be re-saved/upgraded in the user's KiCad **10.0.7**, and a **native DRC with schematic parity** is outstanding. No DRC/thermal/EMC test has been run in the execution environment. The previous **0-error/0-warning ERC** applied to the pre-footprint-synchronization schematic; repeat ERC after the latest schematic footprint assignments.

## Deliverables

- `panellog.kicad_pcb`: placed 61 of 65 schematic symbols (the external RT1 and three ERC PWR_FLAGs correctly have no board instance); 191 pads, 32 named nets, **two preliminary copper segments**; board outline **116 × 86 mm** (x=2..118, y=2..88).
- `panellog-layout-netlist-draft.json`: independent source-structural snapshot of schematic reference designators, numbered pins, net labels, DNP flags and footprint identifiers. Regenerate from the native KiCad netlist after editing.
- `hardware/footprints/PanelLog.pretty/`: nine new project-local review-stage footprint definitions, in addition to the previously existing INA228 footprint.
- Schematic `Footprint` fields updated for U1, U3, Q1, RSH1, J1/J2, L1, C3, J3, J4, Y1.

### Validation performed

1. Parse of generated native PCB S-expressions was successful.
2. Exactly **61 reference designators** and **191 numbered PCB pads** were found, using 32 named electrical nets.
3. Compared every numbered PCB pad to its matching net in the schematic-derived 61-component snapshot: **0 mismatches**, including duplicated pad numbers (BVB Kelvin and LM5164 exposed pad).
4. Approximate axis-aligned pad-overlap screening: **0 overlapping pads on different nets** and **0 pads outside the board outline**. This does **not** detect trace-to-pad clearances, rotated courtyard/interference, copper-zone thermal behavior, silkscreen clashes, mask slivers, via capacities, or all DRC errors.

## Critical footprint verification matrix

| Component | Draft footprint | Source / assessment | Release |
| --- | --- | --- | --- |
| R/C standard | KiCad library 0603, 0805, 1206, 1210 | Board pad sizes copied from [official KiCad footprints](https://kicad.github.io/footprints/), but graphics/courtyards are simplified in the generated board; update footprints from KiCad 10 library | **Pending library update + DRC** |
| Q2 2N7002 | `Package_TO_SOT_SMD:SOT-23` | 1 Gate, 2 Source, 3 Drain; physical pinout and specific vendor required | Pending |
| U2 INA228 DGS10 | `PanelLog:INA228_DGS10` | 10 pads/0.5-mm pitch, 3×3-mm body; TI [INA228AIDGSR](https://www.ti.com/product/INA228/part-details/INA228AIDGSR) | Compare pad spacing/polarity with TI land pattern |
| U1 LM5164 | `PanelLog:LM5164_DDA_PowerPAD_DRAFT` | 8 leads + exposed pad (duplicate pad 1 tied GND), based on TI DDA0008B PowerPAD. Copper, vias, stencil and package land pattern still need verification | **DRAFT / blocked** |
| Q1 Infineon IPT015N10N5 | `PanelLog:IPT015N10N5_TOLL_DRAFT` | Gate 1, sources 2–8, large Drain 9. Intended PG-HSOF-8/TOLL package; drafted using [Infineon footprint drawing](https://www.infineon.com/dgdl/Infineon-PG-HSOF-8-1_IPT015N10N5ATMA1-PD-v01_00-EN.pdf?fileId=5546d46254e133b40154f177a6bb4cd9), approximate pad coordinates and mask/paste | **DRAFT / blocked** |
| RSH1 Isabellenhütte | `PanelLog:BVB_M_R0007_Kelvin` | Four solder lands: MPPT force/sense both pad 1; Q1 force/sense both pad 2, per 2-net schematic. [BVB official datasheet (page 2)](https://www.isabellenhuette.com/hubfs/Files/Data-sheets/BVB.pdf); dimensions of pads still preliminary | **DRAFT / blocked** |
| U3 E73 module | `PanelLog:E73_2G4M08S1C_DRAFT` | 43-pad numbers based on third-party [nRFmicro module footprint](https://github.com/joric/nrfmicro/blob/main/hardware/nrfmicro.pretty/E73-2G4M08S1C-52840.kicad_mod). Some third-party through-hole pads represented here as SMD lands; exact Ebyte recommendation and ceramic antenna keepout **not confirmed** | **DRAFT / blocked** |
| J1/J2 MC4 cable pigtails | `PanelLog:PV_MC4_Pigtail_2x2p8_DRAFT` | Two PTH pads with 2.8-mm drills. This is a **concept**, not a strain-relieved, outdoor-rated, 20-A connector solution. Must finalize cable diameter, mounting and pull-out strength | **DRAFT / blocked** |
| L1 68 µH | `PanelLog:L_68uH_ENVELOPE_DRAFT` | Generic 10×10-mm space allocation. Actual 68-µH MPN, hot Isat, current and height are not selected | **DRAFT / blocked** |
| C3 100-V bulk | `PanelLog:C_10uF_100V_DAMP_DRAFT` | Generic 10-mm envelope. Optional damping capacitor, no confirmed value or MPN | **DRAFT / blocked** |
| J3 temperature cable, J4 SWD pads, Y1 crystal | Project-local J3/J4 drafts; standard 3.2×1.5-mm two-pin Y1 | Physical connector mechanics, probe ESD/wet protection, and crystal CL/MPN need confirmation | **Pending** |

**Footprint source warning:** The prototype PCB includes only simplified pad and courtyard geometry, not all manufacturer's qualified assembly layers/stackups. A correct pad count is not a mechanical qualification. Do not export manufacturing Gerbers at this stage.

## Placement and power routing

- Top edge: E73 13×18-mm module and tentative antenna no-copper reminder, **not yet an actual DRC-enforced keepout**. Must establish the antenna end/direction according to Ebyte datasheet, keep metal and all layers' copper away from RF region.
- J1 module input left, J2 MPPT output right. These are prototype pigtail footprints, not MC4 connectors mounted directly on PCB.
- Q1 TOLL switch is low in the board; RSH1 BVB just to its right, ensuring a **short, straight Q1-drain → shunt pad-2** connection (preliminary 5-mm wide front-layer segment).
- INA228 near shunt, with differentiated Kelvin pads reserved for two independent thin sense tracks. **Kelvin routing is NOT yet completed.**
- Buck components are grouped near PV+ entry, while MCU, 32.768-kHz resonator and SWD remain physically separate.
- Preliminary **9-mm PV+** line runs on B.Cu between the two PTH power terminals. This is NOT a certified 20-A design and other PV+/buck local links are still missing.
- A 20-A DC check at target **2-oz copper** remains open. At 70-µm copper, 9-mm and 5-mm traces have about 0.63 mm² and 0.35 mm² cross sections, respectively (before tolerances), and their operating temperature rise, terminal current crowding, via transfer, cooling, and short-circuit conditions are unverified.
- **PV−/GND and MPPT− return trunks are not routed**. Critical low-side insertion makes the route/plane split important. Do not fill GND across the shunt or short the force/sense points.
- Put sufficient **thermal vias beside** the power MOSFET, not arbitrarily through paste areas; select via geometry after 2-oz capabilities and thermal model are known.
- SWD connection to grounded host can bypass the low-side PV measurement: use isolation or disconnect PV/inverter during debugging.

## Remaining layout work / DRC expected to report unfinished routing

1. Verify exact U3 and Q1 pad geometry against manufacturer's drawing; replace draft footprints, rerun footprint-to-pin verification and **review orientation**.
2. Select and verify L1 and C3 MPNs, finalize PV cable terminations and enclosure/strain relief.
3. **True Kelvin traces** from sense pads on BVB to INA228 IN+/IN− through R11/R12/C10; preserve distance from SW node and 20-A copper.
4. Complete current-carrying path: J1 PV− → Q1 Source, Q1 Drain → RSH1 pad2, RSH1 pad1 → J2 MPPT− and J1/J2 PV+ common. Assess filled copper/stackup/vias for 20-A with thermal margin.
5. Close LM5164 input/BST/SW/output loops, place C1/C21/C22 and bypass caps at actual pins; return FB to quiet ground.
6. Route 3.3-V/I²C/GPIO/ADC/SWD and sensor inputs. Add GND reference planes **without bypassing RSH1**, and RF copper keepout on **all copper layers**.
7. Run full KiCad 10 **ERC and DRC with schematic parity**, fix reported violations, and independently review source-to-board pad mappings, creepage/clearance at 60-V PV, RF and 20-A heating.
8. Prototype thermal/switching, measurement noise, RF and environmental validation before board release.

## Run on Linux Mint with KiCad 10 Flatpak

From repository root:

```bash
git pull --ff-only
flatpak run --command=kicad-cli org.kicad.KiCad pcb upgrade hardware/kicad/panellog.kicad_pcb
flatpak run --command=kicad-cli org.kicad.KiCad pcb drc --schematic-parity --severity-all \
  --output panellog-pcb-drc.rpt hardware/kicad/panellog.kicad_pcb
flatpak run --command=kicad-cli org.kicad.KiCad sch erc \
  -o panellog-sch-erc.rpt hardware/kicad/panellog.kicad_sch
```

The current PCB is **intentionally partly unrouted**, so an ERC/DRC warning/error report is expected. Treat it as design feedback rather than hiding violations.

**Release gate: BLOCKED.** No copper, footprint, DRC, assembly or 20-A qualification has been verified on a manufactured PCB.
