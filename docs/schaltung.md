# Schaltung

## Leistungspfad und Bezugspotential

J6 verbindet den Modul-Pluspol mit `VDC`, J7 den Modul-Minuspol mit `GND`. J2 führt `VDC` zum MPPT-Pluspol. Vom MPPT-Minuspol an J5 fließt der Rückstrom durch RSH1 nach `SHUNT_RETURN`, anschließend durch Q1 nach `GND`. Versorgung und Spannungsmessung sind direkt am Modul angeschlossen.

RSH1 hat vier getrennte Anschlüsse: 1 = Force MPPT_MINUS, 2 = Force SHUNT_RETURN, 3 = Sense+, 4 = Sense−. Die Sense-Leitungen führen unabhängig vom Leistungskupfer zum INA237. Zwischen Force- und Sense-Pads darf keine externe Kupferbrücke liegen.

## Versorgung

U1, LM5163DDAR, erzeugt die gemeinsame 3,3-V-Schiene für Controller, INA237 und Sensoren.

| Netzwerk | Bauteile / Funktion |
|---|---|
| Eingang | C1/C21/C22 je 4,7 µF / 100 V X7R; C2 100 nF / 100 V; C3 10 µF / 100 V |
| Unterspannung | R1 1 MΩ / R2 200 kΩ am EN/UVLO-Eingang |
| Einschaltzeit | R3 27,4 kΩ am RON-Eingang |
| Ausgang | L1 Sumida CDRH127/LDNP-680MC, 68 µH; C5/C6 je 22 µF / 25 V |
| Rückführung | R4 174 kΩ / R5 100 kΩ |
| Ripple-Einspeisung | R6 150 kΩ, C8 3,3 nF, C9 150 pF |
| Bootstrap | C4 2,2 nF |
| Controller-Pufferung | C15 22 µF und lokale 100-nF-Kondensatoren |

PGOOD liegt mit R7 47 kΩ an 3,3 V und geht an GPIO19. Das Exposed Pad von U1 liegt auf GND. D1 ist ein unbestückter TVS-Platzhalter; er stellt keinen vorhandenen Überspannungsschutz dar.

## Strom- und Spannungsmessung

U2, INA237AIDGSR, misst den Spannungsabfall am HoVB4026-Shunt RSH1 (1 mΩ, ±1 %, ±50 ppm/K, 5 W). IN+ liegt über R11 an Sense+, IN− über R12 an Sense−. Beide Widerstände haben 10 Ω; C10 mit 100 nF liegt differentiell zwischen den Eingängen. VBUS erfasst `VDC` über R13 10 Ω und C11 10 nF gegen GND.

A0/A1 liegen an GND: I²C-Adresse 0x40. SDA/SCL führen zu GPIO6/7, mit je 10 kΩ Pull-up (R14/R15). ALERT geht mit Pull-up R16 an GPIO10. Die INA237-Die-Temperatur ist zusätzlich digital verfügbar.

Die gemessene Spannung ist die Modulspannung. Der Shunt erfasst den MPPT-Zweig; der Eigenverbrauch der direkt aus dem Modul gespeisten Elektronik liegt außerhalb dieses Strommesspfads. U × I beschreibt daher die Leistung des MPPT-Zweigs am Modulbezug, einschließlich der nachfolgenden Leitverluste, nicht die gesamte vom Modul erzeugte Leistung.

## Modulschalter und Rückmeldung

Q1, IPT015N10N5, schaltet den negativen Leistungspfad. R8 47 kΩ speist den Gate-Bias aus VDC; D2 MMSZ4697 begrenzt ihn nominal auf 10 V. R9 2,2 kΩ verbindet den Bias mit dem Q1-Gate. Q2, 2N7002, zieht den Bias bei `SWITCH_OFF = HIGH` nach GND und sperrt Q1. R10 100 kΩ hält das Q2-Gate bei hochohmigem Controllerausgang niedrig.

Bei Reset/hochohmigem GPIO soll Q1 passiv leiten. Ein dauerhaft hoher GPIO oder defekter Gatepfad kann Q1 dennoch ausgeschaltet halten. Q1 ist ein einzelner MOSFET: Seine Bodydiode lässt eine Stromrichtung weiterhin zu. Die unbestückten R23/C23 reservieren einen RC-Snubber zwischen Drain und GND.

R27 1 MΩ zieht den Drain schwach nach VDC. R28 1 MΩ / R29 27,4 kΩ teilen seine Spannung für GPIO1; C25 100 nF filtert das Signal. Damit ist ein offener Q1 auch ohne angeschlossenen Wechselrichter beobachtbar. Der hochohmige Pfad überbrückt Q1 absichtlich; galvanische Trennung besteht nicht.

## Temperatur und Versorgungserfassung

| Kanal | Beschaltung | Controller |
|---|---|---|
| Modultemperatur | R18 14,7 kΩ, 0,1 %, 10 ppm/K von 3,3 V zum externen Pt1000 an J3; R19 1 kΩ / C18 100 nF als ADC-Filter | GPIO4 |
| Platinentemperatur | R21 10 kΩ von 3,3 V zum NTC RT2 gegen GND; R22 1 kΩ / C20 100 nF als ADC-Filter | GPIO5 |
| Versorgung | R20/R24 je 100 kΩ; C19 100 nF parallel zum unteren Widerstand | GPIO0 |

RT1 ist ein externer M222 Pt1000 Klasse A (32208572, C17472362), kein auf der Platine bestücktes Bauteil. RT2 ist ein TDK NTCG163JF103FT1S in der Nähe von Q1 und erfasst dessen lokale Platinenumgebung.

## Controller und Erweiterung

U3 ist ein ESP32-C6-WROOM-1-N4 mit 4 MB Flash und integrierter Antenne. R17 10 kΩ / C24 1 µF bilden die EN-Beschaltung. GPIO8/9 haben je 10 kΩ Pull-up; J4 führt UART, EN und BOOT heraus. USB ist nicht herausgeführt.

J8 versorgt einen optionalen POA-Sensor und verbindet ihn über GPIO22/23 mit einem eigenen I²C-Bus. Die Standardbestückung verwendet direkte 0-Ω-Brücken. P82B715-Puffer U4 und zugehörige Optionen bleiben unbestückt; siehe [POA-Schnittstelle](poa_schnittstelle.md).
