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
    SYSTEM_TEMPLATE = {
        'entry': 0,
        'hematuria_level': 0,
        'hematuria_percent': 0.0,
        'supply_percent': 0,
        'supply_volume': 0,
        'supply_time': 0,
        'supply_rate': 0,
        'waste_percent': 0,
        'waste_volume': 0,
        'waste_time': 0,
        'waste_rate': 0,
        'status_level': 'NORMAL',
        'status_message': 'System normal',
        'active_time': 0,
        'date': '00/00/0000',
        'time': '00:00:00',
        'supply_volume_total': 0,
        'supply_volume_gross': 0,
        'supply_replace_count': 0,
        'waste_volume_total': 0,
        'waste_volume_gross': 0,
        'waste_replace_count': 0,
        'automatic': True,
        'inflow_level': 0,
        'mute': False
        }

    USER_TEMPLATE = {
        'entry': 0,
        'supply_replace_volume': 0,
        'supply_replace_count_removed': 0,
        'supply_replace_count_added': 0,
        'waste_replace_volume': 0,
        'waste_replace_count_removed': 0,
        'waste_replace_count_added': 0,
        'automatic': True,
        'inflow_level': 0,
        'mute_count': 0,
        'reset_count': 0
        }

    PATIENT_TEMPLATE = {
        'firstname': '–',
        'lastname': '–',
        'MRN': 0,
        'DOB': '00-00-0000',
        'sex': '–',
        'contact_A': 0,
        'contact_B': 0,
        'start_date': '00/00/0000',
        'start_time': '00:00'
        }
    
    if file == 'system':
        path = 'data/system.db'
        if os.path.exists(path): # remove existing database
            os.remove(path)
            if verbose:
                print(f"removed {path} successfully")

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
            mute                    INTEGER     NOT NULL);''') # create new table in database
        db.close()

        add_data(data=SYSTEM_TEMPLATE, file='system', initialize=True)

        if verbose:
            print(f"table 'system' created in {path} successfully with template data")

    elif file == 'user':
        path = 'data/user.db'
        if os.path.exists(path): # remove existing database
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
            inflow_level                    INTEGER     NOT NULL,
            mute_count                      INTEGER     NOT NULL,
            reset_count                     INTEGER     NOT NULL);''') # create new table in database
        db.close()

        add_data(data=USER_TEMPLATE, file='user', initialize=True)

        if verbose:
            print(f"table 'user' created in {path} successfully with template data")

    elif file == 'patient':
        path = 'data/patient.json'
        if os.path.exists(path): # remove existing database
            os.remove(path)
            if verbose:
                print(f"removed {path} successfully")
        
        add_data(data=PATIENT_TEMPLATE, file='patient', initialize=True)

        if verbose:
            print(f"created {path} successfully with template data")

    else:
        raise Exception(f"file [{file}] not valid")


def add_data(data, file, verbose=False, initialize=False):
    if file in ['system', 'user']: # gets most recent entry from Sqlite database and updates given key-value pairs
        if file == 'system':
            path = 'data/system.db'
        elif file == 'user':
            path = 'data/user.db'
    
        db = sqlite3.connect(path)
        if verbose:
            print(f"opened {path} successfully")

        if initialize == False: # if initializing database, do not reference prior entries in database
            old_data = get_data(keys='all', file=file, n=1, order='DESC')
            entry = int(old_data['entry']) + 1
            old_data.update({key: data[key] for key in old_data.keys() & data.keys()})
            old_data.update({'entry': entry})
            data = old_data
        
        keys_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in list(data.keys()))
        values_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in list(data.values()))

        cursor = db.cursor()
        cursor.execute(f'INSERT INTO {file} ({keys_formatted}) VALUES ({values_formatted})')
        db.commit()
        db.close()
        if verbose:
            print(f"data added to '{file}' in {path} successfully")

    elif file == 'patient': # overwrites existing JSON data
        path = 'data/patient.json'
        js = json.dumps(data, indent=4)
        with open(path, "w") as outfile:
            outfile.write(js)
        if verbose:
            print(f"data added to {path} successfully")

    else:
        raise Exception(f"file [{file}] not valid")


def get_data(keys, file, n=1, order='DESC', verbose=False):
    # lists of all keys available for each file
    SYSTEM_KEYS = [
        'entry',
        'hematuria_level', 'hematuria_percent', 'supply_percent', 
        'supply_volume', 'supply_time', 'supply_rate', 'waste_percent', 'waste_volume', 'waste_time', 'waste_rate', 
        'status_level', 'status_message', 'active_time', 'date', 'time', 'supply_volume_total', 'supply_volume_gross', 
        'supply_replace_count', 'waste_volume_total', 'waste_volume_gross', 'waste_replace_count', 'automatic', 
        'inflow_level', 'mute'
        ]
    USER_KEYS = [
        'entry',
        'supply_replace_volume', 'supply_replace_count_removed', 'supply_replace_count_added',
        'waste_replace_volume', 'waste_replace_count_removed', 'waste_replace_count_added',
        'automatic', 'inflow_level',
        'mute_count', 'reset_count'
        ]
    PATIENT_KEYS = [
        'firstname', 'lastname', 'MRN', 'DOB', 'sex',
        'contact_A', 'contact_B',
        'start_date', 'start_time'
        ]
    
    if keys == 'all': # allow keys input to be 'all'
        if file == 'system':
            keys = SYSTEM_KEYS
        elif file == 'user':
            keys = USER_KEYS
        elif file == 'patient':
            keys = PATIENT_KEYS
    
    if type(keys) is str or type(keys) is not list: # ensure keys input is a list
        keys = [keys]

    for key in keys: # check that all key inputs are valid keys for given file
        if file == 'system':
            if key not in SYSTEM_KEYS:
                raise Exception(f"key [{key}] not valid for file [{file}]")
        if file == 'user':
            if key not in USER_KEYS:
                raise Exception(f"key [{key}] not valid for file [{file}]")
        if file == 'patient':
            if key not in PATIENT_KEYS:
                raise Exception(f"key [{key}] not valid for file [{file}]")
            
    if file in ['system', 'user']: # get entry from Sqlite database file
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
        
        data = [None for key in keys]

        if n == 1: # format data before returning
            for row in selection:
                if len(keys) == 1:
                    data = [row[0]]
                else:
                    data = [x for x in list(row)]
                    # data = [[x] for x in list(row)] # uncomment if single-item list format (i.e., [item]) is wanted for n = 1 condition
            if len(keys) == 1:
                data = data[0]
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
                data = data
                # data = dict(zip(keys, [data]))
            else:
                data = {key: list(values) for key, values in zip(keys, zip(*data))}

        if verbose:
            print(f"data retrieved from {path} successfully")
            
    elif file == 'patient': # get data from JSON data
        path = 'data/patient.json'
        with open(path, 'r') as infile:
            data = json.load(infile)
        data = {key: data[key] for key in keys} # format data before returning
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

    # system test data entry 1
    data_in_1 = {
        'hematuria_level': 30,
        'hematuria_percent': 2.5,
        'supply_percent': 20,
        'supply_volume': 9990,
        'supply_time': 321,
        'supply_rate': 24,
        'waste_percent': 94,
        'waste_volume': 2300,
        'waste_time': 123,
        'waste_rate': 92,
        'status_level': 'NORMAL',
        'status_message': 'SYSTEM NORMAL',
        'active_time': 4201,
        'date': '02/17/2024',
        'time': '04:10:12',
        'supply_volume_total': 6000,
        'supply_volume_gross': 12000,
        'supply_replace_count': 2,
        'waste_volume_total': 5000,
        'waste_volume_gross': 10000,
        'waste_replace_count': 2,
        'automatic': True,
        'inflow_level': 42,
        'mute': False
        }
    add_data(data=data_in_1, file='system', verbose=True)

    # system test data entry 2
    data_in_2 = {
        'hematuria_level': 20,
        'hematuria_percent': 5.5,
        'supply_percent': 18,
        'supply_volume': 5120,
        'supply_time': 311,
        'supply_rate': 28,
        'waste_percent': 98,
        'waste_volume': 2500,
        'waste_time': 99,
        'waste_rate': 54,
        'status_level': 'NORMAL',
        'status_message': 'SYSTEM NORMAL',
        'active_time': 4901,
        'date': '02/18/2024',
        'time': '04:10:13',
        'supply_volume_total': 6000,
        'supply_volume_gross': 12000,
        'supply_replace_count': 2,
        'waste_volume_total': 5000,
        'waste_volume_gross': 10000,
        'waste_replace_count': 2,
        'automatic': True,
        'inflow_level': 42,
        'mute': False
        }
    add_data(data=data_in_2, file='system', verbose=True)

    # system test data entry 3
    data_in_3 = {'time': '04:10:59'}
    add_data(data=data_in_3, file='system', verbose=True)

    # n > 1, len(keys) > 1 condition
    data_out = get_data(keys=['entry', 'time', 'supply_volume'], file='system', n=3, order='DESC', verbose=True)
    print(data_out)
    
    # n > 1, len(keys) = 1 condition
    data_out = get_data(keys='entry', file='system', n=3, order='DESC', verbose=True)
    print(data_out)

    # n = 1, len(keys) > 1 condition
    data_out = get_data(keys=['entry', 'time', 'supply_volume'], file='system', n=1, order='DESC', verbose=True)
    print(data_out)
    
    # n = 1, len(keys) = 1 condition
    data_out = get_data(keys='entry', file='system', n=1, order='DESC', verbose=True)
    print(data_out)