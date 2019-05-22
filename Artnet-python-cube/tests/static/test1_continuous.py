import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
import time
import datetime

filename = "tests/logs/static/test1_continuous.txt"
file = open(filename, "a")


def main_no_artsync(universe, ip='127.0.0.1', tmp=5):
    packet_size = 512
    port = 6454
    a = StupidArtnet(ip, port, universe, packet_size)
    a.flash_all()  # send single packet with all channels at 255
    file.write(StupidArtnet.print_object_and_packet(a))
    a.start()
    time.sleep(tmp)
    a.stop()


def main_artsync(universe, ip='127.0.0.1', nb_packet=50, tmp=5):
    packet_size = 512
    port = 6454
    a = StupidArtnet(ip, port, universe, packet_size)
    a.flash_all()  # send single packet with all channels at 255
    file.write(StupidArtnet.print_object_and_packet(a))
    a.start_artSync(nb_packet)
    time.sleep(tmp)
    a.stop_artSync()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip = sys.argv[2]
        universe1 = sys.argv[3]
        pause_time = sys.argv[4]
        try:
            nb_packets = sys.argv[5]
        except:
            nb_packets = 50

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Flashing universe: {universe1}")
        if type == "noartsync":
            main_no_artsync(int(universe1), ip, float(pause_time))
        elif type == "artsync":
            main_artsync(int(universe1), ip, int(nb_packets), float(pause_time))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type ,ip, universe, time, nb_packet_for_artsync")

    file.close()
