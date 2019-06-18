from . import AST2
from threading import get_ident
from .AST2 import addToClass
from functools import reduce
from .parser_prog import parse
import time
from package.global_variable.variables import *

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

evaluate = {
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
}

function_def = {}
function_args = {}
scope = "main"
vars = {scope: {}}
orders = []


def delay(pause_time):
    time.sleep(pause_time)


def fun_cube(brightness):
    cube.show(brightness)


def face(idx_face, brightness):
    cube.faces[idx_face].show(brightness)


def square(idx_face, idx_square, brightness):
    cube.faces[idx_face].squares[idx_square].show(brightness)


def ledstrip(idx_face, idx_square, idx_ledstrip, brightness):
    cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].show(brightness)


def led(idx_face, idx_square, idx_ledstrip, idx_led, brightness):
    cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].show_led(idx_led, brightness)


dict_function = {'delay': delay, 'cube': fun_cube, 'face': face, 'square': square,
                 'ledstrip': ledstrip, 'led': led}


@addToClass(AST2.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST2.StatementNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST2.CommandeNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST2.CalcNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST2.DataNode)
def execute(self):
    if self.tok in vars[scope]:
        return vars[scope][self.tok]
    elif self.tok in vars["main"]:
        return vars["main"][self.tok]
    else:
        return float(self.tok)


@addToClass(AST2.OrderNode)
def execute(self):
    list_param = []
    for c in self.children:
        list_param.append(c.execute())
    if self.tok != "delay":
        list_param = [int(f) for f in list_param]

    if launcher_access[get_ident()]:
        dict_function[self.tok](*list_param)


@addToClass(AST2.AssignNode)
def execute(self):
    vars[scope][self.children[0].tok] = self.children[1].execute()


@addToClass(AST2.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST2.ForNode)
def execute(self):
    self.set_var.execute()
    while self.cond.execute():
        for c in self.children:
            c.execute()
        self.inc.execute()


@addToClass(AST2.EvalNode)
def execute(self):
    try:
        return evaluate[self.cond](self.var_name.execute(), self.stop_val.execute())
    except ValueError:
        print(f"an error occured in op {self.op} : {self.children[0].tok} or {self.children[1].tok} are not number")
        exit(3)


@addToClass(AST2.FunctionArgumentsNode)
def execute(self):
    if self.arg is not None:
        vars[scope][self.arg] = None
        function_args[scope].append(self.arg)
    for c in self.children:
        c.execute()


@addToClass(AST2.FunctionDefinition)
def execute(self):
    global scope
    function_def[self.name] = self.children[0]
    scope = self.name
    vars[scope] = {}
    function_args[self.name] = []
    self.params.execute()
    scope = "main"


@addToClass(AST2.FunctionCallNode)
def execute(self):
    global scope
    for c in self.children:
        c.execute(self.name, 0)
    scope = self.name
    function_def[self.name].execute()
    scope = "main"


@addToClass(AST2.FunctionParamNode)
def execute(self, fun_scope, i):
    if self.value is not None:
        vars[fun_scope][function_args[fun_scope][i]] = self.value.execute()

    if self.children:
        self.children[0].execute(fun_scope, i + 1)


def perform(prog):
    ast = parse(prog)
    ast.execute()
