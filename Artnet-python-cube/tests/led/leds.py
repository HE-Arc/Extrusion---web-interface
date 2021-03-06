import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.animation.Animation import Animation
import datetime

filename = "tests/logs/dynamic/leds.txt"
file = open(filename, "a")


def main_no_artsync(universe, start_channel, end_channel, brigtness, ip='127.0.0.1', tmp=0.5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    anim = Animation(filename, a)
    anim.anime_noartsync(Animation.anime_2, tmp, start_channel, end_channel, brigtness)


def main_artsync(universe, start_channel, end_channel, ip='127.0.0.1', tmp=0.5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    anim = Animation(filename, a)
    anim.anime_artsync(Animation.anime_2, tmp, start_channel, end_channel)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        start_channel = sys.argv[4]
        end_channel = sys.argv[5]
        bright = sys.argv[6]
        try:
            time = sys.argv[7]
        except:
            time = 1

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(start_channel), int(end_channel), int(bright), ip, float(time))
        elif type == "artsync":
            main_artsync(int(universe1), int(start_channel), int(end_channel), ip, float(time))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, start channel, stop channel,time_animation")

    file.close()
