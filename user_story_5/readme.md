# User Story 5: Conceptversie adviesrapport

TAAI-V1GP-19_2020

| _GP-V1A-Groep 6_ 
| --- |
| 1778763 – Beau Dekker |
| 1778287 – Gaynora van Dommelen  |
| 1779750 – Robin Kroesen |
| 1789287 – Khai-Tam Nguyen |

# Inleiding

_Aanleiding onderzoek_ 

TODO: leg de opdracht uit


_Context_

TODO: beschrijf de opdrachtgevers en jullie rol

Onze opdrachtgever, Joost, wil graag recommendations te zien krijgen die bijdragen aan het helpen van klanten bij het vinden van producten die ze willen kopen. 
Wij, als projectgroep, moeten ervoor zorgen dat op de front-end recommendations worden getoond waarvan de reden voor aanbieden logisch onderbouwd is en niet
als 'het aansmeren van producten' gezien kan worden.

_Probleemstelling_

TODO: wat is het probleem dat jullie gaan oplossen?

Meer omzet door middel van klantgerichte recommendations. Dit doen we door te kijken naar de wensen en voorkeuren van een klant en op basis hiervan
producten aan te bieden. Bij het aanbieden van producten die passen bij de klant als: er geklikt wordt op een pagina, product of gekeken wordt naar de winkelmand, zorgt ervoor
dat klanten sneller producten vinden die voor hun interessant zijn. Hierdoor hoeven ze minder lang te zoeken naar producten. Door het verkorte proces van zoeken naar producten, is de kans verkleind dat een klant eerder de webpagina verlaat, omdat ze niet snel 'hun' product kunnen vinden.

_Doelstelling_

TODO: wat is de doelstelling van jullie project?

Recommendations opzetten op verschillende delen van de front-end die bijdragen aan het gericht aanbieden van producten voor een klant. Om zo klanten het gevoel te geven dat er naar hun voorkeuren en wensen gekeken wordt en ze niet lang meer hoeven te zoeken naar producten die bij hen passen.

# Algoritme 1: Popular

## Beschrijving en onderbouwing

### _Wat is het doel van het algoritme?_

Het doel van het algoritme is het gerichter aanbieden van producten die passen bij het koopgedrag van de user.

### _Hoe is het algoritme bedacht?_

Er is gekeken naar de algemene kenmerken van users en de producten die ze kopen. Daarnaast is gekeken naar het verschil van gekochte producten per pagina en wat de relatie is tussen de profielen, gekochte producten en de pagina's waar ze gekocht zijn. Hieruit volgde dat profielen onderverdeeld kunnen worden op basis van hun surf gedrag op de front-end, het soort geslacht producten iemand koopt en op welke pagina dit gebeurt, zodat op elke pagina nieuwe recommendations verschijnen.

### _Hoe werkt het algoritme?_

![](src/FLOWCHART_userPop.png)

## Validatie van het algoritme

### _Hoe is de werking van het algoritme gevalideerd?_

Er zijn naast de bekende errors als: 
- een user is onbekend
- een user heeft geen orders
- de combinatie segment-gender-category komt niet voor,

geen andere problemen gevonden bij het testen met verschillende profiles en klikken op categoriepagina's.

## Beschrijving opzet recommendation engine 

### _Hoe is de code opgezet_

TODO: Code beschrijving

# Algoritme 2: Combination

## Beschrijving en onderbouwing

### _Wat is het doel van het algoritme?_

### _Hoe is het algoritme bedacht?_

### _Hoe werkt het algoritme?_

## Validatie van het algoritme

### _Hoe is de werking van het algoritme gevalideerd?_

## Beschrijving opzet recommendation engine 

### _Hoe is de code opgezet_

# Algoritme 3: Personal

## Beschrijving en onderbouwing

### _Wat is het doel van het algoritme?_

Het algoritme probeert een zo goed mogelijke algemene aanbeveling te geven aan een specifieke gebruiker. We willen dus aanbevelingen geven gebaseerd op een specifieke gebruiker
waardoor de kans hoger wordt dat hij een van de aanbevelingen gaat kopen.

### _Hoe is het algoritme bedacht?_

Het algoritme is al lang bekend bij collaborative filtering. Deze algoritme hebben we gevonden, terwijl we op google naar algoritmes zaten te zoeken. 
We vonden het logisch dat we aanbevelingen zouden geven gebaseerd op profielen die op de gebruiker lijkt.

### _Hoe werkt het algoritme?_

Elke profiel heeft een eigen profielID. We kijken naar welke producten een profiel heeft gekocht. We kijken dan naar alle sessions die dezelfde producten hebben gekocht
als de profiel. We willen hieruit de 4 beste sessions kiezen. De beste sessions zijn de sessions met het meest aantal dezelfde gekochte producten als de gebruiker. Nadat
we de 4 beste profielen hebben bepaald, kijken we naar welke producten het meeste voorkomt in die 4 profielen. De producten die het meeste voorkomen worden recommendations.

## Validatie van het algoritme

### _Hoe is de werking van het algoritme gevalideerd?_

We hebben alle functies getest met verschillende profielen / producten. We moeten dan opletten of de output exact is wat we willen. Verder hebben we dan gekeken via pgAdmin 
of de algoritme wel klopt. We hebben dan in de database voor een profiel getest en gekeken welke producten hij zou moeten krijgen. Daarna hebben we getest met onze 
algoritme of dit ook daadwerkelijk werkt. 

## Beschrijving opzet recommendation engine 

### _Hoe is de code opgezet_

Ik heb verschillende functies voor het halen van informatie uit de database. We willen zo min mogelijk de query's gebruiken, dus daarom heb ik hele grote query's. 
Ik pas dan mijn functies toe op de data, gebaseerd op de werking van het algoritme. Hierdoor kan ik alles makkelijk hergebruiken.

# Algoritme 4: Similar

## Beschrijving en onderbouwing

### _Wat is het doel van het algoritme?_

### _Hoe is het algoritme bedacht?_

### _Hoe werkt het algoritme?_

## Validatie van het algoritme

### _Hoe is de werking van het algoritme gevalideerd?_

## Beschrijving opzet recommendation engine 

### _Hoe is de code opgezet_

# Advies

TODO: Geef aan welke algoritmes jullie adviseren aan de opdrachtgever, onderbouw dat advies. Koppel het advies aan de doelstellingen
