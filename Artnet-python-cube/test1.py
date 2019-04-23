from lib import StupidArtnet, StupidArtSync
import sys
import time
import datetime

filename = "logs/test1.txt"
file = open(filename,"a+")


def main_no_artsync(universe, ip='127.0.0.1'):
    target_ip = ip
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    file.write(f"{str(a)} /n")
    a.flash_all()  # send single packet with all channels at 255
    file.write(f"{str(a.BUFFER)} /n")
    a.show()
    # time.sleep(3)  # wait a bit, 1 sec
    # a.stop()


def main_artsync(universe, ip='127.0.0.1'):
    target_ip = ip
    packet_size = 512
    port = 6454
    sync = StupidArtSync()
    a = StupidArtnet(target_ip, port, universe, packet_size)
    a.flash_all()  # send single packet with all channels at 255
    sync.send()
    a.show()
    time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        universe = sys.argv[3]
        ip = sys.argv[2]

        file.writelines(f"Test type: test 1: {type}\n")
        file.writelines(f"Test starting: {datetime.datetime.now()} \n")

        print(f"Flashing universe: {universe}")
        if type == "noartsync":
            main_no_artsync(int(universe), ip)
        elif type == "artsync":
            main_artsync(int(universe), ip)
    else:
        print("Wrong arguments,arguments: type ,ip, universe")

    file.close()
