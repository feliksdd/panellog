# Selected components

The current baseline is intentionally small and biased toward parts available from JLCPCB/LCSC where practical.

| Ref/function | MPN | LCSC | Status |
| --- | --- | --- | --- |
| U_MEAS | TI INA228AIDGSR | C2887910 | selected |
| R_SHUNT | Isabellenhütte BVB-M-R0007-1.0, 0.7 mOhm | C5563922 | selected; stock must be checked before order |
| Q_SW | Infineon IPT015N10N5 | C108964 | selected; 100 V, 1.5 mOhm max @10 V |
| U_BUCK | TI LM5164DDAR | C477928 | selected |
| U_MCU | Ebyte E73-2G4M08S1C | project/local | selected, shared platform with poa-sensor |
| T_MODULE | YAGEO Nexensos M222 Pt1000 F0.15 / Class A, 32208572 | external cabled probe | selected sensor element; probe encapsulation required |
| R_RTD_REF | Susumu RG1608N-1472-W-T1, 14.7 kohm 0.05% 10 ppm/K | C1721340 | selected |
| T_INT | TDK NTCG163JF103FT1S or equivalent 10k NTC | JLC/LCSC stocked part | internal MOSFET hotspot monitor |
| Q_GATE | 2N7002 | TBD stocked JLC part | function selected |
| D_GS | 10 V zener, BZT52C10-class | TBD stocked JLC part | function selected |

## Selection notes

- The 0.7 mOhm BVB is selected over larger shunts because it retains 0 +/-20 ppm/K TCR in the manufacturer table while INA228 resolution is still far more than sufficient.
- IPT015N10N5 is preferred because the passive gate network provides about 10 V; its 1.5 mOhm maximum RDS(on) materially reduces behind-module heat versus the earlier logic-level choice.
- LM5164 now generates 3.3 V directly. The former 5 V + TPS7A20 stage is removed.
- The external Pt1000 is a leaded M222 element built into a weather-protected cabled probe and thermally bonded to the module backsheet.
- INA228 die temperature plus an inexpensive NTC next to QSW provide internal thermal information; no separate precision digital PCB temperature sensor is required initially.

Do not substitute the shunt or current monitor without re-running the root-README error budget.
