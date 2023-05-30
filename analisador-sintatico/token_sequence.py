class token_sequence:
    def __init__(self,ts:list) -> None:
        self.__ts = ts
        self.__idx = 0

    def peek(self)->str:
        return self.__ts[self.__idx]
    
    def advance(self)->None:
        self.__idx =  self.__idx + 1

    def match(self,token:str)->None:
        if self.peek() == token:
            self.advance()
        else:
            print('Expected ',token)
            exit(0)