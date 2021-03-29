# User story 1: Datakoppeling realiseren

PostgreSQL

| _GP-V1A-Groep 6_1778763 – Beau Dekker1778287 – Gaynora van Dommelen1779750 – Robin Kroesen1789287 – Khai-Tam Nguyen |
| --- |

# Relaties

_Profile – BUIDS_

Profiel heeft 1 of meer browserid&#39;s.
 Een browserid behoort tot één profiel.

_BUIDS – Session_

Een browserid kan 1 of meer sessies bevatten.
 Een sessie hoort bij één browserid.

_Session – Product_

Een sessie kan 1 of meer producten bevatten.
 Een product kan bij 1 of meer sessies horen.

_Session – Orders_

Een sessie kan 0, 1 of meerdere orders bevatten.
 Een order hoort bij één sessie.

_Orders – Product_

Een order kan 0, 1 of meer producten bevatten.
 Een product kan bij 0, 1 of meer orders zitten

# Logistiek datamodel

![](RackMultipart20210329-4-b70rj4_html_47220ad94eb547c3.png)

# DDL Script

DROP TABLE IF EXISTS Profile CASCADE;
DROP TABLE IF EXISTS BUIDS CASCADE;
DROP TABLE IF EXISTS Sessions CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Events CASCADE;

CREATE TABLE Profile (
 profile\_id varchar(255) PRIMARY KEY,
 viewed\_before VARCHAR(255)[],
 previously\_recommended VARCHAR(255)[],
 segment VARCHAR(50)
 );
CREATE TABLE BUIDS (
 browser\_id varchar(255) PRIMARY KEY,
 profile\_id varchar(255),
FOREIGN KEY (profile\_id)
REFERENCES Profile (profile\_id)
 );
CREATE TABLE Product (
 product\_id varchar(255) NOT NULL,
 naam varchar(255),
 brand varchar(255),
 gender varchar(255),
category varchar(255),
 sub\_category varchar(255),
 sub\_sub\_category varchar(255),
PRIMARY KEY (product\_id)
 );
CREATE TABLE Sessions (
 session\_id varchar(255) PRIMARY KEY,
 browser\_id varchar(255),
FOREIGN KEY (browser\_id)
REFERENCES BUIDS (browser\_id)
 );
CREATE TABLE Orders (
 session\_id varchar(255),
 product\_id varchar(255),
FOREIGN KEY (session\_id)
REFERENCES Sessions (session\_id),
FOREIGN KEY (product\_id)
REFERENCES Product (product\_id)
 );
CREATE TABLE Events (
 product\_id varchar(255) NOT NULL,
 session\_id varchar(255) NOT NULL,
FOREIGN KEY (product\_id)
REFERENCES Product (product\_id),
FOREIGN KEY (session\_id)
REFERENCES Sessions (session\_id)
 );

Deze is terug te vinden in &#39;createTables.py&#39;

# Data overzetten

## Connectie maken met MongoDB

Voor het verbinden met mongodb is de volgende functie aangemaakt:

_def_ conmdb():

    try:

        myclient = MongoClient()

        db = myclient[&quot;huwebshop&quot;]

        return db

    except pymongo.DatabaseError:

        print(&quot;Connection with mongodb failed&quot;)

Deze is terug te vinden in &#39;mdbconnection2.py&#39;

## Connectie maken met PostgreSQL

Voor de verbinding met postgres is eveneens een functie aangemaakt:

_def_ conrdb():

    try:

        connectionRDB = psycopg2.connect(

            _user_=&#39;postgres&#39;,

            _password_=\&lt;ww\&gt;,

            _host_=&#39;localhost&#39;,

            _database_=&#39;DocumentStore&#39;

        )

        cursor = connectionRDB.cursor()

        return connectionRDB, cursor

    except (_Exception_, psycopg2.DatabaseError) as e:

        print(e)

Deze is terug te vinden in &#39;rdbconnection2.py&#39;

## Overzetting

Voor het overschrijven van de tabellen naar de database in postgres zijn verschillende functies geschreven:

### Product

Omdat de tabel product op zichzelf staat (geen FK&#39;s heeft) wordt deze als eerste ingelezen met behulp van de volgende functie:

_def_ PRODUCTS():

    for element in mdbcur[&quot;products&quot;].find():

        temp =[

            element[key]

            if not isinstance(element[key], _dict_) # ervan uitgaande dat er maar één dict in voorkomt

            else get\_subvalue(element[key], None) # neem de values van de sub\_keys

            for key in [

                &quot;\_id&quot;,

                &quot;name&quot;,

                &quot;brand&quot;,

                &quot;gender&quot;,

                &quot;category&quot;,

                &quot;sub\_category&quot;,

                &quot;sub\_sub\_category&quot;]

            if key in element # Doe bovenstaande als de key bestaat in het document

        ]

        while len(temp) \&lt;= 6:

            temp.append(None)

        product\_query = &quot;INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s)&quot;

        rdbcur.execute(product\_query, temp)

        rdbcon.commit()

Voor elke element in de collectie wordt gezocht naar de values van de keys &#39;id&#39;, &#39;name&#39;, &#39;brand&#39;, &#39;gender&#39;, &#39;category&#39;, &#39;sub\_category&#39; en &#39;sub\_sub\_category&#39; als deze bestaan. De worden in een lijst gestopt en evt. aangevuld met &#39;None&#39; als niet alle erin zaten. (In de loop wordt zelf al None toegevoegd als deze niet bestaat, maar alleen als er keys volgen na de specifieke key. Anders wordt geen nieuwe index met None aangemaakt.) Daarna worden de producten naar de rdb geschreven.

### Profile &amp; buids

Na product blijft er één tabel over die op zichzelf staat: Profile.
 Profile en buids worden na elkaar in de rdb gezet, omdat in een document van een profile aangegeven staat welke browserid&#39;s erbij horen en er dan maar één keer door de collectie heen hoeft te worden gelopen. Hiervoor zijn de volgende functies gemaakt:

_def_ PROFILES():

    profile\_var = []

    buids\_var = []

    for element in mdbcur[&quot;profiles&quot;].find():

        temp =[

            element[key]

            if not isinstance(element[key], _dict_) # ervan uitgaande dat er maar één dict in voorkomt

            else get\_subvalue(element[key], [&quot;segment&quot;, &quot;viewed\_before&quot;]) # neem de values van de sub\_keys

            for key in [

                &quot;\_id&quot;,

                &quot;buids&quot;,

                &quot;recommendations&quot;,

                &quot;previously\_recommended&quot;]

            if key in element # Doe bovenstaande als de key bestaat in het document

        ]

        try:

            profile\_var.append([_str_(temp[0]), temp[2][1], temp[3], temp[2][0]])

            for browserid in temp[1]:

                buids\_var.append([browserid, _str_(temp[0])])

        except _IndexError_:

            pass

    profile\_query = &quot;INSERT INTO profile VALUES (%s, %s, %s, %s)&quot;

    rdbcur.executemany(profile\_query, profile\_var)

    rdbcon.commit()

    buids\_query = &quot;INSERT INTO buids VALUES (%s, %s) ON CONFLICT (browser\_id) DO NOTHING&quot;

    rdbcur.executemany(buids\_query, buids\_var)

    rdbcon.commit()

Zoals misschien al wel is opgevallen lijken de functies products en profiles heel erg op elkaar. Dit komt doordat bij het gebruiken van een functie voor het ophalen van deze values en het stoppen van deze values in een lijst zorgde voor enorme overbelasting van de memory waardoor computers vastliepen. Vandaar de keuze meteen in de loop een insertion te doen en de opbouw van het inlezen van de collectie deels hetzelfde is.

Voor de buids geldt, dat naast het doorheen lopen van de profielen onze tabel berust op FK profile\_id en een browser\_id als PK waardoor door de lijst van de buids gegaan wordt en elk browser\_id gelinkt wordt aan een profile\_id. Deze lijsten worden vervolgens naar de bijbehorende tabellen geschreven.

### Sessions, Orders &amp; Events

Evenals bij de profiles wordt hier één keer door de collectie in mongodb heengelopen en worden lijsten aangemaakt voor de verschillende tabellen waarin de bijbehorende values komen te staan.

_def_ SESSIONS():

    limit = 100000

    skip = 0

    time = 0

    for i in range(0, 34):

        begin\_ses\_ev\_or = perf\_counter()

        sessions\_var = []

        events\_var = []

        orders\_var = []

        for element in mdbcur[&quot;sessions&quot;].find().skip(skip).limit(limit):

            temp =[

                element[key]

                if not isinstance(element[key], _dict_) # ervan uitgaande dat er maar één dict in voorkomt

                else get\_subvalue(element[key], [&quot;products&quot;]) # neem de values van de sub\_keys

                for key in [

                    &quot;\_id&quot;,

                    &quot;buid&quot;,

                    &quot;events&quot;,

                    &quot;order&quot;]

                if key in element # Doe bovenstaande als de key bestaat in het document

            ]

            try:

                if temp[3] is not None:

                    if temp[3][0] is not None:

                        for product in temp[3][0]:

                            orders\_var.append([product[&quot;id&quot;], temp[0], temp[0], product[&quot;id&quot;]])

                sessions\_var.extend([[temp[1][0], temp[0], temp[1][0]] if not isinstance(temp[1][0], _list_) else [temp[1][0][0], temp[0], temp[1][0][0]]])

                events\_var.extend([

                    [event[&quot;product&quot;], temp[0], event[&quot;product&quot;], temp[0]]

                    if &quot; &quot; not in event[&quot;product&quot;]

                    else [event[&quot;product&quot;].split(&quot; &quot;)[0], temp[0], event[&quot;product&quot;].split(&quot; &quot;)[0], temp[0]]

                    for event in temp[2]

                    if &quot;product&quot; in event and event[&quot;product&quot;] is not None

                ])

            except _IndexError_:

                pass

        events\_var = [event for event in events\_var if event]

        sessions\_query = &quot;DO $$ BEGIN IF (SELECT EXISTS (SELECT browser\_id FROM buids WHERE browser\_id=%s)::int) THEN INSERT INTO sessions VALUES (%s, %s); END IF; END $$;&quot;

        orders\_query = &quot;DO $$ BEGIN IF (SELECT EXISTS (SELECT product\_id FROM product WHERE product\_id=%s)::int) THEN IF(SELECT EXISTS (SELECT session\_id FROM sessions WHERE session\_id=%s)::int) THEN INSERT INTO orders VALUES (%s, %s); END IF; END IF; END $$;&quot;

        events\_query = &quot;DO $$ BEGIN IF (SELECT EXISTS (SELECT product\_id FROM product WHERE product\_id=%s)::int) THEN IF(SELECT EXISTS (SELECT session\_id FROM sessions WHERE session\_id=%s)::int) THEN INSERT INTO events VALUES (%s, %s); END IF; END IF; END $$;&quot;

        rdbcur.executemany(sessions\_query, sessions\_var)

        rdbcon.commit()

        rdbcur.executemany(orders\_query, orders\_var)

        rdbcon.commit()

        rdbcur.executemany(events\_query, events\_var)

        rdbcon.commit()

        skip += limit

Wat bij deze functie extra is, is de iteratieve manier van documenten inlezen. Voor deze versie deden we dat eerst ineenkeer wat een memory error opleverde en daarna op een recursieve manier waardoor we nog steeds een memory error kregen, daarom is gekozen voor iteratief. Voor deze functie is uniek dat bij het inserten van een row eerst gekeken wordt of de bijbehorende FK&#39;s bestaan, omdat sommige sessions geen bestaande browser\_id hadden in onze tabel buids. Wat als gevolg had dat niet alle sessies bestonden en dus ook op sessies gecheckt moest worden. Daarnaast bestonden sommige product\_id&#39;s niet die voorkwamen in events en/of orders waardoor er bij het invoegen van deze gegegevens in de tabel – naast de session\_id – ook gekeken moest worden naar product\_id.

De code is terug te vinden in &#39;DataOverzetten2.py&#39;.

## De tabellen

D.m.v. van een simpele query als

select \* from \&lt;tabel\_naam\&gt;;

zijn de volgende tabellen opgehaald:

### Product

![](RackMultipart20210329-4-b70rj4_html_669c731e4c37d655.png)

### Profile

![](RackMultipart20210329-4-b70rj4_html_984745849529108f.png)

### Buids

![](RackMultipart20210329-4-b70rj4_html_cbfc406a877ab8f4.png)

### Session

![](RackMultipart20210329-4-b70rj4_html_8137e09b3898831a.png)

### Orders

![](RackMultipart20210329-4-b70rj4_html_f70922c48319efe4.png)

### Events

![](RackMultipart20210329-4-b70rj4_html_c5ce6234e263e6cb.png)