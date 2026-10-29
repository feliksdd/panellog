# PanelLog: Schematic re-layout and PCB sync audit (2026-10-29)

## Sources and scope

- Baseline pre-rearrangement: `7c3efda707fc0d6704f2d95206d8e6191adbb763`.
- User's corrected rearrangement: `8be06925bc9031f82b4e4b96256e184a4c924cfe`.
- Corrective changes on `main`:
  - `62642bf87c7f4334bbcfccfba845104771f3700e`: restore 11 lost schematic footprint assignments.
  - `08f36885ee6d7370413c55615e85f8163c6a612b`: deduplicate PCB and bind all 61 footprints to schematic-symbol UUIDs.
  - `b4ae7aa84c78dff6bc020ed04b8c963cce7e679e`: swap Y1 PCB pad-net assignments to follow the user's new schematic.

**Review covers logic of connections and source-level PCB mappings; it does not substitute a native KiCad 10 ERC/DRC, footprint geometry check or manufacturing qualification.**

## Findings

### Reorganized schematic

- **PV input and 3.3 V supply:** Replaced old net aliases `PV_PLUS` and `VCC_3V3` with KiCad's implicit `VDC` and `+3V3` power-symbol nets. They have been normalized for comparison. The former split `+3.3V`/`+3V3` has been resolved; the LM5164 output, nRF52840 supplies U3.19/U3.23, INA228 U2.6, I²C pullups and SWD supply now belong to the same +3V3 electrical network.
- **LM5164:** VIN/PV, GND, UVLO divider, RON, BST/SW/L1, FB divider, ripple injection and PGOOD pullup have the intended connections. Two-terminal passive pin numbers are often flipped because of rotation; these reversals do not alter resistor/MLCC function.
- **Shunt / low-side switch:** RSH1.1 is `MPPT_MINUS`, RSH1.2 is `SHUNT_RETURN`; Q1.9 drain is on `SHUNT_RETURN` and Q1.2–8 sources on GND. INA228 R11 IN+ filter feeds MPPT_MINUS and R12 IN− filter SHUNT_RETURN. Polarity matches the baseline. The mechanical four-Kelvin-pad BVB footprint remains a **provisional landpattern**.
- **Fail-ON gate:** PV/VDC → R8(47 kΩ) → D2 cathode/Q2 drain/R9(2.2 kΩ) → Q1 gate; D2 anode and Q2 source tied GND. Q2 gate controlled via `SWITCH_OFF`, R10 pulls it to GND. Removed local netlabels are not an open circuit when replaced by real wires.
- **INA228:** VS/GND, I²C/ALERT, bus RC, differential input filters and address pins maintain correct functional connections. Some filter nodes are now intentionally unlabeled.
- **External Pt1000:** +3V3 → R18 14.7 kΩ → J3/RT1 → GND, with R19 1 kΩ in series to `PT1000_ADC` (U3.3), and C18 100 nF from ADC to GND. The incorrectly placed series R/C from the prior rearrangement has been repaired.
- **Local NTC:** +3V3 → R21 10 kΩ → NTC junction → RT2 10 kΩ NTC → GND. NTC junction feeds R22 1 kΩ in series to `NTC_ADC` (U3.7), with C20 100 nF from ADC to GND. This is again the intended anti-alias/charge-reservoir topology. At nominal 25°C, V_ADC≈1.65 V DC; rising temperature causes V_ADC to decrease. NTC Beta/table calibration, ADC acquisition/source impedance, noise and thermal placement remain to validate.
- **32.768 kHz oscillator:** User's rearrangement reversed Y1 pin numbers relative to the old schematic, while preserving XL1/XL2 and the two equal 22-pF capacitors. A two-terminal crystal is not polarity-sensitive. PCB pad nets have been updated to Y1.1=XL2, Y1.2=XL1.

### Footprints (cause of PCB import errors)

Eleven component footprints were blank after re-layout. All were restored **without changing the user's component placement or nets**: `U1, C3, L1, J1, J2, Q1, U3, J3, J4, Y1, RSH1`. The two reported import errors were directly caused by blank `Footprint` properties on Y1 and RSH1.

All nine project-local prototype footprints remain **DRAFT**, not yet verified against OEM land patterns; Y1 uses `Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm`, RSH1 uses `PanelLog:BVB_M_R0007_Kelvin`.

### Board duplicate removal and association

The user's imported PCB contained **83 footprint instances for 61 unique component references**. Exactly 22 imported KiCad-standard footprints were already correctly associated with schematic UUIDs but located off-board; 22 earlier synthetic, on-board placeholder copies had **no schematic path**. The linked KiCad copies were moved to their older placed positions and their unlinked, redundant copies removed.

Y1/RSH1 were the only other unlinked real board components. They now carry the matching schematic-instance paths; the board has **61 unique footprints, all associated with their current schematic instance UUIDs**. The original placement positions were retained as a convenience; KiCad courtyard overlap and fab correctness remain to be checked.

A source-based copper-pad-to-schematic net membership check found the Y1 pin swap as the sole remaining electrical difference after PCB deduplication. Y1 pad-net assignments were then corrected in the native board file.

## Mandatory native checks before further PCB work

From the repository root:

```bash
git pull --ff-only
flatpak run --command=kicad-cli org.kicad.KiCad sch erc \
  hardware/kicad/panellog.kicad_sch -o panellog-erc-new.rpt
flatpak run --command=kicad-cli org.kicad.KiCad pcb drc \
  --schematic-parity --severity-all \
  -o panellog-pcb-drc-new.rpt hardware/kicad/panellog.kicad_pcb
```

Open `hardware/kicad/panellog.kicad_pro` in KiCad 10; inspect **Y1 and RSH1 pad/net association** and update the PCB from schematic once more, checking that nothing is newly added. Expect DRC errors for unfinished routing, footprint courtyards/clearance and RF/thermal keepout; **do not disable DRC checks just to achieve zero warnings**.

**Release gate remains BLOCKED**: KiCad ERC/DRC after this commit, exact BVB/Q1/E73/buck landpatterns, 20-A copper and thermal capability, RF keepout, environmental performance and complete electrical routing are not yet verified.
