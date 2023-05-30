import re
from grammar import Grammar
from token_sequence import token_sequence
from guided_ll1 import guided_ll1_parser

def create_ac_grammar()->Grammar:
    G = Grammar()
    G.add_terminal('floatdcl')
    G.add_terminal('intdcl')
    G.add_terminal('print')
    G.add_terminal('id')
    G.add_terminal('assign')
    G.add_terminal('plus')
    G.add_terminal('minus')
    G.add_terminal('inum')
    G.add_terminal('fnum')
    G.add_terminal('$')
    G.add_nonterminal('S')
    G.add_nonterminal('Dcls')
    G.add_nonterminal('Dcl')
    G.add_nonterminal('Stmts')
    G.add_nonterminal('Stmt')
    G.add_nonterminal('Expr')
    G.add_nonterminal('Val')
    G.add_production('S',['Dcls','Stmts','$']) # 17
    G.add_production('Dcls',['Dcl','Dcls']) # 18
    G.add_production('Dcls',[]) # 19
    G.add_production('Dcl',['floatdcl','id']) # 20
    G.add_production('Dcl',['intdcl','id']) # 21
    G.add_production('Stmts',['Stmt','Stmts']) # 22
    G.add_production('Stmts',[]) # 23
    G.add_production('Stmt',['id','assign','Val','Expr']) # 24
    G.add_production('Stmt',['print','id']) # 25
    G.add_production('Expr',['plus','Val','Expr']) # 26
    G.add_production('Expr',['minus','Val','Expr']) # 27
    G.add_production('Expr',[]) # 28
    G.add_production('Val',['id']) # 29
    G.add_production('Val',['inum']) # 30
    G.add_production('Val',['fnum']) # 31

    return G 


regex_table = {
    r'^f$': 'floatdcl',
    r'^i$': 'intdcl',
    r'^p$': 'print',
    r'^[abcdeghjlmnoqrstuvwxyz]$' : 'id',
    r'^=$':'assign',
    r'^\+$': 'plus',
    r'^\-$': 'minus',
    r'^[0-9]+$': 'inum',
    r'^[0-9]+\.[0-9]+$': 'fnum'
}

def lexical_analyser(filepath) -> str:
    with open(filepath,'r') as f:
        token_sequence = []
        tokens = []
        for line in f:
            tokens = tokens + line.split(' ')
        for t in tokens:
            found = False
            for regex,category in regex_table.items():
                if re.match(regex,t):
                    token_sequence.append(category)
                    found=True
            if not found:
                print('Lexical error: ',t)
                exit(0) 
    token_sequence.append('$')
    return token_sequence
    
if __name__ == '__main__':
    filepath = 'programa.ac'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_ac_grammar()
    parser = guided_ll1_parser(G)
    parser.parse(ts)

