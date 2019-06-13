from threading import Thread, get_ident
import time
from package.global_variable.variables import *


class Launcher(Thread):

    def __init__(self, list_instructions):
        Thread.__init__(self)
        launcher_pool[get_ident()] = self
        self.list_instructions = list_instructions
        self.dict_function = {'delay': self.delay, 'cube': self.cube, 'face': self.face, 'square': self.square,
                              'ledstrip': self.ledstrip, 'led': self.led}

    def run(self):
        for i in self.list_instructions:
            if access:
                self.dict_function[i[0]](*i[1:])
        del launcher_pool[get_ident()]

    def delay(self, pause_time):
        time.sleep(pause_time)

    def cube(self, brightness):
        cube.show(brightness)

    def face(self, idx_face, brightness):
        cube.faces[idx_face].show(brightness)

    def square(self, idx_face, idx_square, brightness):
        cube.faces[idx_face].squares[idx_square].show(brightness)

    def ledstrip(self, idx_face, idx_square, idx_ledstrip, brightness):
        cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].show(brightness)

    def led(self, idx_face, idx_square, idx_ledstrip, idx_led, brightness):
        cube.faces[idx_face].squares[idx_square].ledstrips[idx_ledstrip].show_led(idx_led, brightness)
