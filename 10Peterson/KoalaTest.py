from JackTokenizer import *
from JackAnalyzer import *
from pathlib import *
#import pyexpat
import xml.parsers.expat as expat


def getTargets(targetPath):
    targetList = []
    if targetPath.is_dir():
        for eachFile in targetPath.iterdir():
            if eachFile.suffix == ".jack":
                targetList.append(eachFile)
    elif targetPath.suffix == ".jack":
        targetList.append(targetPath)
    else:
        raise RuntimeError("Error: " + targetPath.name + " is not valid")
        
    return targetList

if __name__ == "__main__":

    #project 10 tests
    target = 'ExpressionlessSquare'
    #target = 'ArrayTest'
    #target = 'Square'


    #project 11 tests
    ##target = 'Seven'
    ##target = 'ConvertToBin'
    ##target = 'square'
    ##target = 'Average'
    ##target = 'Pong'
    ##target = 'ComplexArrays'

    #xmlParser = expat.ParserCreate()

    targetPath = Path(target)
    targetList = getTargets(targetPath)
    #print(targetList)

    #Verify token parsing and tagging
    '''
    for file in targetList:
        print('\n'+str(file)+'\n')
        line = 2
        KoalaTokenizer = JackTokenizer(file)
        KoalaAnalyzer = JackAnalyzer(file)

        token = KoalaTokenizer.advance()
        taggedTokenList = []
        #taggedTokenString = ""
        while token:
            taggedToken = KoalaAnalyzer.__wrapTokenInXML__(token)
            taggedTokenList += [taggedToken]
            #taggedTokenString += taggedToken
            print("{:3} {:10} -> {:10}".format(line,token,str(taggedToken)))
            token = KoalaTokenizer.advance()
            line += 1

        break
    print(taggedTokenList)
    '''

    #Check CompilationEngine
    '''
    KoalaCompiler = CompilationEngine(taggedTokenList)
    taggedToken = KoalaCompiler.__getNextEntry__()
    while taggedToken:
        print("{:3} {}".format(len(KoalaCompiler.tokens),taggedToken))
        taggedToken = KoalaCompiler.__getNextEntry__()
    '''

    KoalaAnalyzer = JackAnalyzer(targetList[0])
    KoalaTokenizer = JackTokenizer(targetList[0])

    #KoalaTokenizer.toParse = "do game.dispose();"
    #KoalaTokenizer.toParse += "let game = SquareGame.new();"

    '''KoalaTokenizer.toParse = """
        function void main() {
            var SquareGame game;
            let game = game;
            do game.run();
            do game.dispose();
            return;}"""
    '''

    KoalaTokenizer.toParse = """
         constructor Square new(int Ax, int Ay, int Asize) {
            let x = Ax;
            let y = Ay;
            let size = Asize;
            do draw();
            return x; }"""

    #taggedTokenList = [(None,None,"<tokens>")]
    taggedTokenList = []
    line = 1
    token = KoalaTokenizer.advance()
    while token:
        taggedToken = KoalaAnalyzer.__wrapTokenInXML__(token)
        taggedTokenList += [taggedToken]
        print("{:3} {:10} -> {:10}".format(line,token,str(taggedToken)))
        token = KoalaTokenizer.advance()
        line += 1
    #taggedTokenList += [ (None,None,"</tokens>") ]
    KoalaCompiler = CompilationEngine(taggedTokenList)
    #KoalaCompiler.__compileDo__()
    #KoalaCompiler.__compileStatements__()
    KoalaCompiler.__compileSubroutine__()



    #KoalaCompiler.compileTokens()







    ''' #Verify JackAnalyzer Output - compare files
    postTCheck = JackAnalyzer(target)
    postTCheck.process()
    '''



  
    






    '''
    def start_element(name, attrs):
        print('Start element:', name, attrs)
    def end_element(name):
        print('End element:', name)
    def char_data(data):
        print('Character data:', repr(data))

    xmlParser.StartElementHandler = start_element
    xmlParser.EndElementHandler = end_element
    xmlParser.CharacterDataHandler = char_data
    
    xmlParser.Parse("<keyword> class </keyword>")
    xmlParser.Parse("<keyword>")
    xmlParser.Parse("</keyword>")

    file = targetList[0].stem+"T.xml"
    print(file)
    openFile = open(file,'rb')
    xmlParser.ParseFile(openFile)
    '''
    
    