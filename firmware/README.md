# Firmware

Target platform: nRF52840 / E73-2G4M08S1C as a Zigbee end device.

## Required behavior

- configure INA228 in the +/-40.96 mV shunt range (ADCRANGE=1) **after every power-on**, set SHUNT_CAL and averaging/conversion periods explicitly, then sample the calibrated shunt/bus readings
- apply per-unit current/voltage calibration coefficients
- read the external calibrated Pt1000 probe channel
- read the internal QSW-area NTC for thermal protection
- log INA228 die temperature as the measurement-chain internal temperature
- integrate calibrated DC energy using MCU/BatteryFlex timestamps
- expose raw INA228 accumulator values as diagnostics, not the authoritative long-term energy total
- control the module switch as whole-module ON/OFF only; no PWM
- enforce minimum dwell/hysteresis around switching
- implement a software OFF lease: on loss/expiry of the curtailment command, **while firmware is executing**, release the OFF GPIO to return the module to ON; a latched HIGH GPIO during an MCU hang is **not** cleared by a firmware-only lease
- publish reset reason, uptime, INA die temperature, QSW-area NTC temperature and radio link quality

## Calibration lifecycle

At boot/sunrise, QSW is passively **ON** by hardware default until the MCU is able to command it OFF. Firmware must not assume that it held QSW OFF throughout startup. Once the MCU is running, it can request a short OFF interval to measure the zero-current offset, provided the operating strategy permits it and a plausibility check supports zero current. Later deliberate OFF intervals can refresh the zero; on MCU reset or lease expiry, return to ON.

Factory calibration data are versioned and CRC-protected and include current/voltage scale and offset, effective current gain tempco when characterized, Pt1000 correction, calibration date and hardware revision.

The full procedure and numerical error budget are in the root [README](../README.md). Startup/fault and electrical details are in [the datasheet-based audit](../docs/electrical_audit_2026-10-29.md). The hardware must be separately evaluated for stuck-HIGH GPIO and hot gate leakage; firmware alone cannot provide independent fail-ON safety.
