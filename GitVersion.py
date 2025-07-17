#!/usr/bin/env python3

import pyodbc
import psycopg2
import logging
import time
import sys

# 👇 CONFIG — EDIT THIS SECTION!
# --------------------------------------------------
import pyodbc

SQL_SERVER_CONN_STR = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=**.**.***.***;'
    'DATABASE=*******;'
    'UID=******;'
    'PWD=*******+;'
    'Encrypt=no;'
)




# PostgreSQL connection settings

POSTGRES_CONN = {
    'dbname': "******",
    'user': "***********",
    'password': "*********",
    'host': "**********+",
    'port': ****
}



DEFAULT_BATCH_SIZE = 5000
LARGE_BATCH_SIZE = 20000

TABLES_TO_MIGRATE = [
    'TableName1',
    'TableName1',
    'TableName1',
    'TableName1',
    'TableName1',
    'GTableName1',
    'TableName1',
    ,....
    'TableName1'
]

TABLES_USING_LARGE_BATCH = [
    'TableNameBigSize1',
    'TableNameBigSize1',
    'TableNameBigSize1',
    .......,
    'TableNameBigSize1'
]
# --------------------------------------------------


# ✅ Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("migration.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


def connect_sql_server():
    try:
        conn = pyodbc.connect(SQL_SERVER_CONN_STR)
        logging.info("✅ Connected to SQL Server.")
        return conn
    except Exception as e:
        logging.error(f"❌ Failed to connect to SQL Server: {e}")
        sys.exit(1)


def connect_postgres():
    try:
        conn = psycopg2.connect(**POSTGRES_CONN)
        logging.info("✅ Connected to PostgreSQL.")
        return conn
    except Exception as e:
        logging.error(f"❌ Failed to connect to PostgreSQL: {e}")
        sys.exit(1)


BOOLEAN_COLUMNS = {'cansendmessagebybot'}

def transform_row(row, columns):
    row = list(row)
    for i, col in enumerate(columns):
        if col.lower() in BOOLEAN_COLUMNS:
            row[i] = bool(row[i]) if row[i] is not None else None
    return row


def fetch_batch_sql_server(cursor, table, offset, batch_size):
    query = f"SELECT * FROM {table} ORDER BY 1 OFFSET {offset} ROWS FETCH NEXT {batch_size} ROWS ONLY"
    cursor.execute(query)
    return cursor.fetchall()


def insert_batch_postgres(pg_cursor, table, columns, batch):
    placeholders = ','.join(['%s'] * len(columns))
    col_list = ','.join(columns)
    insert_sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"
    pg_cursor.executemany(insert_sql, batch)


def migrate_table(sql_cursor, pg_cursor, pg_conn, table, batch_size):
    logging.info(f"🚀 Starting migration for table: {table}")

    sql_cursor.execute(f"SELECT TOP 0 * FROM {table}")
    columns = [desc[0].lower() for desc in sql_cursor.description]  # lowercase column names

    total_rows = 0
    offset = 0
    start_time = time.time()

    while True:
        try:
            batch = fetch_batch_sql_server(sql_cursor, table, offset, batch_size)
            if not batch:
                break

            batch_transformed = [transform_row(r, columns) for r in batch]

            insert_batch_postgres(pg_cursor, table.lower(), columns, batch_transformed)
            pg_conn.commit()

            offset += len(batch)
            total_rows += len(batch)
            logging.info(f"✅ Inserted batch of {len(batch)} rows for {table} (Total so far: {total_rows})")

        except Exception as e:
            logging.error(f"❌ Error migrating batch for table {table}: {e}")
            pg_conn.rollback()
            offset += batch_size

    end_time = time.time()
    logging.info(f"🎯 Finished table {table}. Total rows: {total_rows}. Time: {end_time - start_time:.2f}s")


def main():
    logging.info("🚀 Starting SQL Server → PostgreSQL migration.")

    sql_conn = connect_sql_server()
    sql_cursor = sql_conn.cursor()

    pg_conn = connect_postgres()
    pg_cursor = pg_conn.cursor()

    for table in TABLES_TO_MIGRATE:
        batch_size = LARGE_BATCH_SIZE if table in TABLES_USING_LARGE_BATCH else DEFAULT_BATCH_SIZE
        try:
            migrate_table(sql_cursor, pg_cursor, pg_conn, table, batch_size)
        except Exception as e:
            logging.error(f"❌ Fatal error migrating table {table}: {e}")
            continue

    sql_cursor.close()
    sql_conn.close()
    pg_cursor.close()
    pg_conn.close()

    logging.info("✅ All migrations complete.")


if __name__ == "__main__":
    main()
