# PanelLog: Kosten-Folgeprüfung 06.11.2026

Basis: GitHub main 681e7e40f0e82ad90e166dea82f6e1d44f2719dc.
Auftrag: C5140109, JSCJ 2N7002 und C2452974 prüfen und geeignete Änderungen sowie kleine Einsparungen umsetzen.

## Entscheidungen

| Position | Entscheidung | Begründung |
| --- | --- | --- |
| R8 | VO SCR1206F47K / C5140109 ausgewählt, ersetzt C2889758 | 47 kΩ, 1 % statt 5 %, 250 mW, 200 V, 1206. Gleicher Nennwiderstand und Footprint. |
| C1/C21/C22 | C7500895 statt C2840282 | Identische FH-MPN 1210B475K101NT, 4,7 µF, 100 V, X7R, 10 %, 1210. Nur Beschaffungskanal geändert. |
| Q2 | JSCJ 2N7002 / C8545 vorerst nicht übernommen | Pin-kompatibel, aber keine garantierten 3,3-V- oder Heißleckstromgrenzen im gefundenen Herstellerdatenblatt. |
| L1 | Sumida CDRH127/LDNP-680MC / C2452974 vorerst nicht übernommen | Elektrisch vielversprechend; Betriebsspannungsfreigabe fehlt und Landpattern/Sperrfläche unterscheiden sich. |

INA228, BVB-M-R0007-1.0 und IPT015N10N5 bleiben wie beauftragt erhalten.

## R8 – technische Prüfung

C5140109 ist ein Widerstand, keine Drossel. LCSC identifiziert VO SCR1206F47K mit 47 kΩ ±1 %, 250 mW, 200 V, ±100 ppm/K und -55…155 °C.
Bei 60 V und leitendem Q2 liegt maximal ungefähr die volle Eingangsspannung an R8:
P = 60² / (47000 × 0,99) = 77,4 mW bei 25 °C und negativer Widerstandstoleranz.
Das entspricht 31 % der Nennleistung; die Nennleistungsgrenze gilt nicht unverändert bei beliebiger Temperatur. Bei 10-V-Gateklemme sind es etwa 53,7 mW bei minimalem Widerstand. Die tatsächliche Zenerspannung ist strom- und temperaturabhängig.

Damit ist der Ersatz für den Prototyp geeignet, ohne Leiterplattenänderung. Hersteller-Deratingkurve und lokale Bauteiltemperatur sind vor Serienfreigabe zu bestätigen. Die präzisere Toleranz ersetzt keine Prüfung des Zenerknies. Der zuvor betrachtete UniRoyal C25833 ist eine Alternative gleichen Nennwerts; C5140109 wurde hier entsprechend dem Nutzerwunsch gewählt. Nicht mit 4,7-kΩ-Artikeln verwechseln.

## Q2 – warum noch kein JSCJ-Wechsel

Herstellerdatenblatt JSCJ/CJ, September 2016: SOT-23, G1/S2/D3; VDS 60 V, VGS ±20 V, ID 115 mA. VGS(th) maximal 2,5 V bei lediglich 250 µA und 25 °C. RDS(on) maximal 7 Ω bei 5 V; keine garantierte 3,3-V-Spezifikation. IDSS maximal 80 nA bei 60 V und 25 °C; kein garantierter Heißwert angegeben.

Der statische erforderliche Senkstrom liegt bei maximal rund 1,29 mA (60 V / 46,53 kΩ). Typische Kurven lassen die Funktion plausibel erscheinen, garantieren aber keine ausreichende Absenkung der Q1-Gatespannung bei minimalem GPIO-High und Kälte. Der heiße Sperrstrom beeinflusst den passiven Fail-ON-Gatepfad. Beispielsweise liefert der 47-kΩ-Pfad bei 20 V Eingang und 10 V Gate nur ungefähr 213 µA; ein unbekannter heißer Leckstrom kann daher relevant sein. Dies ist eine Sensitivitätsbetrachtung, kein behaupteter JSCJ-Leckstrom.

C8545 wird von JLCPCB als Basic geführt. Die mögliche Bestückungsgebührenersparnis rechtfertigt keine ungeprüfte Freigabe. Auch der bisherige onsemi-Typ ist in der BOM ausdrücklich CANDIDATE_REVIEW; sein Verbleib bedeutet nicht, dass dessen komplette Temperaturqualifikation bewiesen wäre. Vor einem Wechsel: Herstellergrenzen oder Messung über Temperatur, Eingangsspannung, Versorgung/GPIO-Pegel und mehrere Exemplare; Q1-VGS im ON- und OFF-Zustand sowie Schalttransienten erfassen.

## L1 – Sumida C2452974

Herstellerdatenblatt: 68 µH ±20 %, DCR 92 mΩ typisch / 120 mΩ maximal, Sättigungsstrom-Tabelle 2,60 (3,40 typisch) A bei 25 % Induktivitätsabnahme, Temperaturanstiegsstrom 3,20 A typisch. Bei 500 mA entstehen rechnerisch 30 mW Gleichstrom-Kupferverlust mit maximalem DCR bei Datenblattbedingungen; Ripple-, Kernverluste und Temperaturanstieg des DCR kommen hinzu.

12,3 × 12,3 × 8,0 mm maximal; -40…100 °C einschließlich Eigenerwärmung. Der Hersteller verbietet Leiterbahnen und Vias im markierten Bereich unter der Spule. Deshalb ist dies kein freigegebener Drop-in-Ersatz des Würth-Footprints.

Bei 60 V Eingang / 3,3 V Ausgang liegt während der Einschaltphase ungefähr 56,7 V über der Wicklung, zuzüglich Schaltüberschwingen. Das öffentliche Datenblatt nennt keine zulässige Betriebsspannung. Das beweist keine Untauglichkeit, reicht aber nicht zur Freigabe anstelle des bisherigen 120-V-Teils. Benötigt werden Sumida-Bestätigung zur Anwendungsspannung, Prüfung von Stromripple/Spitzenstrom über Toleranz und Temperatur sowie Landpattern- und Sperrflächenanpassung. Bis dahin bleibt Würth 7447709680.

## Kostenwirkung und Verfügbarkeit

Recherchewerte, keine verbindliche Warenkorb- oder Bestückungsquote; USD ohne Versand, Steuern, Mindestmengen-Mehrverbrauch und JLC-Zuschläge.

- FH C7500895: indexiertes LCSC-Angebot 0,3271 USD ab 10 Stück, Bestand 2377. Für vier Platinen sind 12 Stück nötig. Gegenüber dem zuvor ermittelten C2840282-Wert 0,3975 USD ergibt das indikativ 0,2112 USD pro Platine bzw. 0,8448 USD für vier.
- C5140109: indexierte Angebote etwa 0,0033–0,0034 USD bei Mindestmenge 100, Bestand etwa 700–800. Kauf von 100 Stück kostet etwa 0,33–0,34 USD; vier verbaute Widerstände entsprechen nur 0,0132–0,0136 USD. Den Restbestand nicht als verbrauchte BOM-Kosten behandeln. Keine gesicherte JLC-Basic-Einstufung und keine garantierte Gesamtbestückungsersparnis behauptet.
- Sumida C2452974: recherchiertes Angebot etwa 0,7122 USD bei Einzelabnahme; nicht als umgesetzte Ersparnis angerechnet.
- Für Q2 ist keine Ersparnis eingerechnet, weil nicht ersetzt.

Die FH-Biasqualifikation (effektive Eingangskapazität bei 60 V, Temperatur und Alterung) bleibt erforderlich. Der Wechsel der Bestellnummer verbessert oder verschlechtert sie bei identischer MPN nicht.

## Umsetzung und Prüfung

Beide Stücklisten, Schaltplan und PCB-Bestellfelder aktualisiert. R8 erhielt MPN/LCSC-Felder und den Werttext mit 1 %. Für C1/C21/C22 wurde ausschließlich die LCSC-Nummer ersetzt. Routing, Kupferflächen, Vias, Footprints, Positionen, Netze und DNP-Zustände bleiben byte-identisch.

Beide KiCad-Dateien wurden als S-Expressions strukturell gelesen. Das Rückgängigmachen ausschließlich der erlaubten Feldänderungen reproduziert den jeweiligen Ausgangstext exakt. Kein neuer nativer KiCad-ERC/DRC: KiCad ist in dieser Laufzeit nicht installiert. Die vorhandenen Berichte sind historische Ergebnisse des Basiscommits und keine neu ausgeführten Prüfungen. Kein Hardwaretest durchgeführt.

## Quellen

- [C5140109 / VO SCR1206F47K](https://www.lcsc.com/product-detail/C5140109.html)
- [FH C7500895, MPN und Preisstaffel](https://www.lcsc.com/de/product-detail/C7500895.html?is_substitute=1&original_product_code=C162515&original_unit_price=0.6093)
- [JSCJ Originaldatenblatt C8545](https://datasheet.lcsc.com/datasheet/pdf/a141b8bd86b14475955ac8c4d3eea0a8.pdf?productCode=C8545)
- [JLCPCB C8545 Basic](https://jlcpcb.com/partdetail/2N7002/C8545)
- [Sumida Originaldatenblatt](https://products.sumida.com/products/pdf/CDRH127LD%20(en).pdf)
- [LCSC Sumida C2452974](https://www.lcsc.com/de/product-detail/C2452974.html)
- [LCSC Vergleich der VO-Widerstände](https://www.lcsc.com/de/product-detail/C3018049.html?is_substitute=1&original_product_code=C3989329&original_unit_price=0.0214)
