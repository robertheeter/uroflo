from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random
import os

from .data import *

TESTING = False


# SYSTEM DATA (system.db)
def get_system_data(request):
    print(os.getcwd())
    
    if TESTING == True:
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

                                 'active_time': random.randint(0, 1000),

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


# USER DATA (user.db)
@csrf_exempt
def handle_user_supply_replace_volume(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_supply_replace_removed(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_supply_replace_added(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_waste_replace_volume(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_waste_replace_removed(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_waste_replace_added(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_automatic(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_inflow_level_increase(request):
    os.chdir("system")

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            key1_value = data.get('inflow_level_increase', None)
            # key2_value = data.get('key2', None)
            print('SUCCESS')
            print(key1_value)
            return JsonResponse({'status': 'success', 'message': 'Request processed.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


    response = None
    return response

@csrf_exempt
def handle_user_inflow_level_decrease(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_mute(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_user_reset(request):
    os.chdir("system")

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            key1_value = data.get('inflow_level_increase', None)
            # key2_value = data.get('key2', None)
            print('RESET YEEHAW')
            print(key1_value)
            return JsonResponse({'status': 'success', 'message': 'Request processed.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


    response = None
    return response


# PATIENT DATA (patient.json)
def get_patient_data(request):
    os.chdir("system")

    if TESTING == True:
        response = JsonResponse({'firstname': 'PRINCE',
                                 'lastname': 'HUMPERDINCK',
                                 'MRN': random.randint(10000,99999),
                                 'DOB': '01-01-1829',
                                 'sex': 'M',

                                 'contact_A': random.randint(1000000000, 9999999999),
                                 'contact_B': random.randint(1000000000, 9999999999)
                                 })
        return response
    
    response = None
    return response

@csrf_exempt
def handle_patient_firstname(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_patient_lastname(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_patient_MRN(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_patient_DOB(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_patient_sex(request):
    os.chdir("system")
    
    response = None
    return response

@csrf_exempt
def handle_patient_contact_A(request):
    os.chdir("system")

    response = None
    return response

@csrf_exempt
def handle_patient_contact_B(request):
    os.chdir("system")

    response = None
    return response




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
