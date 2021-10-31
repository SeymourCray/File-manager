import os
from shutil import rmtree, copytree

'''
Перемещение между папками(в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх
'''


class Folder():

    def __init__(self, name, path, index, delim_='/'):
        self.delim = delim_
        self.name = name
        self.path = path
        self.index = index
        self.absolute = path+delim_+name

    # Создание папки(с указанием имени)

    def createdir(self):
        os.mkdir(self.absolute)

    # Удаление папки по имени

    def rm(self):
        rmtree(self.absolute)

    def new_name(self, new):
        os.rename(self.absolute, self.path+self.delim+new)
        self.name = new
        self.absolute = self.path+self.delim+new

    def copy_o(self, to):
        copytree(self.absolute, to + self.delim + self.name)


