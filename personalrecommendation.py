from rdbconnection2 import conrdb
from collections import Counter
import time

rdbcon, rdbcur = conrdb()


def getBoughtProduct(profile_id):
    """
    :param profile_id: str
    :return: Een lijst met producten die een profiel heeft gekocht
    """
    select_productsbought_Query = "SELECT array(SELECT product_id FROM orders, profile, sessions, buids WHERE profile.profile_id=buids.profile_id AND buids.browser_id=sessions.browser_id AND orders.session_id=sessions.session_id and buids.profile_id = %s)"
    rdbcur.execute(select_productsbought_Query, (profile_id,))
    return rdbcur.fetchall()[0][0]


def getSessionsBought(session_id):
    """
    :param session_id: str
    :return: Een lijst met producten die gekocht zijn door de gegeven session
    """
    query = "SELECT array(SELECT product_id FROM orders WHERE session_id = %s)"
    rdbcur.execute(query, (session_id,))
    return rdbcur.fetchall()[0][0]


def getEvents(profile_id):
    """
    :param profile_id: str
    :return: Een lijst met producten waar een gebruiker op heeft geklikt.
    """
    query = "SELECT array(SELECT product_id FROM events, sessions, buids WHERE buids.profile_id = %s AND buids.browser_id = sessions.browser_id AND sessions.session_id = events.session_id)"
    rdbcur.execute(query, (profile_id,))
    return rdbcur.fetchall()[0][0]


def getMostBoughtProducts(amount):
    """
    :param amount: amount of products
    :return: Een lijst met producten die het meest gekocht zijn
    """
    query = "SELECT array(SELECT product_id FROM orders GROUP BY product_id ORDER BY COUNT(*) DESC LIMIT %s)"
    rdbcur.execute(query, (amount,))
    return rdbcur.fetchall()[0][0]

def getSessionsBoughtProduct(product_id):
    """
    :param product_id: str
    :return: Een lijst met session ID's die een gegeven product hebben gekocht.
    """
    select_sessionsbought_query = "SELECT array( SELECT session_id FROM orders WHERE product_id = %s group by session_id order by session_id)"
    rdbcur.execute(select_sessionsbought_query, (product_id,))
    return rdbcur.fetchall()[0][0]


def getSessionFrequency(product_ids, gebruikerID=None):
    """
    :param product_ids: lijst met product-ids
    :param gebruikerID: str van profile_id
    :return: 4 meest overlappende sessions van de gegeven producten
    """

    if type(product_ids) != list:
        print("Input isn't a list")
        return None

    sessions = []
    for product in product_ids:
        sessions.extend(getSessionsBoughtProduct(product))

    # Kies niet de sessions van de gebruiker
    if gebruikerID != None:
        query = "select array(select session_id from sessions natural join buids where profile_id=%s group by session_id);"
        rdbcur.execute(query, (gebruikerID,))
        usersessions = rdbcur.fetchall()[0][0]
        for usersession in usersessions:
            if usersession in sessions:
                sessions.remove(usersession)

    # Return de frequency van sessions die het meest voorkomen in alle producten
    frequency = Counter(sessions)
    frequency = frequency.most_common(4)
    session_recommendations = []
    for session in frequency:
        session_recommendations.append(session[0])
    return session_recommendations


def getProductFrequency(session_ids):
    """
    :param session_ids:
    :return: Een lijst van 4 producten die het meeste voorkomen in de gegeven session_ids
    """
    if type(session_ids) != list:
        print("Error! Input isn't a list")
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
        bestsessions = getSessionFrequency(gekochteproducten, profile_id)
        recommendations = getProductFrequency(bestsessions)
        return recommendations
    else:
        # Als de gebruiker de gebruiker niets heeft gekocht, maar wel op een product heeft geklikt
        bekekenproducten = getEvents(profile_id)
        if bekekenproducten != []:
            bestsessions = getSessionFrequency(bekekenproducten, profile_id)
            recommendations = getProductFrequency(bestsessions)
            return recommendations
        # Als de gebruiker ook geen klik gedrag heeft geven we dan de 4 meest gekochte producten
        else:
            return getMostBoughtProducts(4)