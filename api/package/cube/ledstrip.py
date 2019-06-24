from package.global_variable import variables
from package.cube.led import Led


class Ledstrip:
    def __init__(self, address_ledstrip):
        self.address = address_ledstrip
        self.led = [Led(self.address, i) for i in range(27)]

    def show(self, brightness):
        try:
            if self.address is not None:
                variables.artnet_group.set((self.address[1], self.address[2], self.address[3]), brightness)
                if len(self.address) == 7:
                    variables.artnet_group.set((self.address[4], self.address[5], self.address[6]), brightness)
        except KeyError:
            raise