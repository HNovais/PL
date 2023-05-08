import json
import ply.yacc as yacc
from lexer import tokens

is_nested_key = False

def p_start(p):
    '''start : pairs
             | table'''
    p[0] = p[1]

def p_table(p):
    '''table : L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE pairs
             | NEWLINE L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE pairs'''
    if len(p) == 6:
        p[0] = {p[2]: p[5]}
    else:
        p[0] = {p[3]: p[6]}

def p_pairs(p):
    ''' pairs : pair 
              | pairs pair '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_pair(p):
    '''pair : key EQUAL value 
            | key EQUAL value NEWLINE'''
    p[0] = {p[1]: p[3]}

def p_key(p):
    ''' key : bare_key
            | quoted_key
            | dotted_key'''
    p[0] = p[1]

def p_bare_key(p):
    ''' bare_key : TEXT
                 | INT'''
    p[0] = p[1]

def p_quoted_key(p):
    ''' quoted_key : QUOTED_STRING
                   | PLICA_STRING'''
    p[0] = p[1]

def p_dotted_key(p):
    'dotted_key : key DOT key'
    print(p[1], p[3])

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
    'array : L_SQUARE_BRACKET expression R_SQUARE_BRACKET'
    p[0] = p[2]

def p_expression(p):
    ''' expression : expression COMMA value
                   | value '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}: unexpected token {p.value}")
    else:
        print("Syntax error: unexpected end of input")
    return None

parser = yacc.yacc()

with open("file.toml", encoding="utf-8") as f:
    content = f.read()

result = parser.parse(content)

with open("output.json", "w") as f:
    f.write(json.dumps(result, indent=2)) 