from grammar import Grammar
from derives_empty_string import derives_empty_string_algorithm
from first_operation import first_algorithm
from follow_operation import follow_algorithm

def print_grammar(G: Grammar) -> None:
    print('Terminais:', ' '.join([x for x in G.terminals()]))
    print('Não-terminais:', ' '.join([X for X in G.nonterminals()]))
    # print(G.productions())
    print('Produções:', ' '.join(
        ['id: ' + str(p) + ' ' + str(G.lhs(p)) + '->' + str(G.rhs(p)) for p in G.productions()]))


if __name__ == '__main__':
    G = Grammar()
    G.grammar('S')
    G.add_nonterminal('A')
    G.add_nonterminal('B')
    G.add_terminal('a')
    G.add_terminal('b')
    G.add_terminal('c')
    G.add_production('S', ['A', 'B', 'c'])
    G.add_production('A', ['a'])
    G.add_production('A', ['c'])
    G.add_production('A', [])
    G.add_production('B', 'b')
    G.add_production('B', 'c')
    G.add_production('B', [])
 
    print_grammar(G)
    print('Imprimindo terminais')
    for x in G.terminals():
        print(x)
    print('Imprimindo não-terminais')
    for x in G.nonterminals():
        print(x)
    print('Imprimindo produções')
    for x in G.productions():
        print(x)
    print('Produçoes para A:')
    for productions in G.productions_for('A'):
        print(productions)

    print(G.rhs(6))
    print(G.lhs(6))
    print('Ocorrências de c')
    for occ in G.occurrences('c'):
        print(occ)
    print('Produção de cada ocorrência de c')
    for occ in G.occurrences('c'):
        print(G.production(occ))
    print('Tail de A na regra 6')
    print(G.tail(6,0))

    empty_alg = derives_empty_string_algorithm(G)
    empty_alg.run()
    print(empty_alg.rule_derives_empty())
    print(empty_alg.symbol_derives_empty()) 

    G.add_production('S',['A','B'])

    empty_alg = derives_empty_string_algorithm(G)
    empty_alg.run()
    print(empty_alg.rule_derives_empty())
    print(empty_alg.symbol_derives_empty()) 

    first_alg = first_algorithm(G)
    my_set = first_alg.run(['S'])
    print('First(S) = ',my_set)
    my_set = first_alg.run(['A'])
    print('First(A) = ',my_set)
    my_set = first_alg.run(['B'])
    print('First(B) = ',my_set)

    follow_alg = follow_algorithm(G)
    my_set = follow_alg.run(['A'])
    print('Follow(A) = ',my_set)