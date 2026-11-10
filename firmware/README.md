# Firmware

Zielplattform ist ESP32-C6-WROOM-1-N4 mit ESP-IDF / ESP Zigbee SDK. Enthalten ist der Baustein [poa_soft_i2c](components/poa_soft_i2c/) mit Software-I²C und ADS1115-Auswertung. Eine vollständige Anwendung mit Build-Projekt, INA237-Treiber, Kalibrierspeicher und Zigbee-/BatteryFlex-Anbindung ist nicht enthalten.

## Pinbelegung der Hardware

| Funktion | GPIO | WROOM-Pad |
|---|---:|---:|
| Pt1000 ADC | 4 | 4 |
| NTC ADC | 5 | 5 |
| Versorgung ADC | 0 | 8 |
| Q1-Drain ADC | 1 | 9 |
| INA237 SDA | 6 | 6 |
| INA237 SCL | 7 | 7 |
| INA_ALERT | 10 | 11 |
| SWITCH_OFF | 18 | 16 |
| PGOOD | 19 | 17 |
| POA SDA | 22 | 20 |
| POA SCL | 23 | 21 |
| UART RX | 17 | 24 |
| UART TX | 16 | 25 |
| Boot-Strap HIGH | 8 | 10 |
| BOOT_N | 9 | 15 |

**Der vorhandene POA-Baustein konfiguriert SDA = GPIO21 und SCL = GPIO22. Vor Verwendung an dieser Platine sind die Definitionen `POA_GPIO_SDA` / `POA_GPIO_SCL` an GPIO22/23 anzupassen.**

## UART und Download

| J4-Pin | Signal |
|---:|---|
| 1 | 3,3-V-Referenz |
| 2 | Target TX → Adapter RX |
| 3 | Target RX ← Adapter TX |
| 4 | EN / RESET_N |
| 5 | GND |
| 6 | BOOT_N |

3,3-V-UART-Pegel verwenden; Pin 1 dient der Referenz, nicht der ungeprüften Fremdspeisung. Downloadmodus: GPIO9 über Pin 6 LOW halten, GPIO8 HIGH belassen und EN kurz zurücksetzen. USB ist nicht herausgeführt. Im PV-System galvanisch getrennte Programmierung verwenden; siehe [Anwendung](../docs/anwendung.md).

## Messung und Regelung

- `SWITCH_OFF` zunächst LOW setzen, dann als Ausgang aktivieren. HIGH sperrt Q1; LOW/hochohmig gibt den passiven Gatepfad frei. OFF-Frist, Mindestverweilzeiten und Watchdog gehören in die Anwendung.
- INA237 an Adresse 0x40: `ADCRANGE = 1`, VSHUNT als vorzeichenbehafteter 16-Bit-Wert mit 1,25 µV/LSB; VBUS mit 3,125 mV/LSB. Strom bevorzugt aus kalibriertem Rohwert berechnen: `I = (Vshunt − Vzero) / Reff`.
- Für Hardware-Stromberechnung ist z. B. CURRENT_LSB = 2 mA mit SHUNT_CAL = 6554 möglich. Konfiguration und Kalibrierung müssen zusammenpassen; das Registerformat dem INA237-Datenblatt entnehmen.
- INA237 hat keine Energie-/Ladungsakkumulatoren. Kalibriertes U × I und I mit monotonen Zeitstempeln integrieren; Lücken, Reset und veraltete Daten kennzeichnen.
- ADC-Spannungen kalibrieren, Einschwingzeiten und Quellimpedanz berücksichtigen. Pt1000 nach IEC 60751, NTC nach Hersteller-R/T-Tabelle auswerten; offene/kurzgeschlossene Sensoren und unplausible Nenner als ungültig behandeln. Formeln siehe [Auslegung](../docs/auslegung.md).
- Abschaltrückmeldung aus Drainspannung und Strom gemeinsam bilden; bei Dunkelheit/ungültigen Daten „unbekannt“ melden. Ansatz für Schwellen und Zeiten siehe [Anwendung](../docs/anwendung.md).

## POA-Baustein

`poa_i2c_init()`, `poa_i2c_recover()` und `poa_read_sample()` bedienen einen unabhängigen Open-Drain-Bus mit externen Pull-ups, nominell 25 kHz und ADS1115-Adresse 0x48. Der Baustein liest Shunt differentiell AIN0−AIN1 (±0,256 V) sowie NTC und Versorgung an AIN2/AIN3 (±4,096 V). Er mittelt acht Strommessungen und liefert Messzeit und Kalibrierkennzeichen.

Defaultwerte sind 1-Ω-Shunt, 58,6 mA Referenzzellenstrom bei 25 °C und 1000 W/m² sowie eine NTC-Beta-Näherung. Verbindlich sind die tatsächlich bestückte Gegenstelle und deren Kalibrierung. Aufgabenintegration, Buszugriffsschutz, Fehlerbehandlung und Zigbee-Abbildung fehlen in der vollständigen Anwendung; der Baustein ist nicht als fertiges PanelLog-Image nutzbar.
