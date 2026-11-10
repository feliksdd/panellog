# PanelLog

PanelLog misst und schaltet den DC-Ertrag eines einzelnen PV-Moduls. Ein Knoten sitzt zwischen Modul und MPPT-Eingang, versorgt sich aus dem Modul und soll seine Daten per Zigbee an BatteryFlex übertragen. Pro Modul wird ein eigener Knoten eingesetzt; verschiedene MPPT-Eingänge bleiben elektrisch getrennt.

## Funktionen

- Modulspannung, Modulstrom sowie daraus berechnete DC-Leistung und Energie.
- Modultemperatur über einen externen Pt1000; lokale Platinentemperatur über NTC.
- Langsame Ein-/Ausschaltung des Modulstroms über einen Low-Side-MOSFET mit Spannungsrückmeldung.
- Optional ein kabelgebundener [POA-Sensor](https://github.com/feliksdd/poa-sensor) zur Einstrahlungsmessung, versorgt über 3,3 V und angeschlossen an einen separaten I²C-Bus.

## Aufbau

| Baugruppe | Ausführung |
|---|---|
| Controller / Funk | ESP32-C6-WROOM-1-N4 |
| Strom und Spannung | INA237AIDGSR, HoVB4026-Vierleiter-Shunt mit 1 mΩ |
| Modulschalter | IPT015N10N5, passiv eingeschaltet, aktiv ausgeschaltet |
| Versorgung | LM5163DDAR, direkt vom Modul auf nominal 3,3 V, bis 500 mA |
| Temperatur | Externer M222 Pt1000 Klasse A; interner 10-kΩ-NTC |
| Mechanik | Vierlagige Platine 118 × 90 × 1,6 mm, Kradex Z74JH ABS |

Der PV-Pluspol ist durchverbunden. Der Rückstrom fließt vom MPPT-Minuspol über Shunt und Q1 zum Modul-Minuspol. Die Elektronik liegt auf Modul-Minus und bleibt bei ausgeschaltetem Q1 versorgt.

Der Spannungsentwurf umfasst ein einzelnes Modul bis 60 V DC; die Versorgung startet typisch bei etwa 9 V. 15 A ist der ursprüngliche Strom-Auslegungspunkt, 20 A ein thermischer Betrachtungsfall. Daraus folgt keine gemessene Dauerstromfreigabe. Kalte Leerlaufspannung und Schaltspitzen der konkreten Modul-/MPPT-Kombination müssen innerhalb der Bauteilgrenzen bleiben. Q1 dient der Ertragsregelung; eine sichere Trennstelle entsteht dadurch nicht.

## Dokumentation

| Inhalt | Datei |
|---|---|
| Schaltungsfunktion und Bauteilwerte | [Schaltung](docs/schaltung.md) |
| Berechnungen, Messbereiche und Genauigkeit | [Auslegung](docs/auslegung.md) |
| Verdrahtung, Montage, Kalibrierung und Betrieb | [Anwendung](docs/anwendung.md) |
| POA-Kabel und Bestückungsvarianten | [POA-Schnittstelle](docs/poa_schnittstelle.md) |
| KiCad-Projekt und Lagenaufbau | [Hardware](hardware/README.md) |
| Stückliste und Fertigungsunterlagen | [Bestückung](bom/README.md) |
| Pinbelegung und Softwareumfang | [Firmware](firmware/README.md) |
| Vorhandene Gehäuse- und Bauteilmodelle | [3D-Modelle](hardware/3dmodels/README.md) |

Schaltplan und PCB in [hardware/kicad](hardware/kicad/) definieren die Hardware. Das Repository enthält einen POA-Treiberbaustein, aber noch keine vollständige PanelLog-Firmware mit Zigbee-/BatteryFlex-Anbindung.
