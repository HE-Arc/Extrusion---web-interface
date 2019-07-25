from .ledstrip import Ledstrip
from package.global_variable.data_cube import *


class Square:
    """Represent a square

    """
    def __init__(self, idx_face, idx_square):
        """Constructor of square

        :param idx_face: index of face where is the square
        :param idx_square: index of face
        """
        self.ledstrips = [Ledstrip(address_ledstrip[idx_face][idx_square][i]) for i in range(4)]

    def show(self, brightness):
        """Illuminate the square with brightness

        :param brightness: int between 0 and 15 include
        :raise exception
        """
        try:
            for l in self.ledstrips:
                l.show(brightness)
        except:
            raise
