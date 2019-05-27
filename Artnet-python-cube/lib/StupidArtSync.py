"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf
		http://art-net.org.uk/wordpress/structure/streaming-packets/artdmx-packet-definition/

NOTES
- For simplicity: NET and SUBNET not used by default but optional

"""

import socket
import sys


class StupidArtSync():
    """(Very) simple implementation of ArtnetSync."""

    def __init__(self, targetIP='127.0.0.1', port=6454):
        """Class Initialization."""
        # Instance variables
        self.TARGET_IP = self.get_broadcast_address(targetIP)
        self.UDP_PORT = port
        self.HEADER = bytearray()
        # UDP SOCKET
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.make_header()

    def __str__(self):
        """Printable object state."""
        s = "===================================\n"
        s += "Stupid Artnet initialized\n"
        s += "Target IP: %s:%i \n" % (self.TARGET_IP, self.UDP_PORT)
        s += "==================================="

        return s

    def make_header(self):
        """Make packet header."""
        # 0 - id (7 x bytes + Null)
        self.HEADER = bytearray()
        self.HEADER.extend(bytearray('Art-Net', 'utf8'))
        self.HEADER.append(0x0)
        # 8 - opcode (2 x 8 low byte first)
        self.HEADER.append(0x00)
        self.HEADER.append(0x52)  # ArtSync data packet
        # 10 - prototocol version (2 x 8 high byte first)
        self.HEADER.append(0x0)
        self.HEADER.append(14)
        # 12 - Aux1 1 byte t 0
        self.HEADER.append(0x0)
        # 13 - Aux2 1 byte t 0
        self.HEADER.append(0x0)

    def send(self):
        """Finally send data."""
        packet = bytearray()
        packet.extend(self.HEADER)
        try:
            self.s.sendto(packet, (self.TARGET_IP, self.UDP_PORT))
        except Exception as e:
            print("ERROR: Socket error with exception: %s" % e)

    @staticmethod
    def get_broadcast_address(ip):
        if ip == '127.0.0.1':
            return '127.0.0.1'
        broadcast_ip = ".".join(ip.split('.')[0:-1]) + '.'
        return broadcast_ip + '255'


if __name__ == '__main__':
    print("===================================")
    print("Namespace run")
    target_ip = sys.argv[1]  # typically in 2.x or 10.x range

    a = StupidArtSync(target_ip)

    print("Sending ArtSync")
    a.send()

    print(a.HEADER)
