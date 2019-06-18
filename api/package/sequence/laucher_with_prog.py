from threading import Thread, get_ident
from package.sequence.interpreter_withfunc import perform
from package.global_variable.variables import *


class Launcher(Thread):

    def __init__(self, prog):
        Thread.__init__(self)
        self.prog = prog

    def run(self):
        global state
        launcher_access[get_ident()] = True
        perform(self.prog)

        state = "free"
