from django.urls import path
from . import views

urlpatterns = [
    # DEVICE DATA
    path('system', views.send_device),

    # INTERFACE DATA
    # SUPPLY
    path('user/supply_replace_volume', views.handle_supply_replace_volume),
    path('user/supply_replace_removed', views.handle_supply_replace_removed),
    path('user/supply_replace_added', views.handle_supply_replace_added),

    # WASTE
    path('user/waste_replace_volume', views.handle_waste_replace_volume),
    path('user/waste_replace_removed', views.handle_waste_replace_removed),
    path('user/waste_replace_added', views.handle_waste_replace_added),

    # CONTROL
    path('user/automatic', views.handle_automatic),
    path('user/inflow_level_increase', views.handle_inflow_level_increase),
    path('user/inflow_level_decrease', views.handle_inflow_level_decrease),
    path('user/clear', views.handle_clear),
    path('user/mute', views.handle_mute),
    path('user/reset', views.handle_reset),

    # PATIENT
    path('user/patient_firstname', views.handle_patient_firstname),
    path('user/patient_lastname', views.handle_patient_lastname),
    path('user/patient_middleinitial', views.handle_patient_middleinitial),
    path('user/patient_ID', views.handle_patient_ID),
    path('user/patient_birthdate', views.handle_patient_birthdate),
    path('user/patient_sex', views.handle_patient_sex),

    # CONTACT
    path('user/contact_A', views.handle_contact_A),
    path('user/contact_B', views.handle_contact_B)
]
