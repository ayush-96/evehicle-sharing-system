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

conn = psycopg2.connect(**pg_connection_dict)
conn.autocommit = True

with conn.cursor() as cursor:
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS customer(
            customer_id VARCHAR(32) PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            name VARCHAR(30) NOT NULL,
            phone VARCHAR(15) NOT NULL UNIQUE,
            dob VARCHAR(10),
            vehicle_id VARCHAR(10),
            total_trips INTEGER DEFAULT 0,
            total_billing FLOAT,
            current_status INTEGER DEFAULT 0,
            payment_dues FLOAT DEFAULT 0.0,
            report_defective INTEGER DEFAULT 0
            )
        """
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
