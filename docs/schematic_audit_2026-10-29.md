# PanelLog schematic review — 2026-10-29

Status: **preliminary static audit only; not KiCad ERC, bench validation or release approval**.

## Source and revision

- `main` at start of review: `73896a3a6b82b399e26fca693f7ffb02f9a57b91`.
- Native schematic: `hardware/kicad/panellog.kicad_sch`, KiCad 10 format `20260306`.
- The review used the repository's symbol-library pin definitions and placed schematic labels. **The current environment has no KiCad 10 installation.**

## Connectivity audit — source-structural check

A KiCad S-expression parsing check reconstructed symbol-instance pin endpoints from the project-local library and matched them against labels and explicit no-connect markers:

- 61 symbol instances, 185 instance pins, 160 labels and 25 explicit NC markers.
- All 185 pins matched either at least one label or an explicit no-connect.
- No unmatched labels, label/NC overlaps or pin-coordinate collisions detected.
- The topology uses local labels, with no drawn wires. This means connectivity depends on labels and geometry; **a native KiCad 10 load, netlist export and ERC are still mandatory**.
- This structural check cannot detect wrong physical pin mappings, wrong schematic electrical intent, footprint problems, analog performance or unsafe transient operation.

## Module voltage envelope — provisional calculation

The previously discussed second module is **SOLARWATT Panel vision AM 4.0 black, 400 W**. Confirm the physical nameplate/datasheet revision before release.

Example minimum **cell temperature −25 °C** (assumption, not a local site guarantee). Linear approximation:

`Voc(T) = Voc(25 °C) × [1 + |βVoc| × (25 °C − T)]`

| Module | Voc,STC | βVoc | Voc at −25 °C (nominal) | Isc,STC |
| --- | ---: | ---: | ---: | ---: |
| DMEGC DM370M6-60HBB-S | 41.96 V | −0.265 %/K | 47.52 V | 11.29 A |
| SOLARWATT Panel vision AM 4.0 black 400 W (2025 datasheet revision) | 37.1 V | −0.25 %/K | 41.74 V | 13.9 A |

Sources:
- DMEGC 60HBB-S datasheet: https://www.quesolar.com/wp-content/uploads/2022/05/DM370M6-60HBB-S-powered-by-Taylor.pdf
- SOLARWATT Rev 12 datasheet: https://www.solarwatt.de/canto/download/s6p8qspghh145cii713qp7u50c

Important:
- These are **nominal static** estimates. The applicable extreme minimum temperature, manufacturer tolerances and transients must still be checked.
- The 60 V continuous target is plausible for the nominal single-panel values above but is **not** a verified surge or safety rating.
- **15 A is not a universal maximum**: SOLARWATT's manufacturer table gives Isc 15.3 A at 10% and 16.7 A at 20% bifacial gain for the 400 W class. Verify actual rear irradiance and electrical worst case, and dimension connectors, copper, shunt, MOSFET and protection accordingly. The 15 A measurement specification may need extension.
- The manufacturer revision matters: earlier Solarwatt 400 W datasheets show different Isc values. Confirm nameplate and document revision.

## Circuit-specific observations and open checks

1. **LM5164:** The schematically implemented `R4` is **175 kΩ** and `R5` **100 kΩ**; the old README value of 174 kΩ was inconsistent. The output target is 1.2 V × (1 + 175/100) ≈ **3.30 V**. Verify actual feedback reference range, RON, inductor, Type-3 injection and minimum load using the current TI datasheet; do not freeze 68 µH, 150 kΩ / 3.3 nF / 150 pF solely from this preliminary schematic. Datasheet: https://www.ti.com/lit/ds/symlink/lm5164.pdf
2. **Gate start-up:** The normally-ON passive bias means Q1 can connect the module **before the MCU boots**. A firmware-only instruction to keep Q1 OFF during boot cannot guarantee that state. When powered, firmware may request a verified OFF phase for current-zero calibration. During reset/brownout the intended hardware default remains ON.
3. **Zero-current calibration:** Q1 OFF does not itself prove current is zero if unintended paths, leakage or measuring circuitry are present; require a plausibility test before accepting the zero offset.
4. **TVS D1:** Still DNP; select after tolerance, reverse standoff and clamp coordination with ICs and switch, surge energy and cable environment.
5. **Measurement topology:** INA228 `IN+` is labelled MPPT-side shunt; `IN-` is labelled switch-side shunt. Actual Kelvin effectiveness requires the BVB physical 4-terminal footprint and separate sense traces. This cannot be established by schematic ERC alone.
6. **External Pt1000:** `RT1` is explicitly not a PCB component; `J3` is the external two-wire interface. Check wet/surge/ESD protection and lead-fault diagnostics at the off-board connector.
7. **Footprints:** Critical footprints are missing for RSH1 and Q1 as expected. The selection and pin-to-pad mapping must precede PCB capture.
8. **E73:** VDD and VDDH are tied to 3.3 V and unused supply/USB pins carry explicit NCs. Verify this mode and 32.768-kHz crystal loading against the exact E73/nRF52840 board/module documentation.
9. **PV terminals and safety:** Inline hardware must be mechanically and electrically rated for outdoor PV DC. Q1 curtailment is **not** a maintenance disconnect or safety isolation.

## Release checklist

- [ ] Open, save and ERC with **KiCad 10** and retain full result.
- [ ] Export netlist, independently inspect pin and power-path mapping.
- [ ] Confirm the actual two PV nameplates (especially SOLARWATT revision).
- [ ] Freeze minimum site temperature and static + transient voltage/current envelope.
- [ ] Complete LM5164 design calculation, startup and thermal analysis.
- [ ] Characterize fail-ON gate voltage/time over dawn, low Voc, brownout and full Voc.
- [ ] Freeze TVS, sense filter, external probe protection and PV wiring.
- [ ] Construct verified BVB / IPT015 / connection footprints.
- [ ] PCB layout, ERC/DRC, thermal and RF tests, calibration and test plan.
