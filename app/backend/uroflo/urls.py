from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM DATA
    path('system', views.system_data), # GET

    # USER DATA
    path('user/supply_replace_volume', views.handle_user_supply_replace_volume), # POST
    path('user/supply_replace_removed', views.handle_user_supply_replace_removed), # POST
    path('user/supply_replace_added', views.handle_user_supply_replace_added), # POST

    path('user/waste_replace_volume', views.handle_user_waste_replace_volume), # POST
    path('user/waste_replace_removed', views.handle_user_waste_replace_removed), # POST
    path('user/waste_replace_added', views.handle_user_waste_replace_added), # POST

    path('user/automatic', views.handle_user_automatic), # POST
    path('user/inflow_level_increase', views.handle_user_inflow_level_increase), # POST
    path('user/inflow_level_decrease', views.handle_user_inflow_level_decrease), # POST
    path('user/mute', views.handle_user_mute), # POST
    path('user/reset', views.handle_user_reset), # POST

    # PATIENT DATA
    path('patient', views.patient_data) # GET and POST
    ]
