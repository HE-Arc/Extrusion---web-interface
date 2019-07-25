from package.global_variable import variables

cut_little_ledstrip = 8
cut_big_ledstrip = 19
nb_led_by_ledstrip = 3


# address that is on 2 ledstrips contains 7 values (way, universe1, start_1, end_1, universe2, start_2, end_2)
# address that is on 1 ledstrip contains 4 values (way, universe, start, end)
# way can be 0 or 1

class Led:
    """Represent a led of the cube

    """
    def __init__(self, address, idx_led):
        """Constructor of led

        :param address: tuple of led address
        :param idx_led: led index
        """
        self.exist = False
        if address is not None:
            self.exist = True
            # check if the ledstrip, where is the led, is on 2 universe
            if len(address) == 7:
                # check if the ledstrip, where is the led ,follow coordinate system
                if address[0] == 1:
                    # on 2 universes, take the good universe and start address according to the the led index
                    self.universe, self.address_start, balance = ((address[4], address[5], cut_little_ledstrip),
                                                                  (address[1], address[2], 0))[
                        idx_led < cut_little_ledstrip]

                    # set start address of the led,
                    # remove balance if on the second address. the address on second ledstrip must restart to 0
                    self.address_start = self.address_start + nb_led_by_ledstrip * (idx_led - balance)
                    # set end address according to start address
                    self.address_end = self.address_start + (nb_led_by_ledstrip - 1)
                else:
                    # on 2 universes, take the good universe and start address according to the the led index
                    self.universe, self.address_end, balance = ((address[1], address[3], cut_big_ledstrip),
                                                                (address[4], address[6], 0))[idx_led < cut_big_ledstrip]
                    # set end address of the led,
                    # remove balance if on the second address.
                    # the address on second ledstrip must restart to end address
                    self.address_end = self.address_end - nb_led_by_ledstrip * (idx_led - balance)
                    # set start address according to end address
                    self.address_start = self.address_end - (nb_led_by_ledstrip - 1)
            else:
                self.universe = address[1]
                if address[0] == 1:
                    # set start address according to led index
                    self.address_start = address[2] + nb_led_by_ledstrip * idx_led
                    # set end address according to start address
                    self.address_end = self.address_start + (nb_led_by_ledstrip - 1)
                else:
                    # set end address according to led index
                    self.address_end = address[3] - nb_led_by_ledstrip * idx_led
                    # set start address according to end address
                    self.address_start = self.address_end - (nb_led_by_ledstrip - 1)

    def show(self, brightness):
        """Illuminate the led with brightness

        :param brightness: int between 0 and 15 include
        :raise exception
        """
        try:
            if self.exist:
                variables.artnet_group.set((self.universe, self.address_start, self.address_end), brightness)
        except Exception as e:
            raise
