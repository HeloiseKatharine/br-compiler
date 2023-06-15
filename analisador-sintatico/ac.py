import re
from grammar import Grammar
from token_sequence import token_sequence
from predict import predict_algorithm

def create_ac_grammar()->Grammar:
    G = Grammar()
 
    G.add_production('Programa',['Dcls','Stmts','fim']) #1
    G.add_production('Dcls',['Dcl','Dcls']) #2
    G.add_production('Dcls',[]) #3
    G.add_production('Dcl',['floatdcl','id']) #4
    G.add_production('Dcl',['intdcl','id']) #5
    G.add_production('Stmts',['Stmt','Stmts']) #6
    G.add_production('Stmts',[]) #7
    G.add_production('Stmt',['id','assign','Val','Expr']) #8
    G.add_production('Stmt',['while','Expr','do','Stmt', 'endwhile']) #9
    G.add_production('Stmt',['if','Expr','then','Stmt', 'StmtIf']) #10
    G.add_production('Stmt',['print','Expr']) #11
    G.add_production('Stmt',[]) #12
    G.add_production('StmtIf',['endif']) #13
    G.add_production('StmtIf',['else','Stmt','endif']) #14
    G.add_production('Expr',['Termo','Expr1']) #15
    G.add_production('Expr1',['adicao','Termo','Expr1']) #16
    G.add_production('Expr1',['subtracao','Termo','Expr1']) #17
    G.add_production('Expr1',[]) #18
    G.add_production('Termo',['Fator','Termo1']) #19
    G.add_production('Termo1',['multiplicacao','Fator','Termo1']) #20
    G.add_production('Termo1',['divisao','Fator','Termo1']) #21
    G.add_production('Fator',['id']) #22
    G.add_production('Fator',['inum']) #23
    G.add_production('Fator',['fnum']) #24
    G.add_production('Fator',['num']) #25
    G.add_production('Fator',['(Expr)']) #26
    G.add_production('Fator',['string']) #27
    
    G.add_terminal('floatdcl')
    G.add_terminal('intdcl')
    G.add_terminal('print')
    G.add_terminal('id')
    G.add_terminal('assign')
    G.add_terminal('adicao')
    G.add_terminal('subtracao')
    G.add_terminal('multiplicacao')
    G.add_terminal('divisao')
    G.add_terminal('inum')
    G.add_terminal('fnum')
    G.add_terminal('fim')

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
        ts.match('print')
        Expr(ts,p)
    elif ts.peek() in p.predict(9):
        ts.match('id')
        ts.match('assign')
        Expr(ts,p)
    elif ts.peek() in p.predict(10):
        ts.match('if')
        Expr(ts,p)
        ts.match('then')
        Stmts(ts,p)
        StmtIf(ts,p)
    elif ts.peek() in p.predict(11):
        ts.match('while')
        Expr(ts,p)
        ts.match('do')
        Stmts(ts,p)
        ts.match('endwhile')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def StmtIf(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(12):
        ts.match('else')
        Stmts(ts,p)
    elif ts.peek() in p.predict(13):
        ts.match('endif')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Expr(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(14):
        Termo(ts,p)
        Expr1(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Expr1(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(15):
        ts.match('adicao')
        Termo(ts,p)
        Expr1(ts,p)
    elif ts.peek() in p.predict(16):
        ts.match('subtracao')
        Termo(ts,p)
        Expr1(ts,p)
    elif ts.peek() in p.predict(17):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Termo(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(18):
        Fator(ts,p)
        Termo1(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Termo1(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(19):
        ts.match('multiplicacao')
        Fator(ts,p)
        Termo1(ts,p)
    elif ts.peek() in p.predict(20):
        ts.match('divisao')
        Fator(ts,p)
        Termo1(ts,p)
    elif ts.peek() in p.predict(21):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Fator(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(22):
        ts.match('id')
    elif ts.peek() in p.predict(23):
        ts.match('num')
    elif ts.peek() in p.predict(24):
        ts.match('fnum')
    elif ts.peek() in p.predict(25):
        ts.match('abrepar')
        Expr(ts,p)
        ts.match('fechapar')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

if __name__ == '__main__':
    filepath = 'programa.br'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_ac_grammar()
    p_alg = predict_algorithm(G)
    Prog(ts,p_alg)  
