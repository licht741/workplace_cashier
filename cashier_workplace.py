#!/usr/bin/python
# -*- coding: utf-8 -*-

from cashier_info import cashier_info
from database_connection import database_connection
import datetime

class invalid_environments_exception(Exception):
    pass


class cashier_workplace:
    __is_working = False

    # Функции управления персоналом (кассирами)
    # Авторизация происходит на сервере БД. Пройти авторизацию может только сотрудник, являющийся кассиром
    # и не уволенный на текущий момент. Авторизация должна быть произведена на указанном розничном складе.
    # На момент авторизации: касса должна быть закрыта, установлено соединение с сервером, не должно быть
    # авторизированных в текущем приложении кассиров.
    # Выход из системы должен осуществляться только при наличии авторизированного кассира и закрытой кассе.

    @staticmethod
    def authorization(cashier_id, warehouse_id):
        # TODO: Checking status
        assert database_connection.is_connection() and not cashier_workplace.is_opened() \
               and not cashier_info.is_busy()
        [(auth_id_cs, cashier_name)]           = database_connection.execute_action('AUTH_CASHIER', cashier_id)
        [(auth_id_wh, warehouse_name, wh_loc)] = database_connection.execute_action('AUTH_WAREHOUSE', warehouse_id)
        cashier_info.new_cashier(cashier_name,cashier_id, warehouse_name, warehouse_id)
        if auth_id_cs == 1 or auth_id_wh == 1:
            return False #TODO: Output some message
        return True

    @staticmethod
    def logout():
        assert cashier_info.is_busy() and not cashier_workplace.is_opened()
        cashier_info.destroy_cashier()
        return True

    # Функции управления кассой.
    # При закрытой кассе операции на ней невозможны
    # Открытие кассы возможно только при наличии авторизированного кассира

    @staticmethod
    def is_opened():
        return cashier_workplace.__is_working

    @staticmethod
    def open_cash():
        assert not cashier_workplace.is_opened() and cashier_info.is_busy() \
               and database_connection.is_connection()
        cashier_workplace.__is_working = True

    @staticmethod
    def close_cash():
        assert cashier_workplace.is_opened()
        cashier_workplace.__is_working = False

    # Функции непосредственно кассира

    @staticmethod
    def make_purchase(records):
        assert cashier_workplace.is_opened()
        res_list = []
        if len(records) == 0:
            return -1
        id_goods, count_goods = records[0]
        crnt_date = datetime.date.today()
        id_employee, id_warehouse = cashier_info.get_cashier_id(), cashier_info.get_warehouse_id()
        tmp_rec = (id_employee, id_warehouse, id_goods, count_goods, -1, crnt_date)
        [(result, operation, summ)] = database_connection.execute_action('CREATE_CASHIER_CHECK', tmp_rec)
        res_list.append((result, id_goods, summ))
        for record in records[1:]:
            id_goods, cnt_goods = record
            tmp_rec = (id_employee, id_warehouse, id_goods, cnt_goods, operation, crnt_date)
            [(result, operation, summ)] = database_connection.execute_action('CREATE_CASHIER_CHECK', tmp_rec)
            res_list.append((result, id_goods, summ))

        return (operation, res_list)

    @staticmethod
    def make_refund(check_id, goods_id):
        assert cashier_workplace.is_opened()
        result = database_connection.execute_action('MAKE_REFUND', (check_id, goods_id))
        return result

    @staticmethod
    def get_goods_info():
        assert cashier_workplace.is_opened()
        Table, Fields = 'GOODS', ['ID', 'NAME']
        return database_connection.get_data_from_table(Table, Fields)

    @staticmethod
    def get_bonus_for_cashier():
        id = cashier_info.get_cashier_id()
        res = database_connection.execute_action('GET_CASHIER_BONUS', (id))
        print(res)



if __name__ == '__main__':
     database_connection.connect('IT38', 'it38')
     print(cashier_workplace.authorization('2', '1'))
     cashier_workplace.open_cash()


     records = [(1, 2), (2, 2)]

     # (op, List) = cashier_workplace.make_purchase(records)
     # print((op, List))
     #
     # [(res)] = cashier_workplace.make_refund(op, 2)
     # print(res)
     # cashier_workplace.close_cash()

     database_connection.close()

