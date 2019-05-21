import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.ArtSyncGroup import ArtSyncGroup
import time
import datetime

filename = "tests/logs/static/test3.txt"
file = open(filename, "a+")


def main_no_artsync(universe1, universe2, ip1='127.0.0.1', ip2='127.0.0.2'):
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(ip1, port, universe1, packet_size)
    a2 = StupidArtnet(ip2, port, universe2, packet_size)
    a1.flash_all()  # send single packet with all channels at 255
    a2.flash_all()
    file.write(StupidArtnet.print_object_and_packet(a1))
    file.write(StupidArtnet.print_object_and_packet(a1))
    a1.show()
    a2.show()
    # time.sleep(3)  # wait a bit, 1 sec
    # a.stop()


def main_artsync(universe1, universe2, ip1='127.0.0.1', ip2='127.0.0.2', slp=5):
    packet_size = 512
    port = 6454
    sync = ArtSyncGroup(StupidArtSync(ip1),StupidArtSync(ip2))
    a1 = StupidArtnet(ip1, port, universe1, packet_size)
    a2 = StupidArtnet(ip2, port, universe2, packet_size)
    a1.flash_all()  # send single packet with all channels at 255
    a2.flash_all()
    file.write(StupidArtnet.print_object_and_packet(a1))
    file.write(StupidArtnet.print_object_and_packet(a2))
    sync.send()
    a1.show()
    a2.show()
    time.sleep(slp)
    sync.send()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip1 = sys.argv[2]
        ip2 = sys.argv[3]
        universe1 = sys.argv[4]
        universe2 = sys.argv[5]
        try:
            sleep = sys.argv[6]
        except:
            sleep = 5

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}, {universe2}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(universe2), ip1, ip2)
        elif type == "artsync":
            main_artsync(int(universe1), int(universe2), ip1, ip2, sleep)

        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip1, ip2 ,universe_ip1, universe_ip2, time_sleep_for_artSync")

    file.close()
