import os
import re
import requests

basedir = 'favourites'
a = []
c=0
for name in os.listdir(basedir):
    pattern = r'(?<=>)https(.*?)album'
    with open("favourites/" + name) as inp:
      data = inp.readlines()
      for i in data:
        match = re.search(pattern, i)
        if match is not None:
            a.append(match.group(0))
            img_data = requests.get(match.group(0)).content
            with open(f'image{c}.jpg', 'wb') as handler:
                handler.write(img_data)
                c+=1
