from sqlalchemy import create_engine
from settings import POSTGRES_DB


class DBConnectorPostgres:
    def __init__(self, driver, database, host, port, username, password):
        self.driver = driver
        self.database = database
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.conn_str = f'{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

    def connect(self):
        engine = create_engine(self.conn_str)
        return engine.connect()


db_controller = DBConnectorPostgres(
        POSTGRES_DB['driver'],
        POSTGRES_DB['database'],
        POSTGRES_DB['host'],
        POSTGRES_DB['port'],
        POSTGRES_DB['username'],
        POSTGRES_DB['password']
    )
