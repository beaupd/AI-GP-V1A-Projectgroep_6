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
### _Popular_
run popular_validation.py

Als hetvolgende geprint wordt, werkt het algoritme:
```python
'...'
>>> Verplichte steekproef CHECK! >>>
'...'
>>> Steekproef met verzameling 1 CHECK! >>>
'...'
>>> Steekproef met verzameling 2 en 4 CHECK! >>>
'...'
>>> Steekproef met verzameling 3 en 5 CHECK! >>>
``` 
### _Similar_
run pactum_validation.py

Deze recommendation word gebruikt voor opdracht 1 van de verplichte validaties.
In de volgende tabel staat de uitkomst van "23866": 
```python
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|product_id  |naam                                                                  |brand     |gender    |category            |sub_category      
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|1714        |Neutral Vloeibaar Kleur Parfumvrij Wasmiddel 1425 ml                  |Neutral   |Gezin     |Huishouden          |Wassen en schoonmaken
|20339       |Neutral Wasmiddel Vloeibaar Zwart & Donker Parfumvrij 1000 ml         |Neutral   |Gezin     |Huishouden          |Wassen en schoonmaken
|27337       |Neutral Parfumvrij Waspoeder 1,188 g                                  |Neutral   |Gezin     |Huishouden          |Wassen en schoonmaken
|23889       |Neutral Wasmiddel  Waspoeder Parfumvrij Wit 1188 gr                   |Neutral   |Gezin     |Huishouden          |Wassen en schoonmaken
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
Verplichte steekproef is geslaagd!
```

Als onder aan dit word geprint, werkt het algoritme:
```python
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|product_id  |naam                                                                  |brand     |gender    |category            |sub_category
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|32476       |Airwick Essential Oils Berries & Spice Geurkaars 105 gr               |Airwick   |Unisex    |Wonen & vrije tijd  |Woonaccessoires
|32483       |Airwick Essential Oils Infusion Geurkaars Orange & Festive Spice      |Airwick   |Unisex    |Wonen & vrije tijd  |Woonaccessoires
|32474       |Airwick Essential Oils Infusion Geurkaars Apple & Cinnamon            |Airwick   |Unisex    |Wonen & vrije tijd  |Woonaccessoires
|32480       |Airwick Essential Oils Infusion Geurkaars Apple & Cinnamon            |Airwick   |Unisex    |Wonen & vrije tijd  |Woonaccessoires
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
Eigen steekproef met 20 random productid's is geslaagd!
```
### _Combination_

### _Personal_
