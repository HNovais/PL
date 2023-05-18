import json
import ply.yacc as yacc
from lexer import tokens


tables = {}
currentTable = None
tablesTitles = []

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
               | tables table
               | arrayTable
               | tables arrayTable'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {}
        p[0].update(p[1])
        p[0].update(p[2])
    


def p_table(p):
    '''table : L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE pairs
             | NEWLINE L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE pairs
             | L_SQUARE_BRACKET key R_SQUARE_BRACKET NEWLINE'''


    if len(p) == 5: # Para tabelas vazias!
        key = p[2]
        pairs = {} 
    elif len(p) == 6:
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
            if is_dotted_key(pair[0]):
                nestedDicts(pair[0], pairsDict, pair[1])
            elif isinline(pair[1]):
                pairsin = {}
                inlineAux(pair[1], pairsin)
                pairsDict[pair[0]] = pairsin
            else:
                pairsDict[pair[0]] = pair[1]


    if is_dotted_key(key):
        nestedDicts(key, tables, pairsDict)
    else:
        if is_dotted_key(key):
            lastKey = split_dot(key)[-1]
            tables[lastKey] = pairsDict
        else:
            tables[key] = pairsDict

    if is_dotted_key(key):
        keyFinal = split_dot(key)[0]
        p[0] = {keyFinal: tables[keyFinal]} # Não sei porquê que isto está a funcionar (Não deveria estar -> Já tenho a solução correta)
    else:
        p[0] = {key: tables[key]}

    


def inlineAux(pair, pairsin):
    for pars in pair:
        if pars[0] in pairsin.keys():
            print(" already defined in table " + pars[0])
        else:
            if is_dotted_key(pars[0]):
                nestedDicts(pars[0], pairsin, pars[1])
            # elif isinline(pars[1]):
            #     parsin2 = {}
            #     print("1111111111111111111111111111111111111111111")
            #     inlineAux(pars[1],pairsin2)
            #     pairsin[pars[0]] = pairsin2
            else: 
                pairsin[pars[0]] = pars[1]


def isinline(elemento):
    if isinstance(elemento, list):  # Verifica se é uma lista
        if all(isinstance(tupla, tuple) for tupla in elemento):  # Verifica se todos os elementos da lista são tuplas
            return True
    return False


def nestedDicts(dottedKey, Rdict, last):
    keys = split_dot(dottedKey) 
    nested_dict = Rdict 
    #print(dottedKey)
    for nested_key in keys[:-1]:  
        if nested_key not in nested_dict:
            nested_dict[nested_key] = {}
            print(nested_key)
        nested_dict = nested_dict[nested_key]

    if keys[-1] in nested_dict:
        print(keys[-1] + " already defined in table " + nested_key)
    else:
        nested_dict[keys[-1]] = last


def p_arrayTable(p):
    '''arrayTable : L_SQUARE_BRACKET L_SQUARE_BRACKET key R_SQUARE_BRACKET R_SQUARE_BRACKET NEWLINE pairs
                  | NEWLINE L_SQUARE_BRACKET L_SQUARE_BRACKET key R_SQUARE_BRACKET R_SQUARE_BRACKET NEWLINE pairs
                  | L_SQUARE_BRACKET L_SQUARE_BRACKET key R_SQUARE_BRACKET R_SQUARE_BRACKET NEWLINE'''
                
    if len(p) == 7: # Para tabelas vazias!
        key = p[3]
        pairs = {} 
    elif len(p) == 8:
        key = p[3]
        pairs = p[7]
    else:
        key = p[4]
        pairs = p[8]

    pairsDict = {}
    for pair in pairs:
        if pair[0] in pairsDict.keys():
            print(pair[0] + " already defined in table " + key)
            pass
        else:
            if is_dotted_key(pair[0]):
                nestedDicts(pair[0], pairsDict, pair[1])
            elif isinline(pair[1]):
                pairsin = {}
                inlineAux(pair[1], pairsin)
                pairsDict[pair[0]] = pairsin
            else:
                pairsDict[pair[0]] = pair[1]


    if key in tables:
        if isinstance(tables[key], list): # Verificamos se é uma lista porque pode ser uma tabela já existente
            tables[key].append(pairsDict)
        else:
            print(key + ": Already defined in table")            
    else:
        tables[key] = []
        tables[key].append(pairsDict)        
    

    p[0] = {key: tables[key]}



def p_pairs(p):
    ''' pairs : pair
              | pair pairs'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

# def p_pair(p):
#     '''pair : key EQUAL value 
#             | key EQUAL value NEWLINE
#             | key EQUAL '''
#     p[0] = (p[1], p[3])

def p_pair(p):
    '''pair : key EQUAL value
            | key EQUAL value NEWLINE
            | key EQUAL value COMMA
            | key EQUAL L_CURVE_BRACKET pairs R_CURVE_BRACKET
            | key EQUAL L_CURVE_BRACKET pairs R_CURVE_BRACKET NEWLINE'''
    if len(p) >= 6:
        p[0] = (p[1],p[4])
    else:
        p[0] = (p[1], p[3])

def p_key(p):
    ''' key : bare_key
            | quoted_key
            | key DOT key'''
    if len(p) == 4:
        p[0] = p[1] + '.' + p[3]
    else:
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

def is_dotted_key(key):
    quotes = False

    for char in key:
        if char == '"':
            quotes = not quotes
        elif char == "." and not quotes:
            return True
    return False

def split_dot(key):
    quotes = False
    value = ['']
    index = 0

    for char in key:
        if char == '"':
            quotes = not quotes
        elif char == '.' and not quotes:
            value.append('')
            index += 1
        else:
            value[index] += char

    return value


parser = yacc.yacc()

with open("file.toml", encoding="utf-8") as f:
    content = f.read()

result = parser.parse(content)

print(tables)

with open("output.json", "w") as f:
    f.write(json.dumps(result, indent=2)) 