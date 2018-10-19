#
#simpleParseTest.py
#
#By Teal "Koala" Peterson
#
# CS2001   Project 6 Assembler
# 07 Sep 17
#

'''Program use: place this file into the same folder as your Parse.py file.
   Use whatever method you choose to run simpleParseTest.py.  If this is run
   from the command line, you may type "simpleParseTest.py folder/filename" to
   test your parser on a file you specify (C:\>simpleParseTest.py add/add.asm)
'''

from Parser import Parser

if __name__ == '__main__':
    import sys
    try:
        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            target = "add/add.asm"
        print("\nFile to prep for parse:",target,"\n")
        KoalaParse = Parser(target)
        print("\nFiltered commands:\n",KoalaParse.toParse,"\n")
        
        #Test Parse.Command
        symbol = ""
        destination = ""
        comparison = ""
        jumpcode = ""
        commandType = 0
        count = 0
        programLine = 0
        print("{:4} {:4} {:20} {:20} {:4} {:5} {:4}".format("Line", "Type","Command","Symbol","Dest", "Comp", "Jump"))
        for command in KoalaParse.toParse:
            commandType = KoalaParse.commandType(command)
            if commandType != 2:
                symbol = KoalaParse.symbol(command)
            else: 
                symbol = ""
                
            if commandType == 2:
                destination = KoalaParse.dest(command)
                comparison = KoalaParse.comp(command)
                jumpcode = KoalaParse.jump(command)
            else:
                destination = ""
                comparison = ""
                jumpcode = ""
                
            if commandType == 0:
                print("Not a command: *****",command,"*****")
                count += 1

            print("{:4} {:4} {:20} {:20} {:4} {:5} {:4}".format(programLine,commandType,command,symbol,destination,comparison,jumpcode))
            programLine += 1
        print("Unidentifiable commands:",count)
        
        print("\nRun Parser.processLabels().\n Labels dictionary:\n",KoalaParse.processLabels())
        
        print("\nFinal Command List:\n",KoalaParse.toParse)
        
        
    except Exception:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
    finally:
        print("\n Parse succussfull")
        exit()