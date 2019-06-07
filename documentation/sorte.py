import json

with open('cheminee.txt') as data:
    d = []
    for x in data:
        s = x.split('|')
        d.append((s[1], s[2], s[3], s[4]))

print(d)
newlist = sorted(d, key=lambda k: (k[2], k[1]))
print(newlist)
with open('sortedcheminee.txt', 'w') as f:
    for item in newlist:
        f.write(f"|{item[2]}|{item[0]}|{item[1]}|{item[3]}|\n")
