from package.global_variable import variables
from package.cube.led import Led


class Ledstrip:
    """Represent a ledstrip

    """

    def __init__(self, address_ledstrip):
        """Constructor of ledstrip

        :param address_ledstrip: address of ledstrip
        """
        self.address = address_ledstrip
        self.led = [Led(self.address, i) for i in range(27)]

    def show(self, brightness):
        """Illuminate the ledstrip with brightness

        :param brightness: int between 0 and 15 include
        :raise exception
        """
        try:
            if self.address is not None:
                variables.artnet_group.set((self.address[1], self.address[2], self.address[3]), brightness)
                if len(self.address) == 7:
                    variables.artnet_group.set((self.address[4], self.address[5], self.address[6]), brightness)
        except KeyError:
            raise
