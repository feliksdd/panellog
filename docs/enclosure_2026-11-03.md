# PanelLog: Gehäuse und direkt angelötete Kabel

Ausgewählt: **Spelsberg TK PC 1813-6f-m, 12741501**, grau, 180 × 130 × 63 mm. UV-beständiges glasfaserverstärktes Polycarbonat, IP66, IK08. Herstellerfreigabe: **geschützter Außenbereich**, Montage unter PV-Modul oder Regendach, ohne stehendes Wasser. Keine Freigabe für ungeschützte Dauerbewitterung behauptet.

## Platine und Befestigung

- Neuer Umriss: **150 × 104 mm**, KiCad-Koordinaten x=0…150, y=3…107.
- H1…H4: 3,2-mm-NPTH bei (25,10), (125,10), (25,100), (125,100). Bezogen auf linke obere Platinenkante: (25,7), (125,7), (25,97), (125,97).
- Raster **100 × 90 mm**, entsprechend den vier inneren Bossen 90 × 100 mm aus der Herstellerzeichnung, um 90° gedreht.
- Außenmaß und Schraubdom-Freiraum aus Zeichnung M-TK-1813-flach-m, Freigabe 29.10.2024: Körper 180 × 130; innere Länge 157, enges Quermaß 107 mm. Platine zentriert: 15 mm bzw. 13 mm Abstand zur Gehäuseaußenkontur. Rechnerisch 3,5 mm bzw. 1,5 mm Abstand zum genannten Innenraum; Formschrägen und Toleranzen am Erstgehäuse prüfen.
- Vier isolierende Abstandhalter, Zielhöhe mindestens 8 mm über höchstem darunterliegendem Boden-/Rippenniveau. Gehäuseseitige Schrauben passend zum Kunststoffdom auswählen; **keine M3-Gewinde in den Gehäusedomen voraussetzen**. Platinenbefestigung mit M3-Nylonschrauben möglich, wenn Abstandhalter entsprechend ausgeführt sind. Gehäuseboden bleibt ungebohrt.
- 7 × 7 mm Kupfersperrfläche um jedes Befestigungsloch, beide Lagen. Alle bisherigen elektrischen Bauteile, Leiterbahnen und Zonen gemeinsam um (+15,+10) mm verschoben; Routinggeometrie unverändert. Rückseitige Massezone neu gefüllt.
- Vor Platinenserie mechanischen 1:1-Ausdruck oder Musterplatine im Originalgehäuse prüfen, insbesondere Dome, Rippen, Deckel und Verschraubungen. Herstellerzeichnung ist die Grundlage, kein bereits durchgeführter physischer Passversuch.

## Kabeldurchführungen und direkte Lötanschlüsse

| Anzahl | Teil | Anwendung |
|---:|---|---|
| 1 | Spelsberg 12741501 | Gehäuse |
| 4 | LAPP SKINTOP ST-M M16×1,5 schwarz **53111210**, Klemmbereich 4–10 mm | je eine PV-Einzelader pro Verschraubung |
| 1 | LAPP SKINTOP ST-M M12×1,5 schwarz **53111200**, Klemmbereich 3,5–7 mm | runde, ummantelte Pt1000-Leitung |
| 4+1 | passende Gegenmuttern M16/M12 und geeignete flache Anschlussdichtungen | Abdichtung und Befestigung an Gehäusewand |
| 4 | isolierende Abstandhalter mit geeigneten Schrauben | Platinenmontage |

Schwarze SKINTOP-Ausführung laut LAPP UV-beständig, IP66/IP68/IP69; die fertige Baugruppe erreicht ihre Schutzart nur bei passender Leitung, korrekter Anschlussdichtung und Montage nach Herstellervorgaben. Tatsächlichen Kabelaußendurchmesser vor Bestellung messen. Bei dünnerer Pt1000-Leitung andere Dichtung/Verschraubung passend zum Durchmesser auswählen; keine lose Einzeladern im gemeinsamen runden Dichteinsatz.

**Kabelanordnung:** je zwei PV-Verschraubungen in den beiden gegenüberliegenden 130-mm-Stirnwänden. Die äußeren Vorprägungen mit 70-mm-Achsabstand verwenden; M16 bei einer Seite M12/16 und bei der anderen M16/20 öffnen. Mittlere größere Vorprägungen geschlossen lassen. Sensorleitung an einer freien M12/16-Position einer 180-mm-Längswand. Die Durchführungshöhe folgt den vorhandenen Vorprägungen. Genügend Freiraum für Gegenmutter und Montagewerkzeug einhalten. SW19 benötigt Platz; vor Ausbrechen am Originalgehäuse gegenprüfen.

PV-Modulseite an **J1.1 = PV+ / J1.2 = PV−**, Wechselrichterseite an **J2.1 = MPPT+ / J2.2 = MPPT−** direkt anlöten. Vier separate UV-beständige PV-Leitungen, vorläufig 4 mm²: 2,8-mm-Platinenbohrungen auf Litzenpassung prüfen; die Lötstelle ist keine Zugentlastung. Temperatursensor an **J3.1/J3.2**, direkt verlötet, kein steckbarer Anschluss erforderlich. J4 bleibt internes SWD-Servicepad und benötigt keine externe Durchführung.

Verschraubungen klemmen auf intakter Kabelisolierung. Innen flexible, spannungsfreie Schlaufen; Mindestbiegeradius des konkreten Kabelherstellers einhalten. Montagefolge: Verschraubungen und Muttern einsetzen, Kabel durchführen, ablängen/abisolieren, anlöten, anschließend Schlaufe einstellen und Zugentlastung festziehen. Keine Kräfte auf Lötaugen, keine Leitungen über Antenne, Schaltregler oder heiße Leistungshalbleiter legen. Kabel außerhalb mit Tropfschlaufe und zusätzlicher Befestigung führen; Montage unter dem Modul mit Spritzwasserschutz.

Dichtes Gehäuse verhindert kein Kondensat. Bei relevanten Temperaturwechseln geeigneten IP-erhaltenden Druckausgleich vorsehen; nicht einfach ein offenes Entwässerungsloch bohren. 20-A-Erwärmung im geschlossenen Gehäuse sowie Funkreichweite bleiben Prototypenprüfungen.

## Kostenrahmen / Auswahl

Preisbeispiel Gehäuse: **25,50 € inkl. MwSt., ohne Versand**, Raleo, bei Recherche nicht verfügbar. Kein verbindlicher Bestpreis. Für fünf Markenverschraubungen samt Dichtungen/Gegenmuttern und isolierende Befestigung **zusätzlich grob 12–20 € Planungsbudget** (Schätzung, kein eingeholtes Angebot). Gesamt **ca. 38–46 € ohne Versand**. Das Standardgehäuse vermeidet individuelle Gehäusefertigung und vier große Durchgangsbohrungen für Platinenbefestigung. Billigere ABS-/PS-Universalboxen ohne ausdrückliche UV-Angabe wurden nicht gewählt.

## Nachweise

KiCad **10.0.8**, tatsächliche Prüfung dieser Gehäuserevision: ERC 0 Fehler/0 Warnungen; DRC 0 Verstöße, 0 offene Verbindungen, 0 Schaltplan-PCB-Abweichungen. Geerbte deaktivierte Prüfungen sind in den Berichten aufgeführt; keine zusätzlichen DRC-Ausnahmen eingeführt. Berichte und Frontansicht unter `hardware/kicad/enclosure_review_2026-11-03/`.

Quellen:
- https://www.spelsberg.de/industrieleergehaeuse/mit-/-ohne-metrische-vorpraegungen/12741501/
- Gemeinsame Herstellermaßzeichnung M-TK-1813-flach-m: https://www.e-partner-webshop.de/bildserver/produkt/87788D/9021821/spelsberg-leergehaeuse-tk-pc-1813-8f-tm-13751501.pdf (zeigt gemeinsame Bodenwanne und mehrere Deckelhöhen; für 12741501 gilt 62,5 mm nominal).
- https://products.lappgroup.com/online-catalogue/cable-glands/skintop-cable-glands-plastic-metric/standard/skintop-st-m.html
- Preisbeispiel: https://raleo.de/item/elektro/spelsberg-leergehaeuse-schutzart-ip66-schlagfestigkeit-ik08-schutzklasse-ii-ui-690v-ac-bemessungsisolationsspannung-1000v-dc-ul-dlg-dnv-halogenfrei-12741501/
