# Shutdown feedback, 2026-11-07

Circuit added to schematic and board: R27 1 MΩ from VDC to SHUNT_RETURN
(Q1 drain), R28 1 MΩ from drain to SHUTDOWN_FB_ADC, R29 27.4 kΩ from
ADC to GND, C25 100 nF from ADC to GND. ESP32-C6 GPIO1, module pad 13,
ADC1_CH1. R27/R28: 1206W4F1004T5E, C17927, 200 V / 250 mW / 1%.
R29: C22964; C25: C14663. Q1 and existing fail-ON gate drive retained.

The pull-up makes an open switch observable even with the inverter absent.
At 60 V with Q1 on, R27 dissipates 3.6 mW and carries 60 µA. With Q1 off
and no external drain load, drain voltage is 0.50676 × VDC; ADC voltage is
0.013515 × VDC (0.811 V at 60 V). A drain held at 60 V gives 1.600 V ADC.
The input RC time constant is approximately 2.7 ms.
This is a weak intentional bypass of Q1, not galvanic isolation.

## Firmware requirements (not implemented firmware)

Calibrate ADC voltage using ESP-IDF calibration; Vdrain = Vadc × 37.49635.
Use appropriate attenuation, validated across input range and temperature.
A proposed diagnostic sequence, to validate on hardware:

1. Require fresh, plausible ADC/current data and stable VDC >= 18 V.
2. Command SWITCH_OFF high. Wait at least 100 ms for the transition.
3. Confirm off only if Vdrain >= 0.35 × VDC AND |Ical| <= 0.15 A,
   continuously for 500 ms. Average samples; reject stale samples.
4. Below threshold report shutdown_not_confirmed. Low drain voltage does
   not uniquely identify a shorted MOSFET: external clamps or measurement
   faults can have the same effect. Night/invalid data => unknown/not_testable.
5. Check near-zero drain voltage while Q1 is on as a plausibility check.

No safety-rated disconnection claim. Current alone cannot prove successful
shutdown at zero irradiance. The voltage diagnostic supplements INA237;
reverse current through Q1 body diode remains possible.
Validate externally connected inverter states, charged capacitors, leakage,
minimum PV voltage, and drain transients on hardware. With MCU supply off,
R28 limits possible ADC clamp injection to tens of microamps; verify no
back-powering or latch-up during startup/shutdown. This is not yet a
manufacturing release or a qualified protection function.

## Native validation

KiCad 10.0.8: same 43 pre-existing open connections, zero schematic parity
issues, five unchanged ERC findings. No new copper-clearance or short-circuit
findings. Existing silk/courtyard issues remain; see review_2026-11-07 reports.

Sources: TI INA237 datasheet; Espressif ESP32-C6 datasheet and ADC calibration
API; LCSC C17927 product specification (200 V, 1 MΩ, 1206).
