import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.SychrArtSync import SychronizerArtSync
from lib.ArtNetGroup import ArtNetGroup
import time


class Animation():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, file, *art_net, **kwargs):
        """Class Initialization."""
        # Instance variables
        if kwargs["artSync"]:
            self.art_nets = SychronizerArtSync(50, 30, *art_net)
        else:
            self.art_nets = ArtNetGroup(*art_net)
        self.packet_size = art_net[0].PACKET_SIZE
        self.filename = f"tests/logs/dynamic/{file}"
        self.file = open(self.filename, "a")

    def anime_noartsync(self, anime, tmp=0.5):
        packet_list = anime(self.packet_size)
        for i in range(0, len(packet_list)):
            self.art_nets.set(packet_list[i])
            self.art_nets.write_file(self.file)
            self.art_nets.show()
            time.sleep(tmp)
        self.file.close()

    def anime_pause_noartsync(self, anime, tmp=0.5, pause=5):
        packet_list = anime(self.packet_size)
        for i in range(0, len(packet_list)):
            self.art_nets.set(packet_list[i])
            self.art_nets.write_file(self.file)
            self.art_nets.show()
            if i == len(packet_list) / 2:
                self.art_nets.start()
                time.sleep(pause)
                self.art_nets.stop()
            else:
                self.art_nets.show()
                time.sleep(tmp)
        self.file.close()

    def anime_artsync(self, anime, tmp=0.5):
        packet_list = anime(self.packet_size)
        sync = StupidArtSync()
        for i in range(0, len(packet_list)):
            self.art_nets.set(packet_list[i])
            self.art_nets.write_file(self.file)
            sync.send()
            self.art_nets.show()
            sync.send()
            time.sleep(tmp)
        self.file.close()

    def anime_pause_artsync(self, anime, tmp=0.5, pause=5, nb_packet=50):
        packet_list = anime(self.packet_size)
        sync = StupidArtSync()
        for i in range(0, len(packet_list)):
            self.art_nets.set(packet_list[i])
            self.art_nets.write_file(self.file)
            if i == len(packet_list) / 2:
                self.art_net.start_artSync(nb_packet)
                time.sleep(pause)
                self.art_net.stop_artSync()
            else:
                sync.send()
                self.art_net.show()
                sync.send()
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
