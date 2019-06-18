from .StupidArtnet import StupidArtnet
from .StupidArtSync import StupidArtSync
from .ArtSyncGroup import ArtSyncGroup
from threading import Timer


class ArtNetGroup():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, *args):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = {}
        self.ips = set()
        self.sync = ArtSyncGroup()
        for a in args:
            self.listArtNet[a.UNIVERSE] = a
            self.add_sync(a.TARGET_IP)
        self.fps = 30
        self.nb_art_net = len(self.listArtNet)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def set_all_universe(self, packet):
        for v in self.listArtNet.values():
            v.set(packet)

    def show(self, artSync):
        if artSync:
            self.sync.send()
            for v in self.listArtNet.values():
                v.show()
            self.sync.send()
        else:
            for v in self.listArtNet.values():
                v.show()

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
            self.listArtNet[i.UNIVERSE] = i
            self.add_sync(i.TARGET_IP)

    def add_sync(self, ip):
        ip = StupidArtSync.get_broadcast_address(ip)
        if ip not in self.ips:
            self.sync.add(StupidArtSync(ip))
            self.ips.add(ip)

    def set(self, universe_address, brightness):
        self.listArtNet[universe_address[0]].set_buffer(universe_address[1], universe_address[2], brightness)

    @staticmethod
    def get_artnet(ip1, ip2):
        group = ArtNetGroup()
        port = 6454
        for i in range(24):
            group.add(StupidArtnet(ip1, port, i))
        for i in range(24, 40):
            group.add(StupidArtnet(ip2, port, i))

        return group
