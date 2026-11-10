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
| L1 | Projektbezogener Pfad auf `manufacturer/CDRH127_470M.step`; Variantenmodell, kein Nachweis der exakten 68-µH-LD-Ausführung |
| RSH1 | Projektbezogener Pfad auf `manufacturer/BVB-M-R0007.STEP`; Variantenmodell, kein exaktes HoVB4026-Modell |

L1 und RSH1 verwenden die vorhandenen Variantenmodelle über relative Pfade; die hinterlegten Skalierungen und Ausrichtungen gelten für die Darstellung. Ihre Geometrie belegt keine exakte Bauteilpassung. PCB-Lötflächen und Montagebohrungen benötigen keinen Bauteilkörper.

Kradex-Unterteil und -Deckel liegen als `manufacturer/Kradex_Z74_base.step` und `manufacturer/Kradex_Z74_cover.step` vor und sind am PCB-Footprint H1 über relative Pfade eingebunden. Offset: (45,848 / −40,125 / 46,05) mm, Maßstab 1, Drehung 0°; Deckel mit 25 % Deckkraft. Originalzeichnung, CAD und Montageangaben: [Gehäuse](../../docs/gehaeuse.md). Für vollständige Baugruppendarstellung sind Schrauben und Kabel ergänzend zu berücksichtigen.

Lizenzen: [KiCad-Standardmodelle](standard/LICENSE.md), [Espressif-Bibliothek](../footprints/ESPRESSIF-LICENSE.md). Lizenztexte und Originalhinweise der Quelldateien beibehalten.
