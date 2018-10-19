#
# JackAnalyzer.py
#
# CS2002   Project 10 & 11 Jack Compiler 
#
# Fall 2017
# last updated 23 Nov 17
#

import sys  #for grading server
from pathlib import *

from JackTokenizer import *
from CompilationEngine import *
from JTConstants import *



class JackAnalyzer(object):

##########################################
#Constructor

    def __init__(self, target):
        self.targetPath = Path(target)
        print(self.targetPath)



##########################################
#public methods
        
    def process(self):
        ''' iterates over a directory causing each .jack file to be processed.
            returns the pathname of the directory upon successful completion. '''
        
        if self.targetPath.is_dir():
            for eachFile in self.targetPath.iterdir():
                if eachFile.suffix == '.jack':
                    self.__processFile__(eachFile)  #file as a pathlib object    
        else:
            raise RuntimeError("Error, " + self.targetPath.name + " is not a directory ")
        
        return str(self.targetPath)


##########################################
#private methods
    
    def __processFile__(self, filePath):
        ''' processes a single file, first feeding the file to JackTokenizer to generate a list of tokens
            (output as T.xml files for debugging use) and that token list is fed through
            CompilationEngine to generate a final result list of XML tokens which is output into an .xml file. '''
        

        #Phase 1 Tokenize/Analyze
        tokenizer = JackTokenizer(filePath)
        print(filePath)

        xmlTokenList = ["<tokens>"]
        taggedTokenList = [ ("listStart","tokens",xmlTokenList[0]) ]

        token = tokenizer.advance()
        while token:
            taggedToken = self.__wrapTokenInXML__(token)
            taggedTokenList += [taggedToken]
            xmlTokenList += [taggedToken[TT_XML]]
            token = tokenizer.advance()

        xmlTokenList += ["</tokens>"]
        length = len(xmlTokenList)
        taggedTokenList += [ ("listEnd","tokens",xmlTokenList[length-1]) ]

        Tfilename = str(filePath.parent) + '/' + filePath.stem + "T.xml"
        self.__output__(Tfilename,xmlTokenList)

        #Phase 2 Compile/Translate
        compiler = CompilationEngine(taggedTokenList)
        compiledXMLList = compiler.compileTokens()

        Cfilename = str(filePath.parent) + '/' + filePath.stem + ".xml"
        self.__output__(Cfilename,compiledXMLList)


    def __output__(self, filePath, codeList):
        ''' outputs the VM code codeList into a file and returns the file path'''
            
        file = open(str(filePath), 'w')
        file.write("\n".join(codeList))
        file.close()



    def __wrapTokenInXML__(self, token):
        ''' returns an XML tag pair with the token properly sandwiched.
             conducts proper substitutions and quotation mark removals. '''
        
        flavor = TK_STRINGS[T_UNKNOWN]
        #Possible 'flavor' values: unknown, keyword, symbol, identifier,
        #                          integerConstant, stringConstant
        #From JTConstants TK_STRINGS tuple

        if token in KEYWORDS:
            flavor = TK_STRINGS[T_KEYWORD]
        elif token in SYMBOLS:
            flavor = TK_STRINGS[T_SYMBOL]
            if token in glyphSubstitutes:
                token = glyphSubstitutes[token]
        elif token[0] == '"':
            flavor = TK_STRINGS[T_STRING_CONST]
            token = token.strip('"')
        elif token.isdigit():
            flavor = TK_STRINGS[T_INT_CONST]
        elif token[0] in IDENTIFIER_START_CHARS:
            for c in token[1:]:
                if c not in IDENTIFIER_START_CHARS:
                    raise Exception("Invalid Identifier:", token)
            flavor = TK_STRINGS[T_IDENTIFIER]
        else:
            raise Exception("Unkown Token:", token)

        tokenXML = '<' + flavor + "> " + token + " </" + flavor + '>'

        ###### 'Big' change here is that I'm including 'flavor' in the Tuple #####
        # Doing this eliminated the need to 'unpack' the xml tags for compilation checks.
        # More memory? Perhaps, but few operations in the end.
        return flavor, token, tokenXML




#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

    if len(sys.argv) == 2 :
        target = sys.argv[1]     # use this one for final deliverable

    #project 10 tests
#    target = 'ExpressionlessSquare'
#    target = 'ArrayTest'
#    target = 'Square'


    #project 11 tests
##    target = 'Seven'
##    target = 'ConvertToBin'
##    target = 'square'
##    target = 'Average'
##    target = 'Pong'
##    target = 'ComplexArrays'
    
    analyzer = JackAnalyzer(target)
    print('\n' + analyzer.process() + ' has been translated.')







    
