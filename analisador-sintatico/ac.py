import re
from grammar import Grammar
from token_sequence import token_sequence
from predict import predict_algorithm
from ll1_check import is_ll1

def create_ac_grammar()->Grammar:
    G = Grammar()
 
    G.add_production('Programa',['Dcls','Stmts','fim']) #1
    G.add_production('Dcls',['Dcl','Dcls']) #2
    G.add_production('Dcls',[]) #3
    G.add_production('Dcl',['floatdcl','id']) #4
    G.add_production('Dcl',['intdcl','id']) #5
    G.add_production('Stmts',['Stmt','Stmts']) #6
    G.add_production('Stmts',[]) #7
    G.add_production('Stmt',['id','assign','Expr']) #8
    G.add_production('Stmt',['while','Expr','do','Stmt','Stmts', 'endwhile']) #9
    G.add_production('Stmt',['if','Expr','then','Stmt','Stmts', 'StmtIf']) #10
    G.add_production('Stmt',['print','Expr']) #11
    G.add_production('StmtIf',['endif']) #12
    G.add_production('StmtIf',['else','Stmt','Stmts','endif']) #13
    G.add_production('ExprLogica',['Expr','Comparador', 'Expr']) #14
    G.add_production('Comparador',['maior']) #15
    G.add_production('Comparador',['maiorIgual']) #16
    G.add_production('Comparador',['menor']) #17
    G.add_production('Comparador',['menorIgual']) #18
    G.add_production('Comparador',['igual']) #19
    G.add_production('Comparador',['diferente']) #20
    G.add_production('Expr',['Termo','Expr1']) #21
    G.add_production('Expr1',['adicao','Termo','Expr1']) #22
    G.add_production('Expr1',['subtracao','Termo','Expr1']) #23
    G.add_production('Expr1',[]) #24
    G.add_production('Termo',['Fator','Termo1']) #25
    G.add_production('Termo1',['multiplicacao','Fator','Termo1']) #26
    G.add_production('Termo1',['divisao','Fator','Termo1']) #27
    G.add_production('Termo1',[]) #28
    G.add_production('Fator',['id']) #29
    G.add_production('Fator',['inum']) #30
    G.add_production('Fator',['fnum']) #31
    G.add_production('Fator',['(','Expr',')']) #32
    
    G.add_terminal('floatdcl')
    G.add_terminal('intdcl')
    G.add_terminal('print')
    G.add_terminal('id')
    G.add_terminal('if')
    G.add_terminal('then')
    G.add_terminal('endif')
    G.add_terminal('else')
    G.add_terminal('while')
    G.add_terminal('do')
    G.add_terminal('endwhile')
    G.add_terminal('assign')
    G.add_terminal('adicao')
    G.add_terminal('subtracao')
    G.add_terminal('multiplicacao')
    G.add_terminal('divisao')
    G.add_terminal('inum')
    G.add_terminal('fnum')
    G.add_terminal('fim')
    G.add_terminal('(')
    G.add_terminal(')')
    G.add_terminal('maior')
    G.add_terminal('maiorIgual')
    G.add_terminal('menor')
    G.add_terminal('menorIgual')
    G.add_terminal('igual')
    G.add_terminal('diferente')

    G.add_nonterminal('Programa')
    G.add_nonterminal('Dcls')
    G.add_nonterminal('Dcl')
    G.add_nonterminal('Stmts')
    G.add_nonterminal('Stmt')
    G.add_nonterminal('StmtIf')
    G.add_nonterminal('Expr')
    G.add_nonterminal('Expr1')
    G.add_nonterminal('Termo')
    G.add_nonterminal('Termo1')
    G.add_nonterminal('Fator')
    G.add_nonterminal('ExprLogica')
    G.add_nonterminal('Comparador')
   
    return G 


regex_table = {
    r'^crieUmInteiro$': 'floatdcl',
    r'^crieUmRacional$': 'intdcl',
    r'^mostreNaTela$': 'print',
    r'^agoraEh$':'assign',
    r'^\+$': 'adicao',
    r'^\-$': 'subtracao',
    r'^\*$': 'multiplicacao',
    r'^\/$': 'divisao',
    r'^[a-z]$' : 'id',
    r'^[0-9]+$': 'inum',
    r'^[0-9]+\.[0-9]+$': 'fnum',
    r'^se$': 'if',
    r'^entao$': 'then',
    r'^fimSe$': 'endif',
    r'^senao$': 'else',
    r'^enquanto$': 'while',
    r'^faca$': 'do',
    r'^fimEnquanto$': 'endwhile',
    r'^EhMaior$': 'maior',
    r'^EhMaiorIgual$': 'maiorIgual',
    r'^EhMenor$': 'menor',
    r'^EhMenorIgual$': 'menorIgual',
    r'^EhIgual$': 'igual',
    r'^EhDiferente$': 'diferente'
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

def Prog(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(1):
        Dcls(ts,p)
        Stmts(ts,p)
        ts.match('fim')

def Dcls(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(2):
        Dcl(ts,p)
        Dcls(ts,p)
    elif ts.peek() in p.predict(3):
        return
    
def Dcl(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(4):
        ts.match('floatdcl')
        ts.match('id')
    elif ts.peek() in p.predict(5):
        ts.match('intdcl')
        ts.match('id')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Stmts(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(6):
        Stmt(ts,p)
        Stmts(ts,p)
    elif ts.peek() in p.predict(7):
        return

def Stmt(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(8):
        ts.match('id')
        ts.match('assign')
        Expr(ts,p)
    elif ts.peek() in p.predict(9):
        ts.match('while')
        Expr(ts,p)
        ts.match('do')
        Stmt(ts,p)
        Stmts(ts,p)
        ts.match('endwhile')
    elif ts.peek() in p.predict(10):
        ts.match('if')
        Expr(ts,p)
        ts.match('then')
        Stmt(ts,p)
        Stmts(ts,p)
        StmtIf(ts,p)
    elif ts.peek() in p.predict(11):
        ts.match('print')
        Expr(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)
def StmtIf(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(12):
        ts.match('endif')
    elif ts.peek() in p.predict(13):
        ts.match('else')
        Stmt(ts,p)
        Stmts(ts,p)
        ts.match('endif')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def ExprLogica(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(14):
        Expr(ts,p)
        Comparador(ts,p)
        Expr(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Comparador(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(15):
        ts.match('maior')
    elif ts.peek() in p.predict(16):
        ts.match('maiorIgual')
    elif ts.peek() in p.predict(17):
        ts.match('menor')
    elif ts.peek() in p.predict(18):
        ts.match('menorIgual')
    elif ts.peek() in p.predict(19):
        ts.match('igual')
    elif ts.peek() in p.predict(20):
        ts.match('diferente')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Expr(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(21):
        Termo(ts,p)
        Expr1(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Expr1(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(22):
        ts.match('adicao')
        Termo(ts,p)
        Expr1(ts,p)
    elif ts.peek() in p.predict(23):
        ts.match('subtracao'    )
        Termo(ts,p)
        Expr1(ts,p)
    elif ts.peek() in p.predict(24):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Termo(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(25):
        Fator(ts,p)
        Termo1(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Termo1(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(26):
        ts.match('multiplicacao')
        Fator(ts,p)
        Termo1(ts,p)
    elif ts.peek() in p.predict(27):
        ts.match('divisao')
        Fator(ts,p)
        Termo1(ts,p)
    elif ts.peek() in p.predict(28):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Fator(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(29):
        ts.match('id')
    elif ts.peek() in p.predict(30):
        ts.match('inum')
    elif ts.peek() in p.predict(31):
        ts.match('fnum')
    elif ts.peek() in p.predict(32):
        ts.match('(')
        Expr(ts,p)
        ts.match(')')

if __name__ == '__main__':
    filepath = 'programa.br'
    #tokens = lexical_analyser(filepath)
    #ts = token_sequence(tokens)
    G = create_ac_grammar()
    p_alg = predict_algorithm(G)
    print(is_ll1(G,p_alg))
