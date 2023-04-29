import ply.lex as lex

states = (
    ('value', 'exclusive'),   
    #('array', 'exclusive'),
    ('table', 'exclusive'),
    ('inline', 'exclusive'),
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
    #'EQUAL', # SYMBOLS
    'QUOTE',
    'CARDINAL',
    'BOOLEAN', # BOOLEANS
    'INLINE_OPEN',
    'INLINE_CLOSE',
    'NEWLINE'
)

    
def t_COMMA(t):
    r','
    t.lexer.push_state('value')
    return t

def t_inline_COMMA(t):
    r','
    return t

def t_table_COMMA(t):
    r','
    t.lexer.push_state('value')
    return t

def t_value_BOOLEAN(t):
    r'true|false'
    t.lexer.pop_state()
    return t


def t_value_ARRAY_START(t):
    r'\['
    return t

def t_ARRAY_END(t):
    r'\]'
    return t

def t_table_ARRAY_END(t):
    r'\]'
    return t


def t_TABLE(t): 
    r'\[(.*)\]'
    t.value = t.value.replace(" ", "") # Remove os espaços no meio da string q se encontra dentro de [ ]
    t.lexer.push_state('table')
    return t

def t_table_TABLE(t): 
    r'\[(.*)\]'
    t.value = t.value.replace(" ", "") # Remove os espaços no meio da string q se encontra dentro de [ ]
    #t.lexer.push_state('table')
    return t

def t_table_leave(t):
    r'\n\n'
    t.lexer.pop_state()
    print("leaving table")


def t_TITLE_VALUE(t):
    r'title\s\=\s\"[a-zA-Z\s]+\"'
    words = t.value.split(" ")
    text = ' '.join(words[2:])
    t.value = text.strip()
    return t



def t_COMMENT(t):
    r'\#.*'
    return t


def t_value_ODT(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}(?::\d{2})?)'
    t.lexer.pop_state()
    return t

def t_value_LDT(t):
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?'
    t.lexer.pop_state()
    return t


def t_value_LOCAL_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    t.lexer.pop_state()
    return t


def t_value_LOCAL_TIME(t):
    r'\d{2}:\d{2}:\d{2}(\.\d+)?'
    t.lexer.pop_state()
    return t


def t_value_MLLITERAL_STRING(t):
    r'\'\'\'(\n|.)*?\'\'\''
    t.value = t.value[3:-3].replace('\n', ' ') # ESPAÇOS EXTRA NÃO ESTÃO A SER IGNORADOS
    t.lexer.pop_state()
    return t

def t_value_LITERAL_STRING(t):
    r'\'(.*)\''
    t.value = t.value[1:-1]
    t.lexer.pop_state()
    return t

def t_value_MLBASIC_STRING(t):
    r'"""(\n|.)*?"""'
    t.value = t.value[3:-3].replace("\\", "").replace("\n", " ") # ESPAÇOS EXTRA NÃO ESTÃO A SER IGNORADOS e VER PROBLEMA COM AS BARRAS
    t.lexer.pop_state()
    return t

def t_value_BASIC_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    t.lexer.pop_state()
    return t

def t_value_HEX(t): 
    r'0[xX][\da-fA-F]+'
    t.value = int(t.value, 16)
    t.lexer.pop_state()
    return t

def t_value_OCT(t): 
    r'0[oO][0-7]+'
    t.value = int(t.value, 8)
    t.lexer.pop_state()
    return t

def t_value_BIN(t): 
    r'0[bB][01]+'
    t.value = int(t.value, 2)
    t.lexer.pop_state()
    return t

def t_value_FLOAT(t):
    r'[+-]?\d+\.\d*([eE][+-]?\d+)?|[+-]?\d+[eE][+-]?\d+'
    t.value = float(t.value)
    t.lexer.pop_state()
    return t


def t_value_INT(t):
    r'[+-]*\d+(?:_\d+)*'
    t.value = t.value.replace('_', '')  
    t.lexer.pop_state()
    return t    


def t_QUOTED_KEY(t): # TA A APANHAR DEMASIADO first = "Tom" last = "Preston-Werner" # INVALID
    r'["\'].*?[\'"] *='
    if not t.value.strip(' "\'='): # QUANDO A KEY É NULA ISTO NÃO FUNCIONA # se a key for nula isto devia ignorar a linha e assumir logo q é invalid, podemos fazer com estados, se o estado qnd chega ao igual n for oq queremos então damos invalid
        t.value = ' '
    elif t.value[0] == '\'':
        t.value = t.value.strip(' \'=')
    else:
        t.value = t.value.strip(' "=')
    t.lexer.push_state('value')
    return t

# TABLE_KEY
def t_table_QUOTED_KEY(t): # TA A APANHAR DEMASIADO first = "Tom" last = "Preston-Werner" # INVALID
    r'["\'].*?[\'"] *='
    if not t.value.strip(' "\'='): # QUANDO A KEY É NULA ISTO NÃO FUNCIONA # se a key for nula isto devia ignorar a linha e assumir logo q é invalid, podemos fazer com estados, se o estado qnd chega ao igual n for oq queremos então damos invalid
        t.value = ' '
    elif t.value[0] == '\'':
        t.value = t.value.strip(' \'=')
    else:
        t.value = t.value.strip(' "=')
    t.lexer.push_state('value')
    return t

# INLINE_KEY
def t_inline_QUOTED_KEY(t): # TA A APANHAR DEMASIADO first = "Tom" last = "Preston-Werner" # INVALID
    r'["\'].*?[\'"] *='
    if not t.value.strip(' "\'='): # QUANDO A KEY É NULA ISTO NÃO FUNCIONA # se a key for nula isto devia ignorar a linha e assumir logo q é invalid, podemos fazer com estados, se o estado qnd chega ao igual n for oq queremos então damos invalid
        t.value = ' '
    elif t.value[0] == '\'':
        t.value = t.value.strip(' \'=')
    else:
        t.value = t.value.strip(' "=')
    t.lexer.push_state('value')
    return t

def t_BARE_KEY(t):
    r'[A-Za-z0-9_-]+\s*='
    t.value = t.value.strip('=').strip()
    t.lexer.push_state('value')
    return t

# TABLE_KEY
def t_table_BARE_KEY(t):
    r'[A-Za-z0-9_-]+\s*='
    t.value = t.value.strip('=').strip()
    t.lexer.push_state('value')
    return t

# INLINE_KEY
def t_inline_BARE_KEY(t):
    r'[A-Za-z0-9_-]+\s*='
    t.value = t.value.strip('=').strip()
    t.lexer.push_state('value')
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
    t.lexer.push_state('value')
    return t

# TABLE_KEY
def t_table_DOTTED_KEY(t):
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
    t.lexer.push_state('value')
    return t

# INLINE_KEY
def t_inline_DOTTED_KEY(t):
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
    t.lexer.push_state('value')
    return t

def t_value_INLINE_OPEN(t):
    r'\{'
    t.lexer.pop_state()
    t.lexer.push_state('inline')
    return t

def t_inline_INLINE_CLOSE(t):
    r'\}'
    #if lexer.current_state() == 'inline':
    t.lexer.pop_state()
    return t

def t_table_NEWLINE(t):
    r'\n'
    pass


t_ignore = ' \t\n'
t_value_ignore = ' \t\n'
t_table_ignore = ' \t'
t_inline_ignore = ' \t\n'

def t_ANY_error(t):
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
