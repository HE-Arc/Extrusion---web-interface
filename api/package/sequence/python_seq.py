import ast
import time
import sys
import threading
from package.global_variable.variables import *


def delay(pause_time):
    """Pause function for the language

    :param pause_time: time in seconde between 0 and 10
    """
    try:
        pause = 10 if pause_time > 10 else pause_time
        time.sleep(pause)
    except:
        print("Error in pause")


def fun_cube(brightness):
    """ function to use cube in language

    :param brightness: int between 0 and 15
    :return:
    """
    try:
        cube.show(brightness)
    except:
        print("Error in cube function")


def face(idx_face, brightness):
    """function to use face in language

    :param idx_face: face index
    :param brightness: int between 0 and 15
    """
    try:
        cube.faces[idx_face].show(brightness)
    except:
        print("Error in face function")


def square(idx_face, idx_square, brightness):
    """function to use square in language

    :param idx_face: face index
    :param idx_square: square index
    :param brightness: int between 0 and 15
    """
    try:
        cube.faces[idx_face].squares[idx_square].show(brightness)
    except:
        print("Error in square function")


def ledstrip(idx_face, idx_square, idx_ledstrip, brightness):
    """function to use ledstrip in language

    :param idx_face: face index
    :param idx_square: square index
    :param idx_ledstrip: ledstrip index
    :param brightness: int between 0 and 15
    """
    try:
        cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].show(brightness)
    except:
        print("Error in ledstrip function")


def led(idx_face, idx_square, idx_ledstrip, idx_led, brightness):
    """function to use led in language

    :param idx_face: face index
    :param idx_square: square index
    :param idx_ledstrip: ledstrip index
    :param idx_led: led index
    :param brightness: int between 0 and 15
    """
    try:
        cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].led[idx_led].show(brightness)
    except:
        print("Error in led function")


def xyz(x, y, z, brightness):
    """function to use xyz coordinate in language

    :param x: x coordinate
    :param y: y coordinate
    :param z: z coordinate
    :param brightness: int between 0 and 15
    """
    try:
        cube.xyz[x, y, z].show(brightness)
    except:
        print("Error in xyz function")


def xyz_led(x, y, z, idx_led, brigthness):
    """function to use xyz led in language

    :param x:x coordinate
    :param y:x coordinate
    :param z:x coordinate
    :param idx_led: led index
    :param brigthness: int between 0 and 15
    """
    try:
        cube.xyz[x, y, z].led[idx_led].show(brigthness)
    except:
        print("Error in xyz_led function")


class NoImportsVisitor(ast.NodeVisitor):
    """class to define the node to not authorize

    """
    def visit_import(self, node):
        """Not visit import

        :param node: import
        :raise ValueError
        """
        raise ValueError(f"import is not allowed {node.col_offset}:{node.lineno}")

    def visit_lambda(self, node):
        """Not visit lambda

        :param node: import
        :raise ValueError
        """
        raise ValueError(f"lambda is not allowed {node.col_offset}:{node.lineno}")


class ThreadWithTrace(threading.Thread):
    """Class to contain animation sequence

    """
    def __init__(self, name, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.name = name

    def start(self):
        """Start the thread, the animation

        """
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """redefinition of run ro implement trace system

        """
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
        """kill the thread

        :return:
        """
        self.killed = True


def perform(prog):
    """function to execute custom sequence dode

    :param prog: sequence code
    :return:
    """
    try:
        # create ast tree of code in prog
        tree = ast.parse(prog)
        # check if tree has unauthorized node
        NoImportsVisitor().visit(tree)

        # execute the code
        exec(compile(tree, filename="<ast>", mode="exec"),
             {'exec': None,
              'eval': None,
              'dir': None,
              'compile': None,
              'print': None,
              'delay': time.sleep,
              'cube': fun_cube,
              'face': face,
              'square': square,
              'ledstrip': ledstrip,
              'led': led,
              'xyz': xyz,
              'xyz_led': xyz_led},
             {})
    except:
        print("Error in code")
