from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM DATA
    path('system', views.system), # GET

    # USER DATA
    path('user/supply_replace_volume', views.user_supply_replace_volume), # POST
    path('user/supply_replace_removed', views.user_supply_replace_removed), # POST
    path('user/supply_replace_added', views.user_supply_replace_added), # POST

    path('user/waste_replace_volume', views.user_waste_replace_volume), # POST
    path('user/waste_replace_removed', views.user_waste_replace_removed), # POST
    path('user/waste_replace_added', views.user_waste_replace_added), # POST

    path('user/automatic', views.user_automatic), # POST
    path('user/inflow_level_increase', views.user_inflow_level_increase), # POST
    path('user/inflow_level_decrease', views.user_inflow_level_decrease), # POST
    path('user/mute', views.user_mute), # POST
    path('user/setup', views.user_setup), # POST
    path('user/reset', views.user_reset), # POST

    # PATIENT DATA
    path('patient', views.patient) # GET and POST
    ]
