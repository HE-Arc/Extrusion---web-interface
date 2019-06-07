import ply.lex as lex

reserved_words = (
    'for',
    'delay',
    'cube',
    'face',
    'square',
    'ledstrip',
    'led'
)

tokens = (
             'NUMBER',
             'EVAL_OP',
             'OPP',
             'VAR',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = ';(){}='
t_EVAL_OP = r'<|>|=='
t_OPP = r'\+|-|/|\*'


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_VAR(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex()

