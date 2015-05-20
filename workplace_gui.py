#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


if sys.version_info[0] < 3:
    import Tkinter as Tkinter     ## Python 2.x
else:
    import tkinter as Tkinter     ## Python 3.x

import tkMessageBox

from Tkinter import *
from cashier_workplace import *
from modal_window      import database_authorization, workplace_authorization, record_getter
from goods_list        import *
from checks_keeper     import *

class workplace_gui(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self, None)
        self.parent = None
        self.__goods_list = goods_list([]) #TODO Организовать подгрузку товара
        self.initialize()
        self.crnt_check = checks_keeper()

    def initialize(self):
        # Инициализация формы
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid()
        self.title('Рабочее место кассира')
        self.resizable(width = False, height = False)
        self.check_frame = Tkinter.LabelFrame(self, text = "Информация о чеке")
        self.check_frame.grid(row=0, column=0, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.checks_listbox = Listbox(self.check_frame)
        self.checks_listbox.pack()
        self.create_new_check_btn = Button(self.check_frame, text = "Новый чек",
                                           state = DISABLED, command = self.set_new_check)
        self.execute_check_btn    = Button(self.check_frame, text = "Утвердить",
                                           state = DISABLED, command = self.execute_check)
        self.create_new_check_btn.pack(side = LEFT)
        self.execute_check_btn.pack   (side = LEFT)
        self.add_new_record_btn = Button(self.check_frame, text = "+",
                                         height = 1, width = 1, state = DISABLED, command = self.add_new_record)
        self.remove_last_btn    = Button(self.check_frame, text = "-",
                                         height = 1, width = 1, state = DISABLED, command = self.del_record)
        self.add_new_record_btn.pack()
        self.remove_last_btn.pack()
        self.check_frame_1 = Tkinter.LabelFrame(self, text = "Управлений кассой")
        self.check_frame_1.grid(row=0, column=1, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.goods_frame = Tkinter.LabelFrame(self.check_frame_1, text = "Товары")
        self.goods_frame.pack()
        self.update_goods_info_btn = Button(self.goods_frame, text = "Обновить данные",  state = DISABLED,
                                            command = self.update_goods_info)
        self.get_goods_table_btn   = Button(self.goods_frame, text = "Показать таблицу", state = DISABLED,
                                            command = self.show_goods_table)
        self.update_goods_info_btn.pack()
        self.get_goods_table_btn.pack()
        self.cashier_frame = Tkinter.LabelFrame(self.check_frame_1, text = "Кассир")
        self.cashier_frame.pack()
        self.auth_cashier_btn    = Button(self.cashier_frame, text = "Авторизация", command = self.make_authorization)
        self.compute_bonus_btn   = Button(self.cashier_frame, text = "Бонусная часть", state = DISABLED)
        self.dismiss_cashier_btn = Button(self.cashier_frame, text = "Уволить",
                                          command = self.dismiss_cashier, state = DISABLED)
        self.auth_cashier_btn.pack()
        self.compute_bonus_btn.pack()
        self.dismiss_cashier_btn.pack()
        self.cashier_frame = Tkinter.LabelFrame(self.check_frame_1, text = "Касса")
        self.cashier_frame.pack()
        self.change_cash_status_btn = Button(self.cashier_frame,
                                             text = "Открыть кассу", command = self.open_cash, state = DISABLED)
        self.change_cash_status_btn.pack()
        self.cashier_wp = cashier_workplace

    def close_cash(self):
        self.auth_cashier_btn['state']         = 'normal'
        self.create_new_check_btn['state']     = 'disabled'
        self.execute_check_btn['state']        = 'disabled'
        self.add_new_record_btn['state']       = 'disabled'
        self.remove_last_btn['state']          = 'disabled'
        self.change_cash_status_btn['text']    = 'Открыть кассу'
        self.change_cash_status_btn['command'] = self.open_cash
        cashier_workplace.close_cash()

    def make_logout(self):
        cashier_workplace.logout()
        self.auth_cashier_btn['text'] = "Авторизация"
        self.auth_cashier_btn['command'] = self.make_authorization
        self.compute_bonus_btn['state']      = 'disabled'
        self.dismiss_cashier_btn['state']    = 'disabled'
        self.get_goods_table_btn['state']    = 'disabled'
        self.update_goods_info_btn['state']  = 'disabled'
        self.change_cash_status_btn['state'] = 'disabled'

    def make_authorization(self):
        cashier_id, warehouse_id = workplace_authorization.get_workpace_data()
        #print cashier_id, warehouse_id
        success = True

        error_message = ""

        if None == cashier_id or None == warehouse_id or \
            "" == cashier_id or "" == warehouse_id:
            error_message = "Все указанные поля должны быть заполнены"
            success = False

        if success:
            try:
                res = cashier_workplace.authorization(cashier_id, warehouse_id)
            except Exception:
                res = False
                error_message = "Неверно заполнены поля авторизации"
            success = success and res
            if not res:
                error_message = "Вы не обладаете полномочиями для авторизации. " \
                                "Проверьте вводимые значение. А возможно, вы уже уволены"

        if success:

            self.auth_cashier_btn['command']     = self.make_logout
            self.auth_cashier_btn['text']        = "Деавторизация"
            self.compute_bonus_btn['state']      = 'normal'
            self.dismiss_cashier_btn['state']    = 'normal'
            self.get_goods_table_btn['state']    = 'normal'
            self.update_goods_info_btn['state']  = 'normal'
            self.change_cash_status_btn['state'] = 'normal'
        else:
            tkMessageBox.showerror("Ошибка авторизации", error_message)
        self.mainloop()

    def dismiss_cashier(self):
        print "ЗА ЧТО?!"

    def show_goods_table(self):
        goods_table.show_table(self.__goods_list)

    def set_new_check(self):
        self.crnt_check = checks_keeper()
        if self.checks_listbox.size() > 0:
            self.checks_listbox.delete(0, END)
        self.execute_check_btn['state']        = 'normal'
        self.add_new_record_btn['state']       = 'normal'
        self.remove_last_btn['state']          = 'normal'

    def on_closing(self):
        if database_connection.is_connection():
            database_connection.close()
        if cashier_workplace.is_opened():
            cashier_workplace.close_cash()
        self.destroy()

    def get_cashier_bonus(self):
        res = cashier_workplace.get_bonus_for_cashier()

    def open_cash(self):
        cashier_workplace.open_cash()
        self.auth_cashier_btn['state']         = 'disabled'
        self.create_new_check_btn['state']     = 'normal'
        self.change_cash_status_btn['text']    = 'Закрыть кассу'
        self.change_cash_status_btn['command'] = self.close_cash

    def add_new_record(self):
        goods_id, goods_cnt = record_getter.get_record_data()
        success = True
        try:
            goods_id  = int(goods_id)
            goods_cnt = int(goods_cnt)

        except Exception:
            tkMessageBox.showerror("Ошибка ввода", "Неверный формат для введенных данных")
            return

        if None == self.__goods_list[goods_id]:
            self.update_goods_info()

        if None == self.__goods_list[goods_id]:
            tkMessageBox.showerror("Ошибка записи", "Товар с таким id не был найден в базе")
            success = False

        if success:
            self.crnt_check.add_record(goods_id, goods_cnt)
            if self.checks_listbox.size() > 0:
                self.checks_listbox.delete(0, END)
            for (id, count) in self.crnt_check.get_all_records():
                self.checks_listbox.insert(END, checks_keeper.get_str_view(None, id, count))

    def execute_check(self):
        #TODO: call the procedure
        self.remove_last_btn['state']    = 'disabled'
        self.execute_check_btn['state']  = 'disabled'
        self.add_new_record_btn['state'] = 'disabled'
        if self.checks_listbox.size() == 0:
            return

        res = cashier_workplace.make_purchase(self.crnt_check.get_all_records())
        print(res) #TODO: обработать чек и вывести его (каким то образом)

        self.checks_listbox.delete(0, END)

    def del_record(self):
        print "delete_record"

    def update_goods_info(self):
        records = database_connection.get_data_from_table('GOODS', ['GOODS_ID', 'NOMENCLATURE'])
        for record in records:
            self.__goods_list.add(record)

if __name__ == '__main__':
    success = True
    # db_auth = database_authorization()
    # login, password = db_auth.get_logpass_data()
    login, password = "IT38", "it38"
    try:
        database_connection.connect(login, password)
    except Exception:
        success = False

    if success:
        app = workplace_gui()
        app.mainloop()
    else:
        tkMessageBox.showerror("Ошибка подключения",
            "Подключение к базе данных невозможно. Проверьте интернет соединение, логин и пароль")