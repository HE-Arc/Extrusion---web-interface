import ply.yacc as yacc

from . import AST
from .lex import tokens

PATH_TO_GRAPHVIZ = 'C:/Program Files (x86)/Graphviz2.38/bin/'


def p_programme_statement(p):
    """ program : statement """
    p[0] = AST.ProgramNode(p[1].children)


def p_programme_recursif(p):
    """ program : statement program """
    p[0] = AST.ProgramNode(p[1].children + p[2].children)


def p_statement(p):
    """ statement : for
        | expression ';'
        | function """
    p[0] = AST.StatementNode(p[1])


def p_function(p):
    """ function : FUNCTION VAR '(' param ')' '{' program '}' """
    p[0] = AST.FunctionDefinition(p[2], p[4], [p[7]])


def p_param(p):
    """ param : VAR
        | VAR ',' param
        | """
    if len(p) == 2:
        p[0] = AST.FunctionArgumentsNode(p[1])
    elif len(p) == 4:
        p[0] = AST.FunctionArgumentsNode(p[1], [p[3]])
    else:
        p[0] = AST.FunctionArgumentsNode()


def p_use_function(p):
    """ use_function : VAR '(' call_data ')' """
    p[0] = AST.FunctionCallNode(p[1], [p[3]])


def p_call_data(p):
    """ call_data : number
        | number ',' call_data
        | """
    if len(p) == 2:
        p[0] = AST.FunctionParamNode(p[1])
    elif len(p) == 4:
        p[0] = AST.FunctionParamNode(p[1], [p[3]])
    else:
        p[0] = AST.FunctionParamNode()


def p_assign(p):
    """ assign : VAR '=' number """
    p[0] = AST.AssignNode([AST.DataNode(p[1]), p[3]])


def p_for(p):
    """ for : FOR '(' assign ';' eval ';' assign ')' '{' program '}' """
    p[0] = AST.ForNode(p[3], p[5], p[7], p[10])


def p_expression(p):
    """ expression : section
        | pause
        | use_function
        | assign """
    p[0] = AST.CommandeNode(p[1])


def p_calc(p):
    """ calc : data OPP data """
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_eval(p):
    """ eval : data EVAL_OP data """
    p[0] = AST.EvalNode(p[1], p[2], p[3])


def p_number(p):
    """ number : data
        | calc  """
    p[0] = p[1]


def p_data(p):
    """ data : NUMBER
    | VAR """
    p[0] = AST.DataNode(p[1])


def p_section_cube(p):
    """ section : CUBE number """
    p[0] = AST.OrderNode(p[1], p[2])


def p_section_face(p):
    """ section : FACE number number"""
    p[0] = AST.OrderNode(p[1], [p[2], p[3]])


def p_section_square(p):
    """ section : SQUARE number number number """
    p[0] = AST.OrderNode(p[1], [p[2], p[3], p[4]])


def p_section_ledstrip(p):
    """ section : LEDSTRIP number number number number"""
    p[0] = AST.OrderNode(p[1], [p[2], p[3], p[4], p[5]])


def p_section_led(p):
    """ section : LED number number number number number"""
    p[0] = AST.OrderNode(p[1], [p[2], p[3], p[4], p[5], p[6]])


def p_pause(p):
    """ pause : DELAY number """
    p[0] = AST.OrderNode(p[1], p[2])


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.errok()


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')
