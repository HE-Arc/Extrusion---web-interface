import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
import time
import datetime

filename = "tests/logs/static/test2.txt"
file = open(filename, "a+")


def main_no_artsync(universe1, universe2, ip='127.0.0.1'):
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(ip, port, universe1, packet_size)
    a2 = StupidArtnet(ip, port, universe2, packet_size)
    a1.flash_all()  # send single packet with all channels at 255
    a2.flash_all()
    file.write(StupidArtnet.print_object_and_packet(a1))
    file.write(StupidArtnet.print_object_and_packet(a2))
    a1.show()
    a2.show()
    # time.sleep(3)  # wait a bit, 1 sec
    # a.stop()


def main_artsync(universe1, universe2, ip='127.0.0.1', slp= 5):
    packet_size = 512
    port = 6454
    sync = StupidArtSync(ip)
    a1 = StupidArtnet(ip, port, universe1, packet_size)
    a2 = StupidArtnet(ip, port, universe2, packet_size)
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
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        universe2 = sys.argv[4]
        try:
            sleep = sys.argv[5]
        except:
            sleep = 5

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}, {universe2}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(universe2), ip)
        elif type == "artsync":
            main_artsync(int(universe1), int(universe2), ip,sleep)

        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, universe, time_sleep_for_artSync")

    file.close()
