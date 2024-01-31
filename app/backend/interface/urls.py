from django.urls import path
from . import views

urlpatterns = [
    # DEVICE DATA
    path('api/device/', views.send_device),

    # INTERFACE DATA
    # SUPPLY
    path('api/interface/supply_replace_volume', views.handle_supply_replace_volume),
    path('api/interface/supply_replace_removed', views.handle_supply_replace_removed),
    path('api/interface/supply_replace_added', views.handle_supply_replace_added),

    # WASTE
    path('api/interface/waste_replace_volume', views.handle_waste_replace_volume),
    path('api/interface/waste_replace_removed', views.handle_waste_replace_removed),
    path('api/interface/waste_replace_added', views.handle_waste_replace_added),

    # CONTROL
    path('api/interface/automatic', views.handle_automatic),
    path('api/interface/inflow_level_increase', views.handle_inflow_level_increase),
    path('api/interface/inflow_level_decrease', views.handle_inflow_level_decrease),
    path('api/interface/clear', views.handle_clear),
    path('api/interface/mute', views.handle_mute),
    path('api/interface/reset', views.handle_reset),

    # PATIENT
    path('api/interface/patient_firstname', views.handle_patient_firstname),
    path('api/interface/patient_lastname', views.handle_patient_lastname),
    path('api/interface/patient_middleinitial', views.handle_patient_middleinitial),
    path('api/interface/patient_ID', views.handle_patient_ID),
    path('api/interface/patient_birthdate', views.handle_patient_birthdate),
    path('api/interface/patient_sex', views.handle_patient_sex),

    # CONTACT
    path('api/interface/contact_A', views.handle_contact_A),
    path('api/interface/contact_B', views.handle_contact_B)
]
