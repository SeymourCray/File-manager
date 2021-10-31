from tkinter import *
import re
import os
from functools import partial
from file import File
from folder import Folder
from menu import Dialog_menu


try:
    with open('settings.txt', 'r') as s:
        global main_path
        main_path = s.read()
        delim = re.search(r'[\\/]', main_path).group(0)
except:
    print("Отсутствует файл с настройками!")
    raise SystemExit


a = Dialog_menu(main_path, delim)
a.mainloop()

while not Dialog_menu.launch_flag:
    pass

main_path = Dialog_menu.main_path

paths = {main_path: []}


current_path = ''
root = Tk()
box = Listbox(width=30, height=20, selectmode=EXTENDED)
box.pack(side=LEFT)
scroll = Scrollbar(command=box.yview)
scroll.pack(side=LEFT, fill=Y)
box.config(yscrollcommand=scroll.set)
title = root.title('Файловый менеджер')

f = Frame()
f.pack(padx=30, pady=20)
entry = Entry(f)
entry.pack(side=TOP, fill=X)


def update_index(path):
    for i, item in enumerate(paths[path]):
        item.index = i


def sync():
    try:
        folder = paths[main_path+current_path]
    except KeyError:
        paths[main_path+current_path] = []
        folder = paths[main_path+current_path]
    folder_sys = os.listdir(main_path+current_path)
    if len(folder) < len(folder_sys):
        for i in folder_sys:
            exist = False
            for j in folder:
                if i == j.name:
                    exist = True
                    break
            if exist == False:
                if os.path.isdir(main_path+current_path + delim + i):
                    paths[main_path+current_path].append(
                        Folder(i, main_path+current_path, box.size(), delim))
                    paths[main_path+current_path+delim+i] = []
                elif os.path.isfile(main_path+current_path + delim + i):
                    paths[main_path+current_path].append(
                        File(i, main_path+current_path, box.size(), delim))
    elif len(folder) > len(folder_sys):
        while len(folder) != len(folder_sys):
            for i in folder:
                exist = False
                for j in folder_sys:
                    if i.name == j:
                        exist = True
                        break
                if exist == False:
                    paths[main_path+current_path].pop(i.index)
                    update_index(main_path+current_path)


def fill_box():
    folder = paths[main_path+current_path]
    for item in folder:
        box.insert(END, item.name)


def add_file():
    name = entry.get()
    if name == '':
        return 0
    for item in paths[main_path+current_path]:
        if item.name == name:
            return 0
    a = File(name, main_path + current_path, box.size(), delim)
    a.create_new_file()
    box.insert(END, name)
    entry.delete(0, END)
    for folder in paths.keys():
        if a.path == folder:
            paths[folder].append(a)


def add_folder():
    name = entry.get()
    if name == '':
        return 0
    for item in paths[main_path+current_path]:
        if item.name == name:
            return 0
    a = Folder(name, main_path + current_path, box.size(), delim)
    a.createdir()
    box.insert(END, name)
    entry.delete(0, END)
    for folder in paths:
        if a.path == folder:
            paths[folder].append(a)
    paths[a.absolute] = []


def delete_item():
    select = list(box.curselection())
    select.reverse()
    for i in select:
        box.delete(i)
        if type(paths[main_path+current_path][i]) == File:
            paths[main_path+current_path][i].rmfile()
        elif type(paths[main_path+current_path][i]) == Folder:
            paths[main_path+current_path][i].rm()
        paths[main_path+current_path].pop(i)
        paths[main_path+current_path].insert(i, None)
    paths[main_path+current_path] = [i for i in paths[main_path+current_path] if i]
    update_index(main_path+current_path)


def back():
    global current_path
    if current_path == '':
        return 0
    current_path = re.findall(r'[^\\/]+', current_path)
    current_path.pop(-1)
    if len(current_path) < 1:
        current_path = ''
    else:
        current_path = delim + f'{delim}'.join(current_path)
    box.delete(0, box.size()-1)
    sync()
    fill_box()
    update_label(lbl)


def open_item():
    global current_path
    select = list(box.curselection())
    if len(select) != 1:
        pass
    else:
        item = paths[main_path+current_path][select[0]]
        if type(item) == Folder:
            current_path += delim + item.name
            box.delete(0, box.size()-1)
            sync()
            fill_box()
            update_label(lbl)
        elif type(item) == File:
            window = Tk()
            tit = window.title('Редактор')
            global text
            text = Text(window)
            text.pack(side=TOP)
            Button(window, text="Cохранить", command=partial(
                save, item, window)).pack(fill=X)
            Button(window, text="Закрыть", command=partial(
                close, window)).pack(fill=X)
            text.insert(INSERT, ''.join(item.show()))
            window.mainloop()


def save(obj, win):
    new_text = text.get(1.0, END)
    obj.echo(new_text)
    win.destroy()


def close(win):
    win.destroy()


def quit_():
    raise SystemExit


def update_label(label):
    label.config(text=delim if current_path == '' else current_path)


def rename():
    name = entry.get()
    entry.delete(0, END)
    if name == '':
        return 0
    global current_path
    select = list(box.curselection())
    if len(select) != 1:
        pass
    else:
        try:
            item = paths[main_path+current_path][select[0]]
            item.new_name(name)
            box.delete(0, box.size()-1)
            fill_box()
        except:
            pass


def copy_():
    select = list(box.curselection())
    new_path = entry.get()
    entry.delete(0, END)
    if new_path == '':
        return 0
    if new_path == delim:
        new_path = ''
    if len(select) != 1:
        pass
    else:
        item = paths[main_path+current_path][select[0]]
        if main_path+new_path == item.absolute:
            pass
        else:
            try:
                item.copy_o(main_path+new_path)
            except:
                pass


def move_():
    select = list(box.curselection())
    new_path = entry.get()
    entry.delete(0, END)
    if new_path == '':
        return 0
    if new_path == delim:
        new_path = ''
    if len(select) != 1:
        pass
    else:
        item = paths[main_path+current_path][select[0]]
        if main_path+new_path == item.absolute:
            pass
        else:
            try:
                if type(item) == File:
                    item.replace_file(main_path+new_path)
                elif type(item) == Folder:
                    item.copy_o(main_path+new_path)
                    item.rm()
            except:
                pass
            sync()
            box.delete(0, box.size()-1)
            fill_box()


def update_window():
    sync()
    box.delete(0, END)
    fill_box()


fill_box()
lbl = Label(f, text=delim, font=(16), bg="#423189",
            fg="white", bd=2)
lbl.pack(side=TOP)
Button(f, text="Обновить", command=update_window).pack(side=TOP)
Button(f, text="Новый файл", command=add_file).pack(fill=X)
Button(f, text="Новая папка", command=add_folder).pack(fill=X)
Button(f, text="Открыть", command=open_item).pack(fill=X)
Button(f, text="Назад", command=back).pack(fill=X)
Button(f, text="Переименовать", command=rename).pack(fill=X)
Button(f, text="Копировать", command=copy_).pack(fill=X)
Button(f, text="Переместить", command=move_).pack(fill=X)
Button(f, text="Удалить", command=delete_item).pack(fill=X)
Button(f, text="Завершить работу", command=quit_).pack(fill=X, side=BOTTOM)

root.mainloop()
