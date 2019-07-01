from package.artnet.ArtNetGroup import ArtNetGroup
from package.cube.cube import Cube
from package.global_variable.data_cube import address_xyz
import queue
from package.sequence.queue_manager import QueueManger

ip1 = "192.168.1.142"

ip2 = "192.168.1.142"
fps = 30
artnet_group = ArtNetGroup.get_artnet(ip1, ip2, 0, 24, 24, 46, fps)
queue_size = 100
cube = Cube(artnet_group, address_xyz)
size_packet = 512
queue_manager = QueueManger(queue_size)
tokens = {}
