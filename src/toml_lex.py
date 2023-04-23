import ply.lex as lex

tokens = (
    'TITLE',
    'TITLE_VALUE',
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
t_BOOLEAN = r'true|false'

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
    return t

def t_ODT(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}(?::\d{2})?)'
    return t

def t_LDT(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?'
    return t

def t_LOCAL_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    return t

def t_LOCAL_TIME(t):
    r'\d{2}:\d{2}:\d{2}(\.\d+)?'
    return t

def t_MLLITERAL_STRING(t):
    r'\'\'\'(\n|.)*?\'\'\''
    t.value = t.value[3:-3].replace('\n', ' ') # ESPAÇOS EXTRA NÃO ESTÃO A SER IGNORADOS
    return t

def t_LITERAL_STRING(t):
    r'\'(.*)\''
    t.value = t.value[1:-1]
    return t

def t_MLBASIC_STRING(t):
    r'"""(\n|.)*?"""'
    t.value = t.value[3:-3].replace("\\", "").replace("\n", " ") # ESPAÇOS EXTRA NÃO ESTÃO A SER IGNORADOS e VER PROBLEMA COM AS BARRAS
    return t

def t_BASIC_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_HEX(t):
    r'0[xX][\da-fA-F]+'
    t.value = int(t.value, 16)
    return t

def t_OCT(t):
    r'0[oO][0-7]+'
    t.value = int(t.value, 8)
    return t

def t_BIN(t):
    r'0[bB][01]+'
    t.value = int(t.value, 2)
    return t

def t_FLOAT(t):
    r'[+-]?\d+\.\d*([eE][+-]?\d+)?|[+-]?\d+[eE][+-]?\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[+-]*\d+(?:_\d+)*'
    t.value = t.value.replace('_', '')  
    return t

def t_BARE_KEY(t):
    r'[A-Za-z0-9_-]+\s*='
    t.value = t.value.strip('=').strip()
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
    return t


t_ignore = ' \t\n'

def t_error(t):
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