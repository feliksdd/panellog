# PanelLog – aktuelle Stückliste

Die [Auswahlstückliste](panellog_rev0_selection.csv) führt Referenzen, MPNs, LCSC-Nummern und Qualifikationsstatus. Die [Beschaffungsstückliste für vier Platinen](panellog_c6_procurement_4boards.csv) gruppiert die bestückten Teile; Bestellmengen müssen zusätzlich Mindestmengen und Bestückungsverluste berücksichtigen.

## Kostenrevision vom 06.11.2026

- R8: VO SCR1206F47K, C5140109, 47 kΩ ±1 %, 250 mW, 200 V, 1206.
- C1/C21/C22: FH 1210B475K101NT, nun C7500895 statt C2840282; identische Herstellerteilenummer.
- Q2: onsemi 2N7002 C124475 bleibt. JSCJ C8545 ist mangels garantierter 3,3-V-/Heißkennwerte noch nicht übernommen. Auch die bisherige Auswahl erfordert die dokumentierte Gatepfad-Qualifikation.
- L1: Würth 7447709680 bleibt; Sumida C2452974 benötigt eine Bestätigung der zulässigen Betriebsspannung sowie ein angepasstes Landpattern mit Sperrfläche.
- Damaliger Stand: INA228 und 0,7-mΩ-Shunt; seit 07.11. ersetzt, siehe unten. IPT015N10N5 bleibt unverändert.

Prüfung, Preise und offene Punkte: [Kosten-Folgeprüfung](../docs/cost_followup_2026-11-06.md). Vorherige Änderungen: [C6-/LM5163-Revision](../docs/c6_cost_revision_2026-11-06.md).

## Qualifikationsstand

Dies ist weiterhin ein Prototypenstand. Insbesondere FH-Kapazität unter DC-Bias, Gatepfad über Temperatur, Schalttransienten, Thermik und Kabelzugentlastung müssen praktisch qualifiziert werden. D1 und R23/C23 sind DNP. Y1/C16/C17 sind entfernt. J4 ist die UART-/BOOT-Pogo-Schnittstelle.

Die letzte native KiCad-Prüfung vor dieser reinen Bestelldatenänderung ergab ERC 0 Fehler/0 Warnungen, keine offenen PCB-Verbindungen und keine Schaltplan-Paritätsfehler. Die vorhandenen DRC-Restbefunde stehen im [C6-Review](../hardware/kicad/review_2026-11-06/validation.json). Diese Folgeänderung wurde strukturell geprüft; kein neuer nativer ERC/DRC ausgeführt.

Gehäuse, Befestigung und Kabeldurchführungen: [Mechanikstückliste](../docs/enclosure_kradex_z74.md). Historische CAD-Befunde vom Oktober sind im [damaligen Review](../hardware/kicad/FOOTPRINT_BOM_REVIEW_2026-10-29.md) dokumentiert.

## Strommessung 07.11.2026

U2: INA237AIDGSR, C2864837. RSH1: Milliohm HOVB4026-5W-1mR-1%, C481535, 1 mΩ, 5 W, ±1%, ±50 ppm/K, vier Anschlüsse. Beide CSVs aktualisiert. [Änderung und aktuelle Prüfung](../docs/current_sensor_2026-11-07.md).
