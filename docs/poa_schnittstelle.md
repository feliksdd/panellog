# POA-Schnittstelle

Ein optionaler [POA-Sensor](https://github.com/feliksdd/poa-sensor) besteht aus Referenzzelle, Temperaturmessung und ADC. PanelLog versorgt genau einen Sensor über J8 und liest ihn an einem separaten I²C-Bus aus. INA237 und POA teilen keine Datenleitungen.

## Kabel und Pins

| J8-Pin | Signal | Verdrilltes Paar |
|---:|---|---|
| 1 | 3,3 V über R36 | Mit Pin 2 |
| 2 | GND | Versorgung |
| 3 | SDA, GPIO22 / WROOM-Pad 20 | Mit Pin 4 |
| 4 | GND | SDA-Rückleiter |
| 5 | SCL, GPIO23 / WROOM-Pad 21 | Mit Pin 6 |
| 6 | GND | SCL-Rückleiter |

Drei verdrillte Paare, UV-/außentaugliches Kabel, bis 3 m als Auslegungsziel. Gegenstelle nach Signalnamen anschließen. Kabel von PV-Leistungspfad und Schaltknoten fernhalten. GND entspricht dem Modul-Minuspol; die Schnittstelle ist nicht galvanisch getrennt. Ein Schirm darf keine Verbindung zu Modulrahmen/PE oder anderen Modulmassen herstellen. Am Sensor isoliert lassen; eine einseitige lokale GND-Anbindung setzt eine passende Erdungs-/EMV-Auslegung voraus.

## Bestückung

| Bauteil | Direkt, Standard | Gepuffert, Option |
|---|---|---|
| U4 P82B715DR | Unbestückt | Bestückt |
| C26 100 nF | Unbestückt | Bestückt |
| R30/R31, je 2,2 kΩ | Bestückt | Bestückt |
| R32/R33, je 0 Ω | Bestückt | Unbestückt |
| R34/R35, je 1 kΩ | Unbestückt | Bestückt, mit Gegenstelle abstimmen |
| R36, 0 Ω Versorgung | Bestückt | Bestückt |
| D3 TPD2E2U06DRLR | Bestückt | Bestückt |

Direkte Brücken und Puffer dürfen nicht gleichzeitig bestückt sein. Gepufferter Betrieb benötigt an beiden Kabelenden einen P82B715, lokale S-seitige Pull-ups und abgestimmte L-seitige Pull-ups. U4: Pin 2 Lx/SDA-Kabel, 3 Sx/SDA-MCU, 4 GND, 6 Sy/SCL-MCU, 7 Ly/SCL-Kabel, 8 VCC; 1/5 unbeschaltet.

## Elektrische Auslegung

Für den Direktbetrieb sind 25 kHz als Startwert vorgesehen. 2,2 kΩ Pull-up ergeben bei 3,3 V etwa 1,5 mA Low-Strom je Leitung. Bei 400 pF Gesamtkapazität ist `tr(30–70 %) ≈ 0,8473 × R × C ≈ 746 ns`. Kabel, Gegenstelle, D3 und Pads zählen zur Kapazität. Ein niedriger Takt ersetzt nicht die Einhaltung von Anstiegszeit und Low-Pegel; endgültige Kabellänge und Störfestigkeit ergeben sich am realen Aufbau.

P82B715 arbeitet ab 3 V mit reduzierter dynamischer Senkfähigkeit und hat bis 85 °C zulässige Umgebungstemperatur. Sein Eigenstrom und die Kabelspannung sind im Versorgungsbudget zu berücksichtigen. Zwei 1-kΩ-Kabel-Pull-ups parallel ergeben etwa 6,6 mA Low-Strom bei 3,3 V. Diese Bestückungsoption benötigt eine passende Gegenstelle und Pegel-/Timingcharakterisierung.

D3 schützt die Datenleitungen gegen ESD-Ereignisse im Rahmen seiner Beschaltung. R36 ist eine 0-Ω-Brücke und keine Strombegrenzung: Ein Versorgungskurzschluss im Kabel kann die gemeinsame 3,3-V-Schiene und PanelLog herunterziehen. Die Schnittstelle besitzt keine separate Kabel-Kurzschlussabsicherung.

Der vorhandene [POA-Softwarebaustein](../firmware/components/poa_soft_i2c/) adressiert ADS1115 an 0x48. Seine Pin-Konfiguration muss vor Einsatz zur WROOM-Hardware passen; siehe [Firmware](../firmware/README.md).

Datenblätter: [TI P82B715](https://www.ti.com/lit/ds/symlink/p82b715.pdf), [TI TPD2E2U06](https://www.ti.com/lit/ds/symlink/tpd2e2u06.pdf), [TI ADS1115](https://www.ti.com/lit/ds/symlink/ads1115.pdf).
