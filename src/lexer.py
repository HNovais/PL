import ply.lex as lex
import re


tokens = (
    'TEXT',
    'QUOTED_STRING',
    'HEXADECIMAL',
    'OCTAL',
    'BINARY',
    'PLICA_STRING',
    'ML_QUOTED_STRING',
    'ML_PLICA_STRING',
    'INT',
    'FLOAT',
    'BOOLEAN',
    'O_DATE_TIME',
    'L_DATE_TIME',
    'LOCAL_DATE',
    'LOCAL_TIME',
    'COMMENT',
    'EQUAL',
    'COMMA',
    'DOT',
    'L_SQUARE_BRACKET',
    'R_SQUARE_BRACKET',
    'L_CURVE_BRACKET',
    'R_CURVE_BRACKET',
    'NEWLINE',
    'O_FLOAT'
)

t_O_FLOAT = r'[+-]?(?:inf|nan)'
t_TEXT = r'[a-zA-Z0-9_\-]+'
t_NEWLINE = r'\n+'
t_L_SQUARE_BRACKET = r'\['
t_R_SQUARE_BRACKET = r'\]'
t_L_CURVE_BRACKET = r'\{'
t_R_CURVE_BRACKET = r'\}'
t_EQUAL = '='
t_COMMA = r','
t_DOT = r'\.'

def t_BOOLEAN(t):
    r'true|false'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_HEXADECIMAL(t):
    r'0x([a-zA-Z0-9\_]+)'
    return t

def t_OCTAL(t):
    r'0o[0-7]+'
    return t

def t_BINARY(t):
    r'0b[0-1]+'
    return t

def t_O_DATE_TIME(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}(?::\d{2})?)'
    return t

def t_L_DATE_TIME(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?'
    return t

def t_LOCAL_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    return t

def t_LOCAL_TIME(t):
    r'\d{2}:\d{2}:\d{2}(\.\d+)?'
    return t

def t_FLOAT(t):
    r'[+-]?\d+\.\d*([eE][+-]?\d+)?|[+-]?\d+[eE][+-]?\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[+-]*\d+(?:_\d+)*'
    t.value = t.value.replace('_', '') 
    t.value = int(t.value)
    return t  

def t_ML_QUOTED_STRING(t):
    r'"""(?:[^\"]|\\.)*?"""'
    t.value = t.value[3:-3]
    t.value = re.sub(r'\\(\s)*', '', t.value)
    return t

def t_QUOTED_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t


def t_ML_PLICA_STRING(t):
    r'\'{3}(\n|.)*?\'{3}'
    t.value = t.value[3:-3]
    return t


def t_PLICA_STRING(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1) # Aqui talvez podéssemos dar skip à linha toda, uma vez que quando surge um carater invalido a linha toda fica invalida (ACHO EU!!)

lexer = lex.lex()

with open('file.toml', 'r', encoding="utf-8") as file:
    data = file.read()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)