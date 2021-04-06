from huw_recommend import ReturnSelectExecution

def simple_algorithm(category_page):
    """
        Deze functie modificeert een meegegeven lijst met de recommendation
        producten uit de meest_gekocht tabel filter op basis van de categoriepagina.

        :param category_page: str : categorie
    """
    pass

def gender_category_based_algorithm(huidige_klikt_events, category_page):
    """
        Deze functie modificeert een meegegeven lijst met de recommendation
        producten uit de gender_category tabel filter op basis van het meestvoorkomende
        gender en de huidige categoriepagina.

        :param huidige_klik_events: list: lijst met productid's
        :param category_page: str : categorie
    """ 
    pass

def return_recommended_products(klikevents):
    """
        Deze functie geeft een lijst met productid's terug die
        passen bij het gedrag van de user op de website.

        :param klikevents: list: lijst met productid's
        :returns: list : lijst met productid's
    """
    # 1.    User klikt op 'n categorie pagina (i)
    # 2.    Als user bekend is
    # 2.1       Als user eerdere orders heeft
    # 2.1.1         Select segment van user
    # 2.1.2         Select alle genders die voorkomen in de orders van de user met de frequentie voor elke gender
    # 2.1.3         Select het gender dat het meest voorkomt
    # 2.1.4         Als de combinatie segment-gender-category bestaat in de tabel popular
    # 2.1.4.1           Select de productid's die horen bij de combi segment-gender-category
    # 2.1.4.2           Return productid's (o)
    # 2.1.4.3           END
    # 2.1.5         Anders
    # 2.1.5.1           Return lege lijst (o)
    # 2.1.5.2           EIND
    # 2.2       Anders
    # 2.2.1         Als user huidige klik events heeft -----------------------------------------------------+
    # 2.2.1.1           Select meest voorkomende product gender in klik events                              |
    # 2.2.1.2           Als de combinatie gender-category bestaat in de tabel gender_category               |
    # 2.2.1.2.1             Select de product_id's behorende bij de combinatie gender-category              |   ==============================================
    # 2.2.1.2.2             Return productid's (o)                                                          |   Gender-Category based Recommendation Algorithm
    # 2.2.1.2.3             EIND                                                                            |   ==============================================
    # 2.2.1.3           Anders                                                                              |
    # 2.2.1.3.1             Return lege lijst (o)                                                           |
    # 2.2.1.3.2             EIND ---------------------------------------------------------------------------+
    # 2.2.2         Anders ---------------------------------------------------------------------------------+
    # 2.2.2.1           Select de productid's behorende bij categorie uit de meest_gekocht tabel            |   ================================
    # 2.2.2.2           Return productid's (o)                                                              |   Simple Recommendation Algorithm
    # 2.2.2.3           EIND -------------------------------------------------------------------------------+   ================================
    # 3.    Anders
    # 3.1       Als user huidige klik events heeft ---------------------------------------------------------+
    # 3.1.1         Select meest voorkomende product gender in klik events                                  |
    # 3.1.2         Als de combinatie gender-category bestaat in de tabel gender_category                   |
    # 3.1.2.1           Select de product_id's behorende bij de combinatie gender_category                  |   ==============================================
    # 3.1.2.2           Return productid's (o)                                                              |   Gender-Category based Recommendation Algorithm
    # 3.1.2.3           EIND                                                                                |   ==============================================
    # 3.1.3         Anders                                                                                  |
    # 3.1.3.1           Return lege lijst (o)                                                               |
    # 3.1.3.2           EIND -------------------------------------------------------------------------------+
    # 3.2       Anders -------------------------------------------------------------------------------------+
    # 3.2.1         Select de productid's behorende bij categorie uit de meest_gekocht tabel                |   ===============================
    # 3.2.2         Return productid's (o)                                                                  |   Simple Recommendation Algorithm
    # 3.2.3         EIND -----------------------------------------------------------------------------------+   ===============================
    pass