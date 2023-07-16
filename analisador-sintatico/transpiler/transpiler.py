class Transpiler:
    def __init__(self):
        self.__symbol_table = {}
        self.__code = ""
        self.__address = 0
    
    def insert_symbol_table(self, var_name, var_type, address):
        self.__symbol_table[var_name] = (var_type, address)
    
    def emit_code(self, code):
        self.__code += code + "\n"

    def print_code(self):
        print(self.__code)
    
    def free_address(self):
        self.__address += 1
        return self.__address - 1 
    def get_address(self, var_name):
        try:
            list = self.__symbol_table[var_name]
            return str(list[1])
        except KeyError:
            print("Variable '"+var_name+"' not declared")
            exit(0)




    