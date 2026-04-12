Lift Simulation

Dit project is een lift-simulatie gemaakt in Python met Pygame. In de simulatie bewegen meerdere liften door een gebouw en vervoeren zij personen tussen verschillende verdiepingen. De simulatie houdt rekening met wachttijden, drukte en verschillende instellingen zoals openingstijden.

Functionaliteiten
- Meerdere liften (normaal en snel)
- Personen die automatisch verschijnen en een bestemming kiezen
- Instelbare opening- en sluitingstijden
- Grafieken van wachttijd en aantal personen
- Tweede scherm (monitor view) voor overzicht van liften
- Settings sidebar voor aanpassingen
- Reset dag functie
- Maximaal 10 personen per lift
- Einde van de dag melding waarbij geen nieuwe personen meer verschijnen
- Werking van de simulatie

Personen verschijnen willekeurig in het gebouw en willen naar een andere verdieping.
Liften bewegen automatisch en stoppen op verdiepingen om personen op te halen en af te zetten.
Personen kiezen een lift op basis van afstand en beschikbaarheid.
De wachttijd van personen wordt bijgehouden en weergegeven in grafieken.

- Openingstijden
De simulatie start op de ingestelde openingstijd en stopt op de sluitingstijd.

- Liftcapaciteit
Elke lift kan maximaal 10 personen vervoeren.

- Einde van de dag
Wanneer de dag voorbij is, stoppen nieuwe personen met verschijnen en wordt dit visueel weergegeven.

Hoe start ik het op? 

1 - py -m venv .venv
2 - .venv\Scripts\Activate
3 - python -m pip install -r Requirements.txt
4 - Run via game.py