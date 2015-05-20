#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import  *

class goods_list:
    __g_list = dict()

    def __init__(self, current_list):
        self.__g_list = dict(current_list)

    def __getitem__(self, ind):
        res = None
        if self.__g_list.has_key(ind):
            res = self.__g_list[ind]
        return res

    def get_all(self):
        g_list = [(k, v) for k, v in self.__g_list.iteritems()]
        g_list.sort(key=lambda tup: tup[0])
        return g_list

    def add(self, (id, name)):
        if not self.__g_list.has_key(id):
            self.__g_list[id] = name

class goods_table():

    @staticmethod
    def show_table(g_list):
        master = Tk()
        master.resizable(width = False, height = False)
        master.title('Cписок товаров')
        listbox = Listbox(master)
        listbox.pack()
        for (k, v) in g_list.get_all():
            #f_string = ""
            listbox.insert(END, str(k) + ". " + str(v))

        mainloop()

if __name__ == '__main__':
    g = goods_list([])
    print(g.get_all())
    g.add((1, 'Notebook Asus'))
    g.add((2, 'Smartphone LG'))

    print(g[1])
    print(g[2])
    print(g[3])

    print(g.get_all())