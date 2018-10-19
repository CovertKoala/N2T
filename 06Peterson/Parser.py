#
#Parser.py
#
#By Teal "Koala" Peterson
#Based on code by Loren Peitso
#
# CS2001   Project 6 Assembler
# 31 July 2013
# last updated 26 Aug 2016
#


'''Manages the mechanical work of breaking the input into tokens, and later further breaking
   down presented tokens into component chunks.  The Parser does not know what the chunks mean
   or what to do with them, it just knows how to slice-and-dice. '''

class Parser(object):

    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3
    #These regular expression patterns identify various command types
    A_CMDptn =  r"^(@[a-zA-Z0-9_.$]+)$"
    C_CMDptn =  r"^([AMD]{1,3}=[AMD]?[+\-&|!]?[AMD01])|([AMD0]?;J[GTEQLNMP]{2})$"
    JMPptn =    r"^([AMD0]?;J[GTEQLNMP]{2})$"
    CntJMPptn = r"^([AMD]{1,3}=[AMD]?[+\-&|!]?[AMD01])$"
    L_CMDptn =  r"^(\([a-zA-Z0-9_.$]+\))$"

##########################################
#Constructor

    def __init__(self, fileName):
        import re
        self.re = re
        self.pointer = 0
        self.numOfCommands = 0
        
        #Load file, by line, into a list.
        loadedList = self.__loadFile__(fileName)
        
        #Cut extra characters, comments, etc out of each list element (code line)
        self.toParse = self.__filterFile__(loadedList)
        
        self.numOfCommands = len(self.toParse)
        
        #self.__toTestDotTxt__()


##########################################
#public Methods

    #The following three methods are for my use of the Parser later.
    def getCurrentCommandList(self):
        return self.toParse
        
    def resetPointer(self):
        '''Resets pointer location for the Advance() function to 0'''
        self.pointer = 0
        
    def getPointerLocation(self):
        '''Returns the line that the Advance() function will return'''
        return self.pointer

    def advance(self):
        '''Reads and returns the next command in the input,
           returns false if there are no more commands.  '''
        
        if self.pointer+1 > self.numOfCommands:
            result = False
        elif self.toParse == []:
            result = False
        else:
            result = self.toParse[self.pointer]
            self.pointer += 1
        
        return result


    def commandType(self, command):
        ''' Returns type of the command
            A_COMMAND = 1   @xxx
         or C_COMMAND = 2  c-commands
         or L_COMMAND = 3  a label e.g. (LABEL)
         determines command type by matching a regular expression 
         pattern to the input command.
        '''
        
        if self.re.match(self.A_CMDptn,command):
            result =  self.A_COMMAND
        elif self.re.match(self.C_CMDptn,command):
            result =  self.C_COMMAND
        elif self.re.match(self.L_CMDptn,command):
            result =  self.L_COMMAND
        else:
            result = 0
        
        return result



    def symbol(self, command):
        ''' returns
             symbol or decimal of an A-command
          or symbol of a label'''
        
        if self.re.match(self.A_CMDptn,command):
            #Returns everything after an @ symbol
            result = command[1:len(command)]
        elif self.re.match(self.L_CMDptn,command):
            result = command.strip('()')
            
        #These elif's return an error if an invalid command is passed.
        elif self.re.match(self.C_CMDptn,command):
            raise RuntimeError("Error!!! parse.symbol(): C-Command passed, requires an A- or L-Command")
            result = None
        else:
            raise RuntimeError("Error!!! parse.symbol(): Invalid command passed, requires an A-or L-Command")
            result = None
            
        return result


    def dest(self, command):
        ''' Returns the dest mnemonic portion of the command '''
        
        #Checks for 'dest=' pattern
        assignment = self.re.search(r'[AMD]=',command)
        
        if assignment:
            assignment = assignment.string.split('=')
            result = assignment[0]

        #Dest will always be 'null' if "dest=" is not present
        else:
            result = "null"
            
        return result

    
    def comp(self, command):
        ''' Returns the comp mnemonic portion of the command '''
        
        #Checks for both forms of a C-Command: comp;jump and dest=comp
        toDo = self.re.search(self.CntJMPptn,command)
        jump = self.re.match(self.JMPptn,command)
        
        if toDo:
            toDo = toDo.string.lstrip('AMD')
            result = toDo.lstrip('=')
        elif jump:
            result = jump.string[0]
        else:
            raise RuntimeError("Error!!! parse.symbol(): Invalid C-Command passed")
            result = None
            
        return result


    
    def jump(self, command):
        ''' Returns the jmp mnemonic portion of the command '''

        #Checks for both forms of a C-Command: comp;jump and dest=comp
        toDo = self.re.search(self.CntJMPptn,command)
        jump = self.re.match(self.JMPptn,command)
        
        if jump:
            jump = jump.string.split(';')
            result = jump[1]
        elif toDo:
            result = "null"
        else:
            raise RuntimeError("Error!!! parse.symbol(): Invalid C-Command passed")
            result = None
            
        return result



    def processLabels(self):
        ''' Passes over the list of commands and removes labels from the code being parsed.
            As labels are identified they are added to a dictionary of <label, romAddress>
            pairs.  After passing over the entire file the dictionary is returned. '''        
        labels = {}

        tempParse =[]
        toParsePosition = 0
        
        for command in self.toParse:
            if self.re.match(self.L_CMDptn,command):
                #If L-Command add the label symbol to label dict
                newSymbol = self.symbol(command)
                labels[newSymbol] = toParsePosition
            else:
                #If not an L-Command, add the command to tempParse[]
                tempParse.append(command)
                toParsePosition += 1
                
        self.toParse = tempParse
        
        #Update numOfCommands for Advance()
        self.numOfCommands = len(self.toParse)

        return labels



##########################################
#private/local Methods



    def __toTestDotTxt__(self):
        '''this is just for outputting our stripped file as a test
           this function will not be active in the final program'''

        file = open("test.txt","w")
        file.write("\n".join(self.toParse))
        file.close() 



    def __loadFile__(self, fileName):
        '''Loads the file into memory.

           -fileName is a String representation of a file name,
           returns contents as a simple List.'''
        
        file = open(fileName)
        fileList = file.readlines()
        file.close()
        
        return fileList



    def __filterFile__(self, fileList):
        '''Comments, blank lines and unnecessary leading/trailing whitespace are removed from the list.

           -fileList is a List representation of a file, one line per element
           returns the fully filtered List'''
        
        filteredList = []
        unwantedChar = (' ', '	', '\n')
        
        for line in fileList:
            #Remove characters in 'unwantedChar'
            for char in unwantedChar:
                line = line.replace(char,'')
                
            #Splits and discards everything right of '//' inclusive
            line = line.split("//")[0]
            
            if line != '': #'Save' if not empty
                filteredList.append(line)
        
        return filteredList

