# POA optional wired interface — KiCad prototype status (2026-11-09)

## Base and changes

Based on the fetched GitHub `main` snapshot `d8c4a93ed9e72f3e6fa376e7a5113073003457cb` before any changes. The ESP32-C6-MINI-1-N4 symbol and PCB pads identify **GPIO21 = pad 27, GPIO22 = pad 28**; they were unconnected in the baseline. Existing INA237 I2C on GPIO6/GPIO7 is untouched.

The updated main `hardware/kicad/panellog.kicad_sch` contains: U4 P82B715DR (DNP); J8 six solder pads for three twisted pairs; R30/R31 2.2k pull-ups on GPIO21/22; R32/R33 0R direct bypass (fitted); R34/R35 1k optional cable-side pull-ups (DNP); R36 0R supply link (fitted). All new footprints are placed in `hardware/kicad/panellog.kicad_pcb` with dedicated signal net names. The custom pad footprint lives in `hardware/footprints/PanelLog.pretty/POA_Cable_6pad.kicad_mod`.

**Not fabrication-ready:** The new copper nets have NOT been routed, and native KiCad 10 ERC/DRC, zone refill and schematic–board parity have NOT been executed in this environment. The older `review_2026-11-08` reports apply only to the old circuit, not this revision. Do not order a PCB from this state. The footprint placements are a corridor reservation, not an EMC-approved routing. A simple static check found no old F.Cu signal segments inside the bounding areas of J8/U4/R30–R36; this does not check In2, power planes, clearances, vias, and mechanical interferences.

## Cable pinout: PanelLog J8 ⇄ POA J1

| pin | name | pairing |
|---|---|---|
| 1 | POA_VDD_CABLE (3.3 V) | twisted with pin 2 GND |
| 2 | GND | supply return |
| 3 | POA_SDA_CABLE | twisted with pin 4 GND |
| 4 | GND | SDA return |
| 5 | POA_SCL_CABLE | twisted with pin 6 GND |
| 6 | GND | SCL return |

Use 3 m maximum cable with three twisted pairs, UV/outdoor rated. Avoid routing along the 20 A power conductors and parallel to the PV switching loop. Never bond cable shield to PV module frame or protective earth without a system-level grounding assessment. First prototype: shield insulated at remote sensor; optional one-ended termination to **PanelLog local GND** only after an EMI test. Do not allow shield to carry return current. PanelLog GND is tied to the PV module negative return topology (not an isolated SELV signal domain).

## Populate **DIRECT** — default

- R30, R31 = 2.2k to +3V3, not duplicated on the POA board by default.
- R32, R33 = fitted zero-ohm bypass between the MCU Sx/Sy and cable SDA/SCL.
- R34, R35 = DNP.
- U4 = DNP.
- R36 = 0-ohm fitted **prototype only**: it is NOT cable short-circuit protection.
- POA-side R6/R7 = 0R; U2/R8/R9 = DNP.

At 25 kHz, total 2.2k pull-up and 400 pF cable capacitance give a nominal 30–70 % rise of 746 ns; check the actual twisted pair and probe, with INA237 I2C completely independent.

## Populate **BUFFERED** — alternative, not simultaneously with DIRECT

- Remove R32/R33 at PanelLog AND R6/R7 at POA. **Never** populate a direct bypass concurrently with U4/U2.
- Populate matching P82B715 (PanelLog U4 and POA U2); pinout pin2=Lx, 3=Sx, 4=GND, 6=Sy, 7=Ly, 8=VCC. Pins 1/5 no-connect.
- Retain local S-side pull-ups (PanelLog R30/R31 2.2k; POA-side S-pull-ups must be added/verified before buffered operation). Do not power buffered mode without correct S-side pull-ups.
- Populate line-side R34/R35 and POA R8/R9 (1k each side proposed as a test starting point), confirm available sink-current and VOL margins against P82B715 datasheet.
- Maintain 3.3 V at both ends; the P82B715 does not isolate the two domains.

The current POA draft lacks independent S-side pull-up footprints; therefore **buffered mode is a reserved design option, not a qualified assembly variant**. Correct this on the sensor side before prototyping buffered operation.

## EMC / SI routing requirements before release

1. Keep current INA237 true Kelvin pair and its 10 Ω / 100 nF analog input network unchanged; avoid all new vias or digital traces directly alongside this pair.
2. Route GPIO21/22 as 0.2–0.25 mm traces over continuous GND on In1.Cu. Keep the pair together; never cross the 3.3 V switch-node or run along Q1 gate/drain, RSH1 force return, VDC or high-current vias.
3. Prefer digital routing on In2.Cu with continuous In1.Cu reference; drop near U3 breakout and rise near J8. Check return path under each signal and via transitions; use adjacent ground stitching near cable entry, without crossing other net copper.
4. Place cable-side ESD arrays and a short-circuit-limited 3V3 supply near J8 **before fabrication**. They are not yet present on the connected KiCad PCB; see blocking points below.
5. Route and refill all 4 copper layers with KiCad 10. Re-run full native ERC/DRC, all layer/copper clearances, unconnected net and schematic parity checks. Check actual enclosure wall/mounting/cable gland clearance and RF keepout.
6. Verify I²C 25/50/100 kHz rise times, VOL, noise margins and failure handling, including inverter transients; isolate sensor and capture scope traces with differential/isolated measurement as appropriate.
7. No shield connection to frame or PE from the POA board. Assess ESD to each data conductor and 3V3/GND; 3 m cable can pick up substantial common-mode voltage.

### Blocking items for hardware release

**A. Cable protection:** selected low-leakage digital ESD device footprint/MPN and 3.3 V load switch/current limiter or resettable fuse not integrated. Existing R36=0R is a temporary electrical placeholder only.

**B. Routing:** new footprints placed but all new nets unrouted, including the new MCU GPIOs.

**C. Schematic validation:** native KiCad 10 ERC/DRC unavailable in this runtime. A parenthesis/string scan passed, but is not equivalent to ERC or a connectivity check.

**D. Firmware:** component `firmware/components/poa_soft_i2c/` contains an initial software-I2C and ADS1115 reader. It is not built or hardware tested; integration into the application task, storage calibration, Zigbee clusters and watchdog/concurrency are pending. Do not claim a complete ESP-IDF firmware image.

**E. Sourcing:** component MPN/LCSC values reused from documented project BOM; not all stock/MOQs rechecked live. P82B715DR = LCSC C2649394 (DNP). No current complete procurement BOM or order authorization.

## References

- TI P82B715 datasheet https://www.ti.com/lit/ds/symlink/p82b715.pdf
- TI ADS1115 datasheet https://www.ti.com/lit/ds/symlink/ads1115.pdf
- ESP32-C6 datasheet https://documentation.espressif.com/esp32-c6_datasheet_en.html
- Current original PanelLog firmware pin map `firmware/README.md`
