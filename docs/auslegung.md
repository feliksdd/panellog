# Auslegung

## Einsatzbereich

| Größe | Auslegung / Grenze |
|---|---|
| PV-Anschluss | Ein einzelnes Modul je Knoten und MPPT-Eingang |
| Modulspannung | Bis 60 V DC als Entwurfsbereich; üblicher Arbeitspunkt etwa 30–45 V |
| Versorgung | LM5163: 6–100 V Bauteilbereich; hier UVLO typisch 9,0 V ein / 8,4 V aus |
| Bus-/Sense-Eingänge INA237 | 85-V-Bauteilklasse; zulässige Transienten nach Datenblatt beachten |
| Q1 / Eingangskondensatoren | 100-V-Bauteile |
| Strompfad | 15 A Auslegungspunkt; 20 A thermischer Betrachtungsfall, keine nachgewiesene Dauerstromangabe |
| Kabelannahme | Kurze PV-Leitungen von etwa 1–2 m; POA separat bis 3 m als Auslegungsziel |

Für das konkrete Modul gilt näherungsweise `Voc,kalt = Voc,STC × [1 + βVoc × (Tmin − 25 °C)]`, mit βVoc in 1/K. Modultoleranzen und lokale Temperatur sind zusätzlich einzubeziehen. Die Leerlaufspannung begrenzt keine induktiven Schaltspitzen am Q1-Drain. D1 und R23/C23 sind unbestückt; VDC, Q1-VDS und INA-Eingänge müssen mit dem tatsächlichen MPPT und Kabel innerhalb ihrer Grenzen bleiben.

## 3,3-V-Wandler

`Vout = 1,2 V × (1 + 174 kΩ / 100 kΩ) = 3,288 V` nominal. Die 1-%-Widerstände tragen ungefähr ±1,27 % Ausgangstoleranz bei; Referenztoleranz kommt hinzu. R3 27,4 kΩ entspricht etwa 300 kHz im kontinuierlichen Betrieb; bei geringer Last arbeitet der Wandler mit ausgelassenen Pulsen.

Bei 60 V Eingang, 3,3 V Ausgang und 68 µH ergeben sich ideal etwa 0,152 A Stromripple Spitze–Spitze und 0,576 A Spitzenstrom bei 0,5 A Last. Der LM5163 liefert bis 500 mA; Funkstromspitzen und Einschaltlasten müssen im Gesamtbudget liegen. L1 hat 120 mΩ maximalen DCR, entsprechend 30 mW DC-Kupferverlust bei 0,5 A unter Datenblattbedingungen. Die Sumida-Grenze von 100 °C schließt Eigenerwärmung ein; eine 120-V-Wicklungsfreigabe ist nicht angegeben.

Die drei 4,7-µF-Eingangs-MLCCs ergeben 14,1 µF Nennkapazität. Relevant ist ihre effektive Kapazität unter DC-Bias, Toleranz und Temperatur; Ziel sind mindestens 2,2 µF wirksame HF-Eingangskapazität. C5/C6/C15 sind X5R mit 85 °C oberer Temperaturklasse. Versorgungseinbruch, Ripple und Temperatur sind mit dem realen Funklastprofil zu beurteilen.

## Strommessung und Leitverluste

INA237 mit `ADCRANGE = 1`: ±40,96 mV Messbereich, 1,25 µV Rohwertauflösung. Mit 1 mΩ entspricht das ±40,96 A elektrischem Messbereich und 1,25 mA je ADC-Schritt. Die Auflösung ist keine Genauigkeitsangabe und keine Freigabe des Leistungspfads.

| Strom | Shuntspannung | Shuntverlust | Q1-Verlust bei 1,5 mΩ | Summe |
|---:|---:|---:|---:|---:|
| 12 A | 12 mV | 0,144 W | 0,216 W | 0,360 W |
| 15 A | 15 mV | 0,225 W | 0,338 W | 0,563 W |
| 20 A | 20 mV | 0,400 W | 0,600 W | 1,000 W |

Q1-Werte gelten rechnerisch bei VGS = 10 V und 25 °C. Warm steigt RDS(on); mit doppeltem Q1-Widerstand ergeben sich bei 15 A rund 0,90 W für Shunt und MOSFET. Kupfer-, Kabel- und Anschlussverluste kommen hinzu. Die 5-W-Shuntangabe ersetzt keine thermische Betrachtung der Platine im geschlossenen Gehäuse.

INA237-Offset bis ±50 µV entspricht ±50 mA. Mit ±0,3 % Verstärkungsfehler und ±1 % Shunttoleranz lautet eine anfängliche lineare Abschätzung `±(1,3 % vom Messwert + 50 mA)`, ohne Rauschen und Platinenfehler. Nullpunkt- und Verstärkungskalibrierung sind erforderlich. Bei 50 K Temperaturänderung tragen je 50 ppm/K von Shunt und INA-Verstärkung jeweils 0,25 % bei; Offsetdrift 0,02 µV/K entspricht zusätzlich 1 mA. Das Entwicklungsziel von ungefähr 1 % ab 1 A setzt eine charakterisierte, kalibrierte Messkette voraus.

## Gate und Abschaltrückmeldung

Bei 60 V und heruntergezogenem Bias setzt R8 nominal höchstens `60² / 47 kΩ = 76,6 mW` um. Bei nominal 10 V Bias fließen `(60 − 10) / 47 kΩ = 1,064 mA`. Die wirkliche Gatespannung hängt von D2, Leckströmen und Temperatur ab. Ausreichendes VGS, Q2-Ansteuerung mit 3,3 V sowie Q1-Schaltverluste und SOA sind für den tatsächlichen Betrieb maßgebend. Häufige PWM ist nicht vorgesehen.

`Vdrain = Vadc × (1 MΩ + 27,4 kΩ) / 27,4 kΩ = Vadc × 37,496`. Bei offenem Q1 ohne externe Belastung bildet R27 mit R28/R29 einen weiteren Teiler: Vdrain ≈ 0,5068 × VDC, Vadc ≈ 0,013515 × VDC. Bei 60 V sind das 0,811 V am ADC; ein extern auf 60 V gehaltener Drain ergibt 1,600 V. Die ADC-Zeitkonstante liegt bei etwa 2,7 ms.

## Temperaturkanäle

Mit kalibrierten ADC-Spannungen gilt nominal:

- `Vrail = 2 × Vadc,rail`
- `Rpt = 14700 Ω × Vadc,Pt / (Vrail − Vadc,Pt)`
- `Rntc = 10000 Ω × Vadc,NTC / (Vrail − Vadc,NTC)`

R19/R22 sind Filterwiderstände und gehen ohne ADC-Belastung nicht in die DC-Teilerformeln ein. Für Pt1000 die IEC-60751-Kennlinie verwenden, für RT2 die TDK-R/T-Tabelle. Pt1000-Messstrom bei 0 °C und 3,3 V: etwa 0,210 mA. NTC-Messstrom bei 25 °C: 165 µA; Eigenerwärmungsleistung etwa 0,272 mW.

R20/R24 haben 50 kΩ Quellimpedanz und mit C19 5 ms Zeitkonstante; nach Versorgungsänderungen mindestens 25–30 ms einschwingen lassen. ADC-Kalibrierung, Kanalabweichungen, Leitungswiderstand, Befestigung und Eigenerwärmung bestimmen den Systemfehler. Klasse A des Pt1000 allein garantiert keine ±0,5 °C Systemgenauigkeit.

## Datenblätter

- [TI LM5163](https://www.ti.com/lit/ds/symlink/lm5163.pdf), [TI INA237](https://www.ti.com/lit/ds/symlink/ina237.pdf)
- [Infineon IPT015N10N5](https://www.infineon.com/assets/row/public/documents/24/49/infineon-ipt015n10n5-datasheet-en.pdf)
- [HoVB4026 / C481535](https://www.lcsc.com/product-detail/C481535.html), [Sumida CDRH127/LD](https://products.sumida.com/products/pdf/CDRH127LD%20(en).pdf)
- [Espressif ESP32-C6-WROOM-1](https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf)
- [TDK NTCG163JF103FT1S](https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG163JF103FT1S)
