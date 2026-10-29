# PanelLog

Per-module PV DC logger and curtailment node for BatteryFlex.

PanelLog is installed **inline with one PV module**. Each node measures module voltage, module current, DC power/energy and module backsheet temperature. It can also disconnect that module from its inverter/MPPT input for slow BatteryFlex curtailment. The node is powered directly from the PV module and communicates wirelessly over Zigbee.

Plane-of-array irradiance measurement is deliberately a separate project: [poa-sensor](https://github.com/feliksdd/poa-sensor). This separation lets PanelLog sit electrically and mechanically where the DC wiring is shortest (for example shaded behind the module on the mounting rail), while the battery-powered POA sensor can be placed at the optically best, unshaded point in the same plane as the modules.

## System architecture

One PanelLog node is used per module. Different MPPT inputs are never tied together by the measurement electronics.

```text
PV+ IN ---------------------------------------------------- PV+ OUT / MPPT+
   |                         |
   |                         +--> INA228 VBUS
   +--> LM5164 5 V --> 3.3 V --> MCU / INA228 / Zigbee

MPPT- / PV- OUT --> 0.7 mOhm 4-wire shunt --> D  QSW  S --> PV- IN / local GND
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
- current measurement range: **0...15 A**
- power-switch semiconductor rating: **100 V**
- INA228 bus/common-mode limit: **85 V**
- DC/DC input rating: **100 V**
- ambient/board environment: outdoor, behind a PV module; thermal validation is mandatory

The 60 V design target is not a substitute for the final cold-`Voc` check. Before PCB release, the worst-case open-circuit voltage of **every actual module type** must be calculated at the minimum site temperature and checked against INA228, MOSFET, TVS and DC/DC limits with transient margin.

## Selected components

| Function | Selected part | Key reason | Sourcing |
| --- | --- | --- | --- |
| Current / bus-voltage monitor | TI **INA228AIDGSR** | 20-bit, ±40.96 mV range, ±1 µV max offset, ±0.05% max gain error, 85 V bus/common-mode | LCSC **C2887910** |
| Current shunt | Isabellenhütte **BVB-M-R0007-1.0** | 0.7 mΩ, true 4-terminal, ±20 ppm/K TCR, 8 W | LCSC **C5563922**; stock must be rechecked before ordering |
| PV switch | Infineon **BSC034N10LS5** | 100 V logic-level N-MOSFET, max 4.6 mΩ at VGS=4.5 V | LCSC **C534326** |
| PV-to-5-V buck | TI **LM5164DDAR** | 6...100 V input, synchronous 1 A buck, low no-load IQ | LCSC **C477928** |
| 3.3-V rail | TI **TPS7A2033PDBVR** | 3.3 V / 300 mA, low-IQ LDO | LCSC **C2862740** |
| Radio / MCU | Ebyte **E73-2G4M08S1C** | nRF52840, common platform with poa-sensor, Zigbee-capable | project-local footprint |
| Module-temperature element | Vishay **PTS120601B1K00P100** | Pt1000, IEC 60751, class F0.3, -55...155 °C | external probe assembly |
| RTD reference resistor | Susumu **RG1608N-1472-W-T1** | 14.7 kΩ, ±0.05%, ±10 ppm/K | LCSC **C1721340** |
| Gate pull-down switch | **2N7002** | simple MCU-controlled open-drain pull-down | generic/JLC part |
| Gate clamp | **10 V zener**, e.g. BZT52C10-class | limits QSW VGS for passive fail-ON bias | select stocked JLC part at schematic release |

Primary data sheets:

- INA228: https://www.ti.com/lit/ds/symlink/ina228.pdf
- BVB: https://www.isabellenhuette.com/hubfs/Files/Data-sheets/BVB.pdf
- BSC034N10LS5: https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsc034n10ls5-datasheet-en.pdf
- LM5164: https://www.ti.com/lit/ds/symlink/lm5164.pdf
- TPS7A20: https://www.ti.com/lit/ds/symlink/tps7a20.pdf
- PTS series: https://www.vishay.com/docs/28762/ptsserie.pdf

### Why 0.7 mΩ rather than 2 mΩ

The INA228 has enough resolution that a large shunt voltage is unnecessary. The BVB 0.7 mΩ variant combines a useful signal with a **0 ±20 ppm/K** specified TCR; the 1 mΩ and 2 mΩ BVB variants are specified at 0 ±50 ppm/K. For this application the lower TCR matters more than gaining a few millivolts of signal.

At 12 A:

```text
Vshunt = 12 A * 0.0007 ohm = 8.4 mV
Pshunt = 12^2 * 0.0007 ohm = 100.8 mW
```

At the 15 A design limit:

```text
Vshunt = 10.5 mV
Pshunt = 157.5 mW
```

The BVB-M-R0007 has an internal thermal resistance of about 12 K/W. Shunt self-heating due only to the measured current is therefore approximately 1.2 K at 12 A and 1.9 K at 15 A. The corresponding resistance change at 20 ppm/K is only about 0.0024% and 0.0038%, respectively.

With INA228 `ADCRANGE=1`, one shunt-voltage LSB is 78.125 nV:

```text
I_LSB = 78.125 nV / 0.7 mOhm = 0.112 mA
```

Therefore the 0.7 mΩ shunt does not create a useful-resolution problem.

## Low-side measurement rationale

The INA228 supports both high-side and low-side current sensing. PanelLog deliberately uses low-side sensing because:

- QSW is already a low-side N-MOSFET.
- QSW source can be tied directly to local PV-/MCU ground.
- no high-side gate driver is required.
- INA228 accuracy does not depend on using the shunt high-side.
- the independent VBUS input still measures module voltage directly at PV+ up to 85 V.
- there is no wired inter-node communication that would normally make a low-side ground shift troublesome.

The current path is ordered as:

```text
MPPT- --> shunt --> QSW drain --> QSW source --> PV- / local GND
```

This keeps QSW source at the electronics reference potential. INA228 `IN+` is connected to the MPPT side of the shunt and `IN-` to the MOSFET side.

A grounded USB/SWD debugger can create an unintended current path around the low-side measurement. Debugging an installed node therefore requires an **isolated debugger / isolated bench setup**, or the PV circuit must be disconnected from the inverter.

## MOSFET switch and loss

BSC034N10LS5 is specified to 100 V. Its maximum RDS(on) is 3.4 mΩ at 10 V gate drive and 4.6 mΩ at 4.5 V.

Using the conservative 4.6 mΩ 25 °C limit:

```text
P_QSW(12 A) = 12^2 * 4.6 mOhm = 0.662 W
P_QSW(15 A) = 15^2 * 4.6 mOhm = 1.035 W
```

The MOSFET resistance rises with junction temperature, so the PCB must be thermally designed and tested for substantially more than the 25 °C values. A **1.5...2 W thermal design allowance** is the initial engineering target until enclosure and hot-module measurements exist.

Shunt + MOSFET at 12 A, using the 25 °C maximum MOSFET value:

```text
Rpath = 0.7 + 4.6 = 5.3 mOhm
Vdrop = 63.6 mV
Ploss = 0.763 W
```

At 15 A:

```text
Vdrop = 79.5 mV
Ploss = 1.19 W
```

These values exclude connector, cable and PCB-copper losses and the temperature increase of RDS(on).

### Gate behavior / fail state

The intended switch is **normally ON** and actively pulled OFF:

- QSW gate receives a passive bias from PV+.
- a gate-source zener clamps VGS to about 10 V.
- a high-value series resistor limits clamp current.
- a small 2N7002-class MOSFET pulls QSW gate to PV- when the MCU commands OFF.
- the 2N7002 gate has a hardware pull-down, so MCU reset/high-Z releases QSW back to ON.

This has a stronger availability property than deriving the gate pull-up only from the regulated 5 V rail: loss of the MCU or buck does not by itself command the PV module OFF. Exact gate-bias resistor and zener values are to be frozen together with the final module-voltage/transient envelope.

The switch is an **operational curtailment actuator, not a safety isolator or maintenance disconnect**.

## Power supply

The sensor supply is connected directly across module PV+ / PV- **before QSW**, so the logger stays alive while its module is curtailed.

Baseline:

```text
PV 0...60 V --> LM5164 --> 5.0 V --> TPS7A2033 --> 3.3 V
```

LM5164 is rated 6...100 V. A preliminary operating point is:

- VOUT = 5.0 V
- nominal FSW = 300 kHz
- `RRON ~= 5 V * 2500 / 300 kHz = 41.7 kΩ` -> start with **42.2 kΩ, 1%**
- feedback divider ratio `Rtop/Rbottom = 5/1.2 - 1 = 3.1667`; e.g. **316 kΩ / 100 kΩ** gives about 4.99 V nominal
- input UVLO target about 9.0 V on / 8.4 V off
- using TI's UVLO equations, **1.0 MΩ / 200 kΩ** gives 9.0 V turn-on and 8.4 V turn-off

The inductor/ripple-injection network and input transient suppression are **not release-frozen yet**. They must be finalized from the actual maximum load, layout and cold-`Voc`/surge envelope using the current LM5164 Rev. D design procedure. The initial PCB should reserve generous input-decoupling and TVS area.

## Module temperature channel

The external temperature probe uses a **Pt1000** rather than an NTC so all modules have a standardized, stable transfer function.

Selected element: Vishay PTS120601B1K00P100:

- IEC 60751 platinum characteristic, 3850 ppm/K
- class F0.3: `±(0.30 + 0.005*|T|) °C`
- -55...155 °C
- recommended continuous measurement current for the 1 kΩ PTS1206: 0.1...0.25 mA

A 14.7 kΩ ±0.05%, ±10 ppm/K reference resistor limits current to about 0.21 mA around room temperature and remains below 0.25 mA over the specified temperature range. Excitation is switched only for measurements. The nRF52840 SAADC reads the divider ratiometrically; firmware must compensate the actual excitation/supply reading rather than assuming an exact 3.3 V rail.

The target is **better than ±0.5 °C after probe calibration near the operating range**, but the dominant error is expected to be thermal coupling to the PV backsheet rather than ADC quantization. The probe mechanics and adhesive/insulation stack require prototype validation.

## DC measurement error budget

### Raw, uncalibrated

The 0.7 mΩ shunt has ±1% initial tolerance, so uncalibrated current accuracy is dominated by the shunt. High accuracy therefore **requires per-unit calibration**.

INA228 key maximum errors used here:

- shunt offset: ±1 µV
- shunt offset drift: ±10 nV/K
- shunt gain error: ±0.05%
- shunt gain drift: ±20 ppm/K
- bus-voltage offset: ±2.5 mV
- bus-voltage offset drift: ±20 µV/K
- bus gain error: ±0.05%
- bus gain drift: ±20 ppm/K
- integral non-linearity: ±0.002%

### Calibrated current budget

Production current calibration removes the initial shunt tolerance and initial INA228 gain error as one combined gain term. Zero-current calibration removes the initial INA228 offset.

For a conservative **60 K change from calibration temperature**, budget:

| Contributor | Conservative residual |
| --- | ---: |
| BVB shunt TCR, ±20 ppm/K | 0.120% |
| INA228 gain drift, ±20 ppm/K | 0.120% |
| production current reference / fixture allocation | 0.050% |
| INA228 INL | 0.002% |
| INA228 residual offset drift | 0.857 mA equivalent |

Worst-case linear sum:

| Module current | Offset-drift contribution | Current error |
| ---: | ---: | ---: |
| 1 A | 0.086% | **0.378%** |
| 5 A | 0.017% | **0.309%** |
| 12 A | 0.007% | **0.299%** |
| 15 A | 0.006% | **0.298%** |

The values are deliberately pessimistic: all signed maxima are added in the same direction. RSS values are about 0.20% at 1 A and 0.18% at 5...15 A.

A zero measurement at the current operating temperature removes most of the offset-drift term.

### Calibrated voltage budget

A factory 0 V + precision high-voltage calibration removes initial VBUS offset and gain error.

For the same 60 K temperature excursion:

| Contributor | Conservative residual |
| --- | ---: |
| INA228 bus gain drift | 0.120% |
| calibration voltage reference allocation | 0.050% |
| INA228 INL | 0.002% |
| bus-offset drift | 1.2 mV absolute |

Worst-case voltage error is approximately:

- 0.184% at 10 V
- 0.178% at 20 V
- 0.175% at 40 V
- 0.174% at 60 V

### Calibrated DC power budget

For `P = U * I`, conservative voltage and current worst-case errors are added:

| Operating point | Conservative power error |
| --- | ---: |
| 40 V / 1 A | **0.553%** |
| 40 V / 5 A | **0.484%** |
| 40 V / 12 A | **0.474%** |
| 40 V / 15 A | **0.473%** |

Therefore the first hardware target is:

> **<= 0.5% DC-power error for the useful PV power range after per-unit calibration**, with about 0.55% allowed around 1 A, for a 60 K excursion from calibration temperature.

This is an engineering error budget, not a guaranteed system specification. It excludes long-term shunt aging, thermal gradients between shunt and INA228, calibration-equipment errors beyond the allocated 0.05%, connector/contact thermoelectric effects and PCB/layout mistakes.

A two-temperature current calibration can characterize the *effective* shunt + INA228 gain temperature coefficient of each assembled board. With that correction, the development target becomes **<= 0.3% DC-power error for I >= 1 A**, subject to prototype thermal validation.

## Calibration strategy

Every PanelLog node gets a versioned calibration record stored in nonvolatile memory.

### Factory / bench calibration

1. **Current zero**
   - QSW OFF, source/module voltage present.
   - Verify no external current path.
   - Average a long INA228 conversion sequence.
   - Store zero offset and INA die temperature.

2. **Current gain**
   - Pass a traceable current preferably in the **8...12 A** range through the complete assembled power path.
   - Reference current uncertainty target: <=0.05%.
   - Determine one combined current scale factor; this absorbs initial shunt tolerance and INA228 gain error.

3. **Voltage offset and gain**
   - 0 V point for VBUS offset.
   - one precision point around **35...45 V** for gain.
   - Reference-voltage uncertainty target: <=0.05%.

4. **Pt1000**
   - minimum one-point calibration of the assembled probe/cable near room temperature.
   - use two temperature points if absolute module-temperature accuracy proves important.

5. **Recommended two-temperature electrical calibration**
   - repeat the current-gain point with the assembled board stabilized near about 20 °C and 60 °C.
   - fit one effective current-gain tempco in ppm/K.
   - this is preferred over blindly programming the nominal shunt TCR into INA228 because the shunt TCR is signed/toleranced and INA die temperature is not exactly the shunt temperature.

Calibration record fields should include at least serial number, hardware revision, calibration format/version, UTC date, current gain, current zero, voltage gain, voltage zero, optional gain tempco, Pt1000 correction, reference-equipment ID/uncertainty and CRC.

### Runtime calibration

- On boot / sunrise, hold QSW OFF briefly and refresh the zero-current value before connecting the module.
- Whenever BatteryFlex intentionally curtails the module, use the OFF interval to refresh zero offset.
- Record INA228 die temperature with every calibration/measurement batch.
- Apply the stored effective temperature coefficient only after prototype measurements establish the relation between INA temperature and actual shunt temperature.
- Never infer a new gain calibration from normal PV operation without an independent current reference.

### Energy

INA228's internal energy accumulator is useful as a diagnostic, but not the authoritative long-term energy counter: the device specifies up to 1% energy/charge TME and its internal oscillator has finite tolerance.

PanelLog/BatteryFlex should integrate calibrated voltage and current using its own timestamps:

```text
E += U_cal * I_cal * dt
```

The raw INA228 energy/charge registers can be transmitted as independent plausibility channels.

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
- INA228 die temperature
- 3.3/5 V supply diagnostics where practical
- uptime / reset reason
- Zigbee LQI/RSSI
- calibration revision

## PCB / mechanical constraints

The high-current path is a primary mechanical/electrical design feature, not ordinary signal routing:

- use the manufacturer's true 4-terminal BVB land pattern
- route INA228 IN+/IN- as Kelvin traces directly from the sense terminals; never pick up the voltage from high-current copper
- keep shunt and INA228 close enough for low thermoelectric/EMI error, but characterize their temperature relationship
- use wide, short copper for the MPPT-/shunt/MOSFET/PV- path; **2 oz copper is the initial PCB baseline**
- size copper and thermal vias from actual hot-enclosure testing; no final trace width is frozen yet
- keep the LM5164 switching loop physically away from the shunt/INA228 Kelvin pair
- reserve input-TV S / transient-protection area near the PV cable entry
- use PV-rated pigtails/connectors and strain relief; do not rely on a small generic PCB terminal for the 15 A path
- conformal coating / enclosure materials must tolerate the expected hot-backside temperature and UV/moisture environment

### RF placement

A PV laminate and aluminium rail are poor surroundings for a 2.4 GHz ceramic antenna. Mount the node near a module edge and orient the E73 antenna away from aluminium and the module backsheet as far as practical. Link-margin testing in the final mechanical installation is a release gate; if it is inadequate, change to an external-antenna nRF52840 module variant rather than increasing TX power blindly.

## Release gates

Before the first fabrication/release:

1. cold-`Voc` calculation for every deployed module type
2. select/freeze TVS and input protection from that voltage/transient envelope
3. complete LM5164 inductor/ripple-injection/input-filter design and simulate/check with TI design procedure
4. thermal simulation/estimate plus hot-module prototype measurement for QSW, shunt, buck and enclosure
5. Kelvin-layout review around BVB + INA228
6. validate current/voltage error budget on at least two temperatures
7. characterize INA228 die temperature versus shunt temperature
8. validate Pt1000 attachment and module-temperature tracking
9. RF range test with the enclosure mounted at the intended position behind a real PV module
10. verify inverter/MPPT behavior during repeated module ON/OFF switching
11. confirm that all externally accessible/debug connections cannot bypass the low-side shunt in normal service
12. confirm JLC/LCSC availability immediately before PCB/BOM release

## Repository layout

Planned:

- `hardware/` - KiCad schematic/PCB and project-local libraries
- `bom/` - selected components, sourcing and alternates
- `firmware/` - nRF52840/Zigbee firmware
- `docs/` - validation/calibration reports once measured hardware exists
- `manufacturing/` - JLCPCB outputs and assembly notes

The root README is the architecture and measurement-accuracy source of truth until the first schematic revision is committed.
