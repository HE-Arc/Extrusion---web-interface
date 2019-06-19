from .square import Square
from package.global_variable import variables
from package.global_variable import data_cube


class Face:

    def __init__(self, idx_face):
        self.idx = idx_face
        if idx_face < 4:
            self.squares = [Square(idx_face, i) for i in range(24)]
        else:
            self.squares = [Square(idx_face, i) for i in range(12)]
        # self.face_universe_address = data_cube.face[idx_face]

    def show(self, brightness):
        for s in self.squares:
            s.show(brightness)

    """def show_face(self, brightness):
        try:
            for t in self.face_universe_address:
                variables.artnet_group.set(t, brightness)
        except KeyError:
            pass"""
