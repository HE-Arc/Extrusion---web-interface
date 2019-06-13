from .ledstrip import Ledstrip


class Square:
    def __init__(self, idx_face, idx_square):
        self.idx_face = idx_face
        self.idx_square = idx_square
        self.ledstrips = [Ledstrip(idx_face, idx_square, i) for i in range(4)]

    def show(self, brightness):
        for l in self.ledstrips:
            l.show(brightness)
