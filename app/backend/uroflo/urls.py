from django.urls import path
from . import views

urlpatterns = [
    # DEVICE DATA
    path('device', views.send_device),

    # INTERFACE DATA
    # SUPPLY
    path('control/supply_replace_volume', views.handle_supply_replace_volume),
    path('control/supply_replace_removed', views.handle_supply_replace_removed),
    path('control/supply_replace_added', views.handle_supply_replace_added),

    # WASTE
    path('control/waste_replace_volume', views.handle_waste_replace_volume),
    path('control/waste_replace_removed', views.handle_waste_replace_removed),
    path('control/waste_replace_added', views.handle_waste_replace_added),

    # CONTROL
    path('control/automatic', views.handle_automatic),
    path('control/inflow_level_increase', views.handle_inflow_level_increase),
    path('control/inflow_level_decrease', views.handle_inflow_level_decrease),
    path('control/clear', views.handle_clear),
    path('control/mute', views.handle_mute),
    path('control/reset', views.handle_reset),

    # PATIENT
    path('control/patient_firstname', views.handle_patient_firstname),
    path('control/patient_lastname', views.handle_patient_lastname),
    path('control/patient_middleinitial', views.handle_patient_middleinitial),
    path('control/patient_ID', views.handle_patient_ID),
    path('control/patient_birthdate', views.handle_patient_birthdate),
    path('control/patient_sex', views.handle_patient_sex),

    # CONTACT
    path('control/contact_A', views.handle_contact_A),
    path('control/contact_B', views.handle_contact_B)
]
