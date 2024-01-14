"""Main module."""

import sqlite3


class DatabaseManager:
    """Database Manager Class
    """
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values: tuple = None) -> sqlite3.Cursor:
        """Execute sql statement.

        :param statement: Whole statement
        :type statement: str
        :param values: Parameters of statement, defaults to None
        :type values: tuple, optional
        :return: Cursor
        :rtype: sqlite3.Cursor
        """
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: dict) -> None:
        """Create new table.

        :param table_name: the name of new table
        :type table_name: str
        :param columns: the definition of columns from column name to data type
        :type columns: dict
        """
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]

        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

    def add_or_update(self, table_name: str, data: dict) -> None:
        """Add new data if there is no data that has same primary key,
        or update data.

        :param table_name: target table
        :type table_name: str
        :param data: data typed column to value
        :type data: dict
        """
        primary_key = self.get_primary_key(table_name)

        if primary_key in data.keys():
            self.update(table_name, data)
        else:
            self.add(table_name, data)

    def update(self, table_name: str, data: dict) -> None:
        """Update data

        :param table_name: target table
        :type table_name: str
        :param data: data typed column to value.
        :type data: dict
        """
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

    def add(self, table_name: str, data: dict) -> None:
        """Add new data.

        :param table_name: target table.
        :type table_name: str
        :param data: data typed column to value.
        :type data: dict
        """
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

    def delete(self, table_name: str, criteria: dict) -> None:
        """Delete current data

        :param table_name: target table.
        :type table_name: str
        :param criteria: Criteria to delete. Column name to value.
        :type criteria: dict
        """
        placeholder = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholder)

        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values()),
        )

    def select(
        self,
        table_name: str,
        columns: list = None,
        criteria: dict = None,
        order_by: str = None,
    ):
        """Select specific data.

        :param table_name: Target table.
        :type table_name: str
        :param columns: List of column names, defaults to None
        :type columns: list, optional
        :param criteria: To select data matched by criteria, defaults to None
        :type criteria: dict, optional
        :param order_by: Column name to sort, defaults to None
        :type order_by: str, optional
        :return: _description_
        :rtype: _type_
        """
        criteria = criteria or {}
        columns = columns or "*"
        query = f"SELECT {columns} FROM {table_name}"

        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by:
            query += f" ORDER BY {order_by}"

        return self._execute(query, tuple(criteria.values()))

    def get_primary_key(self, table_name: str) -> str or None:
        """Get primary key from table.

        :param table_name: Target table.
        :type table_name: str
        :return: Column name has primary key if it exists.
        :rtype: str or None
        """
        cursor = self._execute(f"PRAGMA table_info({table_name})")
        for row in cursor.fetchall():
            _, column_name, _, _, _, is_primary_key = row
            if is_primary_key:
                return column_name

        return None
