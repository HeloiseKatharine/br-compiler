class Grammar:

    def __init__(self) -> None:
        self.__terminals = {}
        self.__nonterminals = {}
        self.__productions = {}
        self.__id = 0

    def add_terminal(self, x: str) -> int:
        if x in self.__nonterminals:
            raise ValueError()
        self.__terminals[x] = self.__id
        self.__id = self.__id+1
        return self.__terminals[x]

    def add_nonterminal(self, X: str):
        if X in self.__terminals:
            raise ValueError()
        self.__nonterminals[X] = self.__id
        self.__id = self.__id + 1
        return self.__nonterminals[X]

    def grammar(self, S: str) -> None:
        self.add_nonterminal(S)

    def add_production(self, A: str, rhs: list) -> int:
        self.__productions[self.__id] = {'lhs': '', 'rhs': []}
        self.__productions[self.__id]['lhs'] = A
        self.__productions[self.__id]['rhs'] = rhs
        self.__id = self.__id+1
        return self.__id - 1

    def terminals(self) -> iter:
        return iter(self.__terminals)

    def nonterminals(self) -> iter:
        return iter(self.__nonterminals)

    def productions(self) -> iter:
        return iter(self.__productions)

    def is_terminal(self, X: str) -> bool:
        return X in self.__terminals

    def rhs(self, p: int) -> list:
        return self.__productions[p]['rhs']

    def lhs(self, p: int) -> str:
        return self.__productions[p]['lhs']

    def productions_for(self, A: str) -> list:
        l = []
        for k, v in self.__productions.items():
            if v['lhs'] == A:
                l.append(k)
        return l

    def occurrences(self, X: str) -> list:
        l = []
        for k, v in self.__productions.items():
            for i, rhs in enumerate(v['rhs']):
                if (rhs == X):
                    l.append((k, i))
        return l

    def production(self, O: tuple[int, int]) -> int:
        return O[0]

    def tail(self, p: int, i:int) -> list:
        return self.__productions[p]['rhs'][i+1:]
