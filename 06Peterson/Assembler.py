#
#Assembler.py
#
# CS2001   Project 6 Assembler
# 31 July 2013
# last updated 26 Aug 2016
#
# start code version
#


from Code import *
from SymbolTable import *
from Parser import *


'''Manages the assembly process, used the Parser to do the mechanical tokenizing and then
   determines the semantically correct thing to do with those tokens. Then uses the Parser
   to break tokens into appropriate components and requests the translations of those
   components from the Code module. Labels are passed to the SymbolTable to get mapped
   against addresses.'''

class Assembler(object):

##########################################
#Constructor

    def __init__(self, target):

        index = target.find('.asm')
        if ( index < 1):
            raise RuntimeError( "error, cannot use the filename: " + target )

        self.inputFileName = target
        self.outputFileName = self.inputFileName[:index] + '.hack'

        self.parser = Parser(self.inputFileName)

        self.code = Code()
        self.st = SymbolTable()




##########################################
#public methods

    def assemble(self):
        '''Does the assembly and creates the file of machine commands,
           returning the name of that file '''
        self.__firstPass__()
        return  self.__output__( self.__secondPass__() )




##########################################
#private/local methods
 
    def __output__(self, codeList):
        ''' Output the machine code codeList into a file and returns the filename'''

        file = open(self.outputFileName,"w")
        file.write("\n".join(codeList))
        file.close()
        return self.outputFileName


    def __firstPass__(self):
        ''' Passes over the file contents to populate the symbol table'''
        #MUST prevent the Assembler reaching into the parser
        #while also not requiring the parser to become semantically aware
        #so let parser do mechanical work
        #   and let Assembler do the semantic part on the returned results

        labels = self.parser.processLabels()
        for k,v in labels.items():
            self.st.addEntry(k,v)


    def __secondPass__(self):
        ''' Manage the translation to machine code, returning a list of machine instructions'''
        
        machineCode = []

        command = self.parser.advance()
        while( command ):

            type = self.parser.commandType(command)
            
            if type == self.parser.A_COMMAND:
                bitString = self.__assembleA__(command)
                
            elif type == self.parser.C_COMMAND:
                bitString = self.__assembleC__(command)
                
            else:
                symStr = self.parser.symbol(command)
                raise RuntimeError( 'There should be no labels on second pass, errant symbol is ' + symStr)

            machineCode.append(bitString)
            command = self.parser.advance()

        return machineCode



    def __assembleC__(self, command):
        ''' Do the mechanical work to translate a C_COMMAND, returns a string representation
            of a 16-bit binary word.'''
        
        commandType = self.parser.commandType(command)
        result = ""
        
        destString = self.parser.dest(command)
        compString = self.parser.comp(command)
        jmpString = self.parser.jump(command)
            
        #Verifies that we are not processing an invalid comp.
        if compString.find('A') > -1 and compString.find('M') > -1:
            raise RuntimeError("Error!!! Assembler: Invalid command, comparison may not contain both 'A' and 'M':",command)
            result = None

        result = "111" + self.code.comp(compString) + self.code.dest(destString) + self.code.jump(jmpString)
            
        return result

         
    def __assembleA__(self, command):
        ''' Do the mechanical work to translate an A_COMMAND, returns a string representation
            of a 16-bit binary word.'''

        commandType = self.parser.commandType(command)
        
        symbol = self.parser.symbol(command)
        
        if symbol.isdigit():
            symVal = int(symbol)
            
        elif self.st.contains(symbol):
            symVal = self.st.getAddress(symbol)
            
        else:
            newAddress = self.st.getNextVariableAddress()
            self.st.addEntry(symbol,newAddress)
            symVal = newAddress

        return '0' + "{0:015b}".format(symVal)




#################################
#################################
#################################
#This runs the program and assigns the first argument to 'target'
#
if __name__=="__main__":

    import sys
    try:
        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            target = 'add/Add.asm'       # for internal IDLE testing only
            ##target = 'max/MaxL.asm'      # for internal IDLE testing only
            ##target = 'max/Max.asm'       # for internal IDLE testing only
            ##target = 'rect/RectL.asm'    # for internal IDLE testing only
            ##target = 'rect/Rect.asm'     # for internal IDLE testing only
            ##target = 'pong/PongL.asm'    # for internal IDLE testing only
            ##target = 'pong/Pong.asm'     # for internal IDLE testing only
        print("\nFile to prep for assembly:",target,"\n")
        KoalaAssember = Assembler(target)
        outputFileName = KoalaAssember.assemble()
        print('Done parsing; the assembled file is:', outputFileName )
        
    except Exception:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
    finally:
        print("\nAssembly run complete")
        exit()

