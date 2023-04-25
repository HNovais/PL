import ply.lex as lex

states = (
    ('value', 'exclusive'),
)

tokens = (
    'TITLE',
    'TITLE_VALUE',
    'TABLE',
    'COMMENT',
    'BASIC_STRING', # STRINGS
    'MLBASIC_STRING',
    'LITERAL_STRING',
    'MLLITERAL_STRING',
    'INT', # INTEGERS
    'HEX',
    'OCT',
    'BIN',
    'FLOAT', # FLOATS
    'ODT', # DATES
    'LDT', 
    'LOCAL_DATE',
    'LOCAL_TIME',
    'ARRAY_START', # ARRAYS
    'ARRAY_END',
    'COMMA',
    'BARE_KEY', # KEYS
    'QUOTED_KEY',
    'DOTTED_KEY',
    'TEXT',
    'EQUAL', # SYMBOLS
    'QUOTE',
    'CARDINAL',
    'BOOLEAN' # BOOLEANS
)

t_TITLE = r'title'
t_EQUAL = r'\='
t_QUOTE = r'\"'
t_CARDINAL = r'\#'
t_TEXT = r'[a-zA-Z]+'
t_ARRAY_END = r'\]'
    
t_TABLE = r'\[(.*)\]'

def t_COMMA(t):
    r','
    t.lexer.begin('value')
    return t

def t_value_BOOLEAN(t):
    r'true|false'
    t.lexer.begin('INITIAL')
    return t

def t_value_ARRAY_START(t):
    r'\['
    return t

def t_TITLE_VALUE(t):
    r'title\s\=\s\"[a-zA-Z\s]+\"'
    words = t.value.split(" ")
    text = ' '.join(words[2:])
    t.value = text.strip()
    return t

def t_COMMENT(t):
    r'\#.*'
    pass
    #text = t.value[1:].strip()  
    #t.value = text
    #return t

def t_QUOTED_KEY(t): # TA A APANHAR DEMASIADO first = "Tom" last = "Preston-Werner" # INVALID
    r'["\'].*?[\'"] *='
    if not t.value.strip(' "\'='): # QUANDO A KEY É NULA ISTO NÃO FUNCIONA
        t.value = ' '
    elif t.value[0] == '\'':
        t.value = t.value.strip(' \'=')
    else:
        t.value = t.value.strip(' "=')
    t.lexer.begin('value')
    return t

def t_value_ODT(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}(?::\d{2})?)'
    t.lexer.begin('INITIAL')
    return t

def t_value_LDT(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?'
    t.lexer.begin('INITIAL')
    return t

def t_value_LOCAL_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    t.lexer.begin('INITIAL')
    return t

def t_value_LOCAL_TIME(t):
    r'\d{2}:\d{2}:\d{2}(\.\d+)?'
    t.lexer.begin('INITIAL')
    return t

def t_value_MLLITERAL_STRING(t):
    r'\'\'\'(\n|.)*?\'\'\''
    t.value = t.value[3:-3].replace('\n', ' ') # ESPAÇOS EXTRA NÃO ESTÃO A SER IGNORADOS
    t.lexer.begin('INITIAL')
    return t

def t_value_LITERAL_STRING(t):
    r'\'(.*)\''
    t.value = t.value[1:-1]
    t.lexer.begin('INITIAL')
    return t

def t_value_MLBASIC_STRING(t):
    r'"""(\n|.)*?"""'
    t.value = t.value[3:-3].replace("\\", "").replace("\n", " ") # ESPAÇOS EXTRA NÃO ESTÃO A SER IGNORADOS e VER PROBLEMA COM AS BARRAS
    t.lexer.begin('INITIAL')
    return t

def t_value_BASIC_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    t.lexer.begin('INITIAL')
    return t

def t_value_HEX(t):
    r'0[xX][\da-fA-F]+'
    t.value = int(t.value, 16)
    t.lexer.begin('INITIAL')
    return t

def t_value_OCT(t):
    r'0[oO][0-7]+'
    t.value = int(t.value, 8)
    t.lexer.begin('INITIAL')
    return t

def t_value_BIN(t):
    r'0[bB][01]+'
    t.value = int(t.value, 2)
    t.lexer.begin('INITIAL')
    return t

def t_value_FLOAT(t):
    r'[+-]?\d+\.\d*([eE][+-]?\d+)?|[+-]?\d+[eE][+-]?\d+'
    t.value = float(t.value)
    t.lexer.begin('INITIAL')
    return t

def t_value_INT(t):
    r'[+-]*\d+(?:_\d+)*'
    t.value = t.value.replace('_', '')  
    t.lexer.begin('INITIAL')
    return t

def t_BARE_KEY(t):
    r'[A-Za-z0-9_-]+\s*='
    t.value = t.value.strip('=').strip()
    t.lexer.begin('value')
    return t

def t_DOTTED_KEY(t):
    r'((?:[A-Za-z0-9_-]+|[\'"][^"\n]*[\'"])\s*\.\s*)*(?:[A-Za-z0-9_-]+|[\'"][^"\n]*[\'"])\s*='
    t.value = t.value.strip('=')
    keys = []
    current_key = ''
    in_quotes = False
    for c in t.value:
        if c == '.' and not in_quotes:
            keys.append(current_key.strip(' \''))
            current_key = ''
        else:
            current_key += c
            if c == '"' or c == "'":
                in_quotes = not in_quotes
    keys.append(current_key.strip(' \''))
    t.value = keys
    t.lexer.begin('value')
    return t


t_ANY_ignore = ' \t\n'

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

with open('file.toml', 'r', encoding="utf-8") as file:
    data = file.read()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
