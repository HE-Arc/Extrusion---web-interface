from .square import Square


class Face:
    """Represent the face of th cube

    """
    def __init__(self, idx_face):
        """Constructor of face

        :param idx_face: int between 0 and 5 include
        """
        if idx_face < 4:
            self.squares = [Square(idx_face, i) for i in range(24)]
        else:
            self.squares = [Square(idx_face, i) for i in range(12)]
        # self.face_universe_address = data_cube.face[idx_face]

    def show(self, brightness):
        """Illuminate the face with brightness

        :param brightness: int between 0 and 15 include
        :raise exception
        """
        try:
            for s in self.squares:
                s.show(brightness)
        except:
            raise

