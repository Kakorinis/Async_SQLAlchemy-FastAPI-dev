import csv
from sqlalchemy import text
import pandas as pd
from .db_connector_mssql import DBConnectorMSSQL
from logger import logger
from settings import MSSQL_DB_URL


class GetTablesFromDWH(DBConnectorMSSQL):
    """ класс извлечения таблиц из БД """

    def __init__(self, db_path_some):
        super().__init__(db_path_some)
        self.connection = self.get_connection()
        logger.info('Успешное подключение к БД DWH')

    def fetch_client_full_data(self, chunksize=200000, output_file='default.csv'):
        """
        Метод почанкового чтения строк из таблицы с сохранением данных в файл .csv (запись первого чанка и дозаписи
        последующих).

        :param chunksize: кол-во строк для чтения в чанке.
        :param output_file: название файла куда сохранять данные.
        :return: файл с данными из БД, формирование которого потребляет меньше ОЗУ, чем если читать и писать целиком.
        """
        query = text(
            '''
            SELECT c.fullname,
                c.id as client_id,
                c.birthday,
                c.last_changes_date,
                ci.phone,
                ci.address,
                ci.email,
                pasp.number,
                pasp.series,
                pasp.date_of_issue,
                pasp.issued_by,
                pasp.department_code
            FROM [Clients_database].dbo.[client] as c
            LEFT JOIN [Clients_database].dbo.[clients_info] as ci
                ON ci.client_id=c.id
            LEFT JOIN JOIN [Clients_database].dbo.[clients_passport] as pasp
                ON pasp.client_id=c.id
            WHERE c.fullname IS NOT NULL
                AND LEN(LTRIM(RTRIM(c.fullname))) - LEN(REPLACE(RTRIM(LTRIM(c.fullname)), ' ', '')) >= 1
            ORDER BY c.fullname
            '''
        )
        cursor = self.connection.execute(query)
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')
            csv_writer.writerow(cursor.keys())  # Write column headers

            row_count = 0
            while True:
                rows = cursor.fetchmany(chunksize)
                if not rows:
                    break
                csv_writer.writerows(rows)
                row_count += len(rows)
        logger.info(f'Saved {row_count} rows to {output_file}')

    def fetch_clients_phone_calls(self, chunksize=200000, output_file='default.csv'):
        """
        Метод почанкового чтения строк из таблицы с сохранением данных в файл .csv (запись первого чанка и дозаписи
        последующих).
        Берем только если более одного слова в наименовании клиента.

        :param chunksize: кол-во строк для чтения в чанке.
        :param output_file: название файла куда сохранять данные.
        :return: файл с данными из БД, формирование которого потребляет меньше ОЗУ, чем если читать и писать целиком.
        """
        query = text(
            '''
            WITH CTE AS (
                SELECT
                    LOWER(LTRIM(RTRIM(REPLACE([client_name], '  ', ' ')))) AS [client_fullname],
                    [phone],
                    [id_phone_call]
                FROM [Clients_database].[dbo].[clients_calls]
                WHERE [phone] IS NOT NULL
                    AND [client_name] IS NOT NULL
                    AND LEN(LTRIM(RTRIM([client_name]))) -
                    LEN(REPLACE(RTRIM(LTRIM([client_name])), ' ', '')) >= 1
            )
            SELECT
                [client_fullname],
                [phone],
                STRING_AGG(CAST([id_phone_call] AS varchar(max)), ', ') AS [id_phone_call]
            FROM CTE
            GROUP BY [client_fullname], [phone]
            ORDER BY [client_fullname]
            '''
        )
        cursor = self.connection.execute(query)
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')
            csv_writer.writerow(cursor.keys())  # Write column headers

            row_count = 0
            while True:
                rows = cursor.fetchmany(chunksize)
                if not rows:
                    break
                csv_writer.writerows(rows)
                row_count += len(rows)
        logger.info(f'Saved {row_count} rows to {output_file}')

    def fetch_workers(self):
        """
        Метод чтения и сохранения небольшой таблицы в файл целиком.
        """
        query = text(
            '''
            SELECT fullname, phone, id, address
            FROM [Personal_database].[dbo].[personal] as lds
            '''
        )
        df = pd.read_sql(query, self.connection)
        return df


db_controller = GetTablesFromDWH(MSSQL_DB_URL)
