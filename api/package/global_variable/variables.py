from package.artnet.ArtNetGroup import ArtNetGroup
from package.cube.cube import Cube

artnet_group = ArtNetGroup.get_artnet()

cube = Cube(artnet_group)
launcher_pool = {}
size_packet = 512

access = True
state = "free"
mode = "master"
