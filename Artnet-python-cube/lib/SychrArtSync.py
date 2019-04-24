from lib.StupidArtSync import StupidArtSync
from threading import Timer


class SychronizerArtSync():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, nb_packet, fps, *args):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = []
        self.async = StupidArtSync()
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

    def start(self):
        self._send()
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start)
        self.__clock.daemon = True
        self.__clock.start()
        self.current_nb_packet += 1

    def _send(self):
        if self.current_nb_packet == 0:
            self.async.send()
        elif self.current_nb_packet % self.nb_packet == 0:
            self.async.send()
            self.async.send()
        artnet_to_send = self.nb_packet % self.nb_art_net
        self.listArtNet[artnet_to_send].show()

    def stop(self):
        self.async.send()
        self.stop()
        self.nb_packet = 0


if __name__ == '__main__':
    test = SychronizerArtSync()
    print(str(test))
