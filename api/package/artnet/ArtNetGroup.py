from .StupidArtnet import StupidArtnet
from .StupidArtSync import StupidArtSync
from .ArtSyncGroup import ArtSyncGroup
from threading import Timer


class ArtNetGroup:
    """ArtNetGroup is a class to manage multiple instance of StupidArtnet"""

    def __init__(self, fps, ip1, port1, ip2, port2, *args):
        """Constructor of ArtNetGroup

        :param
        fps -- fps to send all information on the network
        ip1 -- ip of the CaseCheminee side
        port1 -- port of the CaseCheminee side

        """
        # Instance variables
        self.ip1 = ip1
        self.ip2 = ip2
        self.port1 = port1
        self.port2 = port2
        self.listArtNet = {}
        self.ips = set()
        self.sync = ArtSyncGroup()
        for a in args:
            self.listArtNet[a.UNIVERSE] = a
            self.add_sync(a.TARGET_IP)
        self.fps = fps
        self.is_sleeping = False
        self.nb_art_net = len(self.listArtNet)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def set_all_universe(self, packet):
        for v in self.listArtNet.values():
            v.set(packet)

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.fps

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
        self.is_sleeping = False
        self.show(artSync)
        self.__clock = Timer((1000.0 / self.fps) / 1000.0, self.start, [artSync])
        self.__clock.daemon = True
        self.is_sleeping = True
        self.__clock.start()

    def stop(self):
        if self.is_sleeping:
            try:
                self.__clock.cancel()
                self.is_sleeping = False
                return True
            except:
                return False
        return False

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

    def set_ip(self, ip1, port1, ip2, port2, cube1_start, cube1_end, cube2_start, cube2_end):
        self.ips.clear()
        self.sync.clear()
        self.add_sync(ip1)
        self.add_sync(ip2)
        for i in range(cube1_start, cube1_end):
            self.listArtNet[i].TARGET_IP = ip1
            self.listArtNet[i].UDP_PORT = port1
        for i in range(cube2_start, cube2_end):
            self.listArtNet[i].TARGET_IP = ip2
            self.listArtNet[i].UDP_PORT = port2
        self.ip1 = ip1
        self.ip2 = ip2
        self.port1 = port1
        self.port2 = port2

    @staticmethod
    def get_artnet(ip1, port1, ip2, port2, cube1_start, cube1_end, cube2_start, cube2_end, fps):
        group = ArtNetGroup(fps, ip1, port1, ip2, port2)
        for i in range(cube1_start, cube1_end):
            group.add(StupidArtnet(ip1, port1, i))
        for i in range(cube2_start, cube2_end):
            group.add(StupidArtnet(ip2, port2, i))

        return group
