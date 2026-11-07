# INA237 and C481535 current-sensor revision

User-selected hardware: U2 TI INA237AIDGSR (LCSC C2864837), RSH1 Milliohm
HOVB4026-5W-1mR-1% (C481535). Replaces INA228 and BVB 0.7 mΩ.
Q1 IPT015N10N5, ESP32-C6 and LM5163 remain unchanged. Based on GitHub main
2c391741a8585b2565a06ccca502fdc4bcc1744f.

## Source verification

- INA237 datasheet SBOSA20A, May 2022: https://www.ti.com/lit/ds/symlink/ina237.pdf
- Exact HoVB 1 mΩ manufacturer acknowledgement, A0, 2026-03-28,
  pages 3 and 6 (dimensions, ±50 ppm/°C and land pattern):
  https://web-static.partgenie.ai/component/docs/9dab5088b032522538a226a22e2f391d_2304140030_Milliohm-HOVB4026-5W-1mR-1-_C481535.pdf
- Procurement: https://www.lcsc.com/product-detail/C481535.html
  and https://www.lcsc.com/product-detail/C2864837.html

The exact C481535 document confirms the user's ±50 ppm/°C correction.
The 0.5 mΩ version's ±100 ppm/°C value is not applicable.

## Electrical and layout changes

INA237 DGS10 retains pins 1=A1, 2=A0, 3=ALERT, 4=SDA, 5=SCL, 6=VS,
7=GND, 8=VBUS, 9=IN−, 10=IN+. Existing U2 routing and input filter retained.
New named symbol and footprint prevent accidentally ordering INA228.

RSH1 keeps four distinct nets and symbol pins. Project pin numbering:
1 force MPPT_MINUS, 2 force SHUNT_RETURN, 3 sense positive, 4 sense negative.
Manufacturer drawing defines geometry, not these project-specific numbers.
No copper short between force and sense pads is permitted.

HoVB recommended pads: 2.5 mm wide; force length 5.6 mm, sense length
0.9 mm, separation 0.8 mm, overall horizontal span 10.6 mm. Local force
centres (±4.05, −0.85), sense centres (±4.05, 3.2), in millimetres.
RSH1 centre and 180° placement retained. Force pads connect to the existing power planes; placement (151.55, 108.65, 180 degrees) is retained.
Sense traces extended independently to the displaced sense pads.
Courtyard enlarged. Incorrect BVB 3D models removed from the placed RSH1;
no invented simplified replacement model. Accurate HoVB STEP remains unavailable.

## Measurement configuration and qualification

ADCRANGE=1, ±40.96 mV; raw resolution 1.25 µV = 1.25 mA at 1 mΩ.
This electrical full-scale range does not increase the existing 15 A board
design target. Shunt dissipation: 100 mW at 10 A, 225 mW at 15 A.
Compared with 0.7 mΩ this adds 30 mW and 67.5 mW respectively.

Firmware requirements and README error budgets are revised. INA237 register
widths/scales differ from INA228; the repository contains requirements, not a
completed ESP32-C6 driver. Old calibration records must not be reused.
Zero plus 8–12 A gain calibration, two-point bus calibration and temperature
characterization are required. Energy/charge integration belongs in MCU
software, with monotonic timestamps and gap handling.

Shunt drift at a 50 K change: up to 0.25% from the 50 ppm/K specification.
Together with INA237 gain drift another 0.25%, offset drift equivalent to
1 mA, and a 0.05% reference allocation, the partial calibrated-current
budget is 0.55% + 1 mA. This excludes noise, thermal EMFs, aging and other
board errors; approximately 1% above 1 A remains a development target,
not a measured or guaranteed system specification.

## Verification

See `hardware/kicad/review_2026-11-07/` for the current native KiCad checks
and the comparison against the fetched baseline. Previous dated review
reports remain historical; no manufacturing release is implied.
