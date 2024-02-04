'''
DATA

About
- Useful functions for device

Notes
- Uses SQLite3 database format for device.db and control.db (see sqlite.org)
- Uses JSON format for patient.json

Documentation
- SQLite3 data types: https://www.sqlite.org/datatype3.html

'''

import os
import sqlite3
import json


def replace_data(file, verbose=False):
    if file == 'data/device.db':
        if os.path.exists(file):
            os.remove(file)
            if verbose:
                print(f"removed {file} successfully")
            
        db = sqlite3.connect(file)
        if verbose:
            print(f"created {file} successfully")
        
        db.execute('''CREATE TABLE IF NOT EXISTS device (
            entry                   INTEGER     NOT NULL   PRIMARY KEY,
            hematuria_level         INTEGER     NOT NULL,
            hematuria_percent       REAL        NOT NULL,
            supply_percent          INTEGER     NOT NULL,
            supply_volume           INTEGER     NOT NULL,
            supply_time             INTEGER     NOT NULL,
            supply_rate             INTEGER     NOT NULL,
            waste_percent           INTEGER     NOT NULL,
            waste_volume            INTEGER     NOT NULL,
            waste_time              INTEGER     NOT NULL,
            waste_rate              INTEGER     NOT NULL,
            status_message          TEXT        NOT NULL,
            status_color            TEXT        NOT NULL,
            active_time             TEXT        NOT NULL,
            date                    TEXT        NOT NULL,
            time                    TEXT        NOT NULL,
            supply_volume_total     INTEGER     NOT NULL,
            supply_volume_gross     INTEGER     NOT NULL,
            supply_replace_count    INTEGER     NOT NULL,
            waste_volume_total      INTEGER     NOT NULL,
            waste_volume_gross      INTEGER     NOT NULL,
            waste_replace_count     INTEGER     NOT NULL,
            automatic               INTEGER     NOT NULL,
            inflow_level            INTEGER     NOT NULL,
            mute                    INTEGER     NOT NULL,
            clear                   INTEGER     NOT NULL,
            off                     INTEGER     NOT NULL);''')
        
        db.close()
        if verbose:
            print(f"table 'device' created in {file} successfully")

    elif file == 'data/control.db':
        if os.path.exists(file):
            os.remove(file)
            if verbose:
                print(f"removed {file} successfully")
            
        db = sqlite3.connect(file)
        if verbose:
            print(f"created {file} successfully")
        
        db.execute('''CREATE TABLE IF NOT EXISTS control (
            entry                           INTEGER     NOT NULL   PRIMARY KEY,
            supply_replace_volume           INTEGER     NOT NULL,
            supply_replace_count_removed    INTEGER     NOT NULL,
            supply_replace_count_added      INTEGER     NOT NULL,
            waste_replace_volume            INTEGER     NOT NULL,
            waste_replace_count_removed     INTEGER     NOT NULL,
            waste_replace_count_added       INTEGER     NOT NULL,
            automatic                       INTEGER     NOT NULL,
            inflow_level                    INTEGER     NOT NULL,
            mute                            INTEGER     NOT NULL,
            clear_count                     INTEGER     NOT NULL,
            off_count                       INTEGER     NOT NULL,
            reset_count                     INTEGER     NOT NULL);''')
        
        db.close()
        if verbose:
            print(f"table 'control' created in {file} successfully")

    elif file == 'data/patient.json':
        if os.path.exists(file):
            os.remove(file)
            if verbose:
                print(f"removed {file} successfully")
        
        patient = {
            'patient_firstname': '',
            'patient_lastname': '',
            'patient_middleinitial': '',
            'patient_ID': 0,
            'patient_birthdate': '00:00:0000',
            'patient_sex': '',
            'patient_contact_A': 1234567890,
            'patient_contact_B': 1234567890,
            'patient_start_date': '00:00:0000',
            'patient_start_time': '00:00'
        } # template for patient data
        
        js = json.dumps(patient, indent=4)
        with open(file, "w") as outfile:
            outfile.write(js)
        if verbose:
            print(f"created {file} successfully")

    else:
        raise Exception(f"error finding file {file}")


def add_data(data, file, verbose=False):
    if file == 'data/device.db': # adds new entry to Sqlite database
        db = sqlite3.connect(file)
        if verbose:
            print(f"opened {file} successfully")

        data_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in data)

        cursor = db.cursor()
        cursor.execute(f'''INSERT INTO device (entry, hematuria_level, hematuria_percent, supply_percent, 
            supply_volume, supply_time, supply_rate, waste_percent, waste_volume, waste_time, waste_rate, 
            status_message, status_color, active_time, date, time, supply_volume_total, supply_volume_gross, 
            supply_replace_count, waste_volume_total, waste_volume_gross, waste_replace_count, automatic, 
            inflow_level, mute, clear, off)
            VALUES ({data_formatted})''')
        db.commit()
        db.close()
        if verbose:
            print(f"data added to 'device' in {file} successfully")
    
    elif file == 'data/control.db': # adds new entry to Sqlite database
        db = sqlite3.connect(file)
        if verbose:
            print(f"opened {file} successfully")

        data_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in data)

        cursor = db.cursor()
        cursor.execute(f'''INSERT INTO control (entry, supply_replace_volume, supply_replace_count_removed, 
            supply_replace_count_added, waste_replace_volume, waste_replace_count_removed,
            waste_replace_count_added, automatic, inflow_level, mute, clear_count, off_count, reset_count)
            VALUES ({data_formatted})''')
        db.commit()
        db.close()
        if verbose:
            print(f"data added to 'control' in {file} successfully")

    elif file == 'data/patient.json': # overwrites existing JSON data
        js = json.dumps(data, indent=4)
        with open(file, "w") as outfile:
            outfile.write(js)
        if verbose:
            print(f"data added to {file} successfully")

    else:
        raise Exception(f"error finding file {file}")


def get_data(keys, file, n=1, order='DESC', verbose=False):
    if type(keys) is not list:
        keys = list(keys)

    if file in ['data/device.db', 'data/control.db']: # gets entry from Sqlite database
        db = sqlite3.connect(file)
        if verbose:
            print(f"opened {file} successfully")
        
        cursor = db.cursor()
        keys_formatted = ', '.join(map(str, keys))

        if file == 'data/device.db':
            selection = cursor.execute(f"SELECT {keys_formatted} FROM device ORDER BY entry {order} LIMIT {int(n)}")
        elif file == 'data/control.db':
            selection = cursor.execute(f"SELECT {keys_formatted} FROM control ORDER BY entry {order} LIMIT {int(n)}")
        
        if n == 1:
            for row in selection:
                if len(keys) == 1:
                    data = row[0]
                else:
                    data = list(row)
            if len(keys) == 1:
                data = dict(zip(keys, [data]))
            else:
                data = dict(zip(keys, data))

        elif n > 1:
            data = []
            for row in selection:
                if len(keys) == 1:
                    row = row[0]
                else:
                    row = list(row)
                data.append(row)
            if len(keys) == 1:
                data = dict(zip(keys, [data]))
            else:
                data = {key: list(values) for key, values in zip(keys, zip(*data))}

        if verbose:
            print(f"data retrieved from {file} successfully")
            
    elif file == 'data/patient.json': # gets data from JSON data
        with open(file, 'r') as infile:
            data = json.load(infile)
        data = {key: data[key] for key in keys}
        if verbose:
            print(f"data retrieved from {file} successfully")

    else:
        raise Exception(f"error finding file {file}")
    
    return data


# example implementation
if __name__ == '__main__':
    replace_data(file='data/device.db', verbose=True)
    replace_data(file='data/control.db', verbose=True)
    replace_data(file='data/patient.json', verbose=True)

    data_in_1 = [1, 2, 3.0, 4, 5, 6, 7, 8, 9, 10, 11, 'twelve', 'thirteen', 14, 'fifteen', 'sixteen', 17, 18, 19, 20, 21, 22, 0, 24, 0, 0, 0]
    add_data(data=data_in_1, file='data/device.db', verbose=True)

    data_in_2 = [101, 102, 103.0, 104, 105, 106, 107, 108, 109, 110, 111, 'one-hundred twelve', 'one-hundred thirteen', 114, 'one-hundred fifteen', 'one-hundred sixteen', 117, 118, 119, 120, 121, 122, 1, 124, 1, 1, 1]
    add_data(data=data_in_2, file='data/device.db', verbose=True)

    data_out = get_data(keys=['entry', 'time', 'supply_volume'], file='data/device.db', n=2, order='DESC', verbose=True)
    print(data_out)