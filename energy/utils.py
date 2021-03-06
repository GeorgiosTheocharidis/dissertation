"""Exposes common utilities."""

import os

import psycopg2
import pandas as pd

import energy.selects as selects

_CREATE_TABLE = """CREATE TABLE {table_name}
(
    {columns}
);
""".format

_DATA_TYPES_MAP = {
    'float32': 'REAL',
    'float64': 'REAL',
    'int64': 'INT',
    'datetime64[ns]': 'timestamp'
}


def save_to_db(data, table_name):
    """Creates a table to store the passed in data frame to the database.

    :param pd.DataFrame data: The data frame to save to the data base.
    :param str table_name: The name of the table to create.
    """
    data = data.dropna()
    conn = psycopg2.connect(selects.CONN_STR)
    cur = conn.cursor()
    cur.execute(f'drop table if exists {table_name}')

    columns = []
    for column_name, data_type in zip(list(data.columns), list(data.dtypes)):
        data_type = _DATA_TYPES_MAP[str(data_type)]
        columns.append(f'{column_name} {data_type}')

    sql_create_table = _CREATE_TABLE(
        table_name=table_name,
        columns=','.join(columns)
    )

    cur.execute(sql_create_table)
    conn.commit()

    filename = f'/vagrant/data/{table_name}.csv'
    with open(filename, 'w') as f:
        f.write(data.to_csv(index=False, header=False))

    sql = f"copy {table_name} FROM '{filename}' DELIMITER ',' CSV"
    cur.execute(sql)
    conn.commit()

    os.remove(filename)


if __name__ == '__main__':
    data = pd.DataFrame({'a': [1., 2, 3], 'b': [23, 34, 22]})
    save_to_db(data, 'junk')
