import os
import sys
import json
# from dotenv import load_dotenv
import mysql.connector

# dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, '.env'))
# load_dotenv(dotenv_path)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(parentdir)

from secret import tidb_connection_secret

# tidb_config = os.environ.get("tidb_connection_secret")

conn = mysql.connector.connect(**tidb_connection_secret)
cur = conn.cursor()

def test_tidb_conn():
    try:
        cur.execute("SELECT CURDATE()")
        row = cur.fetchone()
        print("Current date is: {0}".format(row[0]))
    except Exception as e:
        print(f'Error: {e}')
    finally:
        conn.close()
        
def tidb_read_from_table(table_name: str, columns_list: list, other_clause: str=""):
    columns_str = (", ").join(columns_list)
    dynamic_query_str = (f"select {columns_str}"
                        f" from {table_name}"
                        f" {other_clause}")
    print(f'{dynamic_query_str=}')
    try:
        cur.execute(dynamic_query_str)
        row_headers=[x[0] for x in cur.description]
        rows = cur.fetchall()
        json_data = list()
        for row in rows:
            json_data.append(dict(zip(row_headers, row)))
    except Exception as e:
        print(f'Error: {e}')
    finally:
        conn.close()
    return json_data

def tidb_read_by_query(query: str=""):
    try:
        cur.execute(query)
        row_headers=[x[0] for x in cur.description]
        rows = cur.fetchall()
        print(f"{cur.rowcount=}")
        json_data = list()
        for row in rows:
            json_data.append(dict(zip(row_headers, row)))
    except Exception as e:
        print(f'Error: {e}')
    finally:
        conn.close()
    return json_data

def tidb_write_by_sql_files(file_path):
    pass