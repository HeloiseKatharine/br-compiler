from grammar import Grammar
from predict import predict_algorithm


def is_ll1(G: Grammar, pred_alg: predict_algorithm) -> bool:
    for A in G.nonterminals():
        pred_set = set()
        print('Nonterminal: ', A)
        for p in G.productions_for(A):
            print('Production: ',G.lhs(p),'->',G.rhs(p))
            print('pred_set',pred_set)
            pred = pred_alg.predict(p)
            print('pred',pred)
            if not pred_set.isdisjoint(pred):
                print('Problem here')
                return False
            pred_set.update(pred)

    return True