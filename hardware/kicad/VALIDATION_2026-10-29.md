> **WICHTIGE KORREKTUR (29.10.2026, Commit b1f31a81086f):** Die frühere strukturelle Prüfung in diesem Dokument verwendete für die vertikale Position der Symbolpins eine falsche Koordinatentransformation. Die alte Aussage „alle Pins angeschlossen“ war **nicht** elektrisch zuverlässig. Der echte KiCad-10-ERC vom 29.10.2026 meldete **35 Fehler und 65 Warnungen**, u. a. vertauschte LM5164-, INA228-, nRF52840- und MOSFET-Anschlüsse. Das Schaltplanmodell wurde daraufhin anhand der tatsächlichen Pinpositionen vollständig umgeordnet und alle Symbolpositionen auf 1,27 mm gerastert. Die frühere Validierung unten dokumentiert nur den historischen Stand; sie darf **nicht** als Nachweis für den aktuellen Schaltplan herangezogen werden. Ein **neuer nativer ERC-Lauf ist erforderlich**. Siehe auch den korrigierten Schaltplan auf `main`.

# KiCad 10 schematic change validation — 2026-10-29

**Source:** `hardware/kicad/panellog.kicad_sch` on `main`, changed in commit `0f8eb1f1974f5979e496329e928d8e2c7cc5ce85`. Native KiCad 10/ERC **has NOT been run** in this environment; the following is a **source/static netlist audit**, not final PCB/sign-off.

## Implemented changes

| Ref | New value and source | Footprint in schematic | Net connectivity |
| --- | --- | --- | --- |
| C1 | 4.7 µF / 100 V X7R, TDK CNA6P1X7R2A475KT000A, LCSC C22877898 | `Capacitor_SMD:C_1210_3225Metric` | 1 PV_PLUS / 2 GND |
| C21 | same as C1 | `Capacitor_SMD:C_1210_3225Metric` | 1 PV_PLUS / 2 GND |
| C22 | same as C1 | `Capacitor_SMD:C_1210_3225Metric` | 1 PV_PLUS / 2 GND |
| R8 | 47 kΩ, 0.25 W design target | `Resistor_SMD:R_1206_3216Metric` | 1 PV_PLUS / 2 QSW_GATE_BIAS |
| D2 | JSCJ MMSZ4697, 10 V, LCSC C2910058 | `Diode_SMD:D_SOD-123` | 1 (K) QSW_GATE_BIAS / 2 (A) GND |
| R9 | 2.2 kΩ | `Resistor_SMD:R_0603_1608Metric` | 1 QSW_GATE_BIAS / 2 QSW_GATE |
| D1 | optional **DNP** unidirectional TVS, exact part not selected | `Diode_SMD:D_SMB` | 1 (K) PV_PLUS / 2 (A) GND |
| R23 | optional **DNP** 10 Ω **TBD** gate-switch RC snubber | `Resistor_SMD:R_1206_3216Metric` | 1 SHUNT_RETURN (Q1 D) / 2 SNUBBER_MID |
| C23 | optional **DNP** 10 nF / 200 V **TBD** gate-switch RC snubber | `Capacitor_SMD:C_1206_3216Metric` | 1 SNUBBER_MID / 2 GND (Q1 S) |

**R23+C23 form a series RC across Q1 drain–source, not a permanent resistive DC path.** Value, capacitor voltage stress, resistor pulse energy and package remain explicitly experimental, unqualified placeholders. Neither Snubber component nor TVS D1 is part of the populated Rev-0 BOM.

The selected TDK C1/C21/C22 part has nominal 4.7 µF but substantially lower capacitance at 50–60 V due to DC bias. Three in parallel is an **engineering prototype choice**, not a full temperature/aging-guaranteed effective-capacitance rating.

## Static validation performed on the revised source

The source file was tokenized as KiCad S-expressions and cross-referenced against its embedded project-local `lib_symbols` using each placed symbol's rotation and pin positions. Direct top-level net labels and explicit `no_connect` positions were matched at symbol pin endpoints. UUIDs and reference designators were checked for uniqueness.

| Check | Prior main | Revised main |
| --- | ---: | ---: |
| Placed symbol instances | 61 | **65** |
| Total instance pins | 185 | **193** |
| Local net labels | 160 | **168** |
| Previously existing pin-to-net assignments changed | 0 | **0** |
| New unassigned symbol pins | — | **0** |
| Label endpoints lacking a symbol pin | — | **0** |
| Duplicate UUIDs / reference designators | — | **0** |
| D1, R23, C23 DNP flags | — | **yes** |

* In the embedded `PanelLog:Zener` symbol, pin 1 is **K**, pin 2 is **A**, and D2's cathode is on QSW_GATE_BIAS. D1 cathode is on PV_PLUS.
* New input capacitors C21/C22 are correctly in parallel with C1 (PV_PLUS/GND).
* The passive gate-bias chain is still PV_PLUS → R8 → QSW_GATE_BIAS → R9 → Q1 G; active Q2 pull-down and zener clamp remain attached to QSW_GATE_BIAS.
* The return high-current path remains MPPT_MINUS → RSH1 → SHUNT_RETURN → Q1 drain → local GND.
* The optional snubber is correctly inserted between SHUNT_RETURN and GND, **in series R23 then C23**.
* INA228 shunt/voltage measurement nets and all other existing pin assignments are unchanged.

## What the static check does NOT establish

- **KiCad 10 file load / serialization / ERC correctness**: no KiCad 10 available to the execution environment. Must run on a machine with KiCad 10 installed.
- Physical footprint pad numbering and manufacturer package/landpattern, especially D2/D1 polarity; source net labels establish symbol polarity but **not physical board pin-1 confirmation**.
- PCB footprint layouts, placement, routing, 15–20-A copper thermals, DRC.
- Electrical gate turn-off SOA with R9=2.2 kΩ, 2N7002 hot leakage, gate drive at cold/dawn conditions.
- High-frequency transient ringing, 85-V INA228 voltage limit, 100-V LM5164/Q1 voltage limit.
- The guaranteed effective 3× TDK capacitance at full temperature and lifetime.

## Next native validation

On a machine with KiCad 10 (native CLI):

```sh
kicad-cli sch erc hardware/kicad/panellog.kicad_sch -o /tmp/panellog-erc.rpt
kicad-cli sch export netlist hardware/kicad/panellog.kicad_sch -o /tmp/panellog.net
```

For a system Flatpak install as in the BatteryFlex development machine, the CLI is commonly exposed via:

```sh
flatpak run --command=kicad-cli org.kicad.KiCad sch erc hardware/kicad/panellog.kicad_sch -o /tmp/panellog-erc.rpt
```

Check the actual installed Flatpak package/command syntax before executing. **Inspect all ERC diagnostics and independently confirm 1=K/2=A on D_SOD-123 and D_SMB footprints** as well as capacitor/resistor pad numbering. After opening/resaving, diff the normalized schematic to preserve all intended connections. Keep this as an explicit release gate.

## Datasheet and sourcing references

* [TDK C22877898 at LCSC](https://www.lcsc.com/product-detail/C22877898.html)
* [JSCJ MMSZ4697 C2910058 at LCSC](https://www.lcsc.com/product-detail/C2910058.html)
* [KiCad footprint library Diode_SMD](https://kicad.github.io/footprints/Diode_SMD)
* [TI LM5164](https://www.ti.com/lit/ds/symlink/lm5164.pdf)
* [TI INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf)
