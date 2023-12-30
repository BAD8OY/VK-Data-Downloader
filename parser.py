from glob import glob
import os
import httplib2
import re


def find_dialogue_name(string):
    pattern = r'(?<=div><div class="ui_crumb" >)(.*?)(?=<\/div><\/div>)'
    try:
        match = re.search(pattern, string)
        res = match.group(0)
        ban_list = "\/:*?<>||"
        for i in ban_list:
            res = res.replace(i, " ")  # разрешение создания названия файла
        return res
    except Exception as e:
        match = e
        return match


def define_file_type(string):
    qm_index = string.find("?")
    if "?" not in string:
        qm_index = len(string)
    return string[qm_index - 3:qm_index]  # TODO: сделать не только расширения длиной 3 символа


def parse_author_and_date(string):
    pattern = r'<.*?>'
    try:
        buf = re.sub(pattern, '', string)
        buf = buf.lstrip()
        buf = buf.rstrip()  # очистка от лишних символов
        ban_list = "\/:*?<>|"
        for i in ban_list:
            buf = buf.replace(i, " ")  # разрешение создания названия файла
        buf_list = [buf[:buf.find(",")], buf[buf.find(",") + 2:]]  # отделение автора сообщения и даты/времени
        if buf_list[1] == "":
            buf_list[1] = "default"
        return buf_list
    except Exception as e:
        return [e, e]


def create_file(link, filetype, dialogue_name, author_and_date):
    try:
        if not os.path.exists(f'result\\{dialogue_name}\\{filetype}'):  # создание папки с типом файла
            os.mkdir(f'result\\{dialogue_name}\\{filetype}')
        if not os.path.exists(
                f'result\\{dialogue_name}\\{filetype}\\{author_and_date[0]}'):  # создание папки с автором сообщения
            os.mkdir(f'result\\{dialogue_name}\\{filetype}\\{author_and_date[0]}')
        h = httplib2.Http('.cache')  # кэширование
        response, content = h.request(link)  # запрос
        out = open(f'result\\{dialogue_name}\\{filetype}\\{author_and_date[0]}\\{author_and_date[1]}.{filetype}',
                   'wb')  # создание файла в папку
        out.write(content)
        out.close()
    except Exception:
        with open("log.txt", "w") as f:
            f.write(
                f'Link: {link} | Filetype: {filetype} | Dialogue_name: {dialogue_name} | '
                f'Author and date: {author_and_date[0] + author_and_date[1]} | k = {progress}' + "\n\n")


def file_analysis(fullname):
    # открытие файла
    with open(fullname, 'r') as file:
        strings = file.readlines()  # чтение файла
        dialogue_name = "default_name"
        for string in strings:
            if string.__contains__(
                    "message__header"):  # если в строке есть класс message__header,
                # то это строка с временем и автором сообщения
                author_and_date = parse_author_and_date(string)  # получение времени и автора сообщения
            if string.__contains__("Сообщения"):  # если в строке есть "Сообщения", то оно содержит название диалога
                dialogue_name = find_dialogue_name(string)  # получение названия диалога
                if not os.path.exists(os.getcwd() + f'\\result\\{dialogue_name}'):
                    os.mkdir(os.getcwd() + f'\\result\\{dialogue_name}')  # создание папки с названием диалога

            if string.__contains__("userapi.com"):  # нахождение строки со ссылкой
                link = string[string.find(
                    "href='") + 6:(string[string.find("href='") + 6::]).find("\'") + string.find(
                    "href='") + 6:]  # вычленение ссылки
                filetype = define_file_type(link)  # получение типа файла
                create_file(link, filetype, dialogue_name, author_and_date)  # функция создания файла


progress = 0
# рекурсивный сбор файлов, имеющих расширение .html
files = glob(os.getcwd() + '/**/*.html', recursive=True)
count = len(files)
# создание папки результата
if not os.path.exists(os.getcwd() + '\\result'):
    os.mkdir('result')
# пробег по всем файлам
for name in files:
    progress += 1
    fullname = os.path.join(os.getcwd(), name)
    print("Анализ файла № " + str(progress) + "из " + str(count))
    file_analysis(fullname)
