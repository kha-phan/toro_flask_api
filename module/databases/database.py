from databases.mysql_database import MySqlDatabase
from databases.mongo_database import MongoDatabase
from utils import config
from exceptions import Error


class Database(object):
    def __init__(self, client_id=None, **kwargs):
        self.vendor = config.get('databases.db_vendor', 'mongo').lower()

        if self.vendor == 'mysql':
            self.__db = MySqlDatabase(client_id, **kwargs)
        elif self.vendor == 'mongo':
            self.__db = MongoDatabase(client_id, **kwargs)
        else:
            raise Error(kwargs, f'Cannot create connection: Database vendor is not supported!')

    def get_db(self):
        return self.__db.get_db()

    def is_ready(self):
        return self.__db.is_ready()

    def check(self):
        return self.__db.check()

    def wait_til_ready(self, timeout: float = None, sleep_time: float = 0.5):
        return self.__db.wait_til_ready(timeout, sleep_time)

    def get_operator(self, data_filter=None, fetched_data=None, *args, **kwargs):
        return self.__db.get_operator(data_filter, fetched_data, *args, **kwargs)

    def get_operator_by_id(self, operator_id: str, fetched_data=None, *args, **kwargs):
        return self.__db.get_operator_by_id(operator_id, fetched_data, *args, **kwargs)

    def get_operators(self, data_filter=None, fetched_data=None, data_sort=None, *args, **kwargs):
        return self.__db.get_operators(data_filter, fetched_data, data_sort, *args, **kwargs)

    def get_config(self, solution: str, fetched_data=None, *args, **kwargs):
        return self.__db.get_config(solution, fetched_data, *args, **kwargs)

    def get_list_of_states(self):
        return self.__db.get_list_of_states()

    def get_boundaries(self, operator_id: str):
        return self.__db.get_boundaries(operator_id)

    def get_landmarks(self, operator_id: str):
        return self.__db.get_landmarks(operator_id)
