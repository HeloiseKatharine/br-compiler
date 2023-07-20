import re
from grammar import Grammar
from token_sequence import token_sequence
from predict import predict_algorithm
from ll1_check import is_ll1
from  transpiler.transpiler import Transpiler

transpiler = Transpiler()

def create_ac_grammar()->Grammar:
    G = Grammar()
 
    G.add_production('Programa',['Dcls','Stmts','$']) #0
    G.add_production('Dcls',['Dcl','Dcls']) #1
    G.add_production('Dcls',[]) #2
    G.add_production('Dcl',['floatdcl','id']) #3
    G.add_production('Dcl',['intdcl','id']) #4
    G.add_production('Stmts',['Stmt','Stmts']) #5
    G.add_production('Stmts',[]) #6
    G.add_production('Stmt',['id','assign','Expr']) #7
    G.add_production('Stmt',['while','ExprLogica','do','Stmt','Stmts', 'endwhile']) #8
    G.add_production('Stmt',['if','ExprLogica','then','Stmt','Stmts', 'StmtIf']) #9
    G.add_production('Stmt',['print','Expr']) #10
    G.add_production('StmtIf',['endif']) #11
    G.add_production('StmtIf',['else','Stmt','Stmts','endif']) #12
    G.add_production('ExprLogica',['Expr','Comparador', 'Expr']) #13
    G.add_production('Comparador',['maior']) #14
    G.add_production('Comparador',['maiorIgual']) #15
    G.add_production('Comparador',['menor']) #16
    G.add_production('Comparador',['menorIgual']) #17
    G.add_production('Comparador',['igual']) #18
    G.add_production('Comparador',['diferente']) #19
    G.add_production('Expr',['Termo','Expr1']) #20
    G.add_production('Expr1',['adicao','Termo','Expr1']) #21
    G.add_production('Expr1',['subtracao','Termo','Expr1']) #22
    G.add_production('Expr1',[]) #23
    G.add_production('Termo',['Fator','Termo1']) #24
    G.add_production('Termo1',['multiplicacao','Fator','Termo1']) #25
    G.add_production('Termo1',['divisao','Fator','Termo1']) #26
    G.add_production('Termo1',[]) #27
    G.add_production('Fator',['id']) #28
    G.add_production('Fator',['inum']) #29
    G.add_production('Fator',['fnum']) #30
    G.add_production('Fator',['(','Expr',')']) #31
 
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
    G.add_terminal('(')
    G.add_terminal(')')
    G.add_terminal('maior')
    G.add_terminal('maiorIgual')
    G.add_terminal('menor')
    G.add_terminal('menorIgual')
    G.add_terminal('igual')
    G.add_terminal('diferente')
    G.add_terminal('$')

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
    # for p in G.productions():
    #     print(p,G.lhs(p),'->',G.rhs(p))
    return G 


regex_table = {
    r'^CrieUmInteiro$': 'intdcl',
    r'^CrieUmRacional$': 'floatdcl',
    r'^MostreNaTela$': 'print',
    r'^AgoraEh$':'assign',
    r'^Se$': 'if',
    r'^Entao$': 'then',
    r'^FimSe$': 'endif',
    r'^Senao$': 'else',
    r'^Enquanto$': 'while',
    r'^Faca$': 'do',
    r'^FimEnquanto$': 'endwhile',
    r'^EhMaior$': 'maior',
    r'^EhMaiorIgual$': 'maiorIgual',
    r'^EhMenor$': 'menor',
    r'^EhMenorIgual$': 'menorIgual',
    r'^EhIgual$': 'igual',
    r'^EhDiferente$': 'diferente',
    r'^\+$': 'adicao',
    r'^\-$': 'subtracao',
    r'^\*$': 'multiplicacao',
    r'^\/$': 'divisao',
    r'^[a-z]+$' : 'id',
    r'^[0-9]+$': 'inum',
    r'^[0-9]+\.[0-9]+$': 'fnum',
    r'^\($':'(',
    r'^\)$':')',
}

def lexical_analyser(filepath) -> str:
    with open(filepath,'r') as f:
        token_sequence = []
        tokens = []
        for line in f:
            line = line.strip()
            for t in line.split(' '):
                if t != '':
                    tokens.append(t)
                
        print(tokens)

        for t in tokens:
            found = False
            for regex,category in regex_table.items():
                if re.match(regex,t):
                    token_sequence.append((category,t))
                    found=True
            if not found:
                print('Lexical error: ',t)
                exit(0)
    token_sequence.append('$')
    print(token_sequence)
    return token_sequence


def Prog(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(0):
        Dcls(ts,p)
        Stmts(ts,p)
        ts.match('$')
        transpiler.print_code()
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Dcls(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(1):
        Dcl(ts,p)
        Dcls(ts,p)
    elif ts.peek() in p.predict(2):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

    
def Dcl(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(3):
        ts.match('floatdcl')
        var_name = ts.get_value()
        transpiler.insert_symbol_table(var_name,'float',transpiler.free_address())
        transpiler.emit_code('PUSHIMM 0.0')
        ts.match('id')
    elif ts.peek() in p.predict(4):
        ts.match('intdcl')
        var_name = ts.get_value()
        transpiler.insert_symbol_table(var_name,'int',transpiler.free_address())
        transpiler.emit_code('PUSHIMM 0')
        ts.match('id')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Stmts(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(5):
        Stmt(ts,p)
        Stmts(ts,p)
    elif ts.peek() in p.predict(6):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Stmt(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(7):
        var_name = ts.get_value()
        ts.match('id')
        ts.match('assign')
        Expr(ts,p)
        transpiler.emit_code('STOREOFF '+transpiler.get_address(var_name))
    elif ts.peek() in p.predict(8):
        ts.match('while')
        ExprLogica(ts,p)
        ts.match('do')
        Stmt(ts,p)
        Stmts(ts,p)
        ts.match('endwhile')
    elif ts.peek() in p.predict(9):
        ts.match('if')
        ExprLogica(ts,p)
        ts.match('then')
        Stmt(ts,p)
        Stmts(ts,p)
        StmtIf(ts,p)
    elif ts.peek() in p.predict(10):
        ts.match('print')
        Expr(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def StmtIf(ts:token_sequence, p:predict_algorithm)->None:
    expected = p.predict(11)
    expected.update(p.predict(12))
    if ts.peek() in p.predict(11):
        ts.match('endif')
    elif ts.peek() in p.predict(12):
        ts.match('else')
        Stmt(ts,p)
        Stmts(ts,p)
        ts.match('endif')
    else:
        print('Syntax error: found',ts.peek(), 'expected ',' or '.join(list(expected)))
        exit(0)

def ExprLogica(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(13):
        Expr(ts,p)
        Comparador(ts,p)
        Expr(ts,p)
    else:
        print('Syntax errorrr: ',ts.peek())
        exit(0)

def Comparador(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(14):
        ts.match('maior')
    elif ts.peek() in p.predict(15):
        ts.match('maiorIgual')
    elif ts.peek() in p.predict(16):
        ts.match('menor')
    elif ts.peek() in p.predict(17):
        ts.match('menorIgual')
    elif ts.peek() in p.predict(18):
        ts.match('igual')
    elif ts.peek() in p.predict(19):
        ts.match('diferente')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Expr(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(20):
        Termo(ts,p)
        Expr1(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Expr1(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(21):
        ts.match('adicao')
        Termo(ts,p)
        Expr1(ts,p)
    elif ts.peek() in p.predict(22):
        ts.match('subtracao'    )
        Termo(ts,p)
        Expr1(ts,p)
    elif ts.peek() in p.predict(23):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Termo(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(24):
        Fator(ts,p)
        Termo1(ts,p)
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Termo1(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(25):
        ts.match('multiplicacao')
        
        Fator(ts,p)
        Termo1(ts,p)
        transpiler.emit_code('TIMES')
    elif ts.peek() in p.predict(26):
        ts.match('divisao')
        Fator(ts,p)
        Termo1(ts,p)
    elif ts.peek() in p.predict(27):
        return
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

def Fator(ts:token_sequence, p:predict_algorithm)->None:
    if ts.peek() in p.predict(28):
        var_name = ts.get_value()
        transpiler.emit_code('PUSHOFF '+transpiler.get_address(var_name))
        ts.match('id')
    elif ts.peek() in p.predict(29):
        transpiler.emit_code('PUSHIMM '+ts.get_value())
        ts.match('inum')
    elif ts.peek() in p.predict(30):
        ts.match('fnum')
    elif ts.peek() in p.predict(31):
        ts.match('(')
        Expr(ts,p)
        ts.match(')')
    else:
        print('Syntax error: ',ts.peek())
        exit(0)

if __name__ == '__main__':
    # filepath = 'programa.br'
    filepath = './codigos/while.br'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_ac_grammar()
    p_alg = predict_algorithm(G)
    #print(is_ll1(G,p_alg))
    Prog(ts,p_alg)
