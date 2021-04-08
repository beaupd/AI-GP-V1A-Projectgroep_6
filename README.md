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
