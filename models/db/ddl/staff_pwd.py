from passlib.hash import pbkdf2_sha256
def hashedpassword(password):
    hashedPassword= pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=12 )
    #print(type(hashedPassword))
    return hashedPassword

print(hashedpassword("pwd123")) #$pbkdf2-sha256$12000$7T0HwJjTGgPgnPM.$URbLD4Iw84ozI/V5dHL1RLfA/rYYYLJ6xtjy1SGGkbE
print(hashedpassword("pwd456")) #$pbkdf2-sha256$12000$PufcOwdAKOUc49wb$Wr2/wa9R9f9Fy8.vSfLfAjebNkTCWq0bLurYzGGZEAE

# INSERT INTO staff (employee_id, password, employee_name, employee_phone, tenure, employee_type, total_vehicles_repaired, 
# total_vehicles_moved, total_vehicle_charged)
# VALUES 
# ('EMP001', '$pbkdf2-sha256$12000$7T0HwJjTGgPgnPM.$URbLD4Iw84ozI/V5dHL1RLfA/rYYYLJ6xtjy1SGGkbE', 'John Doe', '1234567890', '5y3m15d', 'manager', 0, 0, 0),
# ('EMP002', '$pbkdf2-sha256$12000$PufcOwdAKOUc49wb$Wr2/wa9R9f9Fy8.vSfLfAjebNkTCWq0bLurYzGGZEAE', 'Jane Smith', '2345678901', '3y7m12d', 'operator', 0, 0, 0)