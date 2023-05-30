from grammar import Grammar

class derives_empty_string_algorithm:
    def __init__(self, G: Grammar) -> None:
        self.__symbol_derives_empty = {}
        self.__rule_derives_empty = {}
        self.__count = {}
        self.__queue = []
        self.__G = G

    def __check_for_empty(self,p:int)->None:
        if self.__count[p] == 0:
            self.__rule_derives_empty[p] = True
            A = self.__G.lhs(p)
            if not self.__symbol_derives_empty[A]:
                self.__symbol_derives_empty[A] = True
                self.__queue.append(A)

    def symbol_derives_empty(self)->dict:
        return self.__symbol_derives_empty
    
    def rule_derives_empty(self)->dict:
        return self.__rule_derives_empty

    def run(self):
        for A in self.__G.nonterminals():
            self.__symbol_derives_empty[A] = False
        for p in self.__G.productions():
            self.__rule_derives_empty[p] = False
            self.__count[p] = 0
            self.__count[p] += len(self.__G.rhs(p))
            self.__check_for_empty(p)
        while len(self.__queue):
            X = self.__queue.pop(0)
            for occ in self.__G.occurrences(X):
                p = self.__G.production(occ)
                self.__count[p]-=1
                self.__check_for_empty(p)

