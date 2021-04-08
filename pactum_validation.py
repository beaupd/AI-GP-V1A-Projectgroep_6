"""
 _________________________________________________________________
(____________________ VERPLICHTE STEEKPROEF ______________________)
1. Een anonieme bezoeker opent de productdetailpagina van product
met Product_id: '23866'. Welke producten worden als vergelijkbare 
producten aanbevolen?

 _________________________________________________________________
(______________________ EIGEN STEEPROEVEN ________________________)
De 20 eerste producten in de tabel product. Er wordt gekeken naar
de overeenkomsten tussen de kenmerken van de meegegeven product en
de recoms. Als deze minstens met 3 kenmerken overeenkomen worden 
de recommendations goedgekeurd.
"""

from pactum import Pactum
from popular_return_recoms import return_selection
from rdbconnection2 import conrdb

rdbcon, rdbcur = conrdb()

pac = Pactum(rdbcon)

select_product_kenmerken_query = """select array[brand, gender, category, sub_category, sub_sub_category] from product 
                                    where product_id=ANY(%s::varchar[]) 
                                    group by brand, gender, category, sub_category, sub_sub_category;"""


def eigen_steekproef():
    cases_query = """select array(select product_id from product limit 20);"""
    cases = return_selection(cases_query, (None,))
    for case in cases:
        prodids = pac.get_n_recommended(case, 4)
        prodids = [x[0] for x in prodids]
        verwachte_output = return_selection(select_product_kenmerken_query, ([case],))
        output = return_selection(select_product_kenmerken_query, (prodids,))
        _output_ = set(verwachte_output) - set(output)
        assert len(_output_) <= 2, f"De input {case} geeft {output}. De verwachte output is {verwachte_output}."

def main():
    try:
        prodids = pac.get_n_recommended("23866", 4)
        prodids = [x[0] for x in prodids]
        assert return_selection(select_product_kenmerken_query, (["23866"],)) == return_selection(select_product_kenmerken_query, (prodids,)), f"De input geeft niet de verwachte output."

        print("Verplichte steekproef is geslaagd!")

        eigen_steekproef()
        print("Eigen steekproef met 20 random productid's is geslaagd!")
    except AssertionError as ae:
        print(ae)

if __name__ == "__main__":
    main()