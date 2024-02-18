from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM DATA
    path('system', views.system_data),

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
    path('patient', views.patient_data),
]
