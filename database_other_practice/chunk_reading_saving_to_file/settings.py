from os import getenv

from dotenv import load_dotenv

load_dotenv()

DEVICE = str(getenv('DEVICE'))
DEVICE_USERNAME = str(getenv('DEVICE_USERNAME'))
DEVICE_PASSWORD = str(getenv('DEVICE_PASSWORD'))
SFTP_PORT: int = 22

# Настройки подключений для посгри
POSTGRES_DB = {
    'driver': 'postgresql',
    'host': str(getenv('POSTGRES_DB_HOST')),
    'port': int(str(getenv('POSTGRES_DB_PORT'))),
    'database': str(getenv('POSTGRES_DB_DATABASE')),
    'username': str(getenv('POSTGRES_DB_USERNAME')),
    'password': str(getenv('POSTGRES_DB_PASSWORD'))
}
# Настройки подключений для MSSQL
DB_DIALECT = str(getenv('MSSQL_DB_DIALECT'))
SYNC_DB_DRIVER = str(getenv('MSSQL_DB_SYNC_DRIVER'))
DB_LOGIN = str(getenv('MSSQL_DB_LOGIN'))
DB_PASSWORD = str(getenv('MSSQL_DB_PASSWORD'))
DB_SERVER = str(getenv('MSSQL_DB_SERVER'))
DB_NAME = str(getenv('MSSQL_DB_DATABASE'))
DB_ODBC_CONNECT_DRIVER = str(getenv('DWH_DB_ODBC_CONNECT_DRIVER'))
DB_AUTH = f'{DB_LOGIN}:{DB_PASSWORD}'
DB_PATH = f'{DB_SERVER}/{DB_NAME}?driver={DB_ODBC_CONNECT_DRIVER}'
MSSQL_DB_URL = f'{DB_DIALECT}+{SYNC_DB_DRIVER}://{DB_AUTH}@{DB_PATH}'
