# Externe 3D-Modelle – recherchierte Revision

**Keine selbst erzeugten Bauteil- oder Gehäusenäherungen mehr.** Die bisherigen `generated/`-Dateien, der Generator und die darauf beruhende Vorschau wurden entfernt. Die aktuelle Baugruppe ist ausdrücklich **unvollständig**: U3, RSH1 und Y1 besitzen noch kein verifiziertes Modell. Lötanschlüsse J1/J2/J3, SWD-Pads J4 und Bohrungen benötigen keinen erfundenen Bauteilkörper.

## Verwendete externe Dateien

| Referenz | Externes Modell | Prüfung und Herkunft |
|---|---|---|
| U1 LM5164DDAR | `manufacturer/TI_DDA0008B.stp` | **Neu am 2026-11-04:** direktes TI-STEP aus der Suchergebniszeile LM5164DDAR → DDA/8 → DDA0008B. Unveränderte Originaldatei, zehn gültige Solids, Körper 3,9 × 4,9 mm, Gesamthöhe 1,57 mm, Anschlussraster 1,27 mm, Gesamtspanne 6,028 mm. Modell steht auf Z=0; keine Skalierung oder Rotation erforderlich. |
| Gehäuse, optional an H1 | `manufacturer/Spelsberg_12741501.stp` | Vom Nutzer bereitgestellte Originaldatei, bytegleich übernommen; sechs Volumenkörper: Unterteil, Deckel, vier Schrauben; 130 × 180 × 62,5 mm. Header: CADENAS, CC BY-ND 4.0. Attribution: Spelsberg/CADENAS, https://www.spelsberg.de/industrieleergehaeuse/mit-/-ohne-metrische-vorpraegungen/12741501/ |
| L1 7447709680 | `manufacturer/Wurth_WE-PD_1210.stp` | Originaldownload aus der Tabellenzeile **7447709680** auf der Würth-WE-PD-Produktseite. 12 × 12 mm, Z=-0,20…9,26 mm. Modellverschiebung Z=+0,20 mm bringt tiefsten Anschluss auf die Platine. Kein 1280-Modell verwenden! |
| C3 EEEFN2A100P | `manufacturer/Panasonic_Size_F.stp` | Offizieller CAD-Link auf der exakten Panasonic-Produktseite: `DS_Alumi_F.zip`, Originaldatei „Ø8 SIZE CODE F.stp“. Geometrie 9,7 mm inklusive Anschlüssen, Sockelbreite 8,3 mm, Höhe 10,201 mm. Modell steht im Original auf Y und wird in KiCad um X=-90° gedreht. |
| Q1 IPT015N10N5 | `standard/Package_TO_SOT_SMD.3dshapes/Infineon_PG-HSOF-8-1.step` | Original KiCad-Bibliotheksmodell der passenden Infineon-Bauform PG-HSOF-8-1; Höhe 2,32 mm. Mit KiCad-Originalfootprint verglichen: dessen Pin 1 bei (-5,25;-4,2) entspricht nach Drehung der Pin-1-Seite des Projektfootprints (-4,2;+5,29). KiCad-Modellrotation Z=-90°. Kein herstellerspezifisch markierter MPN-Körper behauptet. |
| U2 INA228AIDGSR | `standard/Package_SO.3dshapes/MSOP-10_3x3mm_P0.5mm.step` | KiCad-Bibliotheksmodell, passend zur TI-DGS-Bauform: Körper 3 × 3, Anschlussgesamtbreite 4,9 mm, Höhe 0,95 mm (nominales Bibliotheksmodell innerhalb TI-Maximum 1,1 mm), 10 Pins/0,5-mm-Raster, JEDEC MO-187. Der zuerst geprüfte VSSOP-Kandidat mit 1,2 mm Höhe wurde verworfen. |
| Standard-R/C, D1/D2, Q2 | `standard/` | Bisherige originale KiCad-Bauformmodelle, unverändert. Bei noch nicht festgelegter MPN handelt es sich um Bauformzuordnung, nicht MPN-Verifikation. |

Die externen Dateien wurden geometrisch **nicht verändert**. Drehung und Verschiebung werden in der KiCad-Zuordnung bzw. der Baugruppenplatzierung angewendet. Die Original-Geometrien enthalten zum Teil selbst vereinfachte Herstellerdetails; das ist etwas anderes als projektseitig geschätzte Abmessungen.

## Noch fehlend / genaue Recherche

| Referenz | Ergebnis | Warum nicht eingesetzt |
|---|---|---|
| U3 E73-2G4M08S1C | Vorhandenes Community-STEP in AcheronProject/acheron_3D; Quelle laut Projekt GrabCAD. https://github.com/AcheronProject/acheron_3D | Datei tatsächlich heruntergeladen und als sechs Solids geprüft: 18,288 × 13 × 3,05 mm inklusive Unterseite. Außenlänge weicht von Ebytes 18-mm-Angabe ab. Ohne sichere Erklärung der Abweichung nicht zugeordnet und nicht im Projekt als passend ausgegeben. SnapMagic listet den MPN ebenfalls, direkter verifizierter Download fehlt. |
| RSH1 BVB-M-R0007-1.0 | Hersteller-/Distributordaten und Modellportale recherchiert. Exakter MPN: https://www.digikey.com/en/products/detail/isabellenhuette-usa/BVB-M-R0007-1-0/16836861 | Kein verifizierter frei herunterladbarer STEP für den genauen vierpoligen BVB-Typ gefunden. Kein gewöhnliches 2725-Widerstandsmodell als Ersatz. EasyEDA-Produkt-API lieferte 403; keine Umgehung versucht. |
| Y1 Jauch JTX310 | SamacSys/ComponentSearchEngine listet die JTX310-Familie mit 3D-Angebot: https://componentsearchengine.com/part-view/Q%200%2C032768-JTX310-12%2C5-20-T1-HMR-LF/Jauch%20Quartz | Anbieterdownload erfordert Benutzerzugang. Weiterer GitHub-Kandidat rhinodavid/rhinodavid_kicad enthält JTX310.step, aber keine erkennbare Weitergabelizenz; daher nicht übernommen. Jauch nennt 3,2 × 1,5 × 0,9 mm. |

Damit wird keine vollständige 3D-Bestückung oder vollständige Kollisionsfreiheit behauptet. Für die drei offenen Positionen werden passende Originaldateien oder ein regulärer Anbieterdownload benötigt.

## Gehäuseplatzierung

Die Originaldatei besitzt X=−65…65, Y=−90…90, Z=−44,5…18 mm. Die vier inneren Befestigungsachsen liegen bei X=±45/Y=±50 mm; Domoberkante Z=−33,5 mm. Das bestätigt das vorhandene Platinenraster **100 × 90 mm** nach Drehung ins Querformat.

Physische Baugruppenplatzierung: Rz=+90°, Verschiebung (75;−55;+23,9) mm, PCB-Oberseite Z=0, Unterseite Z=−1,6. Domoberkanten liegen damit bei Z=−9,6 mm: 8-mm-Abstandhalter bis zur PCB-Unterseite. Keine neu erfundenen Dommaße mehr.

In KiCad ist das unveränderte Original am **H1 → Eigenschaften → 3D-Modelle** hinterlegt und standardmäßig ausgeblendet. Die abweichenden Transformationswerte dort berücksichtigen den H1-Ursprung und die KiCad-Modellrotationskonvention. Ein Modell enthält bereits den Deckel; es gibt keine künstlich getrennten Gehäusehälften mehr.

Die Baugruppe lässt sich mit `python tools/export_3d_assembly.py` aus dem aktuellen Board und der unveränderten Original-Gehäusegeometrie erzeugen (KiCad 10 CLI und CadQuery). Drei Bauteilmodelle bleiben fehlend. Der Exportgenerator erzeugt keine Ersatzgeometrie. Veraltete Baugruppen und Vorschauen wurden entfernt; für den aktuellen GitHub-Stand wird kein bereits erneuerter Gesamtexport behauptet.

## Downloads / Nachweise / Lizenzen

- Würth-Produkt: https://www.we-online.com/en/components/products/WE-PD?artnr=7447709680
- Tatsächlicher Download: https://www.we-online.com/components/products/download/Download_WE-PD_1210_STP%20%28rev1%29.stp
- Panasonic-MPN/CAD: https://industrial.panasonic.com/sa/products/pt/aluminum-cap-smd/models/EEEFN2A100P/cad
- Panasonic-Datei: https://industrial.panasonic.com/ww/system/files/data/download/cad/DS_Alumi_F.zip
- KiCad-Originale: https://github.com/KiCad/kicad-packages3D ; Lizenz `standard/LICENSE.md` (CC BY-SA 4.0 mit Bibliotheksausnahme); Originalheader erhalten.
- Gehäuse: vom Nutzer bereitgestellt; CC BY-ND 4.0 laut Originalheader. Originaldatei unverändert, Herkunftsangabe oben. https://creativecommons.org/licenses/by-nd/4.0/
- TI-Gehäusebezeichnung U2: https://www.ti.com/product/INA228
- `validation.json`: SHA256 und tatsächliche Solid-Importprüfung der vorhandenen STEP-Dateien. `model_inventory.json`: Zuordnung/Missing-Status je Referenz.
- Frühere KiCad-10.0.8-Berichte gehören zum damaligen Layoutstand. Nach dem neuen Eingangscommit `130ec6e` wurde hier kein ERC/DRC ausgeführt; KiCad 10 CLI ist in dieser Ausführungsumgebung nicht verfügbar.

## Nachrecherche 2026-11-04

Der direkte TI-Paketdownload löst die bisherige U1-Lücke ohne Ultra-Librarian-Konto:
- Produktzuordnung: https://www.ti.com/packaging/docs/searchproductbypackage.tsp?orderablePartNumber=LM5164DDAR&packageDesignator=&pinCount=&results=results
- Originaldatei: https://webench.ti.com/cad/dlbxl.cgi/newstep/DDA0008B.stp
- TI-Paketportal: https://www.ti.com/design-development/packaging.html

Ein zusätzlich geprüfter KiCad-Kandidat `HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm.step` besitzt nur 1,1 mm Höhe und wurde ebenfalls nicht übernommen. Ein passender Name allein reicht nicht aus.

Die erneute Recherche der Ebyte-Downloadliste und Produktseite, der Isabellenhütte-BVB-Produktseite und des Jauch-Produktportals ergab für U3/RSH1/Y1 keinen zusätzlich verifiziert herunterladbaren Original-STEP. Das ist kein Nachweis, dass solche Dateien nicht existieren. Die drei Positionen bleiben sichtbar als fehlend dokumentiert; es werden keine geschätzten Ersatzkörper eingefügt.

- Ebyte: https://www.cdebyte.com/products/E73-2G4M08S1C/3 und https://www.ebyte.com/datadown/SPISOC.html
- BVB: https://www.isabellenhuetteusa.com/product/bvb/ und https://www.isabellenhuette.com/hubfs/Files/Data-sheets/BVB.pdf
- Jauch: https://www.jauch.com/en-GB/products/frequency_control_components

Die neu beigefügte Gehäusedatei wurde per SHA256 mit dem Projektmodell verglichen: identisch (`9ef3a4fc45162f3478714c5e47d83ea0cc0a5cb1739be936485dd786eb6a6808`). Die Modellzuordnungen wurden auf GitHub-Commit `130ec6e6e619249bba21afbcd5ff13154846e356` mit den neuesten Positionierungs- und Routingänderungen angewendet. Alle 65 Footprints wurden abgeglichen: Nur die Modellknoten wurden ersetzt. Leiterbahnen, Vias, Zonen, Zeichnungen und alle übrigen Footprint-Inhalte bleiben erhalten. Nachweis: `integration_2026-11-04.json`. Ein erneuter Gesamtexport steht für diesen Stand noch aus.
