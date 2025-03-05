def get_aircraft_list():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, has_fault FROM aircraft")
    aircraft_list = cursor.fetchall()
    db.close()
    return aircraft_list

def get_aircraft_data(aircraft_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT sensor_name, value, timestamp FROM sensor_data WHERE aircraft_id = %s ORDER BY timestamp DESC", (aircraft_id,))
    data = cursor.fetchall()
    db.close()
    return data

def reset_aircraft_system(aircraft_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE aircraft SET has_fault = 0 WHERE id = %s", (aircraft_id,))
    db.commit()
    db.close()
