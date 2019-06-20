from package.global_variable import variables
from package.cube.led import Led


class Ledstrip:
    def __init__(self, idx_face, idx_square, idx_ledstrip, address_ledstrip):
        self.address = address_ledstrip[idx_face][idx_square][idx_ledstrip]
        self.led = None
        if self.address is not None:
            self.led = [Led(self.address, i) for i in range(27)]

    def show(self, brightness):
        try:
            if self.address is not None:
                if len(self.address) == 7:
                    variables.artnet_group.set((self.address[0], self.address[1], self.address[2]), brightness)
                    variables.artnet_group.set((self.address[3], self.address[4], self.address[5]), brightness)
                else:
                    variables.artnet_group.set(self.address, brightness)
        except KeyError:
            pass