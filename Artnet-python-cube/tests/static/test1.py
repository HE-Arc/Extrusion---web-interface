import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
import time
import datetime

filename = "tests/logs/static/test1.txt"
file = open(filename, "a")


def main_no_artsync(universe, ip='127.0.0.1'):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    a.flash_all()  # send single packet with all channels at 255
    file.write(StupidArtnet.print_object_and_packet(a))
    a.show()
    # time.sleep(3)  # wait a bit, 1 sec
    # a.stop()


def main_artsync(universe, ip='127.0.0.1', slp=5):
    target_ip = ip
    packet_size = 512
    port = 6454
    sync = StupidArtSync(ip)
    a = StupidArtnet(target_ip, port, universe, packet_size)
    a.flash_all()  # send single packet with all channels at 255
    file.write(StupidArtnet.print_object_and_packet(a))
    sync.send()
    a.show()
    sync.send()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        try:
            sleep = sys.argv[4]
        except:
            sleep = 5

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), ip)
        elif type == "artsync":
            main_artsync(int(universe1), ip, float(sleep))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, time_sleep_for_artSync")

    file.close()
