from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM DATA
    path('system', views.get_system_data),

    # USER DATA
    path('user/supply_replace_volume', views.handle_user_supply_replace_volume),
    path('user/supply_replace_removed', views.handle_user_supply_replace_removed),
    path('user/supply_replace_added', views.handle_user_supply_replace_added),

    path('user/waste_replace_volume', views.handle_user_waste_replace_volume),
    path('user/waste_replace_removed', views.handle_user_waste_replace_removed),
    path('user/waste_replace_added', views.handle_user_waste_replace_added),

    path('user/automatic', views.handle_user_automatic),
    path('user/inflow_level_increase', views.handle_user_inflow_level_increase),
    path('user/inflow_level_decrease', views.handle_user_inflow_level_decrease),
    path('user/mute', views.handle_user_mute),
    path('user/reset', views.handle_user_reset),

    # PATIENT DATA
    path('patient', views.get_patient_data),
    
    path('patient/patient_firstname', views.handle_patient_firstname),
    path('patient/patient_lastname', views.handle_patient_lastname),
    path('patient/patient_MRN', views.handle_patient_MRN),
    path('patient/patient_DOB', views.handle_patient_DOB),
    path('patient/patient_sex', views.handle_patient_sex),
    path('patient/contact_A', views.handle_patient_contact_A),
    path('patient/contact_B', views.handle_patient_contact_B)
]
