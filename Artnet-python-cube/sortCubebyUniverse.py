import json

with open('lib/Cube2.json') as json_data:
    d = json.load(json_data)

# print(d)
#print(d['Items'][0]['universe'])

newlist = sorted(d['Items'], key=lambda k: (k['universe'], k['channel']))
print(newlist)
with open('sortedCube.txt', 'w') as f:
    for item in newlist:
        f.write("%s\n" % item)
