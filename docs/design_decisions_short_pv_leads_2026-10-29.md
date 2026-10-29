# PanelLog design decisions after field-installation constraints (2026-10-29)

Status: **reviewed/provisional decisions; schematic and PCB not yet modified or released.** This supplements, and where explicitly stated **supersedes**, `docs/electrical_audit_2026-10-29.md`. All source-specific facts below are linked; calculations and design assumptions are identified as such.

## User-defined installation and risk profile

- One PV module to one MPPT input; no module strings or common galvanic ground.
- About **1–2 m DC leads**, standard **MC4** connections; manual reconnection very rare and **not under load**.
- Preference for **LCSC** sourcing.
- **No excessively conservative surge protection**; moderate, application-specific risk is acceptable.
- Retain **20 A as a provisional current-path/thermal design case** (not a tested or guaranteed current limit).
- Use an **in-stock LCSC 10-V zener** with published characteristics in the real operating-current range.

## 1. Mechanisms of voltage spikes: qualify their origin

A stand-alone PV module's **steady-state** open-circuit terminal voltage is physically capped by its cold `Voc` (up to data-sheet tolerances). Thus a continuously driven >85-V DC voltage is not expected from either *single* specified module at normal temperatures, provided no other source is electrically connected.

**However `Voc` is NOT a bound on transient voltages** across inductive cables or the low-side series MOSFET Q1:

1. **Q1 switching:** the current in the PV/MPPT wiring and the MPPT input capacitor changes quickly. Approximate loop inductance **1–5 µH for short 1–2 m wiring** is an unverified engineering assumption, depending on actual wire separation and routing. `E = ½LI²`: at L=3 µH, I=20 A, energy ≈ **0.6 mJ**. `V=LΔI/Δt`: a 20-A change over 10 µs is ≈ **6 V** at 3 µH; over 1 µs ≈ **60 V**. Those are **illustrative local inductive drops**, not a simulated or measured terminal voltage or an unconditional 60-V addition to `Voc`.
2. **MPPT capacitance and resonance** can produce ring-down. In particular **Q1 drain-source** and the floating MPPT-negative node may experience a spike even while PV+ relative to module PV- remains near `Voc`. D1 (PV+–local PV-) does **not** by itself clamp Q1 VDS or the floating shunt-sense common mode.
3. **Disconnecting MC4 under load** risks DC arcing; assume connectors are handled only in a suitable de-energized state. Standard MC4 is **not** a load-break switch.
4. **External induced surges** (lightning, neighboring AC equipment) are a separate environmental residual risk, not produced by the module's steady-state I-V curve. For the short, local installation there is no justification yet for a complex industrial surge front end.

**Decision:** use adequate, local 100-V-rated high-frequency capacitance on PV+–PV- to damp fast converter input demands; keep D1 footprint **DNP by default**. Add **optional Q1 drain-source RC/snubber footprint if PCB space allows**. Prioritize real scope captures of Q1 `VDS`, PV+`–PV-` and INA common-mode during Q1 switching into the exact installed MPPT. If spikes approach rating, revisit D1 and/or **Q1-specific** damping rather than blindly installing a TVS across PV+.

The INA228 common-mode/VBUS **85 V** and Q1/LM5164 **100 V** limits remain real *instantaneous* device constraints. A TVS must have a **specified clamp voltage at the relevant pulse current** below the most sensitive limit; a nominal 58/60-V TVS does not necessarily clamp below 85 V. Do not present an unfitted D1 as protection.

Sources: [INA228 TI](https://www.ti.com/product/INA228), [LM5164 TI](https://www.ti.com/product/LM5164), [Infineon IPT015N10N5](https://www.infineon.com/part/IPT015N10N5).

## 2. Input C1: concrete LCSC component and DC-bias evaluation

**Chosen prototype candidate (not a hard BOM freeze):**
- **TDK CNA6P1X7R2A475KT000A**, **LCSC C22877898**, 4.7 µF ±10%, 100 V, X7R, 1210, **soft termination, AEC-Q200**, -55…+125 °C.
- [LCSC listing](https://www.lcsc.com/product-detail/C22877898.html), [TDK identification](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CNA6P1X7R2A475K250AE), [TDK characterization graph, 16 June 2021](https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/charasheet/cna6p1x7r2a475k250ae_210616.pdf).
- **Crucial finding from TDK's published DC-bias curve:** around **−70% capacitance at 50 V** and **−75% at 60 V** (approximate graph readings). One nominal 4.7-µF part therefore retains only about **1.4 µF at 50 V** and **1.2 µF at 60 V** at the plotted reference condition! Merely replacing C1 with one 4.7-µF 100-V MLCC is **not** enough to substantiate TI's ≥2.2-µF effective input-capacitance recommendation.
- **Recommendation: 3 × 4.7 µF in parallel at LM5164 VIN/GND** (current C1 footprint must be adapted; add two parallel footprints). At 60 V expect roughly **3.5 µF nominal effective** from the curve. Roughly **2.7 µF after a separate −10% production and −15% temperature worst-case allowance** (heuristic stacking; check combined bias/temperature characterization and aging). This clears 2.2 µF on a conservative prototype basis. Include adjacent 100-nF/100-V C2.
- 100 V versus nominal <50 V cold `Voc` is reasonable for the user-accepted non-conservative protection profile, but **does not prove transient immunity**. The TDK part is a real stocked candidate; availability must be checked again before ordering.
- **C3 10-µF/100-V bulk damping**: keep a footprint with **DNP** until converter input resonance is assessed; low-ESR MLCCs and cable inductance can ring. A suitable ESR/damping network may be helpful, but a generic electrolytic is not mandatory solely from short lead length. No specific C3 MPN selected yet.

Source: [TI LM5164 Rev D](https://www.ti.com/lit/ds/symlink/lm5164.pdf), high-frequency input capacitance and DC-bias guidance; the TDK manufacturer's plot supersedes the previously undocumented generic “4.7-µF should be enough” assumption.

## 3. Gate clamp: specified at 50 µA, LCSC availability

The old **BZT52C10** family nominal voltage is commonly characterized around **5 mA**; with R8=220 kΩ it receives merely (VPV−VZ)/R ≈ **136 µA at 40 V** and **227 µA at 60 V**, assuming VZ=10 V.

**Better diode: MMSZ4697 (10 V low-current Zener), JSCJ LCSC C2910058, SOD-123, ~350 mW, -55…+150 °C, 9.5–10.5 V around the family specified 50-µA test current**; [LCSC product](https://www.lcsc.com/product-detail/C2910058.html). The **MMSZ4697 family** is documented at `IZT = 50 µA` in [Meritek datasheet](https://www.meritekusa.com/wp-content/uploads/2023/05/MMSZ46xx-3b-230501.pdf), and [MCC datasheet](https://datasheet.lcsc.com/lcsc/2009031007_MCC-Micro-Commercial-Components-MCC-MMSZ4687-TP_C779128.pdf). **Important:** these are family/other-manufacturer data; inspect the **exact JSCJ PDF** at PCB freeze and do not assume the family tests establish all JSCJ hot/leakage characteristics or 1-mA clamp voltage.

**Gate-bias revision proposed for the prototype:**
- R8 **47 kΩ** (from 220 kΩ), at least **1206 / ≥0.25 W and adequate operating-voltage/temperature derating**.
- D2 **MMSZ4697** LCSC C2910058.
- R9 **2.2 kΩ** (from 100 Ω), to **slow deliberate Q1 turn-off** and attenuate inductive switching peaks; Q1 Qg ≈169 nC typ @10 V, but actual turn-off interval depends on plateau and Miller charge. Switching losses/SOA still need bench validation.
- R10 **100 kΩ** gate pulldown retained.
- Q2 remains a 2N7002-class low-side pull-down, but choose a manufacturer with characterized **hot IDSS** at least near 125 °C; generic 2N7002 parts may differ significantly. At Q2 VDS ~10 V actual leakage should be measured; 60-V rated IDSS is not an exact value for this operating point.

With `R8 = 47 kΩ`, nominal 10-V clamp current:

| VPV | (VPV−10V)/47k | R8 power estimate |
| ---: | ---: | ---: |
| 20 V | 0.213 mA | 2.13 mW |
| 40 V | 0.638 mA | 19.1 mW |
| 47.5 V | 0.798 mA | 29.9 mW |
| 60 V | 1.064 mA | 53.2 mW |

D2 current spans more than its 50-µA test point; **its guaranteed clamp upper limit under 1 mA and high temperature still needs checking/measuring**, especially against Q1 `|VGS|max = 20 V`. The margin to 20 V is large at a 10-V nominal clamp, but do not mistake the 50-µA characteristic for a full current/temperature VGS guarantee. The steady-state low-VPV behavior and low-sun source loading remain to be measured.

**Fail-ON boundary:** MCU reset/high impedance requests Q1 ON; an MCU GPIO held permanently HIGH or failed shorted Q2 cannot be solved by this passive circuit. Treat **“normally ON under reset/power-loss”** as the requirement, not “guaranteed ON for every MCU hardware failure.” If independent watchdog fail-ON is later required, add a hardware monostable/lease.

Sources: [Infineon Q1](https://www.infineon.com/part/IPT015N10N5), [JSCJ MMSZ4697 at LCSC](https://www.lcsc.com/product-detail/C2910058.html), [Meritek MMSZ4697 family](https://www.meritekusa.com/wp-content/uploads/2023/05/MMSZ46xx-3b-230501.pdf).

## 4. What is settled / what remains to test

Settled for **prototype direction**, no further user choice required:
- 1–2-m MC4 lead setup and rare switching.
- 20-A provisional design case.
- LCSC C22877898 as C1 material, **3 identical parts** proposed.
- LCSC C2910058 MMSZ4697 as D2 candidate; R8 47 kΩ and R9 2.2 kΩ.
- D1 **optional/DNP**, no complex external surge front end by default.

Still for engineering execution, not requiring new user constraints:
- Exact JSCJ MMSZ4697 datasheet and Q2 leakage derating; qualified Q2 LCSC MPN.
- Hot and cold `VGS`, `VDS`, switching edges, `V_{INA-IN±}` and PV+ with MPPT connected, at least one actual EVT800-B and one DS3-S.
- Validate whether 3 × C1 provides sufficient effective capacitance including aging, assembly and combined bias/temperature.
- KiCad 10 ERC, actual footprint and netlist verification, SOA, thermal and PCB validation.
- If measured >85-V on INA228 or >100-V on Q1/LM5164, reconsider corresponding **targeted** damping/clamp (D1 alone cannot protect all stressed nodes).

**Not yet changed:** native schematic, BOM footprints or netlist. Apply the schematic/BOM revisions together after resolving the exact zener/hot Q2 datasheets, then run KiCad 10 ERC.
