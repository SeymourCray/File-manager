import os
import fileinput
import shutil


class File():

    def __init__(self, name, path, index, delim_='/'):
        self.delim = delim_
        self.name = name
        self.path = path
        self.index = index
        self.absolute = path+delim_+name

    # Создание пустых файлов с указанием имени

    def create_new_file(self):
        with open(self.absolute, 'w') as s:
            pass

    # Просмотр содержимого текстового файла

    def show(self):
        text = []
        for i in fileinput.input(self.absolute):
            text.append(i)
        return text

    # Запись в файлы

    def echo(self, text):
        with open(self.absolute, 'w') as s:
            s.write(text)

    # Удаление файлов по имени

    def rmfile(self):
        os.remove(self.absolute)

    # Перемещение файлов

    def replace_file(self, to):
        shutil.copy(self.absolute, to)
        os.remove(self.absolute)

    # Переименовать файл

    def new_name(self, new):
        os.rename(self.absolute, self.path+self.delim+new)
        self.name = new
        self.absolute = self.path+self.delim+new

    # Копировать файл

    def copy_o(self, to):
        shutil.copy(self.absolute, to)


