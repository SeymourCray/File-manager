from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from folder import Folder
import os


class Dialog_menu(Tk):

    launch_flag = False
    main_path = ''

    def __init__(self, path, delim):

        super().__init__()
        self.title("Вход 👾")
        self.path = path
        self.delim = delim
        self.geometry('300x250')
        self.configure(background="#423189")
        self.text1 = StringVar()
        self.text2 = StringVar()
        Label(self, text="Логин:", font='Times 15', pady=20,
              background="#423189", fg="white").pack(side=TOP)
        self.entry_name = Entry(self, textvariable=self.text1).pack(side=TOP)
        Label(self, text="Пароль:", font='Times 15', pady=20,
              background="#423189", fg="white").pack(side=TOP)
        self.entry_passwd = Entry(self, textvariable=self.text2).pack(side=TOP)
        ttk.Button(self, text="регистрация",
                   command=self.new).pack(side=BOTTOM, fill=X)
        ttk.Button(self, text="войти", command=self.log).pack(
            side=BOTTOM, fill=X)
        self.protocol("WM_DELETE_WINDOW", lambda: exit())

    @staticmethod
    def delete_text(a, b):
        a.set('')
        b.set('')

    @staticmethod
    def exit():
        raise SystemExit

    def registration(name, passwd):
        with open("users.txt", 'a', encoding='utf-8') as a:
            a.write(name+';'+passwd+'\n')

    def login(name, passwd):
        users = Dialog_menu.open_userfile()
        if users:
            for n in users:
                if n[0] == name and n[1] == passwd:
                    return True
            return False
        return False

    def folder_exist(name, path):
        if name in os.listdir(path):
            return True
        return False

    def log(self):
        name = self.text1.get()
        passwd = self.text2.get()
        Dialog_menu.delete_text(self.text1, self.text2)
        n = Dialog_menu.login(name, passwd)
        if n:
            state = Dialog_menu.folder_exist(name, self.path)
            if state:
                pass
            else:
                Folder(name, self.path, len(os.listdir(
                    self.path)), self.delim).createdir()
            Dialog_menu.main_path = self.path + self.delim + name
            Dialog_menu.launch_flag = True
            self.destroy()
        else:
            messagebox.showinfo("Error ✘", "Неверный логин или пароль((")

    def new(self):
        name = self.text1.get()
        passwd = self.text2.get()
        Dialog_menu.delete_text(self.text1, self.text2)
        if len(name) != 0 and len(passwd) != 0:
            users = Dialog_menu.open_userfile()
            if users:
                for n in users:
                    if n[0] == name:
                        messagebox.showinfo(
                            "Error ✘", "Такое имя уже есть((")
                        break
                else:
                    self.a(name, passwd)
            else:
                self.a(name, passwd)

    @staticmethod
    def open_userfile():
        try:
            with open("users.txt", 'r', encoding='utf-8') as a:
                from re import split
                users = [split(r'[;]', i) for i in split(r'\n', a.read())[:-1]]
                return users
        except:
            a = open('users.txt', 'w', encoding='utf-8')
            a.close()
            return False

    def a(self, n, p):
        Dialog_menu.registration(n, p)
        Folder(n, self.path, len(os.listdir(
            self.path)), self.delim).createdir()
        Dialog_menu.main_path = self.path + self.delim + n
        Dialog_menu.launch_flag = True
        self.destroy()
