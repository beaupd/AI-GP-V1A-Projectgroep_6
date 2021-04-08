# AI Group Project ( V1A-Groep 6 )
Deze Repository is voor een schoolproject op de studie Artificial Intelligence aan de Hogeschool Utrecht. 
Met dit schoolproject is het de bedoeling dat we in team aan een recommendation engine gaan werken. 
Recommendation engine is een systeem dat op basis van informatie aanbevelingen probeert te maken.
In ons geval moeten we met een hoop geanonimiseerde data van een failliete product store genaamd "op=op" aanbevelingen voorspellen.
De gekregen data was in json formaat aangeleverd dus hebben we de op BSON gebaseerde documents database [MongoDB](https://www.mongodb.com/) gebruikt.
Via de gekregen richtlijnen vanuit opdrachten met deadlines is het process van het maken van een recommendation engine in ons project als volgt:
Eerst de gekregen datasets importeren naar een lokale mongodb instantie, vervolgens een relationele database ontwerpen wij hebben dit in postgres gedaan,
vervolgens via een procedurele programmeertaal de documents data vanuit mongodb overzetten in de relationele database, ten slotte met de gegeven website template en de data ons uitgekozen filtering aanbeveling systeem uitwerken en laten werken. Hieronder een inhoudsopgave van de verschillende toelichtingen van de stappen in het process, sommige volgens de richtlijnen van de gekregen opdrachten.


## **Inhoudsopgave**
- [Project team](#Project-team)
- [Installation](#install-requirementstxt)
  
## **Project team**
**GP-V1A-Groep 6**  
1778763 – Beau Dekker  
1778287 – Gaynora van Dommelen  
1779750 – Robin Kroesen  
1789287 – Khai-Tam Nguyen  


## Install requirements.txt
open up a command line inside project directory and type:
```pip install -r requirements.txt```

## Opstarten van applicatie
1. Clone de git repository
2. Check of de gegevens in rdbconnection2.py en mdbconnect2.py gelden voor jou. Pas aan waar nodig.
3. Run create_tables.py
4. Run data_overzetten.py 
5. Run popular_setup_tables.py
6. Run pactum.py
7. Voor unix shell gebruikers: Navigeer naar de directory waarin deze repository zich bevindt. Run huw_recommend.sh (command line: sh huw_recommend.sh). Voor Windows gebruikers: Open command prompt en navigeer naar de directory waarin deze repository zich bevindt. Run daar het volgende commando:
```python
set FLASK_APP=huw_recommend.py
python -m flask run --port 5001

### !! Als het werkt, zie je hetvolgende in je terminal verschijnen: * Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```
8. Open nu een nieuw window en run daar het volgende:
```python
set FLASK_APP=huw.py
python -m flask run

### !! Als het werkt, zie je hetvolgende in je terminal verschijnen: * Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```
9. Ga nu naar http://127.0.0.1:5000 waar de front-end runt.

## Valideren van de algoritmes
### popular
run popular_validation.py

Als hetvolgende geprint wordt, werkt het algoritme:
```python
Verplichte steekproef CHECK!
Steekproef met verzameling 1 CHECK!
Steekproef met verzameling 2 en 4 CHECK!
Steekproef met verzameling 3 en 5 CHECK!
``` 
### similar

### combination

### personal