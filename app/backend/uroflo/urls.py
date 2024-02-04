from django.urls import path
from . import views

urlpatterns = [
    # DEVICE DATA
    path('device', views.send_device),

    # INTERFACE DATA
    # SUPPLY
    path('interface/supply_replace_volume', views.handle_supply_replace_volume),
    path('interface/supply_replace_removed', views.handle_supply_replace_removed),
    path('interface/supply_replace_added', views.handle_supply_replace_added),

    # WASTE
    path('interface/waste_replace_volume', views.handle_waste_replace_volume),
    path('interface/waste_replace_removed', views.handle_waste_replace_removed),
    path('interface/waste_replace_added', views.handle_waste_replace_added),

    # CONTROL
    path('interface/automatic', views.handle_automatic),
    path('interface/inflow_level_increase', views.handle_inflow_level_increase),
    path('interface/inflow_level_decrease', views.handle_inflow_level_decrease),
    path('interface/clear', views.handle_clear),
    path('interface/mute', views.handle_mute),
    path('interface/reset', views.handle_reset),

    # PATIENT
    path('interface/patient_firstname', views.handle_patient_firstname),
    path('interface/patient_lastname', views.handle_patient_lastname),
    path('interface/patient_middleinitial', views.handle_patient_middleinitial),
    path('interface/patient_ID', views.handle_patient_ID),
    path('interface/patient_birthdate', views.handle_patient_birthdate),
    path('interface/patient_sex', views.handle_patient_sex),

    # CONTACT
    path('interface/contact_A', views.handle_contact_A),
    path('interface/contact_B', views.handle_contact_B)
]
