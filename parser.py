from glob import glob
import os
from time import sleep
import httplib2
import re
import uuid


def find_dialogue_name(string):
    #print(string)
    match = ...
    pattern = r'(?<=div><div class="ui_crumb" >)(.*?)(?=<\/div><\/div>)'
    try:
        match = re.search(pattern, string)
        return match.group(0)
    except Exception as e:
        match = e
        return match
        

def define_file_type(string):
    qm_index = string.find("?")
    if "?" not in string:
        qm_index = len(string)
    return string[qm_index-3:qm_index]

def working_with_file(fullname):
        with open(fullname, 'r') as file:
            while True:
                string = file.readline()

                if string.__contains__("Сообщения"):
                    name_of_message = find_dialogue_name(string)
                
                if string.__contains__("userapi.com"):
                     working_with_image_link(string, name_of_message)
                if string == "":
                    break


def working_with_image_link(string, name_of_message):
                    k = 0
                    #вычленение из строки html-кода чистой ссылки на скачивание
                    buf = string[string.find("href='")+6:(string[string.find("href='")+6::]).find("\'")+string.find("href='")+6:]
                    list_of_files.append(buf)    
                   

                   #начало скачивания
                    h = httplib2.Http('.cache')
                    response, content = h.request(buf)
                    
                    image_type = define_file_type(buf)

                    out = ...
                    if os.path.exists(f'result\\{name_of_message}') == False:
                        os.mkdir(f'result\\{name_of_message}')
                    if os.path.exists(f'result\\{name_of_message}\\{image_type}') == False:
                        os.mkdir(f'result\\{name_of_message}\\{image_type}')
                    while os.path.exists(f'result\\{name_of_message}\\{image_type}\\{k}.{image_type}'):
                        k = k + 1
                    out = open(f'result\\{name_of_message}\\{image_type}\\{k}.{image_type}', 'wb')
                    out.write(content)
                    out.close()
                



names = os.listdir(os.getcwd())
#print(names)
list_of_files = []
list_of_names = []

files = glob(os.getcwd() + '/**/*.html', recursive=True)
#print(files)
for name in files:
    fullname = os.path.join(os.getcwd(), name)
    if os.path.isfile(fullname) and ".html" in fullname:
        match = ...
        name_of_message = ...
        working_with_file(fullname)
