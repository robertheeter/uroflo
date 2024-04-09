from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random
from datetime import datetime
import pytz
import time

import sys
sys.path.append('../backend')

from system.data import *
from system.components.speaker import Speaker

import os
os.chdir('system')

TEST = False # for backend testing
DEMO = True # for showcase demoing
VERBOSE = False # for debugging

speaker = Speaker()
CLICK_SOUND = 'sound/click.mp3'

# SYSTEM DATA (system.db)
@csrf_exempt
def system(request):
    if request.method == 'GET':
        if TEST:
            response = JsonResponse({
                'hematuria_level': random.randint(0, 99),
                'hematuria_percent': random.uniform(0, 10),
                
                'supply_volume': random.randint(0, 6000),
                'supply_time': random.randint(0, 1000),
                'supply_rate': random.randint(0, 100),
                
                'waste_volume': random.randint(0, 5000),
                'waste_time': random.randint(0, 1000),
                'waste_rate': random.randint(0, 100),
                
                'status_level': 'CAUTION',
                'status_message': 'Supply bag volume <10%.',
                
                'active_time': random.randint(0, 2000),

                'supply_volume_total': 6000,
                'waste_volume_total': 5000
                })
            
            return response
        
        if DEMO:
            # hematuria_level = 
            # hematuria_percent = 
            # supply_volume =
            # supply_time = 
            # supply_rate =
            # waste_volume = 
            # waste_rate = 
            # status_level =
            # status_message = 
            # active_time = 
            # supply_volume_total = 
            # waste_volume_total = 
            
            response = JsonResponse({
                'hematuria_level': 40,
                'hematuria_percent': 5,
                
                'supply_volume': 889,
                'supply_time': 118,
                'supply_rate': 22,
                
                'waste_volume': 1541,
                'waste_time': 182,
                'waste_rate': 20,
                
                'status_level': 'NORMAL',
                'status_message': 'System and patient normal.',
                
                'active_time': 153,

                'supply_volume_total': 1000,
                'waste_volume_total': 3000
            })

            return response
        
        keys = [
            'hematuria_level', 'hematuria_percent',
            'supply_volume', 'supply_time', 'supply_rate',
            'waste_volume', 'waste_time', 'waste_rate',
            'status_level', 'status_message', 'active_time',
            'supply_volume_total', 'waste_volume_total'
            ]
        
        data = get_data(key=keys, file='system', n=1, order='DESC')
        response = JsonResponse(data)
        return response
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})


# INTERFACE DATA (interface.db)
@csrf_exempt
def interface_click(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_supply_replace_volume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            supply_replace_volume = int(data.get('supply_replace_volume', None))
            
            time.sleep(0.2)
            add_data(data={'supply_replace_volume': supply_replace_volume}, file='interface')
            if VERBOSE:
                print(f"supply_replace_volume = {supply_replace_volume}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_supply_replace_removed(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('supply_replace_removed', None)
            
            if value == 'TRUE':
                supply_replace_count_removed = get_data(key=['supply_replace_count_removed'], file='interface', n=1)
                supply_replace_count_removed += 1
                add_data(data={'supply_replace_count_removed': supply_replace_count_removed}, file='interface')
                if VERBOSE:
                    print(f"supply_replace_count_removed = {supply_replace_count_removed}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_supply_replace_added(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('supply_replace_added', None)
            
            if value == 'TRUE':
                supply_replace_count_added = get_data(key=['supply_replace_count_added'], file='interface', n=1)
                supply_replace_count_added += 1
                add_data(data={'supply_replace_count_added': supply_replace_count_added}, file='interface')
                if VERBOSE:
                    print(f"supply_replace_count_added = {supply_replace_count_added}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_waste_replace_volume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            waste_replace_volume = int(data.get('waste_replace_volume', None))
            
            time.sleep(0.2)
            add_data(data={'waste_replace_volume': waste_replace_volume}, file='interface')
            if VERBOSE:
                print(f"waste_replace_volume = {waste_replace_volume}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_waste_replace_removed(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('waste_replace_removed', None)
            
            if value == 'TRUE':
                waste_replace_count_removed = get_data(key='waste_replace_count_removed', file='interface', n=1)
                waste_replace_count_removed += 1
                add_data(data={'waste_replace_count_removed': waste_replace_count_removed}, file='interface')
                if VERBOSE:
                    print(f"waste_replace_count_removed = {waste_replace_count_removed}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_waste_replace_added(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('waste_replace_added', None)
            
            if value == 'TRUE':
                waste_replace_count_added = get_data(key='waste_replace_count_added', file='interface', n=1)
                waste_replace_count_added += 1
                add_data(data={'waste_replace_count_added': waste_replace_count_added}, file='interface')
                if VERBOSE:
                    print(f"waste_replace_count_added = {waste_replace_count_added}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_automatic(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('automatic', None)
            
            if value == 'TRUE':
                automatic = True
            elif value == 'FALSE':
                automatic = False
            
            add_data(data={'automatic': automatic}, file='interface')
            if VERBOSE:
                print(f"automatic = {automatic}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_inflow_level_increase(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('inflow_level_increase', None)
            
            if value == 'TRUE':
                inflow_level = get_data(key='inflow_level', file='interface', n=1)
                inflow_level += 1
                add_data(data={'inflow_level': inflow_level}, file='interface')
                if VERBOSE:
                    print(f"inflow_level = {inflow_level}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_inflow_level_decrease(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('inflow_level_decrease', None)
            
            if value == 'TRUE':
                inflow_level = get_data(key='inflow_level', file='interface', n=1)
                inflow_level -= 1
                add_data(data={'inflow_level': inflow_level}, file='interface')
                if VERBOSE:
                    print(f"inflow_level = {inflow_level}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_mute(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('mute', None)
            
            if value == 'TRUE':
                mute_count = get_data(key='mute_count', file='interface', n=1)
                mute_count += 1
                add_data(data={'mute_count': mute_count}, file='interface')
                if VERBOSE:
                    print(f"mute_count = {mute_count}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})

@csrf_exempt
def interface_setup(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('setup', None)
            
            if value == 'TRUE':
                add_data(data={'setup': True}, file='interface')
                if VERBOSE:
                    print(f"setup = {True}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})
    
@csrf_exempt
def interface_reset(request):
    if request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            data = json.loads(request.body.decode('utf-8'))
            value = data.get('reset', None)
            
            if value == 'TRUE':
                setup = get_data(key='setup', file='interface')
                if setup == True:
                    add_data(data={'reset': True}, file='interface')
                    if VERBOSE:
                        print(f"reset = {True}")
                else:
                    if VERBOSE:
                        print(f"cannot set rest = True until setup == True")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})


# PATIENT DATA (patient.json)
@csrf_exempt
def patient(request):
    if request.method == 'GET':
        if TEST:
            response = JsonResponse({
                'firstname': 'JOHN',
                'lastname': 'DOE',
                'MRN': 1234567890,
                'DOB': '01/01/1900',
                'sex': 'M',
                
                'contact_A': '(123) 456-7890',
                'contact_B': '(421) 512-1231'
                })

            return response

        keys = ['firstname', 'lastname', 'MRN', 'DOB', 'sex',
                'contact_A', 'contact_B']
        
        data = get_data(key=keys, file='patient')
        response = JsonResponse(data)
        return response
    
    elif request.method == 'POST':
        try:
            speaker.play(file=CLICK_SOUND)
            patient = json.loads(request.body.decode('utf-8'))
            
            start_date = datetime.now(pytz.utc).strftime("%m/%d/%Y")
            start_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
            patient.update({'start_date': start_date, 'start_time': start_time})

            add_data(data=patient, file='patient')
            if VERBOSE:
                print(f"patient = {patient}")

            return JsonResponse({'status': 'success', 'message': 'request processed'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'invalid JSON'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid request method'})
