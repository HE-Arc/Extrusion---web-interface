from .square import Square
from package.global_variable import variables
from package.global_variable import data_cube


class Face:

    def __init__(self, idx_face):
        self.idx = idx_face
        self.squares = []
        self.face_universe_address = data_cube.face[idx_face]
        [self.squares.append(Square(idx_face, i)) for i in range(24)]

    def show(self, brightness):
        variables.artnet_group.set(self.face_universe_address, brightness)
