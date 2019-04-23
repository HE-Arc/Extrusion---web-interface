import array
from ola.ClientWrapper import ClientWrapper

channel1 = 127 #sys.argv[1]
channel2 = 127 #sys.argv[2]
channel3 = 127 #sys.argv[3]
final_universe = 48

def DmxSent(state):
  wrapper.Stop()

wrapper = ClientWrapper()
client = wrapper.Client()

for universe in range(final_universe):
    data = array.array('B', [channel1, channel2, channel3] * 170)

    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()