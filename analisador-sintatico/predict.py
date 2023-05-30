from grammar import Grammar
from derives_empty_string import derives_empty_string_algorithm
from follow_operation import follow_algorithm
from first_operation import first_algorithm


class predict_algorithm:
    def __init__(self, G: Grammar) -> None:
        self.__G = G
        self.__first_alg = first_algorithm(self.__G)
        self.__follow_alg = follow_algorithm(self.__G)
        derives_empty_alg = derives_empty_string_algorithm(self.__G)
        derives_empty_alg.run()
        self.__rule_derives_empty = derives_empty_alg.rule_derives_empty()

    def predict(self,p:int)->set:
        ans = self.__first_alg.run(self.__G.rhs(p))
        if self.__rule_derives_empty[p]:
            A = self.__G.lhs(p)
            ans = ans.union(self.__follow_alg.run(A))
        return ans