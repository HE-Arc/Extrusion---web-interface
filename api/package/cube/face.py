from .square import Square
from package.global_variable import variables
from package.global_variable import data_cube


class Face:

    def __init__(self, idx_face):
        self.idx = idx_face
        self.squares = [Square(idx_face, i) for i in range(24)]
        self.face_universe_address = data_cube.face[idx_face]

    def show(self, brightness):
        try:
            for t in self.face_universe_address:
                variables.artnet_group.set(t, brightness)
        except KeyError:
            pass
