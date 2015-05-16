#!/usr/bin/python
# -*- coding: utf-8 -*-

from modal_window import Values

class database_authorization:
    def get_logpass_data(self):
        app = Values(None, 'Логин', 'Пароль')
        app.title('Подключение к БД')
        app.mainloop()
        login, password = app.val1, app.val2
        app.destroy()
        return login, password

class workplace_authorization:
    @staticmethod
    def get_workpace_data():
        app = Values(None, 'ID кассира', 'ID склада')
        app.title('Открытие кассы')
        app.mainloop()
        cashier_id, warehouse_id = app.val1, app.val2
        app.destroy()
        return cashier_id, warehouse_id


if __name__ == '__main__':
    print database_authorization.get_logpass_data()
#    print workplace_authorization.get_workpace_data()
