# Internal temperature and supply measurement review — 2026-11-07

Native schematic netlist checked. The circuit is correctly connected:

| Parts | Connection / function |
|---|---|
| R20 / R24 | 100 kΩ / 100 kΩ: +3V3 → VCC_MON_ADC → GND |
| C19 | 100 nF, VCC_MON_ADC → GND; GPIO0 / module pad 12 |
| R21 / RT2 | 10 kΩ / 10 kΩ NTC: +3V3 → sensor node → GND |
| R22 / C20 | 1 kΩ series into NTC_ADC, 100 nF to GND; GPIO3 / pad 6 |

No divider topology change is needed. R20/R24 measure supply voltage,
not NTC resistance. R22 is an ADC filter/isolation resistor and is not
part of the DC divider equation unless input leakage/loading matters.
Use calibrated ADC voltages sampled close together:

Vrail = Vcc_adc × (R20 + R24) / R24 (nominally 2 × Vcc_adc)

Rntc = R21 × Vntc_adc / (Vrail − Vntc_adc)

T_C = 1 / (1/298.15 + ln(Rntc/10000)/B) − 273.15

Use actual calibrated divider ratios where available. For the full operating
range use the manufacturer's R/T table, rather than one beta approximation.
TDK NTCG163JF103FT1S: R25 10 kΩ ±1%; B25/50 3380 K **typical**;
B25/85 3435 K ±1%. The previous BOM's ±1% attached to B25/50 is corrected.

At 25 °C and 3.3 V: NTC current 165 µA, dissipation 0.272 mW.
TDK's approximately 1 mW/K dissipation factor implies approximately 0.27 K
self-heating under its test conditions. Actual enclosure/PCB coupling differs.
RT2's placement near Q1 measures a PCB hotspot, not ambient or module
backsheet temperature. Keep the separate external Pt1000 for the latter.

R20/R24 draw 16.5 µA. Their 50 kΩ Thevenin impedance with C19 gives 5 ms;
allow at least 25–30 ms after power changes. At 25 °C the NTC path gives
(10 kΩ || 10 kΩ + 1 kΩ) × 100 nF = 0.6 ms. Discard the first sample after
channel switching and verify acquisition with this source impedance.
Use ESP-IDF ADC calibration and averaging, check residual channel mismatch.
The cold NTC voltage approaches the rail; select attenuation that covers it.
Current C6 datasheet specifies 0–3.3 V at ATTEN=3 with ±40 mV calibrated
error under specified test conditions; verify applicable chip revision/date
and Wi-Fi interference. Calibration does not remove every ADC error.

Illustrative 25 °C errors: 1% R21 ≈0.26 K; 1% NTC resistance ≈0.26 K;
worst opposing 1% R20/R24 tolerances cause approximately 1% inferred-rail
error and ≈0.53 K temperature error. ADC errors and self-heating add further
uncertainty. ±0.5 °C system accuracy is therefore not demonstrated. For
thermal monitoring a calibrated approximately ±2 °C development target is
reasonable; validate over the actual board temperature and radio states.

Reject denominator <=0, implausible/open/short NTC voltages, stale Vrail and
supply brownout; return invalid rather than a fabricated temperature. Fault
thresholds must leave margin for valid cold temperatures near the rail.

Sources:
- https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG163JF103FT1S
- https://product.tdk.com/system/files/dam/doc/product/sensor/ntc/chip-ntc-thermistor/data_sheet/datasheet_ntcg163jf103ft1s.pdf
- https://documentation.espressif.com/esp32-c6_datasheet_en.html
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32c6/api-reference/peripherals/adc/index.html
