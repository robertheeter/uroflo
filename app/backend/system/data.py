'''
DATA

Notes
- Wrapper functions for creating, deleting, updating, and querying databases

- Uses SQLite3 database format for system.db and interface.db
- Uses JSON format for patient.json and hematuria.json

Documentation
- SQLite3 data types: https://www.sqlite.org/datatype3.html

'''

import os
import sqlite3
import json


# template entries for each file
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
    'status_level': 'RESET',
    'status_message': 'System must be reset with new patient.',
    'active_time': 0,
    'current_date': '00/00/0000',
    'current_time': '00:00:00',
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

INTERFACE_TEMPLATE = {
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
    'setup': False,
    'reset': False
    }

PATIENT_TEMPLATE = {
    'firstname': '',
    'lastname': '',
    'MRN': 0,
    'DOB': '00/00/0000',
    'sex': 'N',
    'contact_A': 0,
    'contact_B': 0,
    'start_date': '00/00/0000',
    'start_time': '00:00:00'
    }

HEMATURIA_TEMPLATE = {
    'hematuria_percent': 0,
    'hematuria_level': 0,
    'hematuria_violet': 0,
    'hematuria_blue': 0,
    'hematuria_green': 0,
    'hematuria_yellow': 0,
    'hematuria_orange': 0,
    'hematuria_red': 0
    }

# all keys available for each file
SYSTEM_KEYS = [
    'entry',
    'hematuria_level', 'hematuria_percent', 'supply_percent', 
    'supply_volume', 'supply_time', 'supply_rate', 'waste_percent', 'waste_volume', 'waste_time', 'waste_rate', 
    'status_level', 'status_message', 'active_time', 'current_date', 'current_time', 'supply_volume_total', 'supply_volume_gross', 
    'supply_replace_count', 'waste_volume_total', 'waste_volume_gross', 'waste_replace_count', 'automatic', 
    'inflow_level', 'mute'
    ]

INTERFACE_KEYS = [
    'entry',
    'supply_replace_volume', 'supply_replace_count_removed', 'supply_replace_count_added',
    'waste_replace_volume', 'waste_replace_count_removed', 'waste_replace_count_added',
    'automatic', 'inflow_level',
    'mute_count', 'setup', 'reset'
    ]

PATIENT_KEYS = [
    'firstname', 'lastname', 'MRN', 'DOB', 'sex',
    'contact_A', 'contact_B',
    'start_date', 'start_time'
    ]

HEMATURIA_KEYS = [
    'hematuria_percent', 'hematuria_level',
    'hematuria_violet', 'hematuria_blue', 'hematuria_green', 'hematuria_yellow', 'hematuria_orange', 'hematuria_red'
    ]
    

def exists_data(file, verbose=False):
    if file == 'system':
        path = 'data/system.db'
    elif file == 'interface':
        path = 'data/interface.db'
    elif file == 'patient':
        path = 'data/patient.json'
    elif file == 'hematuria':
        path = 'data/hematuria.json'
    else:
        raise Exception(f"file [{file}] not valid")
    
    return os.path.isfile(path)


def delete_data(file, verbose=False):
    if file == 'system':
        path = 'data/system.db'
    elif file == 'interface':
        path = 'data/interface.db'
    elif file == 'patient':
        path = 'data/patient.json'
    elif file == 'hematuria':
        path = 'data/hematuria.json'
    else:
        raise Exception(f"file [{file}] not valid")

    if exists_data(file=file): # remove database if it exists
        os.remove(path)
        if verbose:
            print(f"removed {path} successfully")
    else:
        if verbose:
            print(f"path {path} does not exist")


def create_data(file, verbose=False):
    if file == 'system':
        path = 'data/system.db'
    elif file == 'interface':
        path = 'data/interface.db'
    elif file == 'patient':
        path = 'data/patient.json'
    elif file == 'hematuria':
        path = 'data/hematuria.json'
    else:
        raise Exception(f"file [{file}] not valid")
    
    if exists_data(file=file):
        if verbose:
            print(f"path {path} already exists")
        return
    
    if file == 'system':
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
            current_date            TEXT        NOT NULL,
            current_time            TEXT        NOT NULL,
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

    elif file == 'interface':
        db = sqlite3.connect(path)

        if verbose:
            print(f"created {path} successfully")
        
        db.execute('''CREATE TABLE IF NOT EXISTS interface (
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
            setup                           INTEGER     NOT NULL,
            reset                           INTEGER     NOT NULL);''') # create new table in database
        db.close()

        add_data(data=INTERFACE_TEMPLATE, file='interface', initialize=True)

        if verbose:
            print(f"table 'interface' created in {path} successfully with template data")

    elif file == 'patient':
        add_data(data=PATIENT_TEMPLATE, file='patient', initialize=True)

        if verbose:
            print(f"created {path} successfully with template data")

    elif file == 'hematuria':
        add_data(data=HEMATURIA_TEMPLATE, file='hematuria', initialize=True)

        if verbose:
            print(f"created {path} successfully with template data")


def add_data(data, file, verbose=False, initialize=False):
    if file == 'system':
        path = 'data/system.db'
    elif file == 'interface':
        path = 'data/interface.db'
    elif file == 'patient':
        path = 'data/patient.json'
    elif file == 'hematuria':
        path = 'data/hematuria.json'
    else:
        raise Exception(f"file [{file}] not valid")
    
    if not exists_data(file=file) and file in ['system', 'interface']:
        if verbose:
            print(f"path {path} does not exist")
        return
    
    if file in ['system', 'interface']: # gets most recent entry from Sqlite database and updates given key-value pairs
        db = sqlite3.connect(path)

        if verbose:
            print(f"opened {path} successfully")

        if initialize == False: # if initializing database, do not reference prior entries in database
            old_data = get_data(key='all', file=file, n=1, order='DESC')
            entry = int(old_data['entry']) + 1
            old_data.update({k: data[k] for k in old_data.keys() & data.keys()})
            old_data.update({'entry': entry})
            data = old_data
        
        key_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in list(data.keys()))
        values_formatted = ', '.join(f"'{item}'" if isinstance(item, str) else str(item) for item in list(data.values()))

        cursor = db.cursor()
        cursor.execute(f'INSERT INTO {file} ({key_formatted}) VALUES ({values_formatted})')
        db.commit()
        db.close()

        if verbose:
            print(f"data added to '{file}' in {path} successfully")

    elif file == 'patient': # overwrites existing JSON data
        js = json.dumps(data, indent=4)
        with open(path, "w") as outfile:
            outfile.write(js)

        if verbose:
            print(f"data added to {path} successfully")

    elif file == 'hematuria': # overwrites existing JSON data
        js = json.dumps(data, indent=4)
        with open(path, "w") as outfile:
            outfile.write(js)

        if verbose:
            print(f"data added to {path} successfully")


def get_data(key, file, n=1, order='DESC', verbose=False):
    if file == 'system':
        path = 'data/system.db'
    elif file == 'interface':
        path = 'data/interface.db'
    elif file == 'patient':
        path = 'data/patient.json'
    elif file == 'hematuria':
        path = 'data/hematuria.json'
    else:
        raise Exception(f"file [{file}] not valid")

    if key == 'all': # allow keys input to be 'all'
        if file == 'system':
            key = SYSTEM_KEYS
        elif file == 'interface':
            key = INTERFACE_KEYS
        elif file == 'patient':
            key = PATIENT_KEYS
        elif file == 'hematuria':
            key = HEMATURIA_KEYS
    
    if type(key) is str or type(key) is not list: # ensure keys input is a list
        key = [key]
    
    for k in key: # check that all key inputs are valid keys for given file
        if file == 'system':
            if k not in SYSTEM_KEYS:
                raise Exception(f"key [{k}] not valid for file [{file}]")
        if file == 'interface':
            if k not in INTERFACE_KEYS:
                raise Exception(f"key [{k}] not valid for file [{file}]")
        if file == 'patient':
            if k not in PATIENT_KEYS:
                raise Exception(f"key [{k}] not valid for file [{file}]")
        if file == 'hematuria':
            if k not in HEMATURIA_KEYS:
                raise Exception(f"key [{k}] not valid for file [{file}]")
    
    if not exists_data(file=file):
        if verbose:
            print(f"path {path} does not exist")
        if file == 'system':
            template = SYSTEM_TEMPLATE
        elif file == 'interface':
            template = INTERFACE_TEMPLATE
        elif file == 'patient':
            template = PATIENT_TEMPLATE
        elif file == 'hematuria':
            template = HEMATURIA_TEMPLATE
        return {k: template[k] for k in key}
    
    if file in ['system', 'interface']: # get entry from Sqlite database file
        key_formatted = ', '.join(map(str, key))

        db = sqlite3.connect(path)

        if verbose:
            print(f"opened {path} successfully")
        
        cursor = db.cursor()
        selection = cursor.execute(f"SELECT {key_formatted} FROM {file} ORDER BY entry {order} LIMIT {int(n)}")

        data = [None for k in key]

        if n == 1: # format data before returning
            for row in selection:
                if len(key) == 1:
                    data = [row[0]]
                else:
                    data = [x for x in list(row)]
                    # data = [[x] for x in list(row)] # uncomment if single-item list format (i.e., [item]) is wanted for n = 1 condition
            if len(key) == 1:
                data = data[0]
                # data = dict(zip(key, [data])) # uncomment if single-item list format (i.e., [item]) is wanted for n = 1 condition
            else:
                data = dict(zip(key, data))

        elif n > 1:
            data = []
            for row in selection:
                if len(key) == 1:
                    row = row[0]
                else:
                    row = list(row)
                data.append(row)
            if len(key) == 1:
                data = data
                # data = dict(zip(key, [data]))
            else:
                data = {k: list(values) for k, values in zip(key, zip(*data))}

        if verbose:
            print(f"data retrieved from {path} successfully")
            
    elif file == 'patient': # get data from JSON data
        with open(path, 'r') as infile:
            data = json.load(infile)

        if len(key) == 1:
            data = data[key[0]]
        else:
            data = {k: data[k] for k in key} # format data before returning

        if verbose:
            print(f"data retrieved from {path} successfully")
    
    elif file == 'hematuria': # get data from JSON data
        with open(path, 'r') as infile:
            data = json.load(infile)
        
        if len(key) == 1:
            data = data[key[0]]
        else:
            data = {k: data[k] for k in key} # format data before returning
        
        if verbose:
            print(f"data retrieved from {path} successfully")
    
    return data


def remove_data(file, n=1, order='ASC', verbose=False):
    if file == 'system':
        path = 'data/system.db'
    elif file == 'interface':
        path = 'data/interface.db'
    elif file == 'patient':
        path = 'data/patient.json'
    elif file == 'hematuria':
        path = 'data/hematuria.json'
    else:
        raise Exception(f"file [{file}] not valid")
    
    if not exists_data(file=file):
        if verbose:
            print(f"path {path} does not exist")
        return
    
    if file in ['system', 'interface']: # remove oldest entry from Sqlite database file
        db = sqlite3.connect(path)

        if verbose:
            print(f"opened {path} successfully")
        
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {file} WHERE entry IN (SELECT entry FROM {file} ORDER BY entry {order} LIMIT {int(n)})")
        db.commit()
        db.close()

        if verbose:
            print(f"data removed from {path} successfully")

    elif file == 'patient':
        delete_data('patient')
        create_data('patient')

        if verbose:
            print(f"data removed from {path} successfully")
    
    elif file == 'hematuria':
        delete_data('hematuria')
        create_data('hematuria')

        if verbose:
            print(f"data removed from {path} successfully")
    
    else:
        raise Exception(f"file [{file}] not valid")


# example implementation
def example():
    # test delete_data
    delete_data(file='system', verbose=True)
    delete_data(file='interface', verbose=True)
    delete_data(file='patient', verbose=True)
    delete_data(file='hematuria', verbose=True)

    # test create_data
    create_data(file='system', verbose=True)
    create_data(file='interface', verbose=True)
    create_data(file='patient', verbose=True)
    create_data(file='hematuria', verbose=True)

    # test add_data
    # entry 1
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
        'current_date': '02/17/2024',
        'current_time': '04:10:12',
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

    # entry 2
    data_in_2 = {
        'hematuria_level': 20,
        'hematuria_percent': 0.5,
        'supply_percent': 18,
        'supply_volume': 5120,
        'supply_time': 311,
        'supply_rate': 28,
        'waste_percent': 98,
        'waste_volume': 2500,
        'waste_time': 99,
        'waste_rate': 54,
        'status_level': 'CAUTION',
        'status_message': 'Waste bag almost full',
        'active_time': 4901,
        'current_date': '02/18/2024',
        'current_time': '04:10:13',
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

    # entry 3
    data_in_3 = {'current_time': '04:10:59'}
    add_data(data=data_in_3, file='system', verbose=True)

    # test get_data
    # n > 1, len(key) > 1 condition
    data_out = get_data(key=['entry', 'current_time', 'supply_volume'], file='system', n=3, order='DESC', verbose=True)
    print(data_out)
    
    # n > 1, len(key) = 1 condition
    data_out = get_data(key='entry', file='system', n=3, order='DESC', verbose=True)
    print(data_out)

    # n = 1, len(key) > 1 condition
    data_out = get_data(key=['entry', 'current_time', 'supply_volume'], file='system', n=1, order='DESC', verbose=True)
    print(data_out)
    
    # n = 1, len(key) = 1 condition
    data_out = get_data(key='entry', file='system', n=5, order='DESC', verbose=True)
    print(data_out)

    # test remove_data
    remove_data(file='system', n=1, order='ASC', verbose=True)

    data_out = get_data(key='entry', file='system', n=3, order='DESC', verbose=True)
    print(data_out)


if __name__ == '__main__':
    # run example implementation
    # example()

    # remove any existing data
    delete_data(file='system', verbose=True)
    delete_data(file='interface', verbose=True)
    delete_data(file='patient', verbose=True)
    delete_data(file='hematuria', verbose=True)
