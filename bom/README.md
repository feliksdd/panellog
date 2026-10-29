# Selected components

The current baseline is intentionally small and biased toward parts available from JLCPCB/LCSC where practical.

| Ref/function | MPN | LCSC | Status |
| --- | --- | --- | --- |
| U_MEAS | TI INA228AIDGSR | C2887910 | selected |
| R_SHUNT | Isabellenhütte BVB-M-R0007-1.0, 0.7 mOhm | C5563922 | selected; stock must be checked before order |
| Q_SW | Infineon BSC034N10LS5 | C534326 | selected |
| U_BUCK | TI LM5164DDAR | C477928 | selected |
| U_LDO | TI TPS7A2033PDBVR | C2862740 | selected |
| U_MCU | Ebyte E73-2G4M08S1C | project/local | selected, shared platform with poa-sensor |
| T_MODULE | Vishay PTS120601B1K00P100 Pt1000 | external probe | selected sensor element |
| R_RTD_REF | Susumu RG1608N-1472-W-T1, 14.7 kohm 0.05% 10 ppm/K | C1721340 | selected |
| Q_GATE | 2N7002 | TBD stocked JLC part | function selected |
| D_GS | 10 V zener, BZT52C10-class | TBD stocked JLC part | function selected |

## Selection notes

- The 0.7 mOhm BVB is selected over larger shunts because it retains 0 +/-20 ppm/K TCR in the manufacturer table while INA228 resolution is still far more than sufficient.
- The BSC034N10LS5 is a 100 V logic-level MOSFET and can be driven with a clamped passive gate bias; no high-side gate driver is required.
- The LM5164 provides wide PV-input margin and keeps the node powered while the module is curtailed.
- The Pt1000 is separate from the main PCB and is thermally bonded to the module backsheet.

Do not substitute the shunt or current monitor without re-running the root-README error budget.
