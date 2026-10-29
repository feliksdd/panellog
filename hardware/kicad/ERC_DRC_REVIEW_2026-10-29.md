# PanelLog KiCad 10 ERC and PCB DRC — 2026-10-29 22:34

## Input reports (uploaded from user's KiCad 10 Flatpak)

- `panellog-erc-new.rpt`, 2026-10-29 22:34:03: **3 errors, 0 warnings**. All three `power_pin_not_driven`: `#PWR04` at (58.42,58.42), `#PWR01` at (91.44,87.63), `#PWR011` at (337.82,27.94).
- `panellog-pcb-drc-new.rpt`, 2026-10-29 22:34:11: **53 DRC violations** (7 `shorting_items`, 7 `solder_mask_bridge`, 39 `lib_footprint_mismatch`), **128 `unconnected_items`** and **8 footprint/parity issues** (6 `net_conflict`, 2 `footprint_symbol_field_mismatch`).

These numbers describe the **uploaded, pre-fix revision**, not an ERC/DRC run on the repaired repository. Do not claim a clean ERC or PCB DRC until the user reruns both native tools.

## Corrections made on main

1. **ERC:** Restored three standard `power:PWR_FLAG` instances, deliberately with `(on_board no)`, connected via local net labels to the **actual KiCad nets** `VDC`, `GND` and `+3V3`. No functional copper or circuit connection was changed. Source: https://docs.kicad.org/10.0/en/eeschema/eeschema.html#pwr-flag
2. **PCB high-risk shorts U1:** Fixed the *swapped physical dimensions* of all eight LM5164 DDA lead lands in both the local library file `PanelLog.pretty/LM5164_DDA_PowerPAD_DRAFT.kicad_mod` and the native PCB: `(size 0.65 1.55)` → `(size 1.55 0.6)`. The 1.27-mm lead pitch had been shorter than the original 1.55-mm footprint pad height, directly shorting neighboring pins. The revised 1.55×0.6-mm lands follow the TI DDA0008B sample PCB land dimensions; **EP pad sizing, paste/mask design, and use of pad number 1 for EP (TI's physical EP is designated pad 9)** remain subject to careful design review. Manufacturer land pattern: https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/Package-Outline-DDA0008B_5F00_4214849.pdf
3. **PCB shunt track conflict:** Reconciled names `SHUNT_RETURN`→`/SHUNT_RETURN` in the two shunt pads and single pilot track, removing the *artificial net-label short* between Q1.9 and the PCB track. The physical pilot trace geometry is still preliminary and unrouted elsewhere.
4. **Board schematic parity:** Reconciled RSH1 pad net `MPPT_MINUS`→`/MPPT_MINUS`, Y1 `XL1`→`/XL1` and `XL2`→`/XL2`. This matches the full KiCad 10 net-name spelling shown in the supplied DRC. No crystal pad polarity/connection changed.
5. **Intentionally not suppressed:** 39 library-footprint mismatch warnings due to synthetic/copied (and in some cases intentionally draft) PCB footprint bodies, and 128 physical unconnected-item messages from the overwhelmingly unrouted PCB remain design work. The user should synchronize **verified** KiCad library footprints in GUI, and must first verify/customize DRAFT land patterns against actual OEM drawings.

## Outstanding blockers

- **U1** is still a **DRAFT** land pattern and center exposed pad is currently implemented with duplicate pad number 1 instead of TI's physical pad 9. The electrical GND association is intended, but this needs explicit design approval, solder paste/thermal vias verification, and pin/footprint consistency review.
- **Q1, RSH1, U3, cables, L1, C3** are preliminary footprints; final MPNs and 20-A/current-carrying geometry are not qualified.
- **Most of the board remains unrouted**. Never infer that removing DRC shorts makes the pilot PV+ and shunt traces safe for 20 A.
- **RF keepout** is only a reminder graphic; the antenna copper keepout is not a DRC-enforced multi-layer keepout.
- DRC has ignored checks (courtyard definition, track endpoint-on-via, tuning profiles, footprint filters, pad/component type). Do not suppress other checks simply to get zero warnings.
- The 2 `footprint_symbol_field_mismatch` warnings for RSH1 Datasheet and Y1 Description are metadata, to synchronize by native schematic-to-PCB update.

## Required native KiCad 10 validation

From the repo root:

```bash
git pull --ff-only
flatpak run --command=kicad-cli org.kicad.KiCad sch erc \
  hardware/kicad/panellog.kicad_sch -o panellog-erc-after-drc-fixes.rpt
flatpak run --command=kicad-cli org.kicad.KiCad pcb drc \
  --schematic-parity --severity-all \
  -o panellog-pcb-drc-after-fixes.rpt hardware/kicad/panellog.kicad_pcb
```

After rerunning ERC/DRC, investigate **all remaining shorts** and **footprint mismatches** before more routing. Native KiCad 10/ERC/DRC **was not available in the assistant execution environment**. Release status: **NOT FOR FABRICATION**.
