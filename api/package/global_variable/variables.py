from package.artnet.ArtNetGroup import ArtNetGroup
from package.cube.cube import Cube
from package.global_variable.data_cube import address_xyz

ip1 = "192.168.1.142"

ip2 = "192.168.1.142"

artnet_group = ArtNetGroup.get_artnet(ip1, ip2)

cube = Cube(artnet_group, address_xyz)
launcher_pool = []
launcher_access = {}
size_packet = 512
started = False
state = "free"
mode = "user"
