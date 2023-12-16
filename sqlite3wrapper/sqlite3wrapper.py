"""Main module."""

import sqlite3

class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]

        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

    def add_or_update(self, table_name, data):
        primary_key = self.get_primary_key(table_name)

        if primary_key in data.keys():
            self.update(table_name, data)
        else:
            self.add(table_name, data)

    def update(self, table_name, data):
        primary_key = self.get_primary_key(table_name)
        primary_value = data.pop(primary_key)
        placeholder = ", ".join([key + "=?" for key in data.keys()])
        column_values = tuple(data.values()) + (primary_value,)

        self._execute(
            f"""
            UPDATE {table_name}
            SET {placeholder}
            WHERE {primary_key}=?;
            """,
            column_values,
        )

    def add(self, table_name, data):
        placeholder = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholder});
            """,
            column_values,
        )

    def delete(self, table_name, criteria):
        placeholder = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholder)

        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values()),
        )

    def select(self, table_name, row=None, criteria=None, order_by=None):
        criteria = criteria or {}
        row = row or "*"
        query = f"SELECT {row} FROM {table_name}"

        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by:
            query += f" ORDER BY {order_by}"

        return self._execute(query, tuple(criteria.values()))

    def get_primary_key(self, table_name):
        cursor = self._execute(f"PRAGMA table_info({table_name})")
        for row in cursor.fetchall():
            _, column_name, _, is_primary_key, _, _ = row
            if is_primary_key:
                return column_name

        return None
