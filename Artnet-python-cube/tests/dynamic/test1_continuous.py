import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.animation.Animation import Animation
import time
import datetime

filename = "tests/logs/dynamic/test1_continuous.txt"
file = open(filename, "a")


def main_no_artsync(universe, ip='127.0.0.1', tmp=0.5, pause=5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    anim = Animation(filename, a)
    anim.anime_pause_noartsync(Animation.anime_1, tmp, pause)


def main_artsync(universe, ip='127.0.0.1', tmp=5, pause=5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    anim = Animation(filename, a)
    anim.anime_pause_artsync(Animation.anime_1, tmp, pause)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        time = sys.argv[4]
        pause_time = sys.argv[5]

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Animate universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), ip, float(time), float(pause_time))
        elif type == "artsync":
            main_artsync(int(universe1), ip, float(time), float(pause_time))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, animation_time, pause time")

    file.close()
