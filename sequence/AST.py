"""
Jaggi Charles-Lewis
Jeanneret Steven
HE-ARC
13 janvier 2019

Module to create a syntactic tree and his graphviz representation
Contain the class to create node's tree
"""


import pydot


class Node:
    """
    class that represent a node in the syntactic tree
    """
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'

    def __init__(self, children=None):
        """
        constructor of syntactic node
        :param children: children of the node
        """
        self.ID = str(Node.count)
        Node.count += 1
        if not children:
            self.children = []
        elif hasattr(children, '__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self, next):
        """
        add a node for the sewing
        :param next: node which come next
        """
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c, Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix, type(c), c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
        if not dot: dot = pydot.Dot()
        dot.add_node(pydot.Node(self.ID, label=repr(self), shape=self.shape))
        label = edgeLabels and len(self.children) - 1
        for i, c in enumerate(self.children):
            c.makegraphicaltree(dot, edgeLabels)
            edge = pydot.Edge(self.ID, c.ID)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
        return dot

    def threadTree(self, graph, seen=None, col=0):
        colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
        if not seen: seen = []
        if self in seen: return
        seen.append(self)
        new = not graph.get_node(self.ID)
        if new:
            graphnode = pydot.Node(self.ID, label=repr(self), shape=self.shape)
            graphnode.set_style('dotted')
            graph.add_node(graphnode)
        label = len(self.next) - 1
        for i, c in enumerate(self.next):
            if not c: return
            col = 0
            color = colors[col]
            c.threadTree(graph, seen, col)
            edge = pydot.Edge(self.ID, c.ID)
            edge.set_color(color)
            edge.set_arrowsize('.5')
            edge.set_constraint('false')
            if label:
                edge.set_taillabel(str(i))
                edge.set_labelfontcolor(color)
            graph.add_edge(edge)
        return graph


class ProgramNode(Node):
    """
    extends Node and represent a program in the tree
    """
    type = 'Program'


class OpNode(Node):
    """
    extends Node and represent a arithmetic operation in the tree
    """
    def __init__(self, op, children):
        """
        redefinition of __init__ with an operator
        :param op: arithmetic operation
        :param children: on what is done the operation
        """
        Node.__init__(self, children)
        self.op = op

    def __repr__(self):
        """
        representation of the node
        :return: the string of the operation
        """
        return f"{self.op}"


class LineNode(Node):
    """
    extends Node and represent a Line in the tree
    """
    def __init__(self, children):
        """
        redefinition of __init__
        store line in a variable
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.tok = "line"

    def __repr__(self):
        """
        representation of the node
        :return: the token of the node
        """
        return self.tok


class StyleNode(Node):
    """
    extends Node and represent a Style structure in the tree
    """
    type = 'style'

    def __init__(self, tok, children=None):
        """
        redefinition of __init__
        store style structure in a variable
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.tok = tok

    def __repr__(self):
        """
        representation of the node
        :return: the token of the node
        """
        return self.tok


class WhileNode(Node):
    """
    extends Node and represent a while loop in the tree
    """
    type = 'while'

    def __init__(self, op, children=None):
        """
        redefinition of __init__
        store style operation in a variable
        :param op: operation of while condition
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.op = op

    def __repr__(self):
        """
        representation of the node
        :return: the condition operation of the while
        """
        return f"while {self.op}"


class ForNode(Node):
    """
    extends Node and represent a for loop in the tree
    """
    type = 'for'

    def __init__(self, set_var, cond, inc, children=None):
        """
        redefinition of __init__
        store the variable of the for loop
        store the cond for the loo
        store the incrementation of for loop
        :param set_var: variable set in the for loop
        :param cond: stop condition of the loop
        :param inc: incrementation of for loop
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.set_var = set_var
        self.cond = cond
        self.inc = inc

    def __repr__(self):
        """
        representation of the node
        :return: the condition of the for
        """
        return f"for {self.cond}"


class IfNode(Node):
    """
    extends Node and represent a if condition in the tree
    """
    type = 'if'

    def __init__(self, cond, children):
        """
        edefinition of __init__
        store the stop condition for the if
        :param cond: stop condition of the if
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.cond = cond

    def __repr__(self):
        """
        representation of the node
        :return: the condition of the if
        """
        return f"if {self.cond}"


class EvalNode(Node):
    """
    extends Node and represent an evaluation in the tree
    """
    type = 'eval'

    def __init__(self, var_name, cond, stop_val):
        """
        redefinition of __init__
        store the evaluation
        :param var_name:
        :param cond: condition of evaluation
        :param stop_val:
        """
        Node.__init__(self)
        self.var_name = var_name
        self.cond = cond
        self.stop_val = stop_val

    def __repr__(self):
        """
        representation of the node
        :return: the evaluation
        """
        return f"{self.var_name} {self.cond} {self.stop_val}"


class StatementNode(Node):
    """
    extends Node and represent a statement in the tree
    """
    type = "Statement"


class TokenNode(Node):
    """
    extends Node and represent a token in the tree
    """
    type = 'token'

    def __init__(self, tok, children=None):
        """
        redefinition of __init__
        store token in a variable
        :param tok: token to store
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.tok = tok

    def __repr__(self):
        """
        representation of the node
        :return: the token of the node
        """
        return repr(self.tok)


class AssignNode(Node):
    """
    extends Node and represent a = in the tree
    """
    type = '='


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator
