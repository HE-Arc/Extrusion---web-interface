import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.animation.animation import Animation
import time
import datetime

filename = "tests/logs/dynamic/leds.txt"
file = open(filename, "a")


def main_no_artsync(universe, start_channel, end_channel, ip='127.0.0.1', tmp=0.5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    anim = Animation("leds.txt", a)
    anim.anime_noartsync(Animation.anime_1, tmp)


def main_artsync(universe, start_channel, end_channel, ip='127.0.0.1', tmp=0.5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    anim = Animation("leds.txt", a)
    anim.anime_artsync(Animation.anime_1, tmp)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        start_channel = sys.argv[4]
        end_channel = sys.argv[5]
        try:
            time = sys.argv[6]
        except:
            time = 5

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(start_channel), int(end_channel), ip, time)
        elif type == "artsync":
            main_artsync(int(universe1), ip, int(start_channel), int(end_channel), time)
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, start channel, stop channel,time_sleep_for_artSync")

    file.close()
