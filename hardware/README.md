# Hardware

The root [README](../README.md) is the architecture, dimensioning, error-budget and calibration source of truth.

## Revision 0 target

One PCB per PV module with:

- PV+ pass-through and direct INA228 VBUS measurement
- PV-/return path: MPPT- -> BVB 0.7 mOhm Kelvin shunt -> BSC034N10LS5 -> module PV-
- LM5164 PV-powered 5 V rail before the power switch
- TPS7A2033 3.3 V rail
- E73-2G4M08S1C / nRF52840 Zigbee node
- external two-wire Pt1000 module probe
- passive normally-ON gate bias plus MCU-controlled active pull-down
- SWD plus dedicated calibration/service power pads

## Layout priorities

1. Treat the 15 A current path as power hardware, not ordinary PCB routing.
2. Use the exact 4-terminal BVB land pattern and independent Kelvin pickup.
3. Keep the INA228 sense pair away from the LM5164 switching loop.
4. Keep QSW source at local PV-/MCU ground.
5. Reserve large copper/thermal-via area for QSW and validate behind-module temperature experimentally.
6. Start with 2 oz copper; final widths/via count are released only after thermal/current-path review.
7. Keep the E73 antenna at a module/enclosure edge and out of the aluminium-rail shadow.
8. Do not place a grounded service/debug connector such that it can bypass the low-side shunt in normal installation.

## Not yet frozen

- exact PV cable/MC4 pigtail mechanics
- TVS / surge clamp part number
- LM5164 inductor and final ripple-injection network
- enclosure
- exact gate-bias/zener part numbers
- exact Pt1000 probe encapsulation and adhesive stack

These depend on cold-Voc/transient validation, PCB geometry and the first thermal/RF prototype.
