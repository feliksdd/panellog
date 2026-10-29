# Firmware

Target platform: nRF52840 / E73-2G4M08S1C as a Zigbee end device.

## Required behavior

- configure and sample INA228 in the +/-40.96 mV shunt range
- apply per-unit current/voltage calibration coefficients
- read the external calibrated Pt1000 probe channel
- read the internal QSW-area NTC for thermal protection
- log INA228 die temperature as the measurement-chain internal temperature
- integrate calibrated DC energy using MCU/BatteryFlex timestamps
- expose raw INA228 accumulator values as diagnostics, not the authoritative long-term energy total
- control the module switch as whole-module ON/OFF only; no PWM
- enforce minimum dwell/hysteresis around switching
- implement an OFF lease: loss/expiry of the curtailment command returns the module to ON
- publish reset reason, uptime, INA die temperature, QSW-area NTC temperature and radio link quality

## Calibration lifecycle

On boot/sunrise, keep QSW OFF long enough to acquire a fresh zero-current offset before connecting the module. Every later deliberate OFF interval can refresh the zero.

Factory calibration data are versioned and CRC-protected and include current/voltage scale and offset, effective current gain tempco when characterized, Pt1000 correction, calibration date and hardware revision.

The full procedure and numerical error budget are in the root [README](../README.md).
