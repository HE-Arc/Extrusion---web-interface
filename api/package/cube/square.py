from .ledstrip import Ledstrip
from package.global_variable.data_cube import *


class Square:
    def __init__(self, idx_face, idx_square):
        self.ledstrips = [Ledstrip(idx_face, idx_square, i, address_ledstrip) for i in range(4)]

    def show(self, brightness):
        for l in self.ledstrips:
            l.show(brightness)
