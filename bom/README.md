# Selected components

The current baseline is intentionally small and biased toward parts available from JLCPCB/LCSC where practical.

| Ref/function | MPN | LCSC | Status |
| --- | --- | --- | --- |
| U_MEAS | TI INA228AIDGSR | C2887910 | selected |
| R_SHUNT | Isabellenhütte BVB-M-R0007-1.0, 0.7 mOhm | C5563922 | selected; stock must be checked before order |
| Q_SW | Infineon IPT015N10N5 | C108964 | selected; 100 V, 1.5 mOhm max @10 V |
| U_BUCK | TI LM5164DDAR | C477928 | selected |
| U_MCU | Ebyte E73-2G4M08S1C | project/local | selected, shared platform with poa-sensor |
| T_MODULE | YAGEO Nexensos M222 Pt1000 F0.15 / Class A, 32208572 | external cabled probe | selected sensor element; probe encapsulation required |
| R_RTD_REF | Susumu RG1608N-1472-W-T1, 14.7 kohm 0.05% 10 ppm/K | C1721340 | selected |
| T_INT | TDK NTCG163JF103FT1S or equivalent 10k NTC | JLC/LCSC stocked part | internal MOSFET hotspot monitor |
| Q_GATE | 2N7002 | TBD stocked JLC part | function selected |
| D_GS | 10 V zener, BZT52C10-class | TBD stocked JLC part | function selected |

## Prototype candidates after short-MC4-lead review (2026-10-29)

| Ref | Candidate | LCSC | Qualification status |
| --- | --- | --- | --- |
| C1 input-bank (3 parts total) | TDK CNA6P1X7R2A475KT000A, 4.7 µF, 100 V, X7R, 1210, soft-termination | **C22877898** | Three in parallel proposed to achieve >2.2 µF *effective* at 60 V (TDK bias curve ~−75%); confirm corner cases. Implemented as C1+C21+C22, three 4.7-µF /100-V MLCCs in parallel in the native KiCad schematic; full effective capacitance not yet qualified. |
| D2 gate clamp | JSCJ MMSZ4697, nominal 10 V, SOD-123, low-current MMSZ4697 family test at 50 µA | **C2910058** | Prototype candidate; verify exact manufacturer's hot VZ/leakage over 50 µA to ~1.1 mA. |
| R8 gate pull-up | **47 kΩ**, ≥1206, ≥0.25 W, voltage/temperature derated | TBD LCSC | Implemented 47 kΩ with 1206 footprint; exact resistor MPN not chosen. |
| R9 gate series | **2.2 kΩ**, 0603 | TBD LCSC | Implemented 2.2 kΩ with 0603 footprint; SOA/switching behavior unqualified. |
| D1 input TVS | **DNP**, optional footprint | — | No device fitted unless switching measurements show necessity; PV+ TVS alone does not protect Q1 VDS. |

Source/calculation and user constraints: [2026-10-29 design decisions](../docs/design_decisions_short_pv_leads_2026-10-29.md). Native KiCad 10 **schematic updated**; PCB not created. See [static validation](../hardware/kicad/VALIDATION_2026-10-29.md); native KiCad 10 ERC still pending.

## PCB/footprint release status (2026-10-29)

A [61-part KiCad PCB placement draft](../hardware/kicad/panellog.kicad_pcb) now exists, but **nine project-local review-stage footprint definitions** (TOLL Q1, BVB RSH1, E73 U3, LM5164 DDA U1, two PV pigtail pads, L1 envelope, C3, J3, J4) are **not certified against final manufacturer land patterns**. The standard library pads in this generated PCB also require updating to the installed KiCad-10 footprints. In particular select the 68-µH inductor MPN, cable interface/strain relief and optional C3 before any fabrication. Detailed status: [PCB footprint matrix](../hardware/kicad/PCB_LAYOUT_REV0_DRAFT.md).

## Selection notes

- The 0.7 mOhm BVB is selected over larger shunts because it retains 0 +/-20 ppm/K TCR in the manufacturer table while INA228 resolution is still far more than sufficient.
- IPT015N10N5 is a good low-loss candidate **if** 10 V gate drive is achieved: its 1.5 mOhm maximum RDS(on) is specified at VGS=10 V. The present 220-kOhm gate resistor sources only ~136 uA at 40 V assuming a 10-V clamp; the generic 10-V zener and 2N7002 hot leakage are **not qualified**. Do not claim a guaranteed 10-V gate drive.
- LM5164 now generates 3.3 V directly. The former 5 V + TPS7A20 stage is removed.
- The external Pt1000 is a leaded M222 element built into a weather-protected cabled probe and thermally bonded to the module backsheet.
- INA228 die temperature plus an inexpensive NTC next to QSW provide internal thermal information; no separate precision digital PCB temperature sensor is required initially.

Before BOM freeze, qualify the exact zener/Q2 and the C1 high-voltage MLCC DC-bias characteristics, the LM5164 L1 MPN/hot saturation and exposed-pad footprint, TVS coordination with INA228's 85-V limit, and a provisional 20-A power-path scenario. See [electrical audit](../docs/electrical_audit_2026-10-29.md).

Do not substitute the shunt or current monitor without re-running the root-README error budget.
