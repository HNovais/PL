import json
import ply.yacc as yacc
from lexer import tokens

tables = {}

def p_start(p):
    '''start : tables
             | singles start
             | tables start
             | singles'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].update(p[2])
        p[0] = p[1]

def p_singles(p):
    '''singles : pairs
               | NEWLINE pairs'''
    if len(p) == 2:
        pairs = p[1]
    else:
        pairs = p[2]

    loadPairs(pairs, None)

    p[0] = tables

def p_tables(p):
    ''' tables : table
               | table tables 
               | arrayTable
               | arrayTable tables '''

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
    loadPairs(pairs, pairsDict)

    if is_dotted_key(key):
        keyInitial = split_dot(key)[0]
        if keyInitial in tables and isinstance(tables[keyInitial], list): # Para o caso das subtables de array tables
            nestedDicts(removeFirst(key), tables[keyInitial][-1], pairsDict, 0)
        else:   
            nestedDicts(key, tables, pairsDict, 0)
        keyFinal = split_dot(key)[0]
        p[0] = {keyFinal: tables[keyFinal]}

    else:
        tables[key] = pairsDict
        p[0] = {key: tables[key]}

def p_arrayTable(p):
    '''arrayTable : L_SQUARE_BRACKET L_SQUARE_BRACKET key R_SQUARE_BRACKET R_SQUARE_BRACKET NEWLINE pairs
                  | NEWLINE L_SQUARE_BRACKET L_SQUARE_BRACKET key R_SQUARE_BRACKET R_SQUARE_BRACKET NEWLINE pairs
                  | L_SQUARE_BRACKET L_SQUARE_BRACKET key R_SQUARE_BRACKET R_SQUARE_BRACKET NEWLINE'''
                
    if len(p) == 7:
        key = p[3]
        pairs = {} 
    elif len(p) == 8:
        key = p[3]
        pairs = p[7]
    else:
        key = p[4]
        pairs = p[8]

    pairsDict = {}
    loadPairs(pairs, pairsDict)

    if is_dotted_key(key):
        keyInitial = split_dot(key)[0]
        if keyInitial not in tables:
            print(keyInitial + " must be defined before this nested array table!")
        else:
            newKey = removeFirst(key)
            nestedDicts(newKey, tables[keyInitial][-1], pairsDict, 1)
        p[0] = {keyInitial: tables[keyInitial]}

    elif key in tables:
        if isinstance(tables[key], list): 
            tables[key].append(pairsDict)
            p[0] = {key: tables[key]}
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

def p_pair(p):
    '''pair : key EQUAL value
            | key EQUAL value NEWLINE
            | key EQUAL value COMMA
            | key EQUAL L_CURVE_BRACKET pairs R_CURVE_BRACKET
            | key EQUAL L_CURVE_BRACKET pairs R_CURVE_BRACKET COMMA
            | key EQUAL L_CURVE_BRACKET pairs R_CURVE_BRACKET NEWLINE
            | keyInvalid'''

    if len(p) >= 6:
        p[0] = (p[1],p[4]) 
    elif len(p) == 2:
        print("Key doesn't have a value!!!")
        p[0] = p[1]  
    else:
        p[0] = (p[1], p[3])

def p_keyInvalid(p):
    '''keyInvalid : key EQUAL NEWLINE'''

    p[0] = ("KeyInvalid",-1) 

def p_key(p):
    ''' key : bare_key
            | quoted_key
            | key DOT key'''
    if len(p) == 4:
        p[0] = p[1] + '.' + p[3]
    elif is_float(p[1]):
        int,dec = split_float(p[1])
        p[0] = int + "." + dec
    else:
        p[0] = p[1]

def p_bare_key(p):
    ''' bare_key : TEXT
                 | INT
                 | FLOAT'''
    p[0] = p[1]

def p_quoted_key(p):
    ''' quoted_key : QUOTED_STRING
                   | ML_QUOTED_STRING
                   | PLICA_STRING'''
    p[0] = p[1]
    
def p_value(p):
    ''' value : QUOTED_STRING
              | PLICA_STRING
              | ML_QUOTED_STRING
              | ML_PLICA_STRING
              | INT
              | FLOAT
              | O_FLOAT
              | BOOLEAN
              | O_DATE_TIME
              | L_DATE_TIME
              | LOCAL_DATE
              | LOCAL_TIME
              | octal
              | binary
              | hexadecimal
              | array'''
    p[0] = p[1]

def p_array(p):
    '''array : L_SQUARE_BRACKET expression R_SQUARE_BRACKET
             | L_SQUARE_BRACKET R_SQUARE_BRACKET'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1] + p[2]

def p_hexadecimal(p):
    ''' hexadecimal : HEXADECIMAL'''
    p[0] = int(p[1],16)

def p_octal(p):
    ''' octal : OCTAL'''
    p[0] = int(p[1],8)

def p_binary(p):
    ''' binary : BINARY'''
    p[0] = int(p[1],2)

def p_expression(p):
    ''' expression : expression COMMA value
                   | expression COMMA newvalue
                   | value 
                   | value NEWLINE
                   | newvalue'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_newvalue(p):
    '''newvalue : NEWLINE value
                | NEWLINE value NEWLINE'''
    p[0] = p[2]
    
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}: unexpected token {p.value}")
    else:
        print("Syntax error: unexpected end of input")
    return None

def loadPairs(pairs, dic):
    if dic == None:
        for pair in pairs:
            if pair[0] != "KeyInvalid": # Caso em que a key não tem valor
                if pair[0] in tables.keys():
                    print(pair[0] + " already defined in current dictionary")
                    pass
                else:
                    if is_dotted_key(pair[0]):
                        nestedDicts(pair[0], tables, pair[1], 0)
                    elif isinline(pair[1]):
                        pairsin = {}
                        inlineAux(pair[1], pairsin)
                        tables[pair[0]] = pairsin
                    else:
                        tables[pair[0]] = pair[1]
    else:
        for pair in pairs:
            if pair[0] != "KeyInvalid": 
                if pair[0] in dic.keys():
                    print(pair[0] + " already defined in current dictionary")
                    pass
                else:
                    if is_dotted_key(pair[0]):
                        nestedDicts(pair[0], dic, pair[1], 0)
                    elif isinline(pair[1]):
                        pairsin = {}
                        inlineAux(pair[1], pairsin)
                        dic[pair[0]] = pairsin
                    else:
                        dic[pair[0]] = pair[1]

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

def inlineAux(pair, pairsin):
    for pars in pair:
        if pars[0] in pairsin.keys():
            print(f"Key '{pars[0]}' already defined in table")
        else:
            if is_dotted_key(pars[0]):
                nestedDicts(pars[0], pairsin, pars[1], 0)
            elif isinline(pars[1]):
                nested_table = {}
                pairsin[pars[0]] = inlineAux(pars[1], nested_table)
            else: 
                pairsin[pars[0]] = pars[1]

    return pairsin

def isinline(elemento):
    if isinstance(elemento, list):  # Verifica se é uma lista
        if all(isinstance(tupla, tuple) for tupla in elemento):  # Verifica se todos os elementos da lista são tuplas
            return True
    return False

def is_float(obj):
    return isinstance(obj, float)

def split_float(num):
    num_str = str(num)
    integer_part, decimal_part = num_str.split('.')
    return integer_part, decimal_part

def removeFirst(dottedKey):
    elements = dottedKey.split('.')
    if len(elements) >= 2:
        elements.pop(0)
    return '.'.join(elements)

def nestedDicts(dottedKey, Rdict, last, array):
    keys = split_dot(dottedKey)
    nested_dict = Rdict
    for nested_key in keys[:-1]:  
        if nested_key not in nested_dict:
            nested_dict[nested_key] = {}
        nested_dict = nested_dict[nested_key]

    if keys[-1] in nested_dict and not array:
        print(keys[-1] + " already defined in table!")
    elif keys[-1] in nested_dict and array: # Quando se trata de uma key que ja possui um array neste dicionário, apenas damos append
        if isinstance(nested_dict, list): # Caso em que surge uma tabela normal e de seguida um arrayTable com o mesmo nome
            nested_dict[keys[-1]].append(last)
        else:
            print(keys[-1] + " already defined as a table!")
    elif array:
        nested_dict[keys[-1]] = []
        nested_dict[keys[-1]].append(last)
    else:
        nested_dict[keys[-1]] = last

parser = yacc.yacc()


with open("file.toml", encoding="utf-8") as f:
    content = f.read()

try:
    result = parser.parse(content)
    print("Parsing successful")
except yacc.YaccError as e:
    print("Syntax error encountered")
    error_message = str(e)
    print("Error message:", error_message)

with open("output.json", "w") as f:
    f.write(json.dumps(result, indent=2)) 