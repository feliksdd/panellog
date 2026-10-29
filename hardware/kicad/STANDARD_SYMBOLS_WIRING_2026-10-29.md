# KiCad 10: standards symbols and visible wiring — 2026-10-29

## Goal and implementation

Replace the old project-local generic symbol set with actual **KiCad standard-library symbol IDs**, and connect nearby components using **visible, orthogonal `wire` segments**, rather than solely endpoint labels.

Actual symbol instances:

| KiCad library ID | Number | Function |
| --- | ---: | --- |
| `Device:R` | 24 | All ordinary resistors, plus externally connected Pt1000 RT1 shown as an explicitly identified resistor |
| `Device:C` | 23 | Capacitors |
| `Device:L` | 1 | Buck inductor |
| `Device:D_Zener` | 2 | D1 TVS candidate (DNP) and D2 low-current Zener |
| `Transistor_FET:2N7002` | 1 | Q2 control MOSFET (G=1, S=2, D=3) |
| `Device:Crystal` | 1 | Y1, 32.768 kHz |
| `Device:Thermistor_NTC` | 1 | RT2, hotspot NTC |
| `Connector_Generic:Conn_01x02` | 3 | J1/J2/J3 |
| `Connector_Generic:Conn_01x05` | 1 | J4 SWD |
| `power:PWR_FLAG` | 3 | Power-source ERC flags |
| Project-specific symbols | **5** | LM5164, INA228, E73/nRF52840, BVB four-terminal-physical shunt, IPT015N10N5 |

The project symbol library `hardware/symbols/panellog.kicad_sym` and the corresponding schematic cache now retain **only** those five specific symbols. The generic symbol names above are official KiCad library identifiers; KiCad 10 will resolve these from the normal installed libraries. The 2N7002 symbol's embedded graphical cache was adapted from the standard KiCad BSS138 symbol, which has the same G/S/D pin numbering; explicitly cross-check against your KiCad 10 library when updating symbols.

## Visible wiring

The schematic has **198 real wire segments, 20 junctions, 143 remaining local net labels, and 25 explicit no-connect marks**. Labels are retained for cross-block connections (especially MCU signals, power and measurement references), while wire segments draw out the local networks.

Physically wired local groups include:

- Parallel high-voltage input capacitor bank and selected PV+ / GND rails
- PV module to MPPT positive connection, and MPPT-/shunt/Q1 return path
- LM5164 SW–L1–3.3 V rail, several feedback and supply branches
- Fail-ON gate resistor, Zener, pull-down MOSFET and GPIO OFF control
- INA228 differential shunt filter / Kelvin-net signal paths and VBUS-sense RC branch
- MCU pull-up and local sensor supply rails
- 32.768-kHz crystal / load capacitors

Wires are axis-aligned at the 1.27-mm grid. Two wires crossing without a junction are **not intended to be connected**; the KiCad symbol editor should confirm geometry. A junction is placed at shared, intentional branched net locations.

## Validation performed

A programmatic net reconstruction compared **all 193 symbol pin-number → net assignments** against the baseline commit `67a6a85a49d9cb0e0b55cf68286c7383c5fe5ae8` captured immediately before conversion.

| Check | Result |
| --- | --- |
| Placed symbol instances | 65 |
| Standard-library symbol instances | **60** |
| Special project symbols | **5** |
| Reconstructed pins | **193/193 preserved** |
| Wrong pin-to-net assignments relative to baseline | **0** |
| Multiple different net labels on one physically wired component | **0** |
| Duplicate UUIDs | **0** |
| Explicit NC markers preserved | **25** |
| Visual wire segments | **198** |
| Explicit junction markers | **20** |
| Remaining netlabels | **143** |

**Limitations:** These are structural/S-expression and reconstructed-net checks, **NOT a KiCad 10 ERC result**. The environment used for automatic edits does not provide KiCad 10 rendering or ERC. Consequently, visible field overlap, page readability, footprint association, cached-vs-installed symbol-version discrepancies, and solder-footprint correctness must be confirmed in the KiCad GUI. In particular, open the project using `hardware/kicad/panellog.kicad_pro` and inspect the power supply, gate drive, INA228 and nRF52840 blocks before PCB design.

The last actual native ERC supplied earlier in the conversation (29.10.2026 13:16) was performed **before this symbol and wiring conversion**, and does **not** validate this new revision.

## Run native validation with KiCad 10 Flatpak

From the repository root:

```bash
git pull --ff-only
flatpak run --command=kicad-cli org.kicad.KiCad \
  sch erc hardware/kicad/panellog.kicad_sch \
  -o panellog-erc-after-standard-symbols.rpt
flatpak run --command=kicad-cli org.kicad.KiCad \
  sch export netlist hardware/kicad/panellog.kicad_sch \
  -o panellog-after-standard-symbols.net
```

Do not suppress ERC diagnostics merely to reach zero warnings. Confirm that all standard symbols and custom symbols can be resolved, that the user's KiCad10 saved project keeps all new wires and nets, and that pin numbering and footprints are correct.

## Reference

- [KiCad standard symbol libraries](https://www.kicad.org/libraries/download/)
- Earlier [native ERC analysis](VALIDATION_2026-10-29.md)
- [Original electrical design audit](../../docs/electrical_audit_2026-10-29.md)

No electrical ratings, BOM choices or DNP status were intentionally changed by this symbol/wiring conversion.
