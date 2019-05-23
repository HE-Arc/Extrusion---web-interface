from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.ArtSyncGroup import ArtSyncGroup
from threading import Timer


class ArtNetGroup():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, *args):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = []
        self.ips = set()
        self.sync = ArtSyncGroup()
        for a in args:
            self.listArtNet.append(a)
            self.add_sync(a.TARGET_IP)
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
        self.show(artSync)
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start, [artSync])
        self.__clock.daemon = True
        self.__clock.start()

    def stop(self):
        self.__clock.cancel()

    def write_file(self, file):
        [file.write(StupidArtnet.print_object_and_packet(i)) for i in self.listArtNet]

    def add(self, *args):
        for i in args:
            self.listArtNet.append(i)
            self.add_sync(i.TARGET_IP)

    def add_sync(self, ip):
        ip = StupidArtSync.get_broadcast_address(ip)
        if ip not in self.ips:
            self.sync.add(StupidArtSync(ip))
            self.ips.add(ip)
