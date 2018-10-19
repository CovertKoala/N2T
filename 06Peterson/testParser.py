#
#testParser.py
#
#Loren Peitso
#
# CS2001   Project 6 Assembler
# 01 Jul 14
# last updated 26 Aug 2016
#

import unittest
from Parser import *




class unitTests(unittest.TestCase):
    ''' unit tests for class Parser'''

    def test__init__(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)
        
        self.assertTrue(1 == Parser.A_COMMAND)
        self.assertTrue(2 == Parser.C_COMMAND)
        self.assertTrue(3 == Parser.L_COMMAND)

        self.assertTrue( parser.toParse )  #empty lists are false per PEP 8
        #we will check the delete comments part separately

        

    def test_advance(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)
        self.assertTrue( parser.advance() )   #check normal behavior

        parser.toParse = []
        self.assertFalse( parser.advance() )  #check list empty behavior



    def test_commandType(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)
        self.assertTrue( Parser.A_COMMAND == parser.commandType('@123') )
        self.assertTrue( Parser.C_COMMAND == parser.commandType('D=M') )
        self.assertTrue( Parser.L_COMMAND == parser.commandType('(loop)') )
        


    def test_symbol(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)
        
        command = '@123'
        self.assertTrue( '123' == parser.symbol(command) )

        command = '@INFINITE_LOOP'
        self.assertTrue( 'INFINITE_LOOP' == parser.symbol(command) )

        command = '(loop)'
        self.assertTrue( 'loop' == parser.symbol(command) )
        
    


    def test_dest(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)

        command = 'D=M'
        self.assertTrue( 'D' == parser.dest(command) )

        command = '(loop)'
        self.assertTrue( 'null' == parser.dest(command) )


        
    def test_comp(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)

        command = 'D;JGT'
        self.assertTrue( 'D' == parser.comp(command) )

        command = '0;JMP'
        self.assertTrue( '0' == parser.comp(command) )



    def test_jump(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)

        command = 'D=M'
        self.assertTrue( 'null' == parser.jump(command) )

        command = 'D;JGT'
        self.assertTrue( 'JGT' == parser.jump(command) )

        command = '0;JMP'
        self.assertTrue( 'JMP' == parser.jump(command) )



        
    def test_processLabels(self):
        fileName = 'add/Add.asm'
        parser = Parser(fileName)

        #test empty condition when there are no labels to be found
        labels = parser.processLabels()
        self.assertTrue( labels == {} )
        
        #test file where labels are found
        fileName = 'max/Max.asm' 
        parser = Parser(fileName)

        expected = { 'OUTPUT_FIRST':10, 'OUTPUT_D':12, 'INFINITE_LOOP':14  }
        labels = parser.processLabels()
        self.assertTrue( labels == expected )
        


    def test__toTestDotTxt__(self):
        #this is actually the functional test for the private functions
        pass

    
    def __loadFile__(self, fileName):
        #functional tested via __toTestDotTxt__()
        pass
        
    def __filterFile__(self, fileList):
        #functional tested via __toTestDotTxt__()
        pass

    def __filterOutEOLComments__(self, line):
        #functional tested via __toTestDotTxt__()
        pass




#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)

        
