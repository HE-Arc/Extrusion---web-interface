import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
import time
import datetime

filename = "tests/logs/static/test3_continuous.txt"
file = open(filename, "a")


def main_no_artsync(universe1, universe2, ip1='127.0.0.1', ip2='127.0.0.2', tmp=5):
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(ip1, port, universe1, packet_size)
    a2 = StupidArtnet(ip2, port, universe2, packet_size)
    a1.flash_all()  # send single packet with all channels at 255
    a2.flash_all()
    file.write(StupidArtnet.print_object_and_packet(a1))
    file.write(StupidArtnet.print_object_and_packet(a1))
    a1.start()
    a2.start()
    time.sleep(tmp)
    a1.stop()
    a2.stop()
    # time.sleep(3)  # wait a bit, 1 sec
    # a.stop()


def main_artsync(universe1, universe2, ip1='127.0.0.1', ip2='127.0.0.2', tmp=5, nb_packet=50):
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(ip1, port, universe1, packet_size)
    a2 = StupidArtnet(ip2, port, universe2, packet_size)
    a1.flash_all()  # send single packet with all channels at 255
    a2.flash_all()
    file.write(StupidArtnet.print_object_and_packet(a1))
    file.write(StupidArtnet.print_object_and_packet(a2))
    group = ArtNetGroup(a1, a2)
    group.start(True)
    time.sleep(tmp)
    group.stop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip1 = sys.argv[2]
        ip2 = sys.argv[3]
        universe1 = sys.argv[4]
        universe2 = sys.argv[5]
        pause_time = sys.argv[6]
        try:
            nb_packets = sys.argv[7]
        except:
            nb_packets = 50

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Animate universe: {universe1} on ip {ip1}, {universe2} on ip {ip2}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(universe2), ip1, ip2, float(pause_time))
        elif type == "artsync":
            main_artsync(int(universe1), int(universe2), ip1, ip2, float(pause_time), int(nb_packets))

        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, universe, time, nb_packet_for_artsync")

    file.close()
