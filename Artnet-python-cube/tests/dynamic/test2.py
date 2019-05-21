import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.animation.animation import Animation
import time
import datetime

filename = "tests/logs/dynamic/test2.txt"
file = open(filename, "a")


def main_no_artsync(universe1, universe2, ip='127.0.0.1', tmp=0.5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(target_ip, port, universe1, packet_size)
    a2 = StupidArtnet(target_ip, port, universe2, packet_size)
    anim = Animation("test2.txt", a1, a2)
    anim.anime_noartsync(Animation.anime_1, tmp)


def main_artsync(universe1, universe2, ip='127.0.0.1', tmp=0.5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(target_ip, port, universe1, packet_size)
    a2 = StupidArtnet(target_ip, port, universe2, packet_size)
    anim = Animation("test2.txt", a1, a2)
    anim.anime_artsync(Animation.anime_1, tmp)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        universe2 = sys.argv[4]
        time = sys.argv[5]

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Animate universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(universe2), ip, float(time))
        elif type == "artsync":
            main_artsync(int(universe1), int(universe2), ip, float(time))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, universe, animation_time")

    file.close()
