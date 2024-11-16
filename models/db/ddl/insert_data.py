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
cursor = conn.cursor()

# drop = cursor.execute("""
#     DELETE FROM vehicle;
# """)

vehicle_data = cursor.execute(
    """
INSERT INTO vehicle (id, vehicle_type, current_loc, charge, repair_status, available, cost, total_ride_time,
ride_counts, repair_counts) VALUES
    ('fcd45e12', 'bike', 'G1', 85.43, 0, 1, 5, 0, 0, 0),
    ('ef1234ac', 'cycle', 'G13', 67.22, 0, 1, 2.5, 0, 0, 0),
    ('cb9876ef', 'skateboard', 'G20', 90.55, 0, 1, 3, 0, 0, 0),
    ('a12b3456', 'delivery', 'G4', 77.65, 0, 1, 7.5, 0, 0, 0),
    ('bdc54321', 'bike', 'G44', 55.67, 0, 1, 5, 0, 0, 0),
    ('fa9876bc', 'cycle', 'G2', 62.78, 0, 1, 2.5, 0, 0, 0),
    ('b6543210', 'skateboard', 'G12', 89.34, 0, 1, 3, 0, 0, 0),
    ('acb12345', 'delivery', 'G41', 83.67, 0, 1, 7.5, 0, 0, 0),
    ('ff123abc', 'bike', 'G14', 59.87, 0, 1, 5, 0, 0, 0),
    ('ccb65498', 'cycle', 'G43', 95.55, 0, 1, 2.5, 0, 0, 0),
    ('baa87612', 'skateboard', 'G11', 64.22, 0, 1, 3, 0, 0, 0),
    ('ddc34565', 'delivery', 'G31', 75.89, 0, 1, 7.5, 0, 0, 0),
    ('a1b23cde', 'bike', 'G51', 91.12, 0, 1, 5, 0, 0, 0),
    ('fff34576', 'cycle', 'G52', 74.67, 0, 1, 2.5, 0, 0, 0)
"""
)
