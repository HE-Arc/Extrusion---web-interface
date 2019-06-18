import AST
from AST import addToClass
from functools import reduce
from parser_data import parse

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
}

orders = []
function_def = {}
function_args = {}
scope = "main"
vars = {scope: {}}


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.StatementNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.CommandeNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.CalcNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.DataNode)
def execute(self):
    if self.tok in vars[scope]:
        return vars[scope][self.tok]
    elif self.tok in vars["main"]:
        return vars["main"][self.tok]
    else:
        return float(self.tok)


@addToClass(AST.OrderNode)
def execute(self):
    list_param = []
    for c in self.children:
        list_param.append(c.execute())
    if self.tok != "delay":
        list_param = [int(f) for f in list_param]

    orders.append((self.tok, *list_param))


@addToClass(AST.AssignNode)
def execute(self):
    vars[scope][self.children[0].tok] = self.children[1].execute()


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.ForNode)
def execute(self):
    self.set_var.execute()
    while self.cond.execute():
        for c in self.children:
            c.execute()
        self.inc.execute()


@addToClass(AST.EvalNode)
def execute(self):
    try:
        return evaluate[self.cond](self.var_name.execute(), self.stop_val.execute())
    except ValueError:
        print(f"an error occured in op {self.op} : {self.children[0].tok} or {self.children[1].tok} are not number")
        exit(3)


@addToClass(AST.FunctionArgumentsNode)
def execute(self):
    if self.arg is not None:
        vars[scope][self.arg] = None
        function_args[scope].append(self.arg)
    for c in self.children:
        c.execute()


@addToClass(AST.FunctionDefinition)
def execute(self):
    global scope
    function_def[self.name] = self.children[0]
    scope = self.name
    vars[scope] = {}
    function_args[self.name] = []
    self.params.execute()
    scope = "main"


@addToClass(AST.FunctionCallNode)
def execute(self):
    global scope
    for c in self.children:
        c.execute(self.name, 0)
    scope = self.name
    function_def[self.name].execute()


@addToClass(AST.FunctionParamNode)
def execute(self, fun_scope, i):
    if self.value is not None:
        vars[fun_scope][function_args[fun_scope][i]] = self.value.execute()

    if self.children:
        self.children[0].execute(fun_scope, i + 1)


if __name__ == '__main__':
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
    print(len(orders))

    for p in orders:
        print(f'{p}')
