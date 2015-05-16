#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tkinter     ## Python 2.x
else:
    import tkinter as Tkinter     ## Python 3.x

class Values(Tkinter.Tk):
    """docstring for Values"""
    def __init__(self, parent, fst_value_str, snd_value_str):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize(fst_value_str, snd_value_str)

    def initialize(self, fst_value_str, snd_value_str):
        self.grid()
        stepOne = Tkinter.LabelFrame(self, text=" Заполните указанные поля: ")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Tkinter.Label(stepOne,text=fst_value_str)
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Tkinter.Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val2Lbl = Tkinter.Label(stepOne,text=snd_value_str)
        self.Val2Lbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.Val2Txt = Tkinter.Entry(stepOne)
        self.Val2Txt.grid(row=1, column=1, columnspan=3, pady=2, sticky='WE')

        self.val1 = None
        self.val2 = None

        SubmitBtn = Tkinter.Button(stepOne, text="Подтвердить",command=self.submit)
        SubmitBtn.grid(row=4, column=3, sticky='W', padx=5, pady=2)

    def submit(self):
        self.val1=self.Val1Txt.get()
        if self.val1=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.val2=self.Val2Txt.get()
        if self.val2=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.quit()

if __name__ == '__main__':
    app = Values(None, 'Логин', 'Пароль')
    app.title('Values')
    print app.val1,app.val2