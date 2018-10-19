#
#SymbolTable.py
#
#Loren Peitso
#
# CS2001   Project 6 Assembler
# 31 July 2013
#
#complete
#


class SymbolTable(object):

    def __init__(self):

        self.table = {
            'SP': 0,
           'LCL': 1,
           'ARG': 2,
          'THIS': 3,
          'THAT': 4,
        'SCREEN': 16384,
           'KBD': 24576,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
           'R10': 10,
           'R11': 11,
           'R12': 12,
           'R13': 13,
           'R14': 14,
           'R15': 15   }

        self.varIndex = 16


    
    def addEntry(self, symbol, address):
        ''' adds a symbol:address pair to the table'''
        self.table[symbol] = address


    
    def contains(self, symbol):
        ''' is the requested symbol in the table? '''
        if (self.table.get(symbol) == None):
            return False
        else:
            return True

        
    
    def getAddress(self, symbol):
        ''' returns the address of the requested symbol'''
        return self.table[symbol]
        

    
    def getNextVariableAddress(self):
        ''' gets what memory index the next variable should be assigned'''
        result = self.varIndex
        self.varIndex += 1
        return result 


