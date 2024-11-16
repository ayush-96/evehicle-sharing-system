import psycopg2
from urllib.parse import urlparse

from passlib.hash import pbkdf2_sha256
def hashedpassword(password):
    hashedPassword= pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=12 )
    #print(type(hashedPassword))
    return hashedPassword

print(hashedpassword("pwd123"))
print(hashedpassword("pwd456"))

'''conStr = "postgres://postgres:admin123@localhost:5432/evehicle"
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

vehicle_data = cursor.execute(
    """
INSERT INTO staff (employee_id, password, employee_name, employee_phone, tenure, employee_type, total_vehicles_repaired, 
total_vehicles_moved, total_vehicle_charged)
VALUES 
('EMP001', 'password123', 'John Doe', '1234567890', '5y3m15d', 'manager', 0, 0, 0),
('EMP002', 'password456', 'Jane Smith', '2345678901', '3y7m12d', 'operator', 0, 0, 0),
('EMP003', 'password789', 'Alan White', '3456789012', '8y1m9d', 'manager', 0, 0, 0),
('EMP004', 'password101', 'Sara Black', '4567890123', '4y6m18d', 'operator', 0, 0, 0),
('EMP005', 'password202', 'Tom Brown', '5678901234', '9y5m7d', 'manager', 0, 0, 0),
('EMP006', 'password303', 'Lucy Green', '6789012345', '1y2m5d', 'operator', 0, 0, 0),
('EMP007', 'password404', 'Mark Blue', '7890123456', '10y11m14d', 'manager', 0, 0, 0),
('EMP008', 'password505', 'Emily Grey', '8901234567', '2y9m20d', 'operator', 0, 0, 0),
('EMP009', 'password606', 'Kevin Silver', '9012345678', '6y8m6d', 'manager', 0, 0, 0),
('EMP010', 'password707', 'Chloe Gold', '9123456789', '5y1m2d', 'operator', 0, 0, 0),
('EMP011', 'password808', 'Ryan Lee', '1023456789', '7y10m11d', 'manager', 0, 0, 0),
('EMP012', 'password909', 'Anna Davis', '1123456789', '4y5m23d', 'operator', 0, 0, 0),
('EMP013', 'password010', 'Chris King', '1223456789', '8y4m17d', 'manager', 0, 0, 0),
('EMP014', 'password111', 'Sophia Moore', '1323456789', '1y11m9d', 'operator', 0, 0, 0),
('EMP015', 'password212', 'Jack Taylor', '1423456789', '3y8m25d', 'manager', 0, 0, 0),
('EMP016', 'password313', 'Lily Thompson', '1523456789', '5y6m13d', 'operator', 0, 0, 0),
('EMP017', 'password414', 'Oliver Anderson', '1623456789', '2y10m1 day', 'manager', 0, 0, 0),
('EMP018', 'password515', 'Mia Harris', '1723456789', '7y7m29d', 'operator', 0, 0, 0),
('EMP019', 'password616', 'Harry Clark', '1823456789', '9y2m5d', 'manager', 0, 0, 0),
('EMP020', 'password717', 'Isla Walker', '1923456789', '1y8m11d', 'operator', 0, 0, 0),
('EMP021', 'password818', 'George Hill', '2023456789', '6y3m4d', 'manager', 0, 0, 0),
('EMP022', 'password919', 'Ella Adams', '2123456789', '5y9m22d', 'operator', 0, 0, 0),
('EMP023', 'password020', 'Liam Scott', '2223456789', '10y1m18d', 'manager', 0, 0, 0),
('EMP024', 'password121', 'Grace Young', '2323456789', '2y7m16d', 'operator', 0, 0, 0),
('EMP025', 'password222', 'James Hall', '2423456789', '4y2m8d', 'manager', 0, 0, 0),
('EMP026', 'password323', 'Ava Allen', '2523456789', '3y5m14d', 'operator', 0, 0, 0),
('EMP027', 'password424', 'Ethan Lewis', '2623456789', '9y11m25d', 'manager', 0, 0, 0),
('EMP028', 'password525', 'Olivia Wright', '2723456789', '1y4m13d', 'operator', 0, 0, 0),
('EMP029', 'password626', 'Daniel King', '2823456789', '8y9m7d', 'manager', 0, 0, 0),
('EMP030', 'password727', 'Sophia Baker', '2923456789', '7y2m3d', 'operator', 0, 0, 0),
('EMP031', 'password828', 'Matthew Turner', '3023456789', '2y6m12d', 'manager', 0, 0, 0),
('EMP032', 'password929', 'Amelia Carter', '3123456789', '4y8m10d', 'operator', 0, 0, 0),
('EMP033', 'password030', 'Henry Nelson', '3223456789', '6y4m9d', 'manager', 0, 0, 0),
('EMP034', 'password131', 'Emily Green', '3323456789', '5y2m17d', 'operator', 0, 0, 0),
('EMP035', 'password232', 'Noah Mitchell', '3423456789', '10y5m1 day', 'manager', 0, 0, 0),
('EMP036', 'password333', 'Chloe Perez', '3523456789', '3y9m19d', 'operator', 0, 0, 0),
('EMP037', 'password434', 'Benjamin Collins', '3623456789', '9y6m23d', 'manager', 0, 0, 0),
('EMP038', 'password535', 'Lily Price', '3723456789', '2y3m15d', 'operator', 0, 0, 0),
('EMP039', 'password636', 'Jacob Perry', '3823456789', '8y7m18d', 'manager', 0, 0, 0),
('EMP040', 'password737', 'Ella Sanchez', '3923456789', '1y9m2d', 'operator', 0, 0, 0),
('EMP041', 'password838', 'Samuel Reed', '4023456789', '7y4m6d', 'manager', 0, 0, 0),
('EMP042', 'password939', 'Ava Ross', '4123456789', '4y10m21d', 'operator', 0, 0, 0),
('EMP043', 'password040', 'William Cook', '4223456789', '6y1m11d', 'manager', 0, 0, 0),
('EMP044', 'password141', 'Sophie Morgan', '4323456789', '5y7m8d', 'operator', 0, 0, 0),
('EMP045', 'password242', 'Owen Edwards', '4423456789', '9y12m14d', 'manager', 0, 0, 0),
('EMP046', 'password343', 'Harper Gray', '4523456789', '2y5m4d', 'operator', 0, 0, 0),
('EMP047', 'password444', 'Lucas Bell', '4623456789', '8y2m22d', 'manager', 0, 0, 0),
('EMP048', 'password545', 'Isabella Murphy', '4723456789', '1y7m9d', 'operator', 0, 0, 0),
('EMP049', 'password646', 'Elijah Cox', '4823456789', '10y3m26d', 'manager', 0, 0, 0)
"""
)

'''