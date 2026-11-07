# PanelLog

Current measurement: **INA237 + C481535, 1 mΩ four-terminal shunt**. [Revision and verification](docs/current_sensor_2026-11-07.md).

[C6 revision and qualification status](docs/c6_cost_revision_2026-11-06.md). ESP32-C6-MINI-1 manufacturer model included; external 32 kHz crystal removed.

[Kradex Z74JH ABS enclosure and 118 × 90 mm PCB](docs/enclosure_kradex_z74.md)

Per-module PV DC logger and curtailment node for BatteryFlex.

PanelLog is installed **inline with one PV module**. Each node measures module voltage, module current, DC power/energy and module backsheet temperature. It can also disconnect that module from its inverter/MPPT input for slow BatteryFlex curtailment. The node is powered directly from the PV module and communicates wirelessly over Zigbee.

Plane-of-array irradiance measurement is deliberately a separate project: [poa-sensor](https://github.com/feliksdd/poa-sensor). This separation lets PanelLog sit electrically and mechanically where the DC wiring is shortest (for example shaded behind the module on the mounting rail), while the battery-powered POA sensor can be placed at the optically best, unshaded point in the same plane as the modules.

## System architecture

One PanelLog node is used per module. Different MPPT inputs are never tied together by the measurement electronics.

```text
PV+ IN ---------------------------------------------------- PV+ OUT / MPPT+
   |                         |
   |                         +--> INA237 VBUS
   +--> LM5163 (direct 3.3 V) --> MCU / INA237 / Zigbee

MPPT- / PV- OUT --> 1 mOhm 4-wire shunt --> D  QSW  S --> PV- IN / local GND
                     |              |
                   IN+/IN-        active-low OFF control

external Pt1000 probe ------------------------------> MCU ADC
```

The normal PV return current flows from MPPT- through the shunt and QSW back to PV-. QSW is a **single low-side N-channel MOSFET**. Reverse current from the inverter toward the module is not an application requirement, so a back-to-back switch is intentionally not used.

The local electronics ground is the module-side PV-. Communication is wireless, so normal operation creates no galvanic connection between different modules, MPPTs or BatteryFlex.

## Electrical design envelope

Initial design envelope for one node:

- module operating voltage: nominally about 30...45 V
- PCB design target: **0...60 V continuous**
- historical current-measurement target: **0...15 A**; **not a released power-path maximum**. Solarwatt bifacial Isc can exceed it. Audit now requires a provisional **20-A current-path check** (not a qualified continuous-current rating).
- power-switch semiconductor rating: **100 V**
- INA237 bus/common-mode limit: **85 V**
- DC/DC input rating: **100 V**
- ambient/board environment: outdoor, behind a PV module; thermal validation is mandatory

The 60 V design target is not a substitute for the final cold-`Voc` check. Before PCB release, the worst-case open-circuit voltage of **every actual module type** must be calculated at the minimum site temperature and checked against INA237, MOSFET, TVS and DC/DC limits with transient margin.

## Selected components

| Function | Selected part | Key reason | Sourcing |
| --- | --- | --- | --- |
| Current / bus-voltage monitor | TI **INA237AIDGSR** | 16-bit, ±40.96 mV range, ±50 µV max offset, ±0.3% max gain error, 85 V | LCSC **C2864837** |
| Current shunt | Milliohm **HOVB4026-5W-1mR-1%** | 1 mΩ, four terminals, ±1%, ±50 ppm/K, 5 W | LCSC **C481535** |
| PV switch | Infineon **IPT015N10N5** | 100 V OptiMOS 5, max 1.5 mΩ at VGS=10 V; TOLL/HSOF-8 gives low loss and good thermal margin | LCSC **C108964** |
| PV-to-3.3-V buck | TI **LM5163DDAR** | 6...100 V input, synchronous 500 mA buck, 10.5 µA no-load input IQ; direct 3.3 V avoids a second regulator | LCSC **C2873264** |
| Radio / MCU | Espressif **ESP32-C6-MINI-1-N4** | ESP32-C6, 4 MB flash, Wi-Fi / BLE / IEEE 802.15.4; firmware port required | project-local footprint |
| External module-temperature element | YAGEO Nexensos **M222 Pt1000 F0.15 / Class A**, order 32208572 | leaded Pt1000, DIN EN 60751, intended for a cabled probe bonded to the module backsheet | external probe assembly |
| Internal hotspot sensor | TDK **NTCG163JF103FT1S** or equivalent 10 kΩ NTC | cheap local MOSFET/PCB thermal protection; precision is not required | PCB SMD |
| RTD reference resistor | Susumu **RG1608N-1472-W-T1** | 14.7 kΩ, ±0.05%, ±10 ppm/K | LCSC **C1721340** |
| Gate pull-down switch | **2N7002** | simple MCU-controlled open-drain pull-down | generic/JLC part |
| Gate clamp | **10 V zener**, e.g. BZT52C10-class | limits QSW VGS for passive fail-ON bias | select stocked JLC part at schematic release |

Primary data sheets:

- INA237: https://www.ti.com/lit/ds/symlink/ina237.pdf
- HoVB: https://www.lcsc.com/datasheet/C481535.pdf
- IPT015N10N5: https://www.infineon.com/dgdl/Infineon-IPT015N10N5-DataSheet-v02_04-EN.pdf
- LM5163: https://www.ti.com/lit/ds/symlink/lm5163.pdf
- YAGEO Nexensos M222: https://www.heraeus.com/media/media/hne/datasheets/m_sensors/en_10/m_222_e.pdf

### 1 mΩ four-terminal shunt

C481535 and INA237 replace BVB 0.7 mΩ and INA228 in the 2026-11-07 revision.
At 12 A the shunt produces 12 mV and dissipates 144 mW; at the unchanged
15 A design limit it produces 15 mV and dissipates 225 mW. The 5 W rating is
subject to the manufacturer's thermal derating and is not a board current rating.
At 20 A (comparison only, not a new board rating) dissipation is 400 mW.

ADCRANGE=1 gives ±40.96 A nominal electrical full scale and 1.25 mA per raw
shunt ADC LSB. This is quantization, not guaranteed measurement accuracy.
C481535 is specified at ±50 ppm/K in the exact 1 mΩ datasheet; the 0.5 mΩ
variant's ±100 ppm/K specification does not apply. No BVB thermal-resistance
or self-heating estimate is transferred to HoVB.

## Low-side measurement rationale

The INA237 supports both high-side and low-side current sensing. PanelLog deliberately uses low-side sensing because:

- QSW is already a low-side N-MOSFET.
- QSW source can be tied directly to local PV-/MCU ground.
- no high-side gate driver is required.
- INA237 accuracy does not depend on using the shunt high-side.
- the independent VBUS input still measures module voltage directly at PV+ up to 85 V.
- there is no wired inter-node communication that would normally make a low-side ground shift troublesome.

The current path is ordered as:

```text
MPPT- --> shunt --> QSW drain --> QSW source --> PV- / local GND
```

This keeps QSW source at the electronics reference potential. INA237 `IN+` is connected to the MPPT side of the shunt and `IN-` to the MOSFET side.

A grounded USB/UART programmer can create an unintended current path around the low-side measurement. Debugging an installed node therefore requires an **isolated debugger / isolated bench setup**, or the PV circuit must be disconnected from the inverter.

## MOSFET switch and loss

IPT015N10N5 is specified to 100 V and is a better fit than the earlier BSC034N10LS5 because PanelLog already provides an approximately 10 V passive gate bias. Logic-level operation is therefore unnecessary. IPT015N10N5 specifies maximum RDS(on) = 1.5 mΩ at VGS=10 V and 2.0 mΩ at VGS=6 V.

Using the 1.5 mΩ / 10 V maximum at 25 °C:

```text
P_QSW(12 A) = 12^2 * 1.5 mOhm = 0.216 W
P_QSW(15 A) = 15^2 * 1.5 mOhm = 0.338 W
```

Shunt + MOSFET at 12 A:

```text
Rpath = 1.0 + 1.5 = 2.5 mOhm
Vdrop = 30.0 mV
Ploss = 0.360 W
```

At 15 A:

```text
Vdrop = 37.5 mV
Ploss = 0.563 W
```

RDS(on) still rises with junction temperature. Until the first hot-module prototype is measured, size the PCB thermal path for roughly **2x the 25 °C MOSFET resistance** as a conservative engineering allowance; at 15 A that gives about 0.90 W for shunt + MOSFET before connector/copper losses. The TOLL/HSOF-8 footprint is larger than SuperSO8, but that is beneficial here because switching is rare and conduction/thermal performance dominate gate charge and footprint.

### Gate behavior / fail state

The intended switch is **normally ON** and actively pulled OFF:

- QSW gate receives a passive bias from PV+.
- a gate-source zener is intended to limit VGS toward nominally 10 V; **its actual voltage at the available 45–227 µA must be validated**, rather than inferred from a mA-rated zener specification.
- a high-value series resistor limits clamp current.
- a small 2N7002-class MOSFET pulls QSW gate to PV- when the MCU commands OFF.
- the 2N7002 gate has a hardware pull-down, so MCU reset/high-Z **intends** to release QSW back to ON, provided the passive bias and leakage allow sufficient gate drive.

Unlike a gate bias that depends on the 3.3-V rail, the passive PV-fed bias is available without the MCU or buck. This is **not a guarantee for an arbitrary MCU hang or component failure**: a stuck-HIGH switch-off GPIO, a shorted pull-down transistor, or high-temperature leakage can still hold QSW OFF. The 220-kΩ resistor and nominal 10-V zener are provisional; refer to the [detailed electrical audit](docs/electrical_audit_2026-10-29.md) before freezing them.

The switch is an **operational curtailment actuator, not a safety isolator or maintenance disconnect**.

## Power supply

The sensor supply is connected directly across module PV+ / PV- **before QSW**, so the logger stays alive while its module is curtailed.

Baseline:

```text
PV 0...60 V --> LM5163 --> 3.3 V --> MCU / INA237 / sensors
```

A switching regulator is strongly preferred over a high-voltage linear regulator: at 40 V input a linear regulator would dissipate about 0.37 W already at only 10 mA average load, and about 0.73 W during a 20 mA load interval. That is unnecessary heat behind the PV module. A resistor/zener supply is also unsuitable because the radio load is strongly dynamic.

The former 5 V + LDO architecture is therefore removed. INA237 accepts 2.7...5.5 V and the ESP32-C6 module operates from the 3.3 V rail, so a second regulator does not buy useful accuracy. Use normal local decoupling at INA237; add an RC/ferrite only if prototype EMI testing shows a need.

LM5163 is rated 6...100 V and has 10.5 µA no-load input quiescent current. A preliminary direct-3.3-V operating point is:

- VOUT = 3.3 V
- nominal FSW = 300 kHz
- `RRON ~= 3.3 V * 2500 / 300 kHz = 27.5 kΩ` -> start with **27.4 kΩ, 1%**
- feedback divider ratio `Rtop/Rbottom = 1.74`; the KiCad 10 schematic uses **174 kΩ / 100 kΩ** for about 3.288 V nominal
- input UVLO target about 9.0 V on / 8.4 V off
- using TI's UVLO equations, **1.0 MΩ / 200 kΩ** remains the initial UVLO network

The inductor/ripple-injection network and input transient suppression are **not release-frozen yet**. They must be finalized from the actual maximum load, layout and cold-`Voc`/surge envelope using the current LM5163 Rev. D design procedure. The initial PCB should reserve generous input-decoupling and TVS area.

## Temperature channels

### External PV-module temperature

The module-temperature sensor is **not a PCB SMD component**. It is a cabled Pt1000 probe bonded to the PV-module backsheet near a representative cell area.

Baseline sensor element: YAGEO Nexensos **M222 Pt1000, class F0.15 / Class A, order 32208572**:

- DIN EN 60751 / IEC platinum characteristic, 3850 ppm/K
- class F0.15 (A), valid -50...300 °C
- 2.3 x 2.1 x about 0.9 mm ceramic sensor body with 10 mm leads
- recommended Pt1000 measuring current 0.1...0.3 mA
- the bare element itself is for dry environments, so the PanelLog probe must encapsulate it and provide cable strain relief/weather protection

Use a fixed short cable and calibrate **sensor + cable + analog channel as one probe**. For a roughly 0.5...1 m cable, a 2-wire Pt1000 is adequate for the target because Pt1000 sensitivity is about 3.85 Ω/K and the cable resistance is both small and removed by the per-probe calibration. If later cable lengths become several metres, move to a true 4-wire probe/measurement rather than compensating nominal cable resistance in software.

A 14.7 kΩ ±0.05%, ±10 ppm/K reference resistor keeps excitation near 0.2 mA. Excitation is continuous in this hardware revision. The previous ±0.5 °C system target is not a verified C6 specification: ADC calibration, nonlinearity and sensor mounting require a new temperature error budget. R20/R24 divide the rail by two; firmware must reconstruct Vrail = 2 × VCC_MON_ADC after settling.

Mechanically, use a thin thermally conductive electrically insulating adhesive layer and a small protective aluminium/polyimide patch; validate the complete assembly against a reference sensor. Commercial PV backsheet sensors use the same general approach: a Pt1000 element in a small bonded aluminium body.

### Internal temperatures

No extra precision digital temperature IC is required initially:

1. **INA237 die temperature** is already available digitally and is specified to ±1 °C at 25 °C. Use it for measurement-chain temperature logging and for correlation with the shunt during temperature calibration.
2. Add one cheap **10 kΩ SMD NTC next to QSW** and read it with the ESP32-C6 ADC. This is a hotspot / thermal-protection channel, not a precision ambient sensor. It is more useful than placing a precision sensor elsewhere on the PCB because QSW is the dominant controllable heat source.

If prototype measurements later show that true enclosure ambient temperature is needed independently of shunt and MOSFET temperature, TMP117 is a suitable optional I2C part (up to ±0.1 °C around room temperature), but it is not justified for revision 0.

## DC measurement error budget

The old INA228/BVB numerical budgets are superseded. INA237 maximum initial
shunt offset is ±50 µV (±50 mA at 1 mΩ), gain error ±0.3%, plus shunt ±1%.
Before calibration, the dominant linear current-error estimate is therefore
±(1.3% of reading + 50 mA), excluding noise, INL and board effects.

Per-unit zero and gain calibration are required. At a 50 K temperature change,
50 ppm/K shunt TCR and 50 ppm/K INA gain drift contribute 0.25% each;
0.02 µV/K offset drift contributes another 1 mA. Adding a 0.05% calibration
reference allocation gives a partial budget of 0.55% of reading + 1 mA
(0.65% at 1 A, 0.56% at 10 A). This is NOT a complete guaranteed accuracy:
quantization/noise, thermal EMFs, aging, thermal gradients and calibration
residuals still require measurement. The shunt's TCR test uses room temperature
and 85 °C; validate the actual outdoor range rather than extrapolating blindly.

Development target: approximately 1% current accuracy for I >= 1 A after
calibration over a characterized temperature range. Voltage/power accuracy must
be requalified for INA237; previous <=0.4%/0.3% DC-power claims no longer apply.
Use two-point VBUS calibration and compute power from calibrated U and I.

## Calibration strategy

Every PanelLog node gets a versioned calibration record stored in nonvolatile memory.

### Factory / bench calibration

1. **Current zero**
   - QSW OFF, source/module voltage present.
   - Verify no external current path.
   - Average a long INA237 conversion sequence.
   - Store zero offset and INA die temperature.

2. **Current gain**
   - Pass a traceable current preferably in the **8...12 A** range through the complete assembled power path.
   - Reference current uncertainty target: <=0.05%.
   - Determine one combined current scale factor; this absorbs initial shunt tolerance and INA237 gain error.

3. **Voltage offset and gain**
   - apply two traceable, non-zero module-input voltages, nominally one around **12...15 V** and one around **40...50 V**.
   - solve the affine correction `U_cal = a * U_raw + b`; this determines gain and offset simultaneously while PanelLog remains powered from its normal PV input.
   - Reference-voltage uncertainty target: <=0.05% at both points.
   - A separate calibration/service power input is therefore not required.

4. **Pt1000**
   - minimum one-point calibration of the assembled probe/cable near room temperature.
   - use two temperature points if absolute module-temperature accuracy proves important.

5. **Two-temperature electrical calibration — required for the high-accuracy outdoor target**
   - repeat the current-gain point with the assembled board stabilized near about 20 °C and 60 °C.
   - fit one effective current-gain tempco in ppm/K.
   - validate at an additional temperature outside those two points if the intended outdoor shunt temperature range extends beyond 20...60 °C.
   - apply the measured signed temperature correction in the MCU: INA237 has no INA228-style shunt temperature compensation, and INA die temperature is not necessarily shunt temperature.

Calibration record fields should include at least serial number, hardware revision, calibration format/version, UTC date, current gain, current zero, voltage gain, voltage zero, optional gain tempco, Pt1000 correction, reference-equipment ID/uncertainty and CRC.

### Runtime calibration

- At boot / sunrise QSW is **passively ON** until the MCU actively asserts `SWITCH_OFF`; firmware cannot guarantee OFF before it starts. Once running, firmware may request a brief OFF calibration interval if the operating strategy permits, verify the zero-current condition and then release QSW.
- Whenever BatteryFlex intentionally curtails the module, use the OFF interval to refresh zero offset.
- Record INA237 die temperature with every calibration/measurement batch.
- Apply the stored effective temperature coefficient only after prototype measurements establish the relation between INA temperature and actual shunt temperature.
- Never infer a new gain calibration from normal PV operation without an independent current reference.

### Energy

INA237 has no energy/charge accumulators. Integrate calibrated U*I and current
in the MCU using monotonic sample timestamps. Flag missing/stale intervals;
do not integrate a held last value across resets or communication gaps. The
register map and 16-bit measurement decoding differ from INA228.

See [current-sensor revision](docs/current_sensor_2026-11-07.md) and
[firmware requirements](firmware/README.md).

## Curtailment behavior

Curtailment is deliberately slow and discrete:

- module ON/OFF only; **no PWM**
- hysteresis and minimum dwell time
- re-evaluate PV/battery state after every switching action and MPPT settling interval
- OFF is issued as a **lease**; BatteryFlex must renew the lease
- expired lease returns the module to ON
- BMS/storage protection remains independent; PanelLog curtailment is not the only overcharge safeguard

The firmware should expose at minimum:

- module voltage
- module current
- DC power
- accumulated DC energy
- module temperature
- switch requested state
- switch actual/plausibility state
- INA237 die temperature
- 3.3/5 V supply diagnostics where practical
- uptime / reset reason
- Zigbee LQI/RSSI
- calibration revision

## PCB / mechanical constraints

The high-current path is a primary mechanical/electrical design feature, not ordinary signal routing:

- use the manufacturer's true 4-terminal BVB land pattern
- route INA237 IN+/IN- as Kelvin traces directly from the sense terminals; never pick up the voltage from high-current copper
- keep shunt and INA237 close enough for low thermoelectric/EMI error, but characterize their temperature relationship
- use wide, short copper for the MPPT-/shunt/MOSFET/PV- path; **2 oz copper is the initial PCB baseline**
- size copper and thermal vias from actual hot-enclosure testing; no final trace width is frozen yet
- keep the LM5163 switching loop physically away from the shunt/INA237 Kelvin pair
- reserve input-TVS / transient-protection area near the PV cable entry
- use PV-rated pigtails/connectors and strain relief; do not rely on a small generic PCB terminal for the 15 A path
- conformal coating / enclosure materials must tolerate the expected hot-backside temperature and UV/moisture environment

### RF placement

A PV laminate and aluminium rail are poor surroundings for a 2.4 GHz ceramic antenna. Mount the node near a module edge and orient the C6 antenna away from aluminium and the module backsheet as far as practical. Link-margin testing in the final mechanical installation is a release gate; if it is inadequate, change to an external-antenna ESP32-C6 module variant rather than increasing TX power blindly.

## Field-specific component decisions (2026-10-29)

For the actual **1–2 m MC4 single-module installation**, with rare switching, LCSC preferred, and an accepted non-industrial surge risk profile, see [short-lead PV electrical decisions](docs/design_decisions_short_pv_leads_2026-10-29.md). **Current prototype input capacitors:** FH **1210B475K101NT** (LCSC C2840282), **3× 4.7 µF / 100 V**. FH DC-bias and temperature derating must establish aggregate effective capacitance ≥2.2 µF at 60 V; the previous TDK curve is not applicable. Retained low-current **MMSZ4697** zener (JSCJ C2910058), **R8 47 kΩ**, and **R9 2.2 kΩ**. D1 TVS stays **DNP** unless switching tests establish a need for targeted clamping. **Implemented in the native KiCad 10 schematic:** C1/C21/C22 (3× 4.7 µF/100 V), D2 MMSZ4697, R8 47 kΩ, R9 2.2 kΩ, D1 SMB footprint (DNP), and R23/C23 RC snubber footprints (both DNP). See [static net/pin validation](hardware/kicad/VALIDATION_2026-10-29.md). **See current native checks in the C6 revision report; component qualification and production release remain pending.** Continue the provisional **20-A** current-path check.

### PCB review draft — 2026-10-29

The [native KiCad-10-readable PCB placement draft](hardware/kicad/panellog.kicad_pcb) has **61 PCB components, 191 pads, 32 named nets**, and two preliminary power-path copper segments. The [footprint validation matrix and DRC release gates](hardware/kicad/PCB_LAYOUT_REV0_DRAFT.md) explicitly identify unverified packages, missing power-return/Kelvin/RF routing and thermal/EMC/DRC blockers. **This is not a manufacturing release.**

## Current schematic review

The [initial source-structural review](docs/schematic_audit_2026-10-29.md) records the KiCad label/pin check and provisional module data. The [full datasheet-based electrical audit](docs/electrical_audit_2026-10-29.md) recalculates the LM5163 and its ripple network, identifies gate-bias/2N7002 hot-leakage uncertainty, analyzes INA237 and 85-V transient coordination, and sets an **unqualified 20-A current-path check**. Neither review replaces native KiCad 10 ERC, real transient testing or bench/thermal validation.

## Release gates

Before the first fabrication/release:

1. cold-`Voc` calculation for every deployed module type
2. select/freeze TVS and input protection from that voltage/transient envelope
3. complete LM5163 inductor/ripple-injection/input-filter design and simulate/check with TI design procedure
4. thermal simulation/estimate plus hot-module prototype measurement for QSW, shunt, buck and enclosure
5. Kelvin-layout review around BVB + INA237
6. validate current/voltage error budget on at least two temperatures
7. characterize INA237 die temperature versus shunt temperature
8. validate Pt1000 attachment and module-temperature tracking
9. RF range test with the enclosure mounted at the intended position behind a real PV module
10. verify inverter/MPPT behavior during repeated module ON/OFF switching
11. confirm that all externally accessible/debug connections cannot bypass the low-side shunt in normal service
12. confirm JLC/LCSC availability immediately before PCB/BOM release

## Repository layout

Planned:

- `hardware/` - KiCad schematic/PCB, service/calibration pads and project-local libraries
- `bom/` - selected components, sourcing and alternates
- `firmware/` - ESP32-C6/Zigbee firmware requirements
- `docs/` - validation/calibration reports once measured hardware exists
- `manufacturing/` - JLCPCB outputs and assembly notes

The root README is the architecture and measurement-accuracy source of truth until the first schematic revision is committed.

