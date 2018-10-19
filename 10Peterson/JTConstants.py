#
# JTConstants.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# Capt Teal "Koala" Peterson
# Fall 2017
# last updated 27 Nov 17
#

import string

##############################################################
#Chapter 10 stuff
#
KEYWORDS = frozenset({'boolean', 'char', 'class', 'constructor', 'do', 'else',
            'false', 'field', 'function', 'if', 'int', 'let', 'method',
            'null', 'return', 'static', 'this', 'true', 'var', 'void', 'while'})

SYMBOLS = '{}()[].,;+-*/&|<>=~'

DELIMITERS = ' ' + SYMBOLS 

IDENTIFIER_START_CHARS = string.ascii_letters + '_'
IDENTIFIER_CHARS = IDENTIFIER_START_CHARS + string.digits

glyphSubstitutes = {'<':'&lt;', '>':'&gt;' , '&':'&amp;'}


##############################################################
#Chapter 11 stuff
#


SUBROUTINES = frozenset({'constructor', 'method', 'function'})

STATEMENTS = frozenset({'let', 'if', 'while', 'do', 'return'})

KEYWORD_CONSTANTS = {'true':-1, 'false':0, 'null':0, 'this':999999999}

TYPE_CONSTANT = frozenset({'integerConstant', 'stringConstant',})

UNARY_OPERATORS = {'-':'neg', '~':'not'}

BINARY_OPERATORS = {    '+':'add',
                        '-':'sub',
                        '*':'Math.multiply',
                        '/':'Math.divide',
                    '&amp;':'and',
                        '|':'or',
                     '&lt;':'lt',
                     '&gt;':'gt',
                        '=':'eq'}


TK_STRINGS =  ('unknown', 'keyword', 'symbol', 'identifier',
                  'integerConstant', 'stringConstant',
                  'IDENTIFIER-Defined', 'SCOPE-Subroutine')

T_UNKNOWN = 0
T_KEYWORD = 1
T_SYMBOL = 2
T_IDENTIFIER = 3
T_INT_CONST = 4
T_STRING_CONST = 5
IDENTIFIER_DEFINED = 6
SCOPE_SUBROUTINE = 7
