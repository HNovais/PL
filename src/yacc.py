import json
import ply.yacc as yacc
from lexer import tokens

tables = []
currentTable = None

def p_start(p):
    '''start : tables
             | TITLE NEWLINE tables'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        dict = {"title" : p[1]}
        dict.update(p[3])
        p[0] = dict

def p_tables(p):
    ''' tables : table
               | tables table'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {}
        p[0].update(p[1])
        p[0].update(p[2])

def p_table(p):
    '''table : L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE pairs
             | NEWLINE L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE pairs'''

    if len(p) == 6:
        key = p[2]
        pairs = p[5]
    else:
        key = p[3]
        pairs = p[6]

    pairsDict = {}
    for pair in pairs:
        if pair[0] in pairsDict.keys():
            print(pair[0] + " already defined in table " + key)
            pass
        else:
            pairsDict[pair[0]] = pair[1]

    table_dict = {key: pairsDict}
    tables.append(table_dict)
    p[0] = table_dict

    
def p_pairs(p):
    ''' pairs : pair
              | pair pairs'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_pair(p):
    '''pair : key EQUAL value 
            | key EQUAL value NEWLINE'''
    p[0] = (p[1], p[3])

def p_key(p):
    ''' key : bare_key
            | quoted_key'''
    p[0] = p[1]

def p_bare_key(p):
    ''' bare_key : TEXT
                 | INT '''
    p[0] = p[1]

def p_quoted_key(p):
    ''' quoted_key : QUOTED_STRING
                   | PLICA_STRING'''
    p[0] = p[1]
    
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

print(tables)

with open("output.json", "w") as f:
    f.write(json.dumps(result, indent=2)) 