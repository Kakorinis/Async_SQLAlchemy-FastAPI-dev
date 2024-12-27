from typing import Any
from typing import Union

import sqlalchemy
from sqlalchemy import create_engine


class DBConnectorMSSQL:
    """ Класс подключения к БД """

    def __init__(self, db_path_some):
        self.db_path = db_path_some
        self.__engine = None
        self.__connection = None
        self.create_engine()
        self.create_connection()

    def create_engine(self) -> None:
        """ Создает движок подключения к БД """
        self.__engine = create_engine(self.db_path)

    def create_connection(self) -> None:
        """ Создает подключение к БД  """
        self.__connection = self.__engine.connect()

    def get_engine(self):
        """
        Возвращает движок подключения к БД
        :return: движок подключения к бд
        """
        return self.__engine

    def get_connection(self) -> Union[sqlalchemy.engine.Connection, Any]:
        """
        Возвращает подключение к БД
        :return: подключение к бд
        """
        return self.__connection

    def close_connection(self) -> None:
        """  Закрывает подключение к бд  """
        self.__connection.close()
