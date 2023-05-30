import re

MAX_DEPTH = 20

G = {
    'S' : [['E']],
    'E': [['P','(','E',')'],['v','T']],
    'P': [['f'],[]],
    'T': [['+','E'],[]]
}


def terminal(token):
    terminal_regex=r"[fv\+\(\)]"
    return re.match(terminal_regex,token)

def nonterminal(token):
    return not terminal(token)

def recurse(X,depth):
    print(X,'->',end='')
    if depth == MAX_DEPTH:
        return
    for l in G[X]:
        if(l==[]):
            print('vazio')
        print(''.join(l))
        for token in l:
            if nonterminal(token):
                recurse(token,depth+1)
if __name__ == '__main__':
    recurse('S',0)