import psycopg2
from urllib.parse import urlparse


conStr = "postgres://postgres:admin123@localhost:5432/evehicle"
p = urlparse(conStr)

pg_connection_dict = {
    'dbname': p.path[1:],
    'user': p.username,
    'password': p.password,
    'port': p.port,
    'host': p.hostname
}


def run_db_update_query_params(query, params):
    query_result_flag = False
    conn = psycopg2.connect(**pg_connection_dict)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        query_result_flag = True
    except Exception as e:
        query_result_flag = False
        print("Error while inserting into DB!", str(e))
    finally:
        return query_result_flag


def run_db_update_query(query):
    conn = psycopg2.connect(**pg_connection_dict)
    conn.autocommit = True
    cursor = conn.cursor()
    query_result_flag = False
    try:
        cursor.execute(query)
        conn.commit()
        conn.close()
        query_result_flag = True
    except Exception as e:
        query_result_flag = False
        print("Error while updating the DB!", str(e))
    finally:
        return query_result_flag


def run_db_fetch_query(query):
    conn = psycopg2.connect(**pg_connection_dict)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    query_result_list = []
    if len(query_result) > 0:
        for row in query_result:
            query_result_list.append(row)
    else:
        print("No rows returned! Query: {}".format(query))
    conn.commit()
    conn.close()
    return query_result_list


print(run_db_fetch_query("select * from customer;"))
