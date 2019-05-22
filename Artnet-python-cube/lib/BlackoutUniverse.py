import sys
sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
import sys


# target_ip = '127.0.0.1'

# target_ip = '192.168.0.50'	 # typically in 2.x or 10.x range
# universe = 0 					# see docs
# it is not necessary to send whole universe
def main_artsync(universe, ip):
    pass


def main(universe, ip='127.0.0.1'):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    a.blackout()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        universe = int(sys.argv[2])
        ip = sys.argv[1]
        print(f"Blackout universe: {universe}")
        main(universe, ip)

    else:
        print("Wrong arguments,arguments: ip, universe")
