#
#testAssembler.py
#Loren Peitso
# CS2000   Project 6 Assembler
# 01 Jul 14
# last updated 26 Aug 2016
#

import unittest
from Assembler import *



class unitTests(unittest.TestCase):
    ''' unit tests for class Assembler'''

    def test__init__(self):
        self.assertRaises(RuntimeError, Assembler, '.asm')

        fileName = 'add/Add.asm'
        assembler = Assembler(fileName)
        
        self.assertTrue( assembler.inputFileName == 'add/Add.asm')
        self.assertTrue( assembler.outputFileName == 'add/Add.hack')

        self.assertTrue( assembler.code)
        self.assertTrue( assembler.st)



    def test__assemble__(self):
        #this just calls the other functions, no real work of its own
        pass



    def test__firstPass__(self):
        #test that we can handle a simple file
        fileName = 'add/Add.asm'
        assembler = Assembler(fileName)
        addList = ['@2', 'D=A', '@3', 'D=D+A', '@0', 'M=D']
        assembler.__firstPass__()
        self.assertTrue( assembler.parser.toParse == addList)
    
        #test that we can handle a more complex file including deleting appropriate stuff
        fileName = 'rect/RectL.asm'
        assembler = Assembler(fileName)
        expected = ['@0', 'D=M', '@23', 'D;JLE', '@16', 'M=D', '@16384', 'D=A', '@17', 'M=D',
                    '@17', 'A=M', 'M=-1', '@17', 'D=M', '@32', 'D=D+A', '@17', 'M=D', '@16',
                    'MD=M-1', '@10', 'D;JGT', '@23', '0;JMP']
        assembler.__firstPass__()
        self.assertTrue( assembler.parser.toParse == expected)



    def test__output__(self):
        fileName = 'add/Add.asm'
        assembler = Assembler(fileName)
        outputName = assembler.assemble()
        self.assertTrue( outputName == 'add/Add.hack')

        insts = ['0000000000000010', '1110110000010000', '0000000000000011', '1110000010010000',
                 '0000000000000000', '1110001100001000']
        
        parsedList = []
        file = open('add/Add.hack',"r")
        
        for line in file:
            parsedList.append(line.strip())
            
        file.close()
        self.assertTrue( parsedList == insts)

        

    def test__secondPass__(self):
        #very complex operations and we have a much better test with
        #   the N2T Assembler.sh script
        pass



    def test__assembleC__(self):
        fileName = 'add/Add.asm'
        assembler = Assembler(fileName)
        
        command = 'D=D+A'
        expected = '1110000010010000'
        result = assembler.__assembleC__(command)
        self.assertTrue( result == expected)
        
        command = 'M=D'
        expected = '1110001100001000'
        result = assembler.__assembleC__(command)
        self.assertTrue( result == expected)


        command = '0;JMP'
        expected = '1110101010000111'
        result = assembler.__assembleC__(command)
        self.assertTrue( result == expected)

#
#************* automated tests run below
#
if __name__ == "__main__":
	unittest.main(exit=False)

        
