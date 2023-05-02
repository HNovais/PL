import ply.yacc as yacc
from lexer import tokens

def p_file(p):
    '''file : toms'''
    p[0] = p[1]
    

def p_toms(p):
    '''toms : toms tom
            | tom'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_tom(p):
    '''tom : keyvalue
            | tabela
            | comment'''
            # | title'''
    p[0] = p[1]
    

def p_comment(p):
    '''comment : COMMENT'''
    p[0] = p[1]

def p_keyvalue(p):
    '''keyvalue : key EQUAL value'''
    p[0] = (p[1],p[3])


def p_key(p):
    '''key : quotedkey
            | dottedkey
            | barekey'''
            #| title'''

#def p_title(p):
 #   '''title : TITLE'''
  #  p[0] = p[1]

def p_barekey(p):
    '''barekey : TEXT'''
    p[0] = p[1]

def p_dottedkey(p):
    '''dottedkey : TEXT DOT TEXT'''
    p[0] = (p[1],p[3])

def p_quotedkey(p):
    '''quotedkey : QUOTED_STRING'''
    p[0] = p[1][1:-1]


def p_value(p):
    ''' value : QUOTED_STRING
              | PLICA_STRING
              | ML_QUOTED_STRING
              | ML_PLICA_STRING
              | INT
              | FLOAT
              | BOOLEAN
              | O_DATE_TIME
              | L_DATE_TIME
              | LOCAL_DATE
              | LOCAL_TIME
              | array'''
    p[0] = p[1]

def p_array(p):
    '''array : L_SQUARE_BRACKET elementos R_SQUARE_BRACKET'''
    p[0] = p[2]

def p_elementos(p):
    '''elementos : value
                | value COMMA elementos'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]

def p_tables(p):
    '''tables : tabela
                | inlinetabela'''
                #| arraytabela'''
    p[0] = p[1]


def p_inlinetabela(p):
    '''inlinetabela : L_BRACKET inlinecont R_BRACKET'''
    p[0] = p[1]

def p_inlinecont(p):
    '''inlinecont : keyvalue
                    | keyvalue COMMA inlinecont'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]


def p_tabela(p):
    '''tabela : L_SQUARE_BRACKET subtabela R_SQUARE_BRACKET'''
    p[0] = p[1]

def p_subtabela(p):
    '''subtabela : TEXT
                | TEXT DOT subtabela'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]



def p_error(p):
    if p:
        print("Erro de sintaxe na linha %d, coluna %d: '%s'" % (p.lineno, p.lexpos, p.value))
    else:
        print("Erro de sintaxe: fim inesperado do arquivo")


parser = yacc.yacc()

with open('file.toml', 'r', encoding="utf-8") as file:
    data = file.read()

print(parser.parse(data))
