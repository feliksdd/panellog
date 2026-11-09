# PanelLog buffer assembly and preferred alternatives

No POA repository changes and no firmware development in this revision.

- R18: RESI PTFR0603B14K7N9 / C19680002, 14.7kΩ, 0603, 0.1%, 10ppm/K. Initial tolerance relaxed from 0.05%; perform assembled Pt1000 gain calibration. Temperature coefficient retained.
- C5/C6/C15: Murata GRM21BR61E226ME44L / C86816, 22µF 25V X5R ±20%, 0805. Retain package and nominal ratings; effective DC-bias capacitance and temperature limits still require qualification.
- C26: local 100nF X7R CL10B104KB8NNNC / C1591, 0603, **DNP in direct mode; populate with U4**. Connected directly to U4 supply branch and local ground fill.

## Mutually exclusive assembly options

| Ref | DIRECT default | BUFFERED |
|---|---|---|
| U4 P82B715DR / C2649394 | DNP | fitted |
| C26 100nF / C1591 | DNP | fitted |
| R32/R33 | 0Ω fitted | DNP |
| R30/R31 | 2.2kΩ fitted | 2.2kΩ fitted |
| R34/R35 | DNP | 1kΩ fitted, verify total line pullup with actual peer |

Sx pin3 SDA and Sy pin6 SCL connect MCU, Lx pin2 and Ly pin7 connect cable; pin4 GND, pin8 +3V3, pin1/5 NC. A compatible endpoint is required. A lower clock alone does not waive rise/fall/VOL requirements. TI P82B715 Rev B recommends 4.5–12V; operation down to 3V is explicitly allowed with reduced dynamic sinking capability. At 3.3V/25kHz the circuit is a viable populated option, but final cable/temperature timing measurements are still necessary. Typical quiescent current is 14mA at 5V, not a microamp-class device. Temperature rating is -40 to +85°C.

## Series resistor R36

R36 remains 0Ω pending system decision. A series resistor is a useful passive cable current limiter for the low-current direct sensor, but a high resistance conflicts with a remotely supplied P82B715. Example: 47Ω at 3.3V gives about 70mA short-circuit current and 0.232W continuous dissipation. Use an appropriately derated ≥0.5W part, not the current 0603 footprint. At 0.3mA it drops only 14mV; at 14mA it drops 658mV, which is too much for a 3.3V remote buffer. Small resistors with acceptable buffer voltage drop do not guarantee that a cable short leaves the shared MCU supply alive. Therefore this revision does not install a series-resistor protection claimed to support both assembly modes. A current-limited switch is the robust option if buffering and cable-fault containment are both required.

Models restored from user commit 0b9faa9 are retained exactly (paths, scale, offset and rotation).

Source: https://www.ti.com/lit/ds/symlink/p82b715.pdf
