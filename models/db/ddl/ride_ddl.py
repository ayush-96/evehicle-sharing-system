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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ride(
                ride_id VARCHAR(32) PRIMARY KEY,
                vehicle_id VARCHAR(10) NOT NULL,
                customer_id VARCHAR(32) NOT NULL,
                start_loc VARCHAR(8),
                end_loc VARCHAR(8),
                start_time TEXT,
                total_time INTEGER DEFAULT 0,
                ride_cost FLOAT DEFAULT 0.0,   
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicle(id))""")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
