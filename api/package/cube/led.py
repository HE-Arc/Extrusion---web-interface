from package.global_variable import variables

cut_little_ledstrip = 8
cut_big_ledstrip = 19
nb_led_by_ledstrip = 3


# address that is on 2 ledstrips contains 7 values (way, universe1, start_1, end_1, universe2, start_2, end_2)
# address that is on 1 ledstrip contains 4 values (way, universe, start, end)
# way can be 0 or 1

class Led:
    def __init__(self, address, idx_led):
        self.exist = False
        if address is not None:
            self.exist = True
            if len(address) == 7:
                if address[0] == 1:
                    self.universe, self.address_start, balance = ((address[4], address[5], cut_little_ledstrip),
                                                                  (address[1], address[2], 0))[
                        idx_led < cut_little_ledstrip]

                    self.address_start = self.address_start + nb_led_by_ledstrip * (idx_led - balance)
                    self.address_end = self.address_start + (nb_led_by_ledstrip - 1)
                else:
                    self.universe, self.address_end, balance = ((address[1], address[3], cut_big_ledstrip),
                                                                (address[4], address[6], 0))[idx_led < cut_big_ledstrip]

                    self.address_end = self.address_end - nb_led_by_ledstrip * (idx_led - balance)
                    self.address_start = self.address_end - (nb_led_by_ledstrip - 1)
            else:
                self.universe = address[1]
                if address[0] == 1:
                    self.address_start = address[2] + nb_led_by_ledstrip * idx_led
                    self.address_end = self.address_start + (nb_led_by_ledstrip - 1)
                else:
                    self.address_end = address[3] - nb_led_by_ledstrip * idx_led
                    self.address_start = self.address_end - (nb_led_by_ledstrip - 1)

    def show(self, brightness):
        try:
            if self.exist:
                variables.artnet_group.set((self.universe, self.address_start, self.address_end), brightness)
        except Exception as e:
            print(e)
            raise
