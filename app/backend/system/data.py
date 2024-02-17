'''
DATA

About
- Helper functions for updating and querying databases

Notes
- Uses SQLite3 database format for system.db and user.db (see sqlite.org)
- Uses JSON format for patient.json

Documentation
- SQLite3 data types: https://www.sqlite.org/datatype3.html

'''

import os
import sqlite3
import json


def replace_data(file, verbose=False):
    if file == 'system':
        path = 'data/system.db'
        if os.path.exists(path):
            os.remove(path)
            if verbose:
                print(f"removed {path} successfully")
        print(path)
        db = sqlite3.connect(path)
        if verbose:
            print(f"created {path} successfully")
        
        db.execute('''CREATE TABLE IF NOT EXISTS system (
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
            status_level            TEXT        NOT NULL,
            status_message          TEXT        NOT NULL,
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
            mute                    INTEGER     NOT NULL);''')
        db.close()
        if verbose:
            print(f"table 'system' created in {path} successfully")

    elif file == 'user':
        path = 'data/user.db'
        if os.path.exists(path):
            os.remove(path)
            if verbose:
                print(f"removed {path} successfully")
            
        db = sqlite3.connect(path)
        if verbose:
            print(f"created {path} successfully")
        
        db.execute('''CREATE TABLE IF NOT EXISTS user (
            entry                           INTEGER     NOT NULL   PRIMARY KEY,
            supply_replace_volume           INTEGER     NOT NULL,
            supply_replace_count_removed    INTEGER     NOT NULL,
            supply_replace_count_added      INTEGER     NOT NULL,
            waste_replace_volume            INTEGER     NOT NULL,
            waste_replace_count_removed     INTEGER     NOT NULL,
            waste_replace_count_added       INTEGER     NOT NULL,
            automatic                       INTEGER     NOT NULL,
            inflow_level_increase           INTEGER     NOT NULL,
            inflow_level_decrease           INTEGER     NOT NULL,
            mute_count                      INTEGER     NOT NULL,
            reset_count                     INTEGER     NOT NULL);''')
        db.close()
        if verbose:
            print(f"table 'user' created in {path} successfully")

    elif file == 'patient':
        path = 'data/patient.json'
        if os.path.exists(path):
            os.remove(path)
            if verbose:
                print(f"removed {path} successfully")
        
        patient = {
            'firstname': '',
            'lastname': '',
            'MRN': 0,
            'birthdate': '00-00-0000',
            'sex': '',
            'contact_A': 1234567890,
            'contact_B': 1234567890,
            'start_date': '00-00-0000',
            'start_time': '00:00'
        }
        
        js = json.dumps(patient, indent=4)
        with open(path, "w") as outfile:
            outfile.write(js)
        if verbose:
            print(f"created {path} successfully")

    else:
        raise Exception(f"file [{file}] not valid")


def add_data(data, file, verbose=False):
    if file == 'system': # adds new entry to Sqlite database
        path = 'data/system.db'
        db = sqlite3.connect(path)
        if verbose:
            print(f"opened {path} successfully")

        data_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in data)

        cursor = db.cursor()
        cursor.execute(f'''INSERT INTO system (entry, hematuria_level, hematuria_percent, supply_percent, 
            supply_volume, supply_time, supply_rate, waste_percent, waste_volume, waste_time, waste_rate, 
            status_level, status_message, active_time, date, time, supply_volume_total, supply_volume_gross, 
            supply_replace_count, waste_volume_total, waste_volume_gross, waste_replace_count, automatic, 
            inflow_level, mute)
            VALUES ({data_formatted})''')
        db.commit()
        db.close()
        if verbose:
            print(f"data added to 'system' in {path} successfully")
    
    elif file == 'user': # adds new entry to Sqlite database
        path = 'data/user.db'
        db = sqlite3.connect(path)
        if verbose:
            print(f"opened {path} successfully")

        data_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in data)

        cursor = db.cursor()
        cursor.execute(f'''INSERT INTO user (entry, supply_replace_volume, supply_replace_count_removed, 
            supply_replace_count_added, waste_replace_volume, waste_replace_count_removed,
            waste_replace_count_added, automatic, inflow_level_incrase, inflow_level_decrease, mute_count, reset_count)
            VALUES ({data_formatted})''')
        db.commit()
        db.close()
        if verbose:
            print(f"data added to 'user' in {path} successfully")

    elif file == 'patient': # overwrites existing JSON data
        path = 'data/patient.json'
        js = json.dumps(data, indent=4)
        with open(path, "w") as outfile:
            outfile.write(js)
        if verbose:
            print(f"data added to {path} successfully")

    else:
        raise Exception(f"file [{file}] not valid")


def get_data(keys, file, n=1, order='DESC', format='list', verbose=False):
    if type(keys) is str or type(keys) is not list:
        keys = [keys]

    if file in ['system', 'user']: # gets entry from Sqlite database
        if file == 'system':
            path = 'data/system.db'
        elif file == 'user':
            path = 'data/user.db'

        db = sqlite3.connect(path)
        if verbose:
            print(f"opened {path} successfully")
        
        cursor = db.cursor()
        keys_formatted = ', '.join(map(str, keys))
 
        if file == 'system':
            selection = cursor.execute(f"SELECT {keys_formatted} FROM system ORDER BY entry {order} LIMIT {int(n)}")
        elif file == 'user':
            selection = cursor.execute(f"SELECT {keys_formatted} FROM user ORDER BY entry {order} LIMIT {int(n)}")
        
        if n == 1:
            for row in selection:
                if len(keys) == 1:
                    data = [row[0]]
                else:
                    data = [x for x in list(row)]
                    # data = [[x] for x in list(row)] # uncomment if single-item list format (i.e., [item]) is wanted for n = 1 condition
            if len(keys) == 1:
                data = dict(zip(keys, data))
                # data = dict(zip(keys, [data])) # uncomment if single-item list format (i.e., [item]) is wanted for n = 1 condition
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
            print(f"data retrieved from {path} successfully")
            
    elif file == 'patient': # gets data from JSON data
        path = 'data/patient.json'
        with open(path, 'r') as infile:
            data = json.load(infile)
        data = {key: data[key] for key in keys}
        if verbose:
            print(f"data retrieved from {path} successfully")

    else:
        raise Exception(f"file [{file}] not valid")
    
    return data


# example implementation
if __name__ == '__main__':
    replace_data(file='system', verbose=True)
    replace_data(file='user', verbose=True)
    replace_data(file='patient', verbose=True)
    
    data_in_2 = [101, 102, 103.0, 104, 105, 106, 107, 108, 109, 110, 111, 'one-hundred twelve', 'one-hundred thirteen', 114, 'one-hundred fifteen', 'one-hundred sixteen', 117, 118, 119, 120, 121, 122, 1, 124, 1]
    add_data(data=data_in_2, file='system', verbose=True)

    data_in_1 = [1, 2, 3.0, 4, 5, 6, 7, 8, 9, 10, 11, 'twelve', 'thirteen', 14, 'fifteen', 'sixteen', 17, 18, 19, 20, 21, 22, 0, 24, 0]
    add_data(data=data_in_1, file='system', verbose=True)

    data_out = get_data(keys=['entry', 'time', 'supply_volume'], file='system', n=2, order='DESC', verbose=True)
    print(data_out)
    
    data_out = get_data(keys='entry', file='system', n=2, order='DESC', verbose=True)
    print(data_out)

    data_out = get_data(keys=['entry', 'time', 'supply_volume'], file='system', n=1, order='DESC', verbose=True)
    print(data_out)
    
    data_out = get_data(keys='entry', file='system', n=1, order='DESC', verbose=True)
    print(data_out)