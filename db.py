"""
en: The module contains classes for working with the database
ru: Модуль содержит классы для работы с базой данных
"""
import sqlite3


class Database:
    """
    en: Class for working with the database
    ru: Класс для работы с базой данных
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        en: Create a database connection to a SQLite database
        ru: Создать подключение к базе данных SQLite
        """
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.execute("PRAGMA foreign_keys = 1;")
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(e)

    def close(self):
        """
        en: Close the connection to the database
        ru: Закрыть подключение к базе данных
        """
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """
        en: Context manager method
        ru: Метод менеджера контекста
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        en: Context manager method
        ru: Метод менеджера контекста
        """
        if exc_type:
            print(exc_type, exc_val)
        self.close()

    def execute_query(self, sql, params=None):
        """
        en: Execute sql statement
        ru: Выполнить sql запрос
        """
        if params is None:
            params = ()
        with self:
            self.cursor.execute(sql, params)
            self.connection.commit()

    def fetch_query(self, sql, params=None):
        """
        en: Execute sql statement and return data
        ru: Выполнить sql запрос и вернуть данные
        """
        if params is None:
            params = ()
        with self:
            self.cursor.execute(sql, params)
            data = self.cursor.fetchall()
        return data

    @property
    def tables(self):
        """
        en: Get all tables in the database
        ru: Получить все таблицы в базе данных
        """
        result = self.fetch_query("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in result if row[0] != 'sqlite_sequence']

    def add_table(self, table_name, fields, foreign_keys=None):
        """
        en: Add a new table to the database
        ru: Добавить новую таблицу в базу данных
        """
        if table_name in self.tables:
            print(f"Table {table_name} already exists")
            return
        field_definitions = ", ".join([f"{field} {fields[field]}" for field in fields])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions}"
        if foreign_keys:
            fk_clause = (f", FOREIGN KEY ({foreign_keys['key']}) "
                         f"REFERENCES {foreign_keys['reference']} "
                         f"ON DELETE {foreign_keys['on_delete']} "
                         f"ON UPDATE {foreign_keys['on_update']}")
            sql += fk_clause
        sql += ");"
        self.execute_query(sql)

    def table_info(self, table_name: str):
        """
        en: Get information about the table
        ru: Получить информацию о таблице
        :param table_name: en: Table name / ru: Название таблицы
        :return: list en: Table information / ru: Информация о таблице
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        data = self.fetch_query(f"PRAGMA table_info({table_name});")
        info_dict = {row[1]: row[2] for row in data}
        return info_dict

    def clear_table(self, table_name):
        """
        en: Clear the table / ru: Очистить таблицу
        :param table_name: en: Table name / ru: Название таблицы
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        self.execute_query(f"DELETE FROM {table_name};")

    def drop_table(self, table_name):
        """
        en: Delete the table / ru: Удалить таблицу
        :param table_name: en: Table name / ru: Название таблицы
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        self.execute_query(f"DROP TABLE {table_name};")

    def add_value(self, table_name, data_dict: dict):
        """
        en: Add a value to the table
        :param table_name: en: Table name / ru: Название таблицы
        :param data_dict: en: Data dictionary / ru: Словарь данных
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        keys_list = data_dict.keys()
        keys = ', '.join(keys_list)
        placeholders = ', '.join(['?' for _ in keys_list])
        values = tuple(data_dict[key] for key in keys_list)
        self.execute_query(f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders});", values)

    def update_value(self, table_name, column_name, value, where_column, where_value):
        """
        en: Update table / ru: Обновить таблицу
        :param table_name: en: Table name / ru: Название таблицы
        :param column_name: en: Column name / ru: Название столбца
        :param value: en: Value / ru: Значение
        :param where_column: en: Where column / ru: Где столбец
        :param where_value: en: Where value / ru: Где значение
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        self.execute_query(
            f"UPDATE {table_name} SET {column_name} = ? WHERE {where_column} = ?;",
            (value, where_value)
        )

    def delete_value(self, table_name, column, value):
        """
        en: Delete value from table / ru: Удалить значение из таблицы
        :param table_name: en: Table name / ru: Название таблицы
        :param column: en: Column name / ru: Название столбца
        :param value: en: Value / ru: Значение
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        self.execute_query(f"DELETE FROM {table_name} WHERE {column} = ?;", (value,))

    def get_values(self, table_name, columns=None, value=None):
        """
        en: Get values from table
        ru: Получить значения из таблицы
        :param table_name: en: Table name / ru: Название таблицы
        :param columns: en: Column name / ru: Название столбца
        :param value: en: Value / ru: Значение
        """
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist")
            return
        info = list(self.table_info(table_name))
        if columns and value:
            data = self.fetch_query(f"SELECT * FROM {table_name} WHERE {columns} = ?;", (value,))
        else:
            data = self.fetch_query(f"SELECT * FROM {table_name};")
        data_dict = [{info[i]: row[i] for i in range(len(info))} for row in data]
        return data_dict
