import ast
import time
import sys
import threading
from package.global_variable.variables import *


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
    cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].led[idx_led].show(brightness)


def xyz(x, y, z, brightness):
    cube.xyz[x, y, z].show(brightness)


class NoImportsVisitor(ast.NodeVisitor):

    def visit_import(self, node):
        raise ValueError(f"import is not allowed {node.col_offset}:{node.lineno}")

    def visit_lambda(self, node):
        raise ValueError(f"lambda is not allowed {node.col_offset}:{node.lineno}")


class ThreadWithTrace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def perform(prog):
    tree = ast.parse(prog)
    NoImportsVisitor().visit(tree)

    exec(compile(tree, filename="<ast>", mode="exec"),
         {'exec': None,
          'eval': None,
          'dir': None,
          'compile': None,
          'delay': time.sleep,
          'cube': fun_cube,
          'face': face,
          'square': square,
          'ledstrip': ledstrip,
          'led': led,
          'xyz': xyz},
         {})
