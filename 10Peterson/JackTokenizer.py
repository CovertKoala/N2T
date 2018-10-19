#
# JackTokenizer.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# By Capt Teal "Koala" Peterson
#
# Fall 2017
# last updated 27 Nov 17
#


from JTConstants import *

   
############################################
# Class

class JackTokenizer(object):

############################################
# Constructor

    def __init__(self, filePath):
        loadedList = self.__loadFile__(str(filePath))
        
        self.toParse = self.__filterFile__(loadedList)


# ############################################
# instance methods

    def advance(self):
        '''Reads and returns the next token, returns None if there are no more tokens.'''

        #Final parsing of tokens occurs in advance().  Token 'string' is consumed as it is parsed.
        token = ""
        if self.toParse:
            self.toParse = self.toParse.lstrip()

            if self.toParse[0] in SYMBOLS:
                #Check to see if token belongs to SYMBOLS, then return that symbol
                token = self.toParse[0]
                #Strip token
                self.toParse = self.toParse[1:]
            else:
                #If token doesn't belong to SYMBOLS, return everything up to the next SYMBOL/DELIMITER
                if self.toParse[0] == '"':
                    #Use SYMBOLS as delimiter to allow ' ' internal to a string.
                    tokenEnding = SYMBOLS
                else:
                    tokenEnding = DELIMITERS

                #Find index of any tokenEnding, return up to that index
                i = 0
                while (self.toParse[i] not in tokenEnding):
                    nextChar = self.toParse[i]
                    token += nextChar
                    i += 1

                token = token.rstrip() #if a string, a space may have followed the last ' " '
                self.toParse = self.toParse[i:] #strip token

            return token            

        else:
            return None


    ############   file loading stuff below   ############   

    def __loadFile__(self, fileName):
        '''Loads the file into memory.
           -fileName is a String representation of a file name,
           returns contents as a simple List'''
        
        fileList = []
        file = open(fileName,"r")
        
        for line in file:
            fileList.append(line)
            
        file.close()
        
        return fileList


    def __filterFile__(self, fileList):
        '''Comments, blank lines and unnecessary leading/trailing whitespace are removed from the list.
           -fileList is a  representation of a file, one line per element returns the fully filtered file as a single character array (string)'''

        #This function 'flattens' the file into a single string.  I can parse out block comments with less code this way.
        #Final parsing happens in advance()
        filteredLine = ""
        for line in fileList:
            line = self.__filterOutEOLComments__(line)
            line = line.strip()
            if len( line ) > 0:
                filteredLine = filteredLine + line

        blockCommentStart = filteredLine.find("/*")
        while(blockCommentStart >= 0):
            blockCommentEnd = filteredLine.find("*/")
            filteredLine = filteredLine[0:blockCommentStart] + filteredLine[blockCommentEnd+2:]
            blockCommentStart = filteredLine.find("/*")
        filteredLine = filteredLine.replace('\t',' ') #Remove remaining tabs (since they aren't listed as a delimeter)

        return filteredLine


    def __filterOutEOLComments__(self, line):
        '''Removes end-of-line comments and and resulting whitespace.
           -line is a string representing single line, line endings already stripped
           returns the filtered line, which may be empty '''

        index = line.find('//')
        if index >= 0:
            line = line[0:index]

        return line    
