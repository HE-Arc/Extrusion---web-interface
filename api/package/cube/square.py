from .ledstrip import Ledstrip
class Square:
    def __init__(self, *ledstrip):
        self.ledstrip = []
        for i in ledstrip:
            self.ledstrip.append(i)
