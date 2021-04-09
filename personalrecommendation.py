from rdbconnection2 import conrdb
from collections import Counter
import time

rdbcon, rdbcur = conrdb()


def getBoughtProduct(profile_id):
    """
    :param profile_id: str van profiel ID
    :return: Een lijst met producten die een profiel heeft gekocht
    """
    select_productsbought_Query = "SELECT array(SELECT product_id FROM orders, profile, sessions, buids WHERE profile.profile_id=buids.profile_id AND buids.browser_id=sessions.browser_id AND orders.session_id=sessions.session_id and buids.profile_id = %s)"
    rdbcur.execute(select_productsbought_Query, (profile_id,))
    return rdbcur.fetchall()[0][0]


def getSessionsBought(session_id):
    """
    :param session_id: str van session ID
    :return: Een lijst met producten die gekocht zijn door de gegeven session
    """
    query = "SELECT array(SELECT product_id FROM orders WHERE session_id = %s GROUP BY product_id ORDER BY product_id)"
    rdbcur.execute(query, (session_id,))
    return rdbcur.fetchall()[0][0]


def getEvents(profile_id):
    """
    :param profile_id: str van profiel ID
    :return: Een lijst met producten waar een gebruiker op heeft geklikt.
    """
    query = "SELECT array(SELECT product_id FROM events, sessions, buids WHERE buids.profile_id = %s AND buids.browser_id = sessions.browser_id AND sessions.session_id = events.session_id)"
    rdbcur.execute(query, (profile_id,))
    return rdbcur.fetchall()[0][0]


def getMostBoughtProducts(amount):
    """
    :param amount: hoeveelheid producten die worden getoond
    :return: Een lijst met producten die het meest gekocht zijn
    """
    query = "SELECT array(SELECT product_id FROM orders GROUP BY product_id ORDER BY COUNT(*) DESC LIMIT %s)"
    rdbcur.execute(query, (amount,))
    return rdbcur.fetchall()[0][0]

def getSessionsBoughtProduct(product_id):
    """
    :param product_id: str van product ID
    :return: Een lijst met session ID's die een gegeven product hebben gekocht.
    """
    select_sessionsbought_query = "SELECT array( SELECT session_id FROM orders WHERE product_id = %s group by session_id order by session_id)"
    rdbcur.execute(select_sessionsbought_query, (product_id,))
    return rdbcur.fetchall()[0][0]


def getSessionFrequency(product_ids, gebruikerID):
    """
    :param product_ids: lijst met product-ids
    :return: 12 meest overlappende sessions van de gegeven producten
    """

    if type(product_ids) != list:
        print("Input isn't a list")
        return None

    sessions = []
    for product in product_ids:
        sessions.extend(getSessionsBoughtProduct(product))

    # Kies niet de sessions van de gebruiker
    query = "select array(select session_id from sessions natural join buids where profile_id=%s group by session_id);"
    rdbcur.execute(query, (gebruikerID,))
    usersessions = rdbcur.fetchall()[0][0]
    for usersession in usersessions:
        # Als een sessie van de gebruiker in de lijst zit, verwijder alle sessies.
        if usersession in sessions:
            try:
                while True:
                    sessions.remove(usersession)
            except ValueError:
                pass

    # Return de frequency van sessions die het meest voorkomen in alle producten
    frequency = Counter(sessions)
    frequency = frequency.most_common(12)
    session_recommendations = []
    for session in frequency:
        session_recommendations.append(session[0])
    return session_recommendations


def getProductFrequency(session_ids):
    """
    :param session_ids: lijst met session IDs
    :param gebruikerID: str
    :return: Een lijst van 4 producten die het meeste voorkomen in de gegeven session_ids
    """
    if type(session_ids) != list:
        print("Error! SessionIDs isn't a list")
        return None
    boughtProducts = []
    for session_id in session_ids:
        boughtProducts.extend(getSessionsBought(session_id))

    frequency = Counter(boughtProducts)
    frequency = frequency.most_common(4)
    product_recommendations = []
    # We willen alleen de 4 producten returnen
    for product_id in frequency:
        product_recommendations.append(product_id[0])
    return product_recommendations


def giveRecommendation(profile_id):
    """
    :param profile_id: str
    :return: Kan 3 dingen returnen gebaseerd op of een gebruiker iets heeft gekocht en het klikgedrag van de gebruiker.
    Als de gebruiker niks heeft gekocht wordt er gekeken naar het klikgedrag. Als er geen klikgedrag is wordt er gekeken
    naar de 4 meest gekochte producten.
    """
    gekochteproducten = getBoughtProduct(profile_id)

    # Doe dit alleen als de gebruiker iets heeft gekocht
    if gekochteproducten != []:
        begin = time.time()
        bestsessions = getSessionFrequency(gekochteproducten, profile_id)
        recommendations = getProductFrequency(bestsessions)
        end = time.time()
        print(end - begin)
        return recommendations
    else:
        # Als de gebruiker de gebruiker niets heeft gekocht, maar wel op een product heeft geklikt
        bekekenproducten = getEvents(profile_id)
        if bekekenproducten != []:
            bestsessions = getSessionFrequency(bekekenproducten, profile_id)
            recommendations = getProductFrequency(bestsessions)
            return recommendations
        # Als de gebruiker ook geen klik gedrag heeft, dan geven we de 4 meest gekochte producten
        else:
            return getMostBoughtProducts(4)