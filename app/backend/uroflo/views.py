from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random
import os
from datetime import datetime

import sys
sys.path.append('../backend')

from system.data import *

os.chdir('system')

TESTING = True
VERBOSE = True

# SYSTEM DATA (system.db)
@csrf_exempt
def system_data(request):
    if request.method == 'GET':
        if TESTING:
            response = JsonResponse({'hematuria_level': random.randint(0, 99),
                                    'hematuria_percent': random.uniform(0, 10),

                                    'supply_volume': random.randint(0, 6000),
                                    'supply_time': random.randint(0, 1000),
                                    'supply_rate': random.randint(0, 100),

                                    'waste_volume': random.randint(0, 5000),
                                    'waste_time': random.randint(0, 1000),
                                    'waste_rate': random.randint(0, 100),

                                    'status_level': 'normal',
                                    'status_message': 'This is a test message.',

                                    'active_time': random.randint(0, 2000),

                                    'supply_volume_total': 6000,
                                    'waste_volume_total': 5000
                                    })
            return response
        
        keys = ['hematuria_level', 'hematuria_percent',
                'supply_volume', 'supply_time', 'supply_rate',
                'waste_volume', 'waste_time', 'waste_rate',
                'status_level', 'status_message', 'active_time',
                'supply_volume_total', 'waste_volume_total']
        
        data = get_data(keys=keys, file='system', n=1, order='DESC')
        response = JsonResponse(data)
        return response
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})


# USER DATA (user.db)
@csrf_exempt
def handle_user_supply_replace_volume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            supply_replace_volume = int(data.get('supply_replace_volume', None))
            
            add_data(data={'supply_replace_volume': supply_replace_volume}, file='user')
            if VERBOSE:
                print(f"supply_replace_volume = {supply_replace_volume}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_supply_replace_removed(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('supply_replace_removed', None)
            
            if value == 'TRUE':
                supply_replace_removed = get_data(keys=['supply_replace_removed'], file='user', n=1)
                supply_replace_removed += 1
                add_data(data={'supply_replace_removed': supply_replace_removed}, file='user')
                if VERBOSE:
                    print(f"supply_replace_removed = {supply_replace_removed}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_supply_replace_added(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('supply_replace_added', None)
            
            if value == 'TRUE':
                supply_replace_added = get_data(keys=['supply_replace_added'], file='user', n=1)
                supply_replace_added += 1
                add_data(data={'supply_replace_added': supply_replace_added}, file='user')
                if VERBOSE:
                    print(f"supply_replace_added = {supply_replace_added}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_waste_replace_volume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            waste_replace_volume = int(data.get('waste_replace_volume', None))
            
            add_data(data={'waste_replace_volume': waste_replace_volume}, file='user')
            if VERBOSE:
                print(f"waste_replace_volume = {waste_replace_volume}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_waste_replace_removed(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('waste_replace_removed', None)
            
            if value == 'TRUE':
                waste_replace_removed = get_data(keys=['waste_replace_removed'], file='user', n=1)
                waste_replace_removed += 1
                add_data(data={'waste_replace_removed': waste_replace_removed}, file='user')
                if VERBOSE:
                    print(f"waste_replace_removed = {waste_replace_removed}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_waste_replace_added(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('waste_replace_added', None)
            
            if value == 'TRUE':
                waste_replace_added = get_data(keys=['waste_replace_added'], file='user', n=1)
                waste_replace_added += 1
                add_data(data={'waste_replace_added': waste_replace_added}, file='user')
                if VERBOSE:
                    print(f"waste_replace_added = {waste_replace_added}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_automatic(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('automatic', None)
            
            if value == 'TRUE':
                automatic = True
            elif value == 'FALSE':
                automatic = False
            
            add_data(data={'automatic': automatic}, file='user')
            if VERBOSE:
                print(f"automatic = {automatic}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_inflow_level_increase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('inflow_level_increase', None)
            
            if value == 'TRUE':
                inflow_level = get_data(keys=['inflow_level'], file='user', n=1)
                inflow_level += 1
                add_data(data={'inflow_level': inflow_level}, file='user')
                if VERBOSE:
                    print(f"inflow_level = {inflow_level}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_inflow_level_decrease(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('inflow_level_increase', None)
            
            if value == 'TRUE':
                inflow_level = get_data(keys=['inflow_level'], file='user', n=1)
                inflow_level -= 1
                add_data(data={'inflow_level': inflow_level}, file='user')
                if VERBOSE:
                    print(f"inflow_level = {inflow_level}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_mute(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('mute', None)
            
            if value == 'TRUE':
                mute_count = get_data(keys=['mute_count'], file='user', n=1)
                mute_count += 1
                add_data(data={'mute_count': mute_count}, file='user')
                if VERBOSE:
                    print(f"mute_count = {mute_count}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def handle_user_reset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('reset', None)
            
            if value == 'TRUE':
                reset_count = get_data(keys=['reset_count'], file='user', n=1)
                reset_count += 1
                add_data(data={'reset_count': reset_count}, file='user')
                if VERBOSE:
                    print(f"reset_count = {reset_count}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})


# PATIENT DATA (patient.json)
@csrf_exempt
def patient_data(request):
    if request.method == 'GET':
        if TESTING:
            response = JsonResponse({'firstname': 'PRINCE',
                                    'lastname': 'HUMPERDINCK',
                                    'MRN': random.randint(10000,99999),
                                    'DOB': '01/01/1829',
                                    'sex': 'M',

                                    'contact_A': '(123) 456-7890',
                                    'contact_B': '(421) 512-1231'
                                    })
            return response
        
        keys = ['firstname', 'lastname', 'MRN', 'DOB', 'sex',
                'contact_A', 'contact_B']
        
        data = get_data(keys=keys, file='patient')
        response = JsonResponse(data)
        return response
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            firstname = data.get('firstname', None)
            lastname = data.get('lastname', None)
            MRN = data.get('MRN', None)
            DOB = data.get('DOB', None)
            sex = data.get('sex', None)
            contact_A = data.get('contact_A', None)
            contact_B = data.get('contact_B', None)
            start_date = datetime.now().strftime("%m/%d/%Y")
            start_time = datetime.now().strftime("%H:%M:%S")


            # FINISH THIS
            
            add_data(data={'supply_replace_volume': supply_replace_volume}, file='user')
            if VERBOSE:
                print(f"supply_replace_volume = {supply_replace_volume}")


            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})


# EXAMPLE FROM CHATGPT

# def update_interface_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
            
#             key1_value = data.get('key1', None)
#             key2_value = data.get('key2', None)

#             return JsonResponse({'status': 'success', 'message': 'Request processed.'})
        
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
