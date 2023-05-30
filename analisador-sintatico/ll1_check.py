from grammar import Grammar
from predict import predict_algorithm


def is_ll1(G: Grammar, pred_alg: predict_algorithm) -> bool:
    for A in G.nonterminals():
        pred_set = set()
        for p in G.productions_for(A):
            pred = pred_alg.predict(p)
            if len(pred_set & pred) != 0:
                return False
            pred_set.union(pred)
    return True
