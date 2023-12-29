import os
import re
import requests

basedir = 'favourites'
arr = []
counter = 0
for name in os.listdir(basedir):
    pattern = r'(?<=>)https(.*?)album'
    with open("favourites/" + name) as inp:
        data = inp.readlines()
        for line in data:
            match = re.search(pattern, line)
            if match is not None:
                arr.append(match.group(0))
                img_data = requests.get(match.group(0)).content
                with open(f'result/image{counter}.jpg', 'wb') as handler:
                    handler.write(img_data)
                    counter += 1
print('finish')
