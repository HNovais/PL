import ply.lex as lex
import sys

tokens = [
    'DOCTYPE',
    'HTML_START',
    'LANG_EQ',
    'TAG_VALUE',
    'HEAD',
    'TITLE',
    'EQUAL',
    'PAGE_TITLE',
    'TYPE_EQ',
    'JS_TYPE',
    'SCRIPT_CONTENT',
    'IF',
    'CONDITION',
    'ELSE',
    'BODY',
    'H1',
    'DIV',
    'DIV_ABR',
    'DIV_ID',
    'DIV_CLASS',
    'IF_STATEMENT',
    'ELSE_STATEMENT',
    'PARAGRAPH',
    'TEXT',
    'PERIOD',
    'L_BRACE',
    'R_BRACE',
    'H1_TEXT',
    'P_TEXT',
    'P_DOT_TEXT',
    'TITLE_TEXT',
    'UL',
    'LI_TEXT',
    'SCRIPT',
    'LONG_SCRIPT',
    'INDENT'
]

t_DOCTYPE = r'doctype\s[a-zA-Z]*'
t_HTML_START = r'html'
t_LANG_EQ = r'lang='
t_TAG_VALUE = r'[\'"]([\w/-]+)[\'"]'
t_HEAD = r'head'
t_TITLE = r'title'
t_EQUAL = r'='
t_SCRIPT = r'script'
t_TYPE_EQ = r'type='
t_JS_TYPE = r'text/javascript'
t_IF = r'if'
t_ELSE = r'else'
t_BODY = r'body'
t_H1 = r'h1'
t_DIV_ABR = r'\#'
t_DIV = r'div'
t_IF_STATEMENT = r'if .+'
t_ELSE_STATEMENT = r'else'
t_PARAGRAPH = r'p'
t_PERIOD = r'\.'
t_L_BRACE = r'\('
t_R_BRACE = r'\)'
t_UL = r'ul'
t_INDENT = r'\s{4}'     

def t_DIV_ID(t):
    r'\#[a-zA-Z][a-zA-Z0-9_-]*'
    t.value = t.value[1:]
    return t

def t_DIV_CLASS(t):
    r'\.[a-zA-Z][a-zA-Z0-9_-]*'
    t.value = t.value[1:]
    return t

def t_TITLE_TEXT(t):
    r'title\s+.*'
    words = t.value.split(' ')
    text = ' '.join(words[1:])
    t.value = text.strip()
    return t 

def t_H1_TEXT(t):
    r'h1\s+.*'
    words = t.value.split(' ')
    text = ' '.join(words[1:])
    t.value = text.strip()
    return t

def t_P_TEXT(t):
    r'p\s+.*'
    words = t.value.split(' ')
    text = ' '.join(words[1:])
    t.value = text.strip()
    return t

def t_LI_TEXT(t):
    r'li\s+.*'
    words = t.value.split(' ')
    text = ' '.join(words[1:])
    t.value = text.strip()
    return t

def t_LONG_SCRIPT(t):
    r'script\.[\n\s]+(.+\n)+'
    lines = t.value.split('\n')
    script_lines = []
    indent_level = None
    for line in lines:
        if indent_level is None:
            if len(line) - len(line.lstrip()) != 0:
                indent_level = len(line) - len(line.lstrip()) - 4
        elif len(line) - len(line.lstrip()) <= indent_level:
            break
        script_lines.append(line)
    t.value = ' '.join(script_lines)
    return t
   
def t_P_DOT_TEXT(t):
    r'p\.\n([\t ]+.+\n)+'
    lines = t.value.split('\n')[1:-1]
    text = ' '.join([line.strip() for line in lines])
    t.value = text
    return t

def t_PAGE_TITLE(t):
    r'title=.*'
    t.value = t.value.split('=')[1].strip()
    return t

def t_CONDITION(t):
    r'if .+'
    t.value = t.value.split('if ')[1].strip()
    return t

t_ignore = '\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

with open(sys.argv[1], 'r') as file:
    data = file.read()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
