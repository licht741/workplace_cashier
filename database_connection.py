import firebirdsql
import functools

# Модуль, реализующий соединение и работу с базой данных. Используется библиотека firebirdsql.
# Реализуется посредством паттерна Singleton. В каждый момент времени допускается только одно соединение

class not_connected_exception(Exception):
    pass

class database_connection:
    class __connection:
        def __init__(self, user, password):
            if not database_connection.is_connection():
                self.__connect = firebirdsql.connect(
                    dsn      = 'class.mmcs.sfedu.ru:/fbdata/38mi/newtest_podgr3.fdb',
                    user     = user,
                    password = password)

        def get_connection(self):
            return self.__connect

    __instance = None
    
    @staticmethod
    def __get_instance():
        return database_connection.__instance.get_connection()
    
    @staticmethod
    def connect(user, password):
        if not database_connection.is_connection():
            database_connection.__instance = database_connection.__connection(user, password)

    @staticmethod
    def is_connection():
        return database_connection.__instance != None

    @staticmethod
    def close():
         if database_connection.is_connection():
             database_connection.__get_instance().close()
             database_connection.__instance = None

    @staticmethod
    def get_data_from_table(table, fields):
        if not database_connection.is_connection():
            raise not_connected_exception
        cur = database_connection.__get_instance().cursor()
        req_fields = functools.reduce(lambda x, y: x + ', ' + y, fields)
        cur.execute('select ' + req_fields + ' from ' + table)
        return cur.fetchall()

    @staticmethod
    def execute_action(proc, params):
        if not database_connection.is_connection():
            raise not_connected_exception
        cur = database_connection.__get_instance().cursor()
        cur.callproc(proc, params)
        result = cur.fetchall()
        database_connection.__get_instance().commit()
        return result

    @staticmethod
    def instance(user = None, password = None):
        if database_connection.__instance is None:
            database_connection.__instance = database_connection.__connection(user, password)
        return database_connection.__instance


if __name__ == '__main__':
    database_connection.connect('IT38', 'it38')
    print(database_connection.get_data_from_table('EMPLOYEE', ['NAME', 'SALARY']))
    database_connection.close()
