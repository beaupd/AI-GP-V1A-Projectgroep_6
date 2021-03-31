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
De similar recommendation engine ookwel pactum recommendation, zoekt op basis van specificaties van een product soortgelijke producten. De engine werkt als volgt: Allereerst geef je het een product id, vervolgens zoekt de engine de bijbehorende specificaties en hun waarde op in de database, dan kijkt de engine welke producten overeenkomen met de waarde voor dezelfde specificaties, en sorteert de gevonden producten op basis van de frequentie dus hoevaak hetzelfde product bij meerdere specificaties overeenkomt met het gegeven product. Dit is in mijn opzicht de meest logisch gevonden manier om met de verkregen data soortgelijke producten aan te bevelen. Omdat je zo op basis van specificerende eigenschappen "meest" overeenkomende producten vind.

### _Wat is het doel van het algoritme?_
Om met een gegeven product soortgelijke producten te vinden om die aan te kunnen bevelen aan de klant. Dit kan bijvoorbeeld een klant helpen om een betere variant te vinden op een product waar de klant interesse in heeft(op heeft geklikt), zo kan het zorgen voor meer omzet omdat de interesse van de klant word ondersteund.

### _Hoe is het algoritme bedacht?_
Na te hebben gebrainstormed over de data en logische verbanden ertussen voor soortgelijke producten, vond ik dit op basis van de beschikbare data het meest logische verband voor de similar recommendation engine. 

### _Hoe werkt het algoritme?_
In een nieuwe tabel worden alle product-id's van waardes bij specificaties van alle producten gestopt in arrays in rows bij de bijbehorende waarde voor de specificatie. Zo ontstaan er arrays van producten die bij een specificatie dezelfde waarde delen. Vervolgens kan de engine met een gegeven product-id kijken in welke arrays die voorkomt, deze arrays opvragen en hier een grote lijst van maken, vervolgens de gevonden product-id's sorteren of optellen op basis van frequentie en dan kan je makkelijk de producten eruit kiezen die het meest voorkomen in de gesorteerde lijst.

## Validatie van het algoritme


### _Hoe is de werking van het algoritme gevalideerd?_
Gekijkt in de product tabel welke producten met meerdere specificaties overeenkomen, vervolgens een van deze producten gegeven aan de recommendatie engine en gekeken of de bedachte overeenkomende producten terug kwamen als return. Dit heb ik met meerdere product overeenkomende specificatie groepen geprobeert en werkte perfect.

## Beschrijving opzet recommendation engine 
De engine bestaat uit een klasse die gebruik maakt van data uit de bij eerdere user-stories opgestelde relationele database. het belangrijkste gedeelte van de klasse is opgezet in drie functies: een functie die de tabel voor de recommendation engine aanmaakt, een functie die de aangemaakte tabel vult met data uit de product tabel en een functie die met een gegeven product-id onder andere een lijst terug geeft van alle product-id's uit de arrays waar het gegeven product-id in voorkomt uit de gevulde tabel.

### _Hoe is de code opgezet_
De similar engine recommendatie code bestaat uit een klasse waaraan je een open connectie meegeeft met de relationele database(postgresql). Er zijn eigenlijk 2 functies die andere functies in de klasse aanroepen. De eerste om de recommendation werking te initialiseren en de tweede om "n" aantal producten te returnen die "similar" zijn aan het meegegeven produt-id. De eerste functie "setup_recommendation" callt 2 functies en ziet er als volgt uit;
```python
def setup_recommendation(self):
        self.create_table()
        self.populate_table()
```
De eerste functie die gecalled word is deze:
```python
def create_table(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS equals CASCADE")
        cur.execute("""
            CREATE TABLE equals (
                keyfield VARCHAR,
                value VARCHAR PRIMARY KEY,
                products VARCHAR[],
                length INT
            );
        """)
        self.conn.commit()
        cur.close()
```
Deze functie maakt met de meegegeven connection, die geinitialiseerd is als een object variable, een cursor aan en execute daarmee op de postgresql de code om de tabel aan te maken. De tweede functie die hieruit word gecalled is als volgt:
```python
def populate_table(self):
        values = ["product_id", "brand", "gender", "category", "sub_category", "sub_sub_category"]
        cur = self.conn.cursor()
        cur.execute(f"SELECT {', '.join(values)} from product")
        rows = cur.fetchall()
        
        print(f"Found {len(rows)} rows, inserting...")
        start_all = perf_counter()
        for idx, r in enumerate(rows): # loop door alle opgevraagde rows
            for i, c in enumerate(r[1:], 1): # loop door alle columns behalve de eerste want het id gebruiken we in de niewe tabel als identificator
                if c:# als de column niet leeg is
                    p = str(c).replace("'", "") # sommige columns hebben quote er in en dat geeft een error
                    p_id = r[0].replace("'", "") # sommige columns hebben quote er in en dat geeft een error
                    # hieronder de sql insert code om een row aan te maken of van een row met dezelfde "value" de array aan te passen(append) 
                    cur.execute(f"INSERT INTO equals(keyfield, value, products, length) VALUES ('{values[i]}', '{p}', ARRAY['{p_id}'], 1) ON CONFLICT (value) DO UPDATE SET products = array_append((SELECT products from equals where value='{p}'), '{p_id}'), length = array_length(array_append((SELECT products from equals where value='{p}'), '{p_id}'), 1);")
            if idx % 1000 == 0 and idx != 0: # x aantal executes committen vooral om efficientie te testen en om een coole tussentijdse tijden te berekenen
                temp = perf_counter()
                print(f"On row {idx}, current time is {temp - start_all}s estimated time is {((temp-start_all)/idx)*len(rows)}s\ncommiting...")
                self.conn.commit()
        self.conn.commit()
        eind_whole = perf_counter()
        print(f"Done, total took {eind_whole - start_all} seconds...")
        cur.close()
```
Deze functie vraagt met de meegegeven connectie en een aantal bedachte specificaties in een lijst de waardes op van alle waardes van de producten bij de in de lijst voorkomende specificaties, vervolgens word er een moment opname gedaan om uiteindelijk de totale tijd te kunnen berekenen, daarna loopt de functie door alle gevonden rows en loopt die per row weer door alle columns(de specificaties), al de gevonden waardes van de specificaties van de producten stopt de functie in de nieuwe tabel in de array met diezelfde specificatie waarde. Per 1000 rows vind er een commit plaats, een berekening van de tijd en een schatting van de totale tijd. Op het einde is er nog een commit naar de database en een print van de totale tijd.

De tweede functie, deze wordt gebruikt vanuit de front-end, deze returned "n" aantal aanbevolen producten met een meegegeven product-id. Deze ziet er als volgt uit:
```python
def get_n_recommended(self, product_id, n):
        try:
            return self.recommend_products(product_id)["occurences"].most_common(n)
        except:
            return None
```
Deze functie ontleed een response van de functie die die called, de called functie ziet er als volgt uit:
```python
def recommend_products(self, product_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM equals WHERE '{product_id}'=ANY(products)") # kijken waar de gegeven product_id voorkomt in de array
        rows = cur.fetchall()
        if not rows:
            return None
        # print([item for sublist in [c[2] for c in rows] for item in sublist])
        # rows.sort(key = lambda rows: rows[-1]) # soorteren op groote array zodat we de kleinste kunnen pakken dit is meestal het meest overeenkomig qua eigenschappen.
        found_list = list(filter(lambda p: p != product_id, [item for sublist in [c[2] for c in rows] for item in sublist]))# lijst van alle gevonden producten met het gegeven product id eruit gefilterd
        res = {
            "length": len(found_list),
            "products": found_list,
            "occurences": Counter(found_list) # occurences van de items zodat je de products kan kiezen die met de meeste overeenkomen 
        }
        return res
```
Deze functie vraagt alle producten op die in de arrays voorkomen waar het gegeven product-id ook in voorkomt. Dit zijn meestal meerdere rows met grote arrays, deze list of lists word geflattened en op zijn beurt weer gesorteerd op frequentie. De functie returned de response en die bestaat uit de totale lijst, de lengte van de totale lijst en de lijst gesorteerd op frequentie.


# Advies

TODO: Geef aan welke algoritmes jullie adviseren aan de opdrachtgever, onderbouw dat advies. Koppel het advies aan de doelstellingen
