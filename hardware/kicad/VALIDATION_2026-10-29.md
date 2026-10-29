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


## Re-audit of uploaded native KiCad ERC (13:03:59, 2026-10-29)

Real KiCad 10 reported **100 findings: 35 errors and 65 warnings**:

| Rule | Count | Root cause / corrective action |
| --- | ---: | --- |
| `pin_not_connected` | 13 | Mirrored placement of connection labels against physical pin coordinates |
| `label_dangling` | 10 | Same transformation error |
| `power_pin_not_driven` | 6 | Mostly consequences of dislocated power labels / PWR_FLAG |
| `pin_not_driven` | 6 | Inputs with misplaced labels, some wrongly tied to unrelated nets |
| `ground_pin_not_ground` | 1 | INA228 U2 GND was attached to 3.3 V label, not actual GND |
| `pin_to_pin` | 1 | LM5164 SW incorrectly assigned PGOOD net feeding MCU |
| `endpoint_off_grid` | 61 | Symbol origins were arbitrary decimal millimeter positions; now all placed onto 50-mil (1.27-mm) grid |
| `footprint_link_issues` | 2 | U2 VSSOP-10 footprint missing in installed `Package_SO`; RT2 used nonexisting `Thermistor_SMD` library |

### Actual root cause and correction

The original autogenerated schematic had calculated labeled connection positions using `Y = symbol_Y + pin_local_Y`. KiCad uses `Y = symbol_Y − pin_local_Y` for unrotated placed symbols. Thus even many labels which appeared geometrically to occupy a pin (because of vertically mirrored *other* pins) were connected to the **wrong functional pin**. Critical cases:

* LM5164 U1: VIN was floating; SW, PGOOD, BST, FB mismatched.
* INA228 U2: GND, VS, VBUS, INA_IN+, INA_IN−, SCL/SDA/ALERT mismatched.
* E73 nRF52840 U3: VDD/VDDH, I²C, ADC, SWD and no-connect positions mismatched.
* IPT015N10N5 Q1: gate and drain **interchanged**; 2N7002 Q2 drain/source swapped.

The repair in commit `b1f31a81086f9e0e37cf29fe60faa0fb638767f4` remaps **every** label and NC onto the physical terminal computed from embedded KiCad symbol pin definitions and snaps every symbol instance origin to a **1.27-mm grid**. All old reference designators/UUIDs are preserved.

Source-structural post-repair checks (not native ERC):

* **65 symbol instances, 193 placed pins, 168 labels, 25 NCs**.
* **193/193 pin positions** exactly mapped to one label or explicit NC.
* **0 symbol-pin endpoints off a 1.27-mm grid**.
* No duplicate pin-position assignments.
* Pin-level critical net assertions validated for U1, U2, Q1, Q2 and U3 (including supply and SWD).
* Retained the 3× 4.7-µF/100-V input bank, MMSZ4697 D2, R8=47 kΩ, R9=2.2 kΩ, D1 DNP and Q1 snubber R23/C23 both DNP.

Corrected INA228 U2 expected pin mapping:

| Pin | Signal | Net |
| --- | --- | --- |
| 1 | A1 | GND |
| 2 | A0 | GND |
| 3 | ALERT | INA_ALERT |
| 4 | SDA | I2C_SDA |
| 5 | SCL | I2C_SCL |
| 6 | VS | VCC_3V3 |
| 7 | GND | GND |
| 8 | VBUS | VBUS_SENSE |
| 9 | IN− | INA_INM |
| 10 | IN+ | INA_INP |

### Footprints

* RT2 NTC is 0603; its footprint assignment was changed from missing `Thermistor_SMD:NTC_0603_1608Metric` to installed-standard `Resistor_SMD:R_0603_1608Metric`. A generic 0603 resistor footprint is suitable **as a package candidate**; final NTC manufacturer's landpattern still needs comparison.
* The valid KiCad community `Package_SO:VSSOP-10_3x3mm_P0.5mm` footprint exists upstream, but the uploaded ERC states it was missing in the user's particular KiCad installation. **Not yet repaired.** The attempted creation of a project-local footprint and footprint table failed due connector safety checks; no local footprint file was created. Inspect the installed KiCad footprint libraries and either restore the official footprint or create/verify a project-local footprint. Reference: https://kicad.github.io/footprints/Package_SO.html

### Mandatory repeat

Run KiCad 10 ERC again on the latest `main`. A native **zero-error result has not been demonstrated**; this document claims only static geometric/net reconciliation. In particular evaluate any remaining input-driver assertions and the unresolved U2 footprint. Recheck the actual pin-to-pad mapping and physical footprint against TI INA228 DGS and the other major component datasheets before PCB design.

```bash
git pull --ff-only
flatpak run --command=kicad-cli org.kicad.KiCad sch erc hardware/kicad/panellog.kicad_sch -o panellog-erc-after-fix.rpt
```
