from grammar import Grammar
from derives_empty_string import derives_empty_string_algorithm
from first_operation import first_algorithm


class follow_algorithm:
    def __init__(self, G: Grammar) -> None:
        self.__G = G
        self.__first_alg = first_algorithm(G)
        self.__empty_string_alg = derives_empty_string_algorithm(G)
        self.__visited = {}
        self.__symbol_derives_empty = {}

    def run(self, A: str) -> set:
        self.__empty_string_alg.run()
        self.__symbol_derives_empty = self.__empty_string_alg.symbol_derives_empty()
        for X in self.__G.nonterminals():
            self.__visited[X] = False
        return self.internal_follow(A)

    def internal_follow(self, A: str) -> set:
        ans = set()
        if not self.__visited[A]:
            self.__visited[A] = True
            for (p, i) in self.__G.occurrences(A):
                tail = self.__G.tail(p, i)
                ans = ans.union(self.__first_alg.run(tail))
                if self.all_derive_empty(tail):
                    lhs = self.__G.lhs(self.__G.production((p, i)))
                    ans = ans.union(self.internal_follow(lhs))
        return ans

    def all_derive_empty(self, gamma: list) -> bool:
        for X in gamma:
            if self.__G.is_terminal(X) or not self.__symbol_derives_empty[X]:
                return False
        return True
