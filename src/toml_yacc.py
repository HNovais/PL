import ply.yacc as yacc
from toml_lex import tokens


def p_tom(p):
    '''tom : keyvalue
            | tabela
            | title
            | comment'''
    p[0] = p[1]
    print(p[0])

def p_comment(p):
    '''comment : COMMENT'''
    p[0] = p[1]
def p_title(p):
    '''title : TITLE_VALUE'''
    p[0] = p[1]

def p_tabela(p):
    '''tabela : TABLE
                | tabela'''
    p[0] = p[1][1:-1]



def p_keyvalue(p):
    '''keyvalue : BARE_KEY value
                | DOTTED_KEY value
                | QUOTED_KEY value'''

    p[0] = (p[1], p[2])


# def p_barekey(p):
#   '''barekey : BARE_KEY value'''
#  p[0] = (p[1], p[2])
# print("bare"+ str(p[0]))


# def p_dottedkey(p):
#   '''dottedkey : ID DOT ID value'''
#  p[0] = (p[1], p[3], p[4])
# print("ola")
# print("dotted"+ str(p[0]))

def p_elementos(p):
    '''elementos : value
                | value COMMA elementos'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]

def p_array(p):
    '''array : ARRAY_START elementos ARRAY_END'''
    p[0] = p[2]

def p_value(p):
    '''value : string
            | BOOLEAN
            | array
            | number
            | data'''
    p[0] = p[1]

def p_data(p):
    '''data : ODT
            | LDT
            | LOCAL_DATE
            | LOCAL_TIME'''
    p[0] = p[1]

def p_number(p):
    '''number : INT
                | FLOAT
                | HEX
                | OCT
                | BIN'''
    p[0] = p[1]

def p_string(p):
    '''string : BASIC_STRING
                | MLBASIC_STRING
                | MLLITERAL_STRING
                | LITERAL_STRING'''
    p[0] = p[1]

def p_error(p):
    if p:
        print("Erro de sintaxe na linha %d, coluna %d: '%s'" % (p.lineno, p.lexpos, p.value))
    else:
        print("Erro de sintaxe: fim inesperado do arquivo")


parser = yacc.yacc()

with open('file.toml', 'r', encoding="utf-8") as file:
    data = file.read()

print(parser.parse(data))
