from django.http import JsonResponse
import json

# for testing
import random

TESTING = True

def get_update(request):

    if TESTING == True:
        response = JsonResponse({'hematuria_level': random.randint(0, 99),
                                 'hematuria_percent': random.uniform(0, 10),

                                 'supply_percent': random.randint(0, 100),
                                 'supply_time': random.randint(0, 1000),
                                 'supply_volume': random.randint(0, 6000),
                                 'supply_rate': random.randint(0, 100),

                                 'waste_percent': random.randint(0, 100),
                                 'waste_time': random.randint(0, 1000),
                                 'waste_volume': random.randint(0, 5000),
                                 'waste_rate': random.randint(0, 100),

                                 'status_message': 'Normal. This is a test message.',
                                 'status_color': 'yellow',

                                 'active_time': random.randint(0, 1000),
                                 'date': '2014-07-05',
                                 'time': '14:34:14'
                                 })
        return response

    # ADD HERE

    response = JsonResponse({'level': random.randint(0,100)})
    return response

# def post_update(request):
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
