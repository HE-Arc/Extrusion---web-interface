from package.artnet.ArtNetGroup import ArtNetGroup
from package.cube.cube import Cube
from package.global_variable.data_cube import address_xyz
from package.sequence.queue_manager import QueueManger

ip1 = "192.168.0.51"
port1 = 6454
start_cube1 = 0
end_cube1 = 24
ip2 = "192.168.0.50"
port2 = 6454
start_cube2 = 24
end_cube2 = 46
fps = 44
artnet_group = ArtNetGroup.get_artnet(ip1, port1, ip2, port2, start_cube1, end_cube1, start_cube2, end_cube2, fps)
queue_size = 100
cube = Cube(artnet_group, address_xyz)
size_packet = 512
queue_manager = QueueManger(queue_size)
tokens = {}
