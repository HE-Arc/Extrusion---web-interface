class ArtSyncGroup:
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, *args):
        """Class Initialization."""
        # Instance variables
        self.listArtNet = []
        for a in args:
            self.listArtNet.append(a)

    def __str__(self):
        return str(self.listArtNet)

    def ___repr__(self):
        return str(self.listArtNet)

    def send(self):
        for i in self.listArtNet:
            i.send()

    def add(self, *args):
        for i in args:
            self.listArtNet.append(i)
