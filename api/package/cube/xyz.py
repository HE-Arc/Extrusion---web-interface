from package.global_variable import variables
from package.cube.led import Led


class Xyz:
    """The class is the implementation of xyz coordinate

    """
    def __init__(self, address, x, y, z):
        """Constructor of Xyz

        :param address: all xyz datas
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        self.address = address[x, y, z]
        self.x = x
        self.y = y
        self.z = z
        self.led = [Led(self.address, i) for i in range(27)]

    def show(self, brightness):
        """Illuminate the ledstrip xyz

        :param brightness: int between 0 and 15 include
        :raise exception
        """
        try:
            if self.address is not None:
                variables.artnet_group.set((self.address[1], self.address[2], self.address[3]), brightness)
                if len(self.address) == 7:
                    variables.artnet_group.set((self.address[4], self.address[5], self.address[6]), brightness)
        except:
            raise
