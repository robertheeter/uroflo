from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random

from .system.data import *

TESTING = True


# SYSTEM DATA (system.db)
def get_system_data(request):
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
    
    response = None
    return response


# USER DATA (user.db)
@csrf_exempt
def handle_supply_replace_volume(request):
    response = None
    return response

@csrf_exempt
def handle_supply_replace_removed(request):
    response = None
    return response

@csrf_exempt
def handle_supply_replace_added(request):
    response = None
    return response

@csrf_exempt
def handle_waste_replace_volume(request):
    response = None
    return response

@csrf_exempt
def handle_waste_replace_removed(request):
    response = None
    return response

@csrf_exempt
def handle_waste_replace_added(request):
    response = None
    return response

@csrf_exempt
def handle_automatic(request):
    response = None
    return response

@csrf_exempt
def handle_inflow_level_increase(request):
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
def handle_inflow_level_decrease(request):
    response = None
    return response

@csrf_exempt
def handle_mute(request):
    response = None
    return response

@csrf_exempt
def handle_reset(request):
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
    if TESTING == True:
        response = JsonResponse({'firstname': 'PRINCE',
                                 'lastname': 'HUMPERDINCK',
                                 'MRN': random.randint(10000,99999),
                                 'DOB': '01:01:1829',
                                 'sex': 'M',

                                 'contact_A': random.randint(1000000000, 9999999999),
                                 'contact_B': random.randint(1000000000, 9999999999)
                                 })
        return response
    
    response = None
    return response

@csrf_exempt
def handle_patient_firstname(request):
    response = None
    return response

@csrf_exempt
def handle_patient_lastname(request):
    response = None
    return response

@csrf_exempt
def handle_patient_MRN(request):
    response = None
    return response

@csrf_exempt
def handle_patient_DOB(request):
    response = None
    return response

@csrf_exempt
def handle_patient_sex(request):
    response = None
    return response

@csrf_exempt
def handle_patient_contact_A(request):
    response = None
    return response

@csrf_exempt
def handle_patient_contact_B(request):
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
