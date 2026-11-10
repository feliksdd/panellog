# POA-I²C-Schnittstelle — aktualisiert 2026-11-10

Die Anschlussentscheidung ist umgesetzt: maximal ein POA pro PanelLog, maximal 3 m, drei verdrillte Paare, direkte Lötpads. Maßgeblich ist [POA architecture.md](https://github.com/feliksdd/poa-sensor/blob/main/docs/architecture.md), Revision 0.3.

## Aktuelle Pins

SDA: GPIO22 / C6-WROOM-Modulpad 20. SCL: GPIO23 / Modulpad 21. J8: 1=geschützte 3V3, 2=GND, 3=SDA, 4=GND, 5=SCL, 6=GND; jeweils 1/2, 3/4 und 5/6 verdrillen und 1:1 mit POA J1 verbinden. INA237 bleibt auf GPIO6/GPIO7. Vorherige MINI-Angaben GPIO21/22 nicht mehr verwenden. Bestehende Firmware ist damit noch nicht automatisch angepasst; diese Änderung enthält keine Firmwareentwicklung.

## Versorgung und DIRECT-Bestückung

R36 ist aus dem Schaltplan entfernt. U5 TPS2553DBVR (C55266), SOT-23-6: IN=1/EN=3/ILIM=5 an +3V3; GND=2; OUT=6 an POA_VDD_CABLE; FAULT=4 NC. ILIM direkt an IN: 50–100 mA, typisch 75 mA laut TI. C27=1 µF an IN; C28=1 µF an OUT. Der begrenzte Ausgang speist J8.1 und R34/R35. Keine Resetfestigkeit ohne Kurzschluss-/Sendeburstmessung behaupten.

DIRECT: R32/R33=0 Ω bestückt; R34/R35=2,2 kΩ bestückt an POA_VDD_CABLE; R30/R31, U4 und C26 unbestückt. Die Kabel-Pull-ups gehen somit beim Einbruch der geschützten Versorgung mit herunter. MCU ausschließlich Open-Drain/hochohmig betreiben, interne Pull-ups aus. Auf dem POA sind R6/R7 bestückt und sämtliche zusätzlichen Pull-ups unbestückt.

## Option BUFFERED

An beiden Enden alle direkten Bypässe entfernen (Host R32/R33; POA R6/R7). Host U4/C26 sowie R30/R31=2,2 kΩ bestücken; Host R34/R35 von 2,2 kΩ auf 1 kΩ ändern. POA U2/C5, R8/R9=1 kΩ und R10/R11=2,2 kΩ bestücken. C26=100 nF gehört unmittelbar an U4. Der Host-Buffer wird ebenfalls von POA_VDD_CABLE gespeist. Diese Option bleibt bis zur Spannungs-/VOL-/Ausfallprüfung unqualifiziert und DNP.

## Stand und nächste Arbeit

Die Anpassung betrifft **nur Schaltplan, Symbole, BOM und Dokumentation**. Das vorhandene PanelLog-PCB und seine JLCPCB-Dateien enthalten weiter den alten R36-Aufbau und die bisherige Pull-up-Bestückung. U5/C27/C28/C26 sind dort noch nicht platziert/geroutet. Vor Fertigung: Schaltplan nach PCB übernehmen, strombegrenzten Kabelzweig und ESD-Rückführung routen, alle Lagen prüfen und native DRC einschließlich Schaltplan-Parität ausführen. Keine neue Fertigungsfreigabe.

Start 25 kHz, 2,2 kΩ, Lastziel ≤400 pF pro Leitung. Anstiegszeit ≤1 µs, VOL und Wechselrichter-Störfestigkeit am realen Kabel prüfen. Versorgungskurzschluss kann bis zu 100 mA plus dynamische Umladung beanspruchen; Haupt-3V3 dabei messen. Keine galvanische Isolation und keine unabhängige POA-Nachtversorgung.

Quelle TPS2553: https://www.ti.com/lit/ds/symlink/tps2553.pdf

Projektbibliothek: Die vorhandenen HOVB- und C6-WROOM-Symboldefinitionen sind aus dem aktuellen Schaltplancache synchronisiert; Pinbelegung und Schaltplansymbolgeometrie dieser Bauteile bleiben erhalten.
