from threading import Timer
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.ArtSyncGroup import ArtSyncGroup
from threading import Timer
from ipaddress import IPv4Network


class ArtNetGroup():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, *args):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = []
        ips = set()
        self.sync = ArtSyncGroup()
        for a in args:
            self.listArtNet.append(a)
            ip = self.get_broadcast_address(a.TARGET_IP)
            if ip not in ips:
                self.sync.add(StupidArtSync(ip))
                ips.add(ip)
        self.fps = 30
        self.nb_art_net = len(self.listArtNet)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def set(self, packet):
        [i.set(packet) for i in self.listArtNet]

    def show(self, artSync):
        if artSync:
            self.sync.send()
            [i.show() for i in self.listArtNet]
            self.sync.send()
        else:
            [i.show() for i in self.listArtNet]

    def start(self, artSync):
        if artSync:
            self.sync.send()
            self.show(False)
            self.sync.send()
        else:
            self.show(False)
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start, [artSync])
        self.__clock.daemon = True
        self.__clock.start()

    def stop(self):
        self.__clock.cancel()

    def write_file(self, file):
        [file.write(StupidArtnet.print_object_and_packet(i)) for i in self.listArtNet]

    @staticmethod
    def get_broadcast_address(ip):
        broadcast_ip = ".".join(ip.split('.')[0:-1]) + '.'
        return broadcast_ip + '255'
