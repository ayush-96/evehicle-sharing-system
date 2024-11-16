import psycopg2
from urllib.parse import urlparse


conStr = "postgres://postgres:admin123@localhost:5433/evehicle"
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
            """CREATE TABLE IF NOT EXISTS staff(
            employee_id VARCHAR(32) PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            employee_name VARCHAR(30) NOT NULL,
            employee_phone VARCHAR(15) NOT NULL UNIQUE,
            tenure VARCHAR(10),
            employee_type VARCHAR(8),
            total_vehicles_repaired INTEGER DEFAULT 0,
            total_vehicles_moved INTEGER DEFAULT 0,
            total_vehicle_charged INTEGER DEFAULT 0
            )
        """
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
