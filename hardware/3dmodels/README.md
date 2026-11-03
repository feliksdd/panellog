# 3D-Modelle / PanelLog

Alle Dateien sind relativ zum Projekt verknüpft (`${KIPRJMOD}/../3dmodels/…`). KiCad 10 benötigt dafür keine systemweit installierte 3D-Bibliothek.

- **standard/**: neun Originalmodelle aus KiCad/kicad-packages3D, https://github.com/KiCad/kicad-packages3D/tree/master, abgerufen 2026-11-03. Lizenz und Ausnahmeregelung in `standard/LICENSE.md`; Ursprungsheader in STEP-Dateien erhalten. Generische Gehäusemodelle, keine Zusicherung der exakten bestellten MPN-Ausführung.
- **generated/**: zwölf eigene, vereinfachte STEP-Modelle. Erzeugbar mit `python tools/generate_3d_envelopes.py` (CadQuery 2.7). Projektgenerierte Modellgeometrien und Generator stehen unter CC0-1.0. Keine Hersteller-CAD-Dateien.
- **assembly/PanelLog_in_Spelsberg_ENVELOPE.step**: bestückte Platine im vereinfachten geschlossenen Gehäuse; Boden und Deckel getrennte Baugruppenobjekte. **Kein fertigungstaugliches Gehäusemodell**.
- **assembly/preview.png**: offene Vorschau mit ausgeblendetem Deckel.
- **model_inventory.json**: Zuordnung aller elektrischen Footprints. H1 enthält zusätzlich die optionalen Gehäusemodelle; Montagebohrungen H2–H4 und SWD-Pads J4 benötigen keinen eigenen Bauteilkörper.
- **validation.json**: SHA256-Prüfsummen und erfolgreiche STEP-Solid-Importprüfung sämtlicher STEP-Dateien.

## Verwendung in KiCad

`hardware/kicad/panellog.kicad_pcb` öffnen und 3D-Ansicht starten. Gehäusemodelle sind im Footprint **H1 → Eigenschaften → 3D-Modelle** hinterlegt, standardmäßig ausgeblendet. Zum Einblenden beide Modelle aktivieren. Boden und Deckel sind bereits im richtigen Projektkoordinatensystem ausgerichtet; die Modellverschiebung in H1 kompensiert dessen Lage. H1 bleibt ein mechanischer Footprint; die Gehäusezuordnung ändert keine Netze.

Direkt angelötete Kabel an J1/J2 und J3 erscheinen als kurze gerade Ansätze. J4 sind unbestückte interne SWD-Pads. Die DNP-Bauteile D1/R23/C23 haben ebenfalls Modelle, werden aber im STEP-Bestückungsexport entsprechend DNP ausgelassen. Sichtbarkeit in KiCad hängt von der DNP-Anzeigeeinstellung ab.

## Herkunft und Genauigkeit

| Bauteil | Modell | Genauigkeit / Einschränkung |
|---|---|---|
| R/C, D1/D2, Q2 | KiCad-Originalmodelle | Generische Standardbauformen; MPN-spezifische Höhe gesondert prüfen |
| U1 LM5164, U2 INA228 | Eigene Gehäuse-/Leadmodelle | Grundriss an DDA/DGS-Footprint orientiert; Leads vereinfacht; Höhen Schätzwerte |
| Q1 IPT015N10N5 | Eigene TOLL-Hüllgeometrie | Body 10,3 × 11,7; Bodyhöhe 2,3 mm als Vorschauwert; Leads vereinfacht |
| RSH1 BVB | Eigene Hüllgeometrie | 6,9 × 6,6; Vorschauhöhe 1,6 mm, nicht mechanisch freigegeben |
| L1 7447709680 | Eigene Hüllgeometrie | Grundriss 12,5-mm-Durchmesser, Höhe 8 mm als Vorschauwert |
| C3 Panasonic | Eigene Elko-Hüllgeometrie | Ø8 × 10,2 mm einschließlich Sockel; Lötanschlüsse vereinfacht |
| U3 E73 | Eigene Modul-Hüllgeometrie | 13 × 18 mm; Platine 0,8 mm, Aufbauten bis 3 mm als Vorschauwert, Antenne symbolisch |
| Y1 | Eigenes 3215-Hüllmodell | 3,2 × 1,5 × 1,0 mm als Vorschauwert; vorheriger KiCad-Dateiname war nicht auflösbar |
| J1/J2/J3 | Eigene Kabelansätze | Illustrativ; keine festgelegte Biegeradius-/Kollisionsgeometrie |
| Spelsberg 12741501 | Eigene Boden-/Deckelhülle | Außen 180 × 130 × 62,5; Wände, Dome, Deckel und Rippen vereinfacht; keine Dichtung, Gewinde, Rastungen oder Durchführungsbohrungen |

Original-Spelsberg-CAD ist laut Hersteller nur über meinSpelsberg erhältlich. Deshalb ist das beigefügte Modell ausdrücklich eine selbst erzeugte Vorschau anhand der gemeinsamen Maßzeichnung M-TK-1813-flach-m. Es ist für Ansichten und grobe Platzkontrolle geeignet. Schraubdomdetails, alle Bauteilhöhen, Kabelverschraubungen, Biegeradien und Toleranzen müssen vor einer mechanischen Freigabe mit tatsächlichen Herstellerdaten oder am Muster geprüft werden. Das Modell behauptet keine verifizierte Kollisionsfreiheit.

Quellen:
- KiCad: https://github.com/KiCad/kicad-packages3D
- Spelsberg: https://www.spelsberg.de/industrieleergehaeuse/mit-/-ohne-metrische-vorpraegungen/12741501/
- CAD-Zugang: https://www.spelsberg.de/service/downloads/
- Ebyte: https://www.ebyte.com/product/444.html
- Mechanik-Grundlagen der Projektfootprints: `../../docs/review_2026-11-03.md` und `../../docs/enclosure_2026-11-03.md`.

Gesamtexport und Vorschau reproduzieren: `python tools/export_3d_assembly.py` mit `kicad-cli` 10 im PATH, CadQuery 2.7 und Matplotlib. Modellpfade wurden auf Dateiexistenz geprüft, alle 22 STEP-Dateien erfolgreich als gültige Solids importiert. KiCad 10.0.8 DRC: 0 Verstöße / 0 offene Verbindungen / 0 Schaltplanabweichungen; Bericht unter `hardware/kicad/model_review_2026-11-03/`.
