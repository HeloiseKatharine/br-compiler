


class transpiler:
    def __init__(self, tokens):
        self.tokens = tokens
        self.freeMemory = 0
        self.storeCommands = []
        self.expressions = []

def getTokens(tokens):
    dict_tokens = {}
    freeMemory = 0
    i = 0
    while i < len(tokens):
      if tokens[i] == 'CrieUmInteiro':
          dict_tokens[tokens[i+1]] = [freeMemory, 0]
          freeMemory += 1
          i += 2
      if tokens[i] == 'CrieUmRacional':
            dict_tokens[tokens[i+1]] = [freeMemory, 0.0]
            freeMemory += 1
            i += 2
      if tokens[i] == 'AgoraEh':
            dict_tokens[tokens[i-1]][0] = [dict_tokens[tokens[i-1]][0], tokens[i+1]]
      
      i += 1

    