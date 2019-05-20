from threading import Timer
from lib.StupidArtnet import StupidArtnet
from threading import Timer


class ArtNetGroup():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, *args, ):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = []
        for a in args:
            self.listArtNet.append(a)
        self.fps = 30
        self.nb_art_net = len(self.listArtNet)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def set(self, packet):
        [i.set(packet) for i in self.listArtNet]

    def show(self):
        [i.show() for i in self.listArtNet]

    def start(self):
        self.show()
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start)
        self.__clock.daemon = True
        self.__clock.start()

    def stop(self):
        self.__clock.cancel()

    def write_file(self, file):
        [file.write(StupidArtnet.print_object_and_packet(i)) for i in self.listArtNet]
