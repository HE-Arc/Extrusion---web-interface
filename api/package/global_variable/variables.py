from package.artnet.ArtNetGroup import ArtNetGroup
from package.cube.cube import Cube

ip1 = "192.168.1.142"

ip2 = "192.168.1.142"

artnet_group = ArtNetGroup.get_artnet(ip1, ip2)

cube = Cube(artnet_group)
launcher_pool = []
launcher_access = {}
size_packet = 512

state = "free"
mode = "user"
