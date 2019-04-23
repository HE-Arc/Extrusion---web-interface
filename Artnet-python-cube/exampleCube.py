import sys

from lib import CubeAPI, StupidArtnet
import time

target_ip = '127.0.0.1'  # typically in 2.x or 10.x range
port = 6454  # for the simulator, the second cube is on an other port not an different ip adresse
universe = 0  # see docs
packet_size = 512  # it is not necessary to send whole universe
allowed_indices = [i for i in range(0, 9)] + \
                  [i for i in range(100, 109)]


def send_packets(_vertical, artnet):
    packet = bytearray(packet_size)  # create packet for Artnet
    brightness = 255
    for key in _vertical:
        print(f'Universe: {key} => channels: {_vertical[key]}')
        for i in range(packet_size):  # fill packet with sequential values
            packet[i] = brightness if i + 1 in _vertical[key] else 0
        subnet = int(key / 16)
        universe = key % 16
        print(f'subnet: {subnet}, universe: {universe}, packet: {packet}')
        artnet.set_subnet(subnet)
        artnet.set_universe(universe)
        artnet.set(packet)  # set the packet to stupid Artnet
        print(artnet)
        artnet.show()  # send the data


def turn_off(_vertical, artnet):
    # SOME DEVICES WOULD HOLD LAST DATA, TURN ALL OFF WHEN DONE
    for key in _vertical:
        subnet = int(key / 16)
        universe = key % 16
        print(f'blackout subnet {subnet} universe {universe}')
        artnet.set_subnet(subnet)
        artnet.set_universe(universe)
        artnet.blackout()


def main(param):
    global port  # just for test
    indice = int(param[0])
    if indice > 8 and indice < 18:
        port = 6454
    if len(param) > 1:
        sleep_time = float(param[1])
    else:
        sleep_time = 5

    # CREATING A STUPID ARTNET OBJECT
    # SETUP NEEDS A FEW ELEMENTS
    # TARGET_IP   = DEFAULT 127.0.0.1
    # PORT        = DEFAULT 6454
    # UNIVERSE    = DEFAULT 0
    # PACKET_SIZE = DEFAULT 512
    # FRAME_RATE  = DEFAULT 30
    a = StupidArtnet(target_ip, port, universe, packet_size)

    a.set_simplified(False)
    # MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
    # NET         = DEFAULT 0
    # SUBNET      = DEFAULT 0

    # CHECK INIT
    print(a)

    a.start()  # start continuous sending, else error pops when cleaning

    cubeAPI = CubeAPI()
    vertical = cubeAPI.get_vertical(indice)  # set the indice of vertical bar (0 to 8)

    send_packets(vertical, a)
    time.sleep(sleep_time)
    turn_off(vertical, a)

    # ... REMEMBER TO CLOSE THE THREAD ONCE YOU ARE DONE
    a.stop()

    # CLEANUP IN THE END
    del a


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("len(sys.argv)" + str(len(sys.argv)))
        main(sys.argv[1:])
    else:
        indice_needed = True
        number = 0
        while indice_needed:
            print(f"Allowed indices: {allowed_indices}")
            ind = input('Enter vertical indice :')
            try:
                number = float(ind)
            except ValueError:
                print("Invalid number")
            if number not in allowed_indices:
                print(f"Unallowed indice. Allowed indices are: "
                      f"{allowed_indices}")
            else:
                indice_needed = False
        main([number])
