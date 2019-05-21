from lib.StupidArtSync import StupidArtSync
from lib.StupidArtnet import StupidArtnet
from threading import Timer


class SychronizerArtSync():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, nb_packet, fps, artSync, args):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = []
        self.sync = artSync
        self.nb_packet = nb_packet
        self.current_nb_packet = 0
        self.fps = fps
        for a in args:
            self.listArtNet.append(a)

        self.nb_art_net = len(self.listArtNet)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def set(self, packet):
        [i.set(packet) for i in self.listArtNet]

    def start(self):
        self.show()
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start)
        self.__clock.daemon = True
        self.__clock.start()

    def show(self):
        if self.current_nb_packet == 0:
            self.sync.send()
        elif self.current_nb_packet % self.nb_packet == 0:
            self.sync.send()
            self.sync.send()
        artnet_to_send = self.current_nb_packet % self.nb_art_net
        self.listArtNet[artnet_to_send].show()
        self.current_nb_packet += 1

    def stop(self):
        self.sync.send()
        self.stop()
        self.nb_packet = 0

    def write_file(self, file):
        [file.write(StupidArtnet.print_object_and_packet(i)) for i in self.listArtNet]


if __name__ == '__main__':
    test = SychronizerArtSync()
    print(str(test))
