from .ledstrip import Ledstrip
from package.global_variable.data_cube import *


class Square:
    def __init__(self, idx_face, idx_square):
        self.ledstrips = [Ledstrip(address_ledstrip[idx_face][idx_square][i]) for i in range(4)]

    def show(self, brightness):
        try:
            for l in self.ledstrips:
                l.show(brightness)
        except:
            raise
