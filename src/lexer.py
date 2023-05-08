import ply.lex as lex

tokens = (
    'TEXT',
    'QUOTED_STRING',
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
    'L_BRACKET',
    'R_BRACKET',
    'L_SQUARE_BRACKET',
    'R_SQUARE_BRACKET',
    'L_CURVE_BRACKET',
    'R_CURVE_BRACKET',
)


t_BOOLEAN = r'true|false'
t_TEXT = r'[a-zA-Z_\-]+'
#t_NEWLINE = r'\n+'
t_L_BRACKET = r'\('
t_R_BRACKET = r'\)'
t_L_SQUARE_BRACKET = r'\['
t_R_SQUARE_BRACKET = r'\]'
t_L_CURVE_BRACKET = r'\{'
t_R_CURVE_BRACKET = r'\}'
t_EQUAL = '='
t_COMMA = r','
t_DOT = r'.'

def t_COMMENT(t):
    r'\#.*'
    pass

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
    return t  

def t_QUOTED_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_PLICA_STRING(t):
    r'\'(.*)\''
    return t

def t_ML_QUOTED_STRING(t):
    r'"""(\n|.)*?"""'
    return t

def t_ML_PLICA_STRING(t): 
    r'\'{3}(\n|.)*?\'{3}'
    return t

t_ignore = ' \t\n'

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