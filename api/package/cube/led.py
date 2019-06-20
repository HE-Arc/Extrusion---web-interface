from package.global_variable import variables


class Led:
    def __init__(self, address, idx_led):
        if len(address) == 7:
            if address[6] == 1:
                if idx_led < 8:
                    self.universe = address[0]
                    self.address_start = address[1] + 3 * idx_led
                    self.address_end = self.address_start + 2
                else:
                    self.universe = address[3]
                    self.address_start = address[4] + 3 * idx_led
                    self.address_end = self.address_start + 2
            else:
                if idx_led < 18:
                    self.universe = address[3]
                    self.address_end = address[5] - 3 * idx_led
                    self.address_start = self.address_end - 2
                else:
                    self.universe = address[0]
                    self.address_end = address[2] - 3 * idx_led
                    self.address_start = self.address_end - 2
        else:
            self.universe = address[0]
            if address[3] == 1:
                self.address_start = address[1] + 3 * idx_led
                self.address_end = self.address_start + 2
            else:
                self.address_end = address[2] - 3 * idx_led
                self.address_start = self.address_end - 2

    def show(self, brightness):
        try:
            variables.artnet_group.set((self.universe, self.address_start, self.address_end), brightness)
        except KeyError:
            pass
