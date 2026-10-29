# PanelLog electrical design audit — 2026-10-29 (datasheet review)

**Status: preliminary / NOT released.** This is a source-based audit of the native KiCad 10 schematic on `main`, combined with manufacturer datasheets. The schematic itself, its netlist and its PCB have **not** been validated in KiCad 10; there is no bench/oscilloscope or thermal confirmation. Do not label these calculations “hardware proven”.

## Traceability / sources

Schematic: `hardware/kicad/panellog.kicad_sch` (format 20260306), local symbols: `hardware/symbols/panellog.kicad_sym`.

* [TI LM5164 Rev D, February 2026](https://www.ti.com/lit/ds/symlink/lm5164.pdf), especially §§5, 6.3.9, 7.2.2, equations 13–26.
* [TI INA228 Rev A, May 2022](https://www.ti.com/lit/ds/symlink/ina228.pdf), especially §§5–6, 7.3, 8.1.4.
* [Infineon IPT015N10N5 Rev 2.4](https://www.infineon.com/assets/row/public/documents/24/49/infineon-ipt015n10n5-datasheet-en.pdf).
* [onsemi 2N7002/NDS7002A Rev 11, March 2025](https://www.onsemi.com/pdf/datasheet/nds7002a-d.pdf).
* [Diodes Inc. BZT52C10](https://www.diodes.com/part/view/BZT52C10) (example family, **not** a selected/qualified MPN).
* [Isabellenhütte BVB, issue 18 February 2025](https://www.isabellenhuette.com/hubfs/Files/Data-sheets/BVB.pdf).
* [SOLARWATT Panel vision AM 4.0 black Rev 12, February 2025](https://www.solarwatt.com/canto/download/s6p8qspghh145cii713qp7u50c).
* [DMEGC 370 60HBB-S electrical data, “powered by Taylor” variant](https://www.quesolar.com/wp-content/uploads/2022/05/DM370M6-60HBB-S-powered-by-Taylor.pdf) — **variant may differ from actual nameplate; confirm physical module**.
* [Nordic nRF52840 power-supply modes](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/power.html).

## 1. LM5164: design recalculation

Schematic: U1 = LM5164DDAR, C1 2.2 µF/100 V X7R, C2 100 nF/100 V, C3 10 µF/100 V bulk (candidate), C4 2.2 nF bootstrap, L1 68 µH (no MPN), C5/C6 22 µF/10 V, R1/R2 1 MΩ/200 kΩ, R3 27.4 kΩ, R4/R5 **175 kΩ/100 kΩ**, R6/C8/C9 **150 kΩ/3.3 nF/150 pF**.

### Confirmed arithmetic

* `VOUT = 1.2 V × (1 + 175k/100k) = 3.300 V` nominal; the 1.2-V FB reference has a **1.181–1.218 V** datasheet min/max, so ignoring resistor tolerance: **3.248–3.350 V**. Check the resulting full VDD range against E73 + INA228 and include 0.1% feedback-resistor tolerance.
* `FSW(kHz) ≈ 3.3 × 2500 / 27.4 = 301.1 kHz` in CCM (TI equation 15); at low load the converter intentionally pulse-skips, so 300 kHz is **not** a constant switching frequency.
* `VIN,on ≈ 1.5 × (1 + 1M/200k) = 9.0 V`; `VIN,off ≈ 1.4 × 6 = 8.4 V` (TI equations 13–14), **typical**, not guaranteed thresholds. Rising-threshold range 1.45–1.55 V implies about **8.7–9.3 V** before resistor tolerances; falling 1.35–1.44 V implies **8.1–8.64 V**.
* At VOUT=3.3 V and FSW=301.1 kHz, 50-ns minimum on-time corresponds to `VIN ≈ 3.3/(50 ns × FSW) ≈ 219 V`; this particular limitation does **not** bind at 60 V, although absolute 100-V ratings do.
* For L1=68 µH, using TI equation 18 in CCM:

| VIN | ideal tON | ΔIL p-p | CCM/load boundary (approx. ΔIL/2) |
| ---: | ---: | ---: | ---: |
| 9 V | 1.218 µs | 0.102 A | 51 mA |
| 40 V | 0.274 µs | 0.148 A | 74 mA |
| 47.5 V | 0.231 µs | 0.150 A | 75 mA |
| 60 V | 0.183 µs | 0.152 A | 76 mA |

At a hypothetical 250-mA peak system load, the 60-V CCM inductor peak is ~0.326 A; at 1 A rated load ~1.076 A. TI requires inductor saturation margin above the converter current-limit behavior; the schematic's `Isat >=1.8 A` is only a starting selection rule, **not a validated inductance/Isat-at-temperature part**. Need actual maximum radio/MCU load and selected L1 MPN.

### Type-3 injection: mathematically plausible, not release-frozen

TI Eq. 24 minimum `CA = 10/(FSW × (RFB1 || RFB2)) ≈ 0.522 nF`. Present C8=3.3 nF exceeds this. With `RA×CA = 150k×3.3nF = 495 µs`, Eq. 25 estimates FB-ripple ~**14.0 mV at 9 V**, **20.3 mV at 40 V**, **20.9 mV at 60 V** in CCM. TI recommends a minimum of 12 mV at minimum VIN. R6 150 kΩ therefore fits the simple steady-state equations.

TI Eq. 26: C9=150 pF corresponds to `t_settling = 3×175k×150pF ≈ 78.75 µs`. These figures do **not** prove COT stability under discontinuous/pulse-skipping operation or with real component parasitics. Bench-test wakeup, Zigbee burst loading and 9–60 V line ramps; consider TI simulation.

### Unresolved / release blockers

1. **C1 input MLCC:** TI recommends at least **2.2 µF** high-frequency input capacitance and choosing capacitor voltage rating around **2× worst-case VIN** to account for DC bias. Schematic C1 **2.2 µF nominal / 100 V** is not demonstrated to provide 2.2 µF **effective at 47–60 V** and is below the 120-V voltage-rating guideline at a 60-V target. Check exact capacitance-vs-DC-bias curve and consider higher-rated/larger or parallel capacitors. C2 is supplemental, not a substitute. The 100-V electrolytic C3 needs ESR, ripple, low-temperature and hot-module lifetime verification.
2. **Output caps C5/C6**: verify combined **effective** capacitance at 3.3 V including bias/temperature and loop/load transients; rated 10 V is not automatically a capacitance guarantee. C4 2.2 nF across BST–SW is consistent with TI required range 1.5–2.5 nF.
3. **Thermal and footprint:** verify LM5164 **DDA PowerPAD / exposed pad to GND** (datasheet explicitly instructs grounding the EP) and package-to-footprint mapping. No release-qualified U1 footprint yet. Hot outdoor duty plus buck thermal rise requires assessment.
4. **All PV front end surge handling** unresolved; a 100-V-rated buck does **not** protect an 85-V INA228.

## 2. Fail-ON gate control: not yet robustly proven

Schematic: R8 220 kΩ from PV+ to `QSW_GATE_BIAS`; D2 nominal 10-V zener from that node to PV-; R9 100 Ω from bias node to Q1 gate; Q2 2N7002 actively pulls bias node to PV-; R10 100 kΩ ensures Q2 gate LOW for MCU high-Z/reset. Q1 is IPT015N10N5. This is **reset/high-Z => intended ON**, not an independently guaranteed hardware fail-ON for all fault cases.

With D2 hypothetically conducting at exactly 10 V, `I_R8=(VPV−10 V)/220k`:

| PV voltage | maximum available gate-bias current with 10-V clamp |
| ---: | ---: |
| 20 V | 45 µA |
| 40 V | 136 µA |
| 47.5 V | 170 µA |
| 60 V | 227 µA |

**Critical:** Standard BZT52C10 examples specify nominal 10 V at **5 mA**, which is >20× the available current even at 60 V. With 220 kΩ the zener knee/gate voltage **cannot be inferred from the nominal 10 V**. Q1's stated max `RDS(on)=1.5 mΩ` is conditional on `VGS=10 V` (and is not guaranteed merely because a nominal 10-V diode exists).

**Hot leakage:** Example 2N7002 datasheet gives `IDSS ≤ 0.5 mA` at 125 °C and `VDS=60 V` (not the actual ~10-V drain voltage). This does not establish leakage at 10 V, but demonstrates that **an unscreened generic 2N7002 is not guaranteed to leak less than the available 45–227 µA over all hot conditions**. Gate resistor and zener leakage must likewise be included.

**Startup and fault cases:** before the MCU is powered (buck UVLO ~9 V), Q1 receives only a PV-dependent passive gate voltage. At low PV voltage the nominal 10-V enhancement condition is impossible; analyze linear-region dissipation if the MPPT drags PV voltage below 9 V while current remains available. MCU GPIO stuck HIGH, Q2 shorted, zener shorted or gate short to ground can hold the module OFF indefinitely. A firmware lease cannot correct an MCU hang with GPIO still HIGH. If stronger reset-independent availability is essential, design an **independent hardware timeout/watchdog** or explicitly narrow the fail-ON specification.

Q1 100-V VDS, 10-V-gate `RDS(on)` and large gate charge (~169 nC typ) remain suitable for slow switching; test the turn-on/turn-off transition into real MPPT input capacitance and module source. Check positive/negative VGS excursions, Miller injection, Q2 hot leakage, D2 temperature and Q1 SOA. Do **not** use PWM.

**Recommendation:** leave R8/D2/part numbers **provisional**. At least characterize `VGS(VPV,T)` with Q2 OFF and Q2 ON, Q1 `VDS` and temperature, from dawn through 60 V, including Q2 hot leakage, regulator brownout and a GPIO-stuck-high fault. Specify exact 2N7002 and diode MPN only after this.

## 3. Input envelope and transient coordination

Assume one PV module per sensor (never series string). Nominal cold open circuit estimates at **cell T = −25 °C**, linear coefficient extrapolation:

| Module/datasheet variant | Voc STC | βVoc | Voc nominal at −25 °C |
| --- | ---: | ---: | ---: |
| DMEGC DM370M6-60HBB-S (verify physical junction-box variant) | 41.96 V | −0.265 %/K | 47.52 V |
| Solarwatt Panel vision AM 4.0 black 400 W Rev 12 | 37.1 V | −0.25 %/K | 41.74 V |

Solarwatt Rev 12 lists **±10% Voc measurement tolerance**: the 41.74 V estimate becomes ~**45.91 V** with a deliberately conservative +10% multiplier. This does not account for every external transient. DMEGC source above is labelled *powered by Taylor*; check that real modules do not use a different revision/junction-box architecture. **Physical nameplates and installed conditions govern.**

Protection coordination is more demanding than choosing a TVS rated between 60 V and 100 V:

* TVS reverse standoff must stay above the **worst-case legitimate cold Voc** including tolerance.
* TVS clamping **under the defined surge waveform and source impedance** must protect **INA228 VBUS and IN± ≤ 85 V** as well as LM5164/Q1 **≤ 100 V**; note that an ordinary “60-V” TVS can clamp above 85 V at its stated surge current.
* Cables, MPPT-side capacitors and opening Q1 can create ringing, differentials and ground bounce; analyze positive **and negative** transients plus the Q1 OFF state where MPPT- may float.
* R13=10 Ω and C11=10 nF at VBUS are **filters, not validated clamps**. Shunt 10-Ω sense resistors provide limited input-event damping, not system surge protection.
* D1 is **DNP** in the schematic and is **not a fitted protection device**. Select concrete TVS and/or coordinated secondary protection only after an agreed transient requirement, with energy and thermal verification. Confirm connector polarity/misconnection risks and service disconnection procedures.

**Release status: protection NOT frozen.**

## 4. INA228 measurement chain

Native connectivity: RSH1 0.7-mΩ BVB on the return, MPPT- → shunt → Q1 drain → Q1 source/PV-; U2 `IN+` through R11 10 Ω from MPPT side and `IN-` through R12 10 Ω from Q1 side, C10 100 nF differential, U2 VBUS from PV+ via R13=10 Ω and C11=10 nF to GND. INA228 VS=3.3 V. INA A1/A0=GND means I²C **7-bit address 0x40**.

* `VSHUNT(15 A) = 10.5 mV`, `VSHUNT(20 A) = 14.0 mV`. ADCRANGE=1 ±40.96 mV is adequate (idealized ±58.5 A input range at 0.7 mΩ, ignoring protection and power path). INA228 VSHUNT LSB=78.125 nV, equivalent to **0.112 mA/LSB**.
* R11/R12 with differential C10 gives an idealized `fc ≈ 1/[2π×(10+10)Ω×100nF] ≈ 79.6 kHz`. This matches TI's 0.1–1 µF recommended filter capacitor range and ≤100-Ω series resistors. Check analog netlist, impedance effects and physical Kelvin routing. **Do not assign any confidence to the schematic-only “Kelvin” claim until the four-terminal PCB footprint and routing are checked.**
* INA228 analog input differential absolute limit **±40 V**, common-mode/VBUS **−0.3 to 85 V**; these limits apply with Q1 OFF/floating MPPT return as well as ON. TI confirms common-mode input and device supply sequencing are independent, within ratings.
* VBUS R13/C11 ideal `fc ≈ 1.59 MHz` and does **not** provide appreciable rejection at the 301-kHz converter frequency by itself; input PV decoupling and PCB separation remain necessary. Evaluate increasing filter time constant if test data show VBUS ripple bias/aliasing.
* Set `ADCRANGE=1`, conversion times/averaging, `SHUNT_CAL`, and optional diagnostics in firmware explicitly **after each power-up**; INA reset defaults use larger ±163.84-mV range. Use calibrated raw voltage/current and independent stable timebase for energy.
* Current error budget in root README remains **a calibrated model, not a system guarantee**; review temperature gradients, connector thermoelectric voltages, shunt drift, calibrated reference uncertainty, and linearity at lower currents. INA die temp is **not** shunt temperature.
* Zero-current measurement during Q1 OFF requires validating actual zero current plus common-mode stability; do not accept an arbitrary floating-input reading as an offset.
* Bus measurement from PV+ relative to module PV- corresponds to **module terminal voltage**; the inverter sees a small lower DC voltage because PanelLog shunt/Q1 insertion losses are intentionally included in the system efficiency calculation.
* The external Pt1000 J3 has direct exposure to an outdoor cable: add **ESD/surge, broken-wire/short-circuit detection**, and verify high-impedance ADC/Pt1000 accuracy. Present 14.7-kΩ excitation at 3.3 V and 1-kΩ sensor yields about **0.210 mA**; the resulting ~0.210-V node must be verified against SAADC gain, acquisition time and oversampling for the ±0.5 °C target.

## 5. Current/thermal and module limits

Solarwatt Rev 12 specifies Isc 13.9 A at STC, **15.3 A at 10%** and **16.7 A at 20% bifacial gain**, and lists **±10% current measurement tolerance**. A conservative combination 16.7×1.10=**18.37 A** (not a probabilistic simultaneous-event prediction) is already above the documented 15-A design target. High-irradiance transients further require consideration.

**Decision needed before footprints/routing:** choose a new provisional **20-A current-path design-check case** for copper, connectors, hot RDS(on) and switching, while the minimum-guaranteed continuous current rating remains open pending actual modules and environment. This is *not* a claim of 20-A field qualification.

At 20 A, nominal 25°C `Pshunt = I² × 0.7mΩ = 0.280 W`; `Pmos = I² × 1.5mΩ = 0.600 W`; combined **0.880 W**. With an illustrative doubled hot Q1 RDS(on) the combined figure becomes **1.48 W**, excluding cables/copper/connectors and switching transients. BVB-M-R0007 data sheet states 8 W at 70°C and 4 W above 100°C under its conditions; high-current capacity alone is **not** PCB thermal approval. RF mounting and enclosure temperature remain release blockers.

## 6. Release blockers / acceptance tests (ordered)

| Priority | Blocker | Evidence required |
| --- | --- | --- |
| P0 | Gate bias at 220k / zener µA knee + Q2 hot leakage | Manufacturer part-specific curves plus bench VGS/temperature/brownout/MPPT tests |
| P0 | PV input transient and coordinated 85-V INA / 100-V power components | Define surge/negative spike profile; select and verify clamping and voltage limits |
| P0 | 15-A path inadequate as blanket bound | Confirm actual Solarwatt/DMEGC nameplates, bifacial conditions, choose 20-A or higher case |
| P0 | No native KiCad 10 ERC / netlist/pin-to-pad validation | Open/save project, ERC, export netlist, review all symbol/footprint pad mappings |
| P1 | C1 actual capacitance and 100-V rating vs TI guidance | Qualified MLCC DC-bias curve, VIN envelope, input ripple, placement |
| P1 | LM5164 L1 MPn, hot Isat, output capacitance, regulator thermal | Concrete hot-rated MPNs, calculation and bench captures 9–60 V + RF TX bursts |
| P1 | Q1 SOA in turn-off/turn-on and low-gate-voltage region | Hot module + MPPT dynamic test; VDS, ID, VGS, thermal |
| P1 | INA228 measurement chain accuracy and floating sense pins | Kelvin pad routing, analog filtering and transient tests, calibration at ≥2 temperatures |
| P1 | Off-board Pt1000 + PV cable ESD / water protection | Probe/connector protection and wet/fault tests |
| P1 | Actual 3.3-V buck footprint/EP, package mechanics | Verified DDA package landpattern with grounded exposed pad |

**Decision:** do not assign a final TVS, zener, 2N7002, C1/C3 or L1 MPN from the present schematic alone. Keep the native schematic unchanged until values and pin/footprints are justified. This document records *audited findings*, not an automatic PCB release.
