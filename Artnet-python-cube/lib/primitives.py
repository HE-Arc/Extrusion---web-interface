__version__ = '0.1'

import json
import array


class CubeAPI():
    def get_vertical(self, indice):
        """

        :param indice: indice of vertical edge of the cube
         to enlighten. The indice can vary from 0 to 8
        :return: a dictionary containing the universes as key,
        and an array of channels for each universe
        """
        start_pixel = 85
        led_bar = dict()
        for strip in range(0, 6):
            # print("################ NEW STRIP ###########s")
            for y_offset in range(0, 27):
                # print(self.get_artnet_params(indice * 28, start_pixel + y_offset))
                universe, indices = self.get_artnet_params(indice * 28, start_pixel + y_offset)
                if universe in led_bar:
                    led_bar[universe] = led_bar[universe] + indices
                else:
                    led_bar[universe] = indices
                # print(f"led_bar: {led_bar}")

            start_pixel += 28
        # print(led_bar)
        return led_bar

    @staticmethod
    def get_artnet_params(x_coord, y_coord):

        # Calculate strip x and y coordinates
        if x_coord % 28 == 0:
            strip_x = int(x_coord / 28) * 2
        else:
            strip_x = int(x_coord / 28) * 2 + 1

        if y_coord % 28 == 0:
            strip_y = int(y_coord / 28) * 2
        else:
            strip_y = int(y_coord / 28) * 2 + 1

        # calculate led_offset
        if x_coord % 2 == 0:
            # Handle empty coordinates between vertical ledstrips
            if y_coord % 28 == 0:
                return
            led_offset = y_coord
        else:
            # Handle empty coordinates between horizontal ledstrips
            if x_coord % 28 == 0:
                return
            led_offset = x_coord
        led_offset %= 28
        led_offset -= 1
        led_offset *= 3

        # print(f'#################  x: {x_coord}, y: {y_coord}')
        with open('lib/cube.json') as json_data:
            d = json.load(json_data)
        # print(f'strip_x: {strip_x}, strip_y: {strip_y}')
        strip = d[str(strip_x)][str(strip_y)]
        universe = strip['universe']
        channel = strip['channel']
        # print(f'universe: {universe}, channel: {channel}, led_offset: {led_offset}')
        start_led = channel + led_offset
        universe_add = int(start_led / 511)
        if universe_add > 0:
            universe += universe_add
            # print(f'universe: {universe}, channel: {channel}, led_offset: {led_offset}')
            start_led %= 511
            start_led += 1
        return universe, [start_led, start_led + 1, start_led + 2]

    def change_pixel(self, intensity, *coord):
        universe, indices = self.get_artnet_params(coord[0], coord[1])
        data_array = [intensity if (i in indices) else 0 for i in range(0, 511)]
        print(f'Data: {data_array}')
        print(f'Universe: {universe}')
        return array.array('B', data_array), universe


def main(argv):
    print(argv)
    # send_artnet_frame(int(argv[0]), int(argv[1]), int(argv[2]))


'''if __name__ == '__main__':
    # call example for pixel 0, 85 and intensity = 127:
    # 'python cube_case.py 127 0 85'
    CubeAPI.get_vertical(8)

    get_vertical(2)
    get_vertical(4)
    get_vertical(6)
    get_vertical(8)
    main(sys.argv[1:])

    print(get_artnet_params(0, 85))
    print(get_artnet_params(0, 86))
    print(get_artnet_params(0, 85 + 26))
    print(get_artnet_params(0, 85 + 27))
    print(get_artnet_params(0, 113))
    print(get_artnet_params(0, 114))
    print(get_artnet_params(0, 113 + 26))
    send_artnet_frame(127, 0, 85)'''
