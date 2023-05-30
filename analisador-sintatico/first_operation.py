from derives_empty_string import derives_empty_string_algorithm
from grammar import Grammar


class first_algorithm:
    def __init__(self, G: Grammar) -> None:
        self.__G = G
        self.__visited = {}
        self.__symbol_derives_empty = {}

    def internal_first(self, alfa: list):
        if alfa == []:
            return set()
        X = alfa[0]
        beta = alfa[1:]
        if self.__G.is_terminal(X):
            return set([X])
        ans = set()
        if not self.__visited[X]:
            self.__visited[X] = True
            for p in self.__G.productions_for(X):
                rhs = self.__G.rhs(p)
                ans = ans.union(self.internal_first(rhs))
        if self.__symbol_derives_empty[X]:
            ans = ans.union(self.internal_first(beta))
        return ans

    def run(self, alfa: list) -> set:
        for X in self.__G.nonterminals():
            self.__visited[X] = False
        alg_empty = derives_empty_string_algorithm(self.__G)
        alg_empty.run()
        self.__symbol_derives_empty = alg_empty.symbol_derives_empty()
        return self.internal_first(alfa)
