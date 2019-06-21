from package.global_variable import variables


class Led:
    def __init__(self, address, idx_led):
        if len(address) == 7:
            if address[0] == 1:
                self.universe, self.address_start, balance = ((address[4], address[5], 8),
                                                              (address[1], address[2], 0))[idx_led < 8]

                self.address_start = self.address_start + 3 * (idx_led - balance)
                self.address_end = self.address_start + 2
            else:
                self.universe, self.address_end, balance = ((address[1], address[3], 19),
                                                            (address[4], address[6], 0))[idx_led < 19]

                self.address_end = self.address_end - 3 * (idx_led - balance)
                self.address_start = self.address_end - 2
        else:
            self.universe = address[1]
            if address[0] == 1:
                self.address_start = address[2] + 3 * idx_led
                self.address_end = self.address_start + 2
            else:
                self.address_end = address[3] - 3 * idx_led
                self.address_start = self.address_end - 2

    def show(self, brightness):
        try:
            variables.artnet_group.set((self.universe, self.address_start, self.address_end), brightness)
        except KeyError:
            pass
