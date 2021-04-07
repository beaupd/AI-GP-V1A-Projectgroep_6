from huw_recommend import ReturnSelectExecution
from collections import Counter

def highest_frequency(array):
    """
        Zoekt het element met de hoogste frequentie in een lijst.

        :param array: list: lijst met elementen
    """
    freq = Counter(array)
    return freq.most_common(1)[0][0]

def simple_algorithm(prodids, category_page):
    """
        Deze functie modificeert een meegegeven lijst met de recommendation
        producten uit de meest_gekocht tabel filter op basis van de categoriepagina.

        :param category_page: str : categorie
    """
    pass

def gender_category_based_algorithm(prodids, klik_events, category_page):
    """
        Deze functie modificeert een meegegeven lijst met de recommendation
        producten uit de gender_category tabel filter op basis van het meestvoorkomende
        gender en de huidige categoriepagina.

        :param klik_events: list: lijst met productid's
        :param category_page: str : categorie
    """ 
    user_all_genders_query = """"select array(select lower(gender) from product where product_id=ANY(%s::varchar[]));""""
    user_all_genders = ReturnSelectExecution(user_all_genders_query, (klikevents,))
    user_gender = highest_frequency(user_all_genders)
    _combi_bestaat_query = """select exists(select * from gender_category where gender=%s and category=%s)::int"""
    if ReturnSelectExecution(_combi_bestaat_query, (user_gender, category_page,)):
        prodids_query = """select array[product_id1, product_id2, product_id3, product_id4] from gender_category where gender=%s and category=%s"""
        prodids = ReturnSelectExecution(prodids_query, (user_gender, category_page,))

def return_recommended_products(profileid, category_page, klik_events):
    """
        Deze functie geeft een lijst met productid's terug die
        passen bij het gedrag van de user op de website.

        :param klikevents: list: lijst met productid's
        :returns: list : lijst met productid's
    """
    prodids = []
    _user_is_bekend_query = """select exists (select * from profile where profile_id=%s)::int"""
    _user_heeft_orders_query = """select exists(select * from orders
                                    natural join(select * from sessions
                                    natural join(select browser_id from buids
                                    where profile_id=%s) as _id) as __id)::int;"""
    if ReturnSelectExecution(_user_is_bekend_query, (profileid,)) and ReturnSelectExecution(_user_heeft_orders_query, (profileid,)):
        user_segment_query = """select lower(segment) from profile where profile_id=%s"""
        user_segment = ReturnSelectExecution(user_segment_query, (profileid,))
        user_all_genders_query = """select array(select lower(gender) from product
                                    natural join(select product_id from orders
                                    natural join(select session_id from sessions
                                    natural join(select browser_id from buids
                                    where profile_id=%s) as _id) as __id) as ___id)"""
        user_all_genders = ReturnSelectExecution(user_all_genders_query, (profileid,))
        user_gender = highest_frequency(user_all_genders)
        _combi_bestaat_query = """select exists(select * from popular where lower(segment)=%s and lower(gender)=%s and lower(category)=%s)::int;"""
        if ReturnSelectExecution(_combi_bestaat_query, (user_segment, user_gender, category_page,)):
            prodids_query = """select array[product_id1, product_id2, product_id3, product_id4] from popular
                                where lower(segment)=%s and lower(gender)=%s and lower(category)=%s;"""
            prodids = ReturnSelectExecution(prodids_query, (user_segment, user_gender, category_page,))
    else:
        if klikevents:
            gender_category_based_algorithm(prodids, klik_events, category_page)
        else:
            simple_algorithm(prodids, category_page)
    return prodids