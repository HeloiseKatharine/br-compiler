from grammar import Grammar
from predict import predict_algorithm
from token_sequence import token_sequence
from ll1_check import is_ll1


class guided_ll1_parser:
    def __init__(self, G: Grammar) -> None:
        self.__G = G
        self.__lltable = {}
        self.__pred_alg = predict_algorithm(G)
        if not is_ll1(self.__G, self.__pred_alg):
            print('The grammar is not LL1')
            exit(0)
        self.__fill_table()

    def __fill_table(self) -> None:

        for A in self.__G.nonterminals():
            for a in self.__G.terminals():
                self.__lltable[(A, a)] = -1
        for A in self.__G.nonterminals():
            for p in self.__G.productions_for(A):
                for a in self.__pred_alg.predict(p):
                    self.__lltable[(A, a)] = p

    def __apply(self, stck: list, p: int) -> None:
        stck.pop()
        rhs = self.__G.rhs(p)
        for t in reversed(rhs):
            stck.append(t)

    def parse(self, ts: token_sequence):
        stck = ['S']
        accept = False
        while not accept:
            top = stck[-1]
            if self.__G.is_terminal(top):
                ts.match(top)
                if top == '$':
                    accept = True
                stck.pop()
            else:
                p = self.__lltable[(top, ts.peek())]
                if p == -1:
                    print('Syntax error. No rule for (', top, ',', ts.peek(), ')')
                    exit(0)
                self.__apply(stck, p)
