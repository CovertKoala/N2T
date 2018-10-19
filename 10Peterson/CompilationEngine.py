#
# CompilationEngine.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# By Capt Teal "Koala" Peterson
#
# Fall 2017
# last updated 27 Nov 17
#

from JTConstants import *

TT_TYPE = 0
TT_TOKEN = 1
TT_XML = 2

class CompilationEngine(object):

############################################
# Constructor
    def __init__(self, taggedTokenList):
        self.tokens = taggedTokenList   #the list of tagged tokens to process (a copy was previously output as ____T.xml )

        #add and delete from this to reach left padding for XML file readability
        self.indentation = 0
        

############################################
# instance methods

    def compileTokens(self):
        ''' primary call to do the final compilation.
            returns a list of properly identified structured XML with appropriate indentation.'''

        result = []

        tokenTuple = self.__getNextEntry__()        

        if tokenTuple[TT_XML] == '<tokens>':
            result.extend( self.__compileClass__() )

            tokenTuple = self.__getNextEntry__()
            if tokenTuple[TT_XML] != '</tokens>':
                raise RuntimeError('Error, this file was not properly tokenized, missing </tokens>')
                
        else:
            raise RuntimeError('Error, this file was not properly tokenized, missing <tokens>')

        return result
    

############################################
# private/utility methods


    def __getNextEntry__(self):
        ''' removes and returns the next token from the list of tokens as a tuple of the form
            (type, token, <tag> token </tag>).
            TT_TYPE, TT_TOKEN, and TT_XML should be used for accessing the tuple components '''
        
        if len(self.tokens)>0:
            taggedToken = self.tokens.pop(0)
            return taggedToken
        else:
            return None
 
 
    def __peekAtNextEntry__(self):
        ''' copies, but does not remove the next token from the list of tokens as a tuple of the form
            (type, token, <tag> token </tag>).
            TT_TYPE, TT_TOKEN, and TT_XML should be used for accessing the tuple components '''
        
        if len(self.tokens)>0:
            taggedToken = self.tokens[0]
            return taggedToken
        else:
            return None
 

    def __replaceEntry__(self, entry):
        ''' returns a token to the head of the list.
            entry must be in the form "(type, token, <tag> token </tag>)" '''
              
        self.tokens.insert(0,entry) 
 

    def __compileClass__(self):
        ''' Compiles a class declaration returning a list of VM commands. '''
        
        result = ['<class>'] #structure label for class
        self.indentation += 2      #indentation level adjustment.

        tokenTuple = self.__getNextEntry__()
        if tokenTuple[TT_TOKEN] == 'class':
            #Class Keyword
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            
            #ClassName Identifier
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            
            #'{' symbol
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            
            tokenTuple = self.__peekAtNextEntry__()
            while tokenTuple[TT_TOKEN] != '}':
                if tokenTuple[TT_TOKEN] in SUBROUTINES:
                    result.extend( self.__compileSubroutine__() )
                elif tokenTuple[TT_TOKEN] in {"static","field"}:
                    result.extend( self.__compileClassVarDec__() )
                tokenTuple = self.__peekAtNextEntry__()

            #'}' symbol
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        else:
            raise RuntimeError('Error, token provided is not class:', tokenTuple[TT_TOKEN])
        
        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( '</class>' ) #keyword class
            
        return result


    def __compileClassVarDec__(self):
        ''' compiles a class variable declaration statement returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<classVarDec>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        #keyword static|field
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
 
        #keyword type
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #identifier varName
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__getNextEntry__()
        while tokenTuple[TT_TOKEN] == ',':
            #symbol ','
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #identifier varName
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            tokenTuple = self.__getNextEntry__()

        #symbol ';'
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</classVarDec>' )

        return result


    def __compileSubroutine__(self):
        ''' Compiles a function/method returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<subroutineDec>' ) #structure label
        self.indentation += 2      #indentation level adjustment.
        
        #keyword constructor|method|function
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
        
        #Keyword type | Identifier type
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #identifier subroutineName
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Symbol '('
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #<parameterList>
        result.extend( self.__compileParameterList__() )

        #Symbol ')'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        result.append( (self.indentation * ' ') +  '<subroutineBody>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        #Symbol '{'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Variable Declarations
        tokenTuple = self.__peekAtNextEntry__()
        while tokenTuple[TT_TOKEN] == "var":
            result.extend( self.__compileVarDec__() )
            tokenTuple = self.__peekAtNextEntry__()
        
        #Statements
        result.extend( self.__compileStatements__() )

        #Symbol '}'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</subroutineBody>' )

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</subroutineDec>' )

        return result


    def __compileParameterList__(self):
        ''' Compiles a parameter list from a function/method returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<parameterList>' ) #structure label
        self.indentation += 2      #indentation level adjustment. 

        tokenTuple = self.__peekAtNextEntry__()
        #Symbol ')' | Keyword type
        while tokenTuple[TT_TOKEN] != ')':
            #Keyword type
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Identifier varName
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            tokenTuple = self.__peekAtNextEntry__()
            if tokenTuple[TT_TOKEN] == ',':
                #Symbol ','
                tokenTuple = self.__getNextEntry__()
                result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</parameterList>' )

        return result


    def __compileVarDec__(self):
        ''' Compiles a single variable declaration line, returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<varDec>' ) #structure label
        self.indentation += 2      #indentation level adjustment.
        
        #Keyword Var
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Keyword type
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Identifier varName
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__getNextEntry__()
        while tokenTuple[TT_TOKEN] == ',':
            #Symbol ','
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Identifier varName
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            tokenTuple = self.__getNextEntry__()

        #Symbol ';'
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</varDec>' )

        return result


    def __compileStatements__(self):
        ''' Compiles statements returning a list of VM commands. 
            Assumes any leading and trailing braces are be consumed by the caller''' 

        result = []
        result.append( (self.indentation * ' ') + '<statements>' ) #structure label
        self.indentation += 2      #indentation level adjustment.
        
        tokenTuple = self.__peekAtNextEntry__()
        while tokenTuple:
            #Keyword let
            if tokenTuple[TT_TOKEN] == "let":
                result.extend( self.__compileLet__() )

            #Keyword if
            elif tokenTuple[TT_TOKEN] == "if":
                result.extend( self.__compileIf__() )

            #Keyword while
            elif tokenTuple[TT_TOKEN] == "while":
                result.extend( self.__compileWhile__() )

            #Keyword do
            elif tokenTuple[TT_TOKEN] == "do":
                result.extend( self.__compileDo__() )

            #Keyword return
            elif tokenTuple[TT_TOKEN] == "return":
                result.extend( self.__compileReturn__() )

            else:
                break

            tokenTuple = self.__peekAtNextEntry__()


        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</statements>' )

        return result


    def __compileDo__(self):
        ''' Compiles a function/method call returning a list of VM commands. '''

        result = []
        result.append( (self.indentation * ' ') + '<doStatement>' ) #structure label
        self.indentation += 2      #indentation level adjustment.
        
        #Keyword do
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Subroutine Call
        result.extend( self.__compileSubroutineCall__() )

        #Symbol ';'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</doStatement>' )

        return result


    def __compileLet__(self):
        ''' Compiles a variable assignment statement returning a list of VM commands. '''

        result = []
        result.append( (self.indentation * ' ') + '<letStatement>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        #Keyword let
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Identifier varName
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__getNextEntry__()
        if tokenTuple[TT_TOKEN] == '[':
            #Symbol '['
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Expression
            result.extend( self.__compileExpression__() )

            #Symbol ']'
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            tokenTuple = self.__getNextEntry__()

        #Symbol '='
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Expression
        result.extend( self.__compileExpression__() )

        #Symbol ';'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</letStatement>' )

        return result


    def __compileWhile__(self):
        ''' Compiles a while loop returning a list of VM commands. '''

        result = []
        result.append( (self.indentation * ' ') + '<whileStatement>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        #Keyword while
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Symbol '('
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #compileExpression
        result.extend( self.__compileExpression__() )

        #Symbol ')'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Symbol '{'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #compileStatements
        result.extend( self.__compileStatements__() )

        #Symbol '}'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</whileStatement>' )

        return result


    def __compileReturn__(self):
        ''' Compiles a function return statement returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<returnStatement>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        #get
        #'return' -> keyword
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Expression
        tokenTuple = self.__peekAtNextEntry__()
        if tokenTuple[TT_TOKEN] != ';':
            result.extend( self.__compileExpression__() )

        #Symbol ';'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</returnStatement>' )

        return result


    def __compileIf__(self):
        ''' Compiles an if(else)? statement block returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<ifStatement>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        #Keyword if
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Symbol '('
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Expression
        result.extend( self.__compileExpression__() )

        #Symbol ')'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Symbol '{'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #Statements
        result.extend( self.__compileStatements__() )

        #Symbol '}'
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__peekAtNextEntry__()
        if tokenTuple[TT_TOKEN] == "else":
            #Keyword else
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Symbol '{'
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Statements
            result.extend( self.__compileStatements__() )

            #Symbol '}'
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</ifStatement>' ) #keyword

        return result


    def __compileExpression__(self):
        ''' Compiles an expression returning a list of VM commands. '''

        result = []
        result.append( (self.indentation * ' ') + '<expression>' ) #structure label
        self.indentation += 2      #indentation level adjustment.  it will be paired at the bottom with a negative re-adjustment
 
        #Term
        result.extend( self.__compileTerm__() )

        tokenTuple = self.__peekAtNextEntry__()
        while tokenTuple[TT_TOKEN] in BINARY_OPERATORS:
            #Symbol operator
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Term
            result.extend( self.__compileTerm__() )
            
            tokenTuple = self.__peekAtNextEntry__()

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</expression>' )

        return result


    def __compileTerm__(self):
        ''' Compiles a term returning a list of VM commands. '''
        
        result = []
        result.append( (self.indentation * ' ') + '<term>' ) #structure label
        self.indentation += 2      #indentation level adjustment.

        tokenTuple = self.__getNextEntry__() 
        if tokenTuple[TT_TYPE] in TYPE_CONSTANT:
            #Integer/String Constants
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        elif tokenTuple[TT_TOKEN] in KEYWORD_CONSTANTS:
            #Keyword Constants
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        elif tokenTuple[TT_TOKEN]  == '(':
            #Symbol '('
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            
            #Expression
            result.extend( self.__compileExpression__() )

            #Symbol ')'
            tokenTuple = self.__getNextEntry__() 
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        elif tokenTuple[TT_TOKEN] in UNARY_OPERATORS:
            #Symbol unary operator
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            
            #Term
            result.extend( self.__compileTerm__() )

        elif tokenTuple[TT_TYPE] == "identifier":
            peek = self.__peekAtNextEntry__()
            if peek[TT_TOKEN] in {'(','.'}:
                #Subroutine Call
                self.__replaceEntry__(tokenTuple) #replace tokenTuple for Subroutine Call
                result.extend( self.__compileSubroutineCall__() )
            else:
                result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
                if peek[TT_TOKEN] == '[':
                    tokenTuple = self.__getNextEntry__()
                    #Symbol '['
                    result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
                
                    #Expression
                    result.extend( self.__compileExpression__() )
                
                    #Symbol ']'
                    tokenTuple = self.__getNextEntry__() 
                    result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</term>' )

        return result


    def __compileExpressionList__(self):
        ''' Compiles a list of expressions returning a list of VM commands. '''

        result = []
        result.append( (self.indentation * ' ') + '<expressionList>' ) #structure label
        self.indentation += 2      #indentation level adjustment.  it will be paired at the bottom with a negative re-adjustment

        tokenTuple = self.__peekAtNextEntry__()
        while tokenTuple[TT_TOKEN] != ')':
            #Expression
            result.extend( self.__compileExpression__() )

            tokenTuple = self.__peekAtNextEntry__()
            if tokenTuple[TT_TOKEN] == ',':
                tokenTuple = self.__getNextEntry__()
                #Symbol ','
                result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2     #indentation level re-adjustment. 
        result.append( (self.indentation * ' ') + '</expressionList>' ) #keyword

        return result


    def __compileSubroutineCall__(self):
        ''' Compiles a subroutine call returning a list of VM commands. '''
        
        result = []

        #Identifier subroutinename|classname|varName
        tokenTuple = self.__getNextEntry__()
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__getNextEntry__()
        if tokenTuple[TT_TOKEN] == '.':
            #Symbol '.'
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            #Identifier subroutineName
            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

            tokenTuple = self.__getNextEntry__() 

        #Symbol '('
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        #complieExpressionlist
        result.extend( self.__compileExpressionList__() )

        #Symbol ')'
        tokenTuple = self.__getNextEntry__() 
        result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        return result
