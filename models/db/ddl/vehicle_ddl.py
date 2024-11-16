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
            """
        CREATE TABLE IF NOT EXISTS vehicle(
            id VARCHAR(32) PRIMARY KEY,
            vehicle_type VARCHAR(10) NOT NULL,
            current_loc VARCHAR(8) NOT NULL,
            charge FLOAT NOT NULL,
            repair_status INTEGER NOT NULL DEFAULT 0,
            available INTEGER NOT NULL DEFAULT 1,
            cost FLOAT NOT NULL,
            total_ride_time INTEGER NOT NULL DEFAULT 0,
            ride_counts INTEGER DEFAULT 0,
            repair_counts INTEGER DEFAULT 0
            )
        """
        )
        #print("vehicle table created")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
