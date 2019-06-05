import ply.yacc as yacc
import AST
from lex import tokens

vars = {}


def p_programme_statement(p):
    ''' programme : statement ';'
        | statement '''
    p[0] = AST.ProgramNode(p[1])


def p_programme_recusif_1(p):
    '''  programme: statement ';' programme '''
    p[0] = AST.ProgramNode(p[1] + p[3].children)


def p_programme_recursif_2(p):
    ''' statement programme '''
    p[0] = AST.ProgramNode(p[1] + p[2].children)


def p_statement(p):
    ''' statement : for
        | expression '''
    p[0] = AST.StatementNode(p[1])


def p_var_assign(p):
    ''' assign : VAR '=' NUMBER '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), AST.TokenNode(p[3])])


def p_var_use(p):
    """ use_var : VAR """
    p[0] = AST.TokenNode(p[1])


def p_eval(p):
    """ eval : VAR EVAL_OP NUMBER"""
    p[0] = AST.EvalNode(AST.TokenNode(p[1]), p[2], p[3])


def p_for(p):
    ''' for : FOR '(' assign ';' eval ';' assign ')' '{' statement '}' '''
    p[0] = AST.ForNode(p[3], p[5], p[7], p[10].children)


def p_number(p):
    ''' number : NUMBER | use_var '''
    p[0] = AST.TokenNode(p[1])


def p_number_follow(p):
    ''' number : NUMBER number
        | use_var number'''
    p[0] = AST.TokenNode(p[1], p[2])


def p_expression(p):
    ''' expression : section
        | pause '''
    p[0] = AST.OrderNode(p[1], p[2])


def p_section(p):
    ''' section : CUBE number
        | SQUARE number
        | FACE number
        | SQUARE number
        | LEDSTRIP number
        | LED number '''
    p[0] = AST.OrderNode(p[1], p[2])


def p_pause(p):
    ''' pause : DELAY NUMBER '''


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.errok()


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    print(result)
