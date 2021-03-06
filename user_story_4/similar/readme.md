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
