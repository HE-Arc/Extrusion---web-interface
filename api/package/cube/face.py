from .square import Square


class Face:

    def __init__(self, idx_face):
        if idx_face < 4:
            self.squares = [Square(idx_face, i) for i in range(24)]
        else:
            self.squares = [Square(idx_face, i) for i in range(12)]
        # self.face_universe_address = data_cube.face[idx_face]

    def show(self, brightness):
        try:
            for s in self.squares:
                s.show(brightness)
        except:
            raise

