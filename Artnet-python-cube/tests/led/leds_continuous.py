import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
from lib.animation.Animation import Animation
import datetime, time

filename = "tests/logs/dynamic/leds_continuous.txt"
file = open(filename, "a")


def main_no_artsync(universe, start_channel, end_channel, ip='127.0.0.1', tmp=5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    packet = Animation.anime_2(packet_size, start_channel, end_channel)
    a.set(packet[0])
    file.write(StupidArtnet.print_object_and_packet(a))
    group = ArtNetGroup(a)
    group.start(False)
    time.sleep(tmp)
    group.stop()
    group.set(bytearray(512))
    group.show(False)


def main_artsync(universe, start_channel, end_channel, ip='127.0.0.1', tmp=5):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    packet = Animation.anime_2(packet_size, start_channel, end_channel)
    a.set(packet[0])
    file.write(StupidArtnet.print_object_and_packet(a))
    group = ArtNetGroup(a)
    group.start(True)
    time.sleep(tmp)
    group.stop()
    group.set(bytearray(512))
    group.show(True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        start_channel = sys.argv[4]
        end_channel = sys.argv[5]
        try:
            duration = sys.argv[6]
        except:
            duration = 5

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(start_channel), int(end_channel), ip, float(duration))
        elif type == "artsync":
            main_artsync(int(universe1), int(start_channel), int(end_channel), ip, float(duration))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, start channel, stop channel, duration")

    file.close()
