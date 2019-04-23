from lib import StupidArtnet, StupidArtSync
import sys
import time


# target_ip = '127.0.0.1'

# target_ip = '192.168.0.50'	 # typically in 2.x or 10.x range
# universe = 0 					# see docs
# it is not necessary to send whole universe


def main(universe, blackout):
    target_ip = '2.16.18.12'
    packet_size = 512
    port = 6454
    a = StupidArtnet(target_ip, port, universe, packet_size)
    b = StupidArtSync(target_ip, port)
    a.flash_all()  # send single packet with all channels at 255
    a.start()
    time.sleep(5)  # wait a bit, 1 sec
    a.stop()
    if blackout:
        a.blackout()

    # time.sleep(3)  # wait a bit, 1 sec
    #a.stop()
    return
    # a.flash_all()
    packet = bytearray(packet_size)
    for i in range(packet_size):  # fill packet with sequential values
        packet[i] = 255
    a.set(packet)
    count = 0
    while True:
        print(f"flash {count}")
        count += 1
        a.show()
        time.sleep(1)
        a.blackout()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        universe = sys.argv[1]
        blackout = sys.argv[2]
        print(f"Flashing universe: {universe}")
        main(int(universe), bool(blackout))
    else:
        print("Wrong argument")
