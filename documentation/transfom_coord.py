import json

with open('cheminee.txt') as data:
    d = []
    for x in data:
        s = x.split('|')
        d.append((s[1], s[2], s[3], s[4]))


with open('for_api_cheminee.txt', 'w') as f:
    tab = "["
    f.write("")
    for item in d:
        f.write(f"|{item[2]}|{item[0]}|{item[1]}|{item[3]}|\n")
