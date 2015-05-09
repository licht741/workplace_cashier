class cashier_info:
    class __cashier:
        def __init__(self, cashier_name, cashier_id, wh_name, wh_id):
            self.cashier_name, self.cashier_id = cashier_name, cashier_id
            self.warehouse_name, self.warehouse_id = wh_name, wh_id

    __instance = None

    @staticmethod
    def is_busy():
        return cashier_info.__instance != None

    @staticmethod
    def new_cashier(cashier_name, cashier_id, wh_name, wh_id):
        assert not cashier_info.is_busy()
        cashier_info.__instance = cashier_info.__cashier(cashier_name, cashier_id, wh_name, wh_id)

    @staticmethod
    def destroy_cashier():
        assert cashier_info.is_busy()
        cashier_info.__instance = None

    @staticmethod
    def get_cashier_id():
        if cashier_info.is_busy():
            return cashier_info.__instance.cashier_id
        else:
            return None

    @staticmethod
    def get_cashier_name():
        if cashier_info.is_busy():
            return cashier_info.__instance.cashier_name
        else:
            return None

    @staticmethod
    def get_warehouse_id():
        if cashier_info.is_busy():
            return cashier_info.__instance.warehouse_id
        else:
            return None

    @staticmethod
    def get_warehouse_name():
        if cashier_info.is_busy():
            return cashier_info.__instance.warehouse_name
        else:
            return None

if __name__ == '__main__':
    print(cashier_info.get_cashier_id(), cashier_info.get_cashier_name(), cashier_info.get_warehouse_id(), cashier_info.get_warehouse_name())
    cashier_info.new_cashier('Ivan Rakov', 1488, 'Aksay Ind', 666)
    print(cashier_info.get_cashier_id(), cashier_info.get_cashier_name(), cashier_info.get_warehouse_id(), cashier_info.get_warehouse_name())
