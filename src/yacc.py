import json
import ply.yacc as yacc
from lexer import tokens

def p_pairs(p):
    ''' pairs : pairs pair 
              | pair '''
    if len(p) == 2:
        p[0] = dict([p[1]])
    else:
        if len(p[2]) == 2:
            p[0] = dict([p[1], p[2]])
        else:
            print("Error: invalid pair")

def p_pair(p):
    'pair : key EQUAL value'
    p[0] = (p[1], p[3])
    print("Pair:", p[0])

def p_key(p):
    ''' key : TEXT
            | QUOTED_STRING '''
    p[0] = p[1]
    print("Key:", p[0])

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
              | LOCAL_TIME '''
    p[0] = p[1]
    print("Value:", p[0])

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}: unexpected token {p.value}")
    else:
        print("Syntax error: unexpected end of input")
    # Return None to indicate that parsing failed
    return None

parser = yacc.yacc()

with open("file.toml") as f:
    content = f.read()

result = {}
for pair in parser.parse(content):
    key, value = pair
    if isinstance(value, str):
        if value.startswith('"') or value.startswith("'"):
            # Handle quoted strings
            value = value[1:-1]
        elif value.lower() in ['true', 'false']:
            # Handle boolean values
            value = value.lower() == 'true'
        else:
            # Handle other strings (e.g., dates)
            value = str(value)
    result[key] = value

# Write the output file in JSON format
with open("output.json", "w") as f:
    f.write(json.dumps(result, indent=2))