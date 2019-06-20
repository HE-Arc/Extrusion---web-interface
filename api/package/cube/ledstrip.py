from package.global_variable import variables


class Ledstrip:
    def __init__(self, idx_face, idx_square, idx_ledstrip, address_ledstrip):
        self.idx_face = idx_face
        self.idx_square = idx_square
        self.idx_ledstrip = idx_ledstrip
        self.address = address_ledstrip[idx_face][idx_square][idx_ledstrip]

    def show(self, brightness):
        try:
            if len(self.address) == 6:
                variables.artnet_group.set((self.address[0], self.address[1], self.address[2]), brightness)
                variables.artnet_group.set((self.address[3], self.address[4], self.address[5]), brightness)
            else:
                variables.artnet_group.set(self.address, brightness)
        except KeyError:
            pass

    def show_led(self, idx_led, brightness):
        pass
