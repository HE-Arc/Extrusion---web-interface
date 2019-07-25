class ArtSyncGroup:
    """ArtSyncGroup is a class to manage multiple instance of StupidArtSync"""

    def __init__(self, *args):
        """Constructor of ArtNet

        :param args: StupidArtSnyc objects
        """
        self.listArtNet = []
        for a in args:
            self.listArtNet.append(a)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def send(self):
        """Send all StupidArtSync data

        """
        for i in self.listArtNet:
            i.send()

    def clear(self):
        """Erase all object in group

        :return:
        """
        self.listArtNet.clear()

    def add(self, *args):
        """add StupidArtSync object to group

        :param args: StupidArtSync Objects
        :return:
        """
        for i in args:
            self.listArtNet.append(i)
