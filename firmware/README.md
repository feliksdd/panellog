# PanelLog C6 firmware requirements

Target: ESP32-C6-MINI-1-N4, 4 MB flash, ESP-IDF / ESP Zigbee SDK. This repository does not yet contain a completed C6 firmware port.

| Function | GPIO | Module pad |
|---|---:|---:|
| Pt1000 ADC | 2 | 5 |
| NTC ADC | 3 | 6 |
| VCC monitor ADC | 0 | 12 |
| I2C SDA | 6 | 15 |
| I2C SCL | 7 | 16 |
| SWITCH_OFF | 18 | 24 |
| PGOOD | 19 | 25 |
| INA_ALERT | 20 | 26 |
| UART RX | 17 | 30 |
| UART TX | 16 | 31 |
| Boot strap high | 8 | 22 |
| BOOT_N | 9 | 23 |

GPIO8 and GPIO9 have 10 kΩ pull-ups. J4 pin 6 grounds GPIO9 for download mode, with GPIO8 high; pulse EN (J4 pin 4). J4: 1=3V3 reference, 2=target TX, 3=target RX, 4=EN, 5=GND, 6=BOOT_N. Use 3.3 V UART levels. Pin 1 is a voltage reference, not permission to back-power the target. USB D+/D− are not routed. Use isolated programming for an installed PV circuit or disconnect PV and inverter before programming.

EN has 10 kΩ / 1 µF reset delay. External 32.768 kHz crystal removed; use internal low-power clock and validate Zigbee sleep timing/current. The existing Nordic firmware design cannot be used unchanged.

Default SWITCH_OFF low/high-impedance keeps Q1 conducting through the existing fail-ON gate network. Explicitly drive GPIO18 low before enabling output; preserve this behavior through reboot, watchdog and firmware update. High turns Q2 on and Q1 off. Rate-limit curtailment; no high-frequency PWM operation is qualified.

INA237AIDGSR with C481535 (1 mΩ, four-terminal) is selected. Q1 IPT015N10N5 remains unchanged. Invalidate old INA228/0.7 mΩ calibration records by hardware revision. Port the driver explicitly; do not reuse INA228 register widths/scales.

- CONFIG.ADCRANGE=1 (±40.96 mV); raw VSHUNT is signed 16-bit, 1.25 µV/LSB, hence 1.25 mA/LSB at 1 mΩ.
- VBUS is 16-bit, 3.125 mV/LSB. Preserve IN+ on MPPT_MINUS and IN− on SHUNT_RETURN via separate Kelvin nets.
- Optional hardware current calculation: CURRENT_LSB=0.002 A; SHUNT_CAL=round(819.2e6 * 0.002 * 0.001 * 4)=6554 (0x199A). Rounding adds about +61 ppm gain, removed by per-unit calibration. ADC range, not CURRENT register range, limits measurement to approximately ±40.96 A; board remains rated for the existing 15 A design target.
- Prefer calibration from raw VSHUNT: Ical=(Vshunt−Vzero)/R_effective. Calibrate zero and gain at 8–12 A; characterize temperature dependence.
- Recalculate alert thresholds for INA237 register formats; do not copy raw INA228 settings. Existing 10 Ω/100 nF input filter remains.
- No hardware energy/charge accumulators or shunt-temperature compensation: integrate calibrated U*I and I with monotonic timestamps, flag gaps and apply any validated temperature correction in MCU software.
- Start with long conversions and averaging for PV telemetry; verify latency against required alert response on hardware.

R20=R24=100 kΩ divides the supply by two. C19=100 nF gives approximately 5 ms time constant; allow ≥25 ms settling, and validate sample acquisition/loading at 50 kΩ source impedance. Apply ESP-IDF ADC calibration at the configured attenuation, average samples and characterize residual nonlinearity. Vrail=2×Vadc_rail; Rpt=14700×Vadc_pt/(Vrail−Vadc_pt). Pt1000 excitation is continuously enabled by R18, not software switched. Retain the precision R18. NTC is a thermal protection/hotspot channel. A C6 system temperature accuracy of ±0.5 °C is not yet demonstrated.

Power budget: LM5163 is rated 500 mA, not 1 A. Validate radio bursts and 3.3 V droop across the complete input range, hot enclosure and sleep/wake transitions. Deep sleep numbers for the bare chip are not a board-level guarantee. External sensors, INA237, dividers and radio duty cycle contribute.
