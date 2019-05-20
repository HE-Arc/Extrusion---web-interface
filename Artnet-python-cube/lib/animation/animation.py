import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
import time


class Animation():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, art_net,file):
        """Class Initialization."""
        # Instance variables
        self.art_net = art_net
        self.filename = f"tests/logs/dynamic/{file}"
        self.file = open(self.filename, "a")

    def one_universe_anime_1_noartsync(self, tmp=0.5):
        packet_list = Animation.anime_1(self.art_net.PACKET_SIZE)
        for i in range(0, len(packet_list)):
            self.art_net.set(packet_list[i])
            self.file.write(StupidArtnet.print_object_and_packet(self.art_net))
            self.art_net.show()
            time.sleep(tmp)
        self.file.close()

    def one_universe_anime_1_artsync(self, tmp=0.5):
        packet_list = Animation.anime_1(self.art_net.PACKET_SIZE)
        sync = StupidArtSync()
        for i in range(0, len(packet_list)):
            self.art_net.set(packet_list[i])
            self.file.write(StupidArtnet.print_object_and_packet(self.art_net))
            sync.send()
            self.art_net.show()
            time.sleep(tmp)
        self.file.close()

    @staticmethod
    def anime_1(packet_size):
        packet_list = []
        for i in range(0, packet_size, 3):
            packet = bytearray(packet_size)
            if i <= packet_size - 3:
                packet[i] = 255
                packet[i + 1] = 255
                packet[i + 2] = 255
                packet_list.append(packet)
        return packet_list


if __name__ == '__main__':
    pass
