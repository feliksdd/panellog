# 3D-Modelle

Die tatsächlich eingebundenen Modelle stehen in den Modellzuordnungen von [panellog.kicad_pcb](../kicad/panellog.kicad_pcb). `manufacturer/` enthält bereitgestellte Hersteller-/Gehäusedateien; `standard/` enthält KiCad-Bauformmodelle.

| Bauteil | Modell / Einbindung im PCB |
|---|---|
| U3 WROOM-1 | `manufacturer/ESP32-C6-WROOM.step`, projektbezogener Pfad |
| U1 LM5163, DDA | `manufacturer/TI_DDA0008B.stp`, projektbezogener Pfad |
| C3 Panasonic Größe F | `manufacturer/Panasonic_Size_F.stp`, projektbezogener Pfad |
| U2 INA237, DGS10 | KiCad MSOP-10-Bauformmodell unter `standard/` |
| Q1 IPT015N10N5 | KiCad PG-HSOF-8-1-Bauformmodell unter `standard/` |
| Standard-R/C, Dioden, Q2, U4 | Überwiegend KiCad-10-Systembibliothek `${KICAD10_3DMODEL_DIR}` |
| L1 | Absoluter lokaler Pfad auf `CDRH127_470M.step`; Variantenmodell, kein Nachweis der exakten 68-µH-LD-Ausführung |
| RSH1 | Absoluter lokaler Pfad auf `BVB-M-R0007.STEP`; Variantenmodell, kein exaktes HoVB4026-Modell |

Die absoluten L1-/RSH1-Pfade sind auf anderen Rechnern nicht portabel. Ihre Dateien liegen im Verzeichnis `manufacturer/`; ihre Geometrie belegt keine exakte Bauteilpassung. PCB-Lötflächen und Montagebohrungen benötigen keinen Bauteilkörper.

Kradex-Unterteil und -Deckel liegen als `manufacturer/Kradex_Z74_base.step` und `manufacturer/Kradex_Z74_cover.step` vor. Im PCB sind sie nicht an H1 eingebunden. Die mechanischen Originaldaten befinden sich unter [mechanical/](../mechanical/). Für vollständige Baugruppen-/Kollisionsdarstellung sind Modellzuordnung, Schrauben und Kabel ergänzend zu berücksichtigen.

Lizenzen: [KiCad-Standardmodelle](standard/LICENSE.md), [Espressif-Bibliothek](../footprints/ESPRESSIF-LICENSE.md). Lizenztexte und Originalhinweise der Quelldateien beibehalten.
