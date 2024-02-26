from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM DATA
    path('system', views.system), # GET

    # INTERFACE DATA
    path('interface/supply_replace_volume', views.interface_supply_replace_volume), # POST
    path('interface/supply_replace_removed', views.interface_supply_replace_removed), # POST
    path('interface/supply_replace_added', views.interface_supply_replace_added), # POST

    path('interface/waste_replace_volume', views.interface_waste_replace_volume), # POST
    path('interface/waste_replace_removed', views.interface_waste_replace_removed), # POST
    path('interface/waste_replace_added', views.interface_waste_replace_added), # POST

    path('interface/automatic', views.interface_automatic), # POST
    path('interface/inflow_level_increase', views.interface_inflow_level_increase), # POST
    path('interface/inflow_level_decrease', views.interface_inflow_level_decrease), # POST
    path('interface/mute', views.interface_mute), # POST
    path('interface/setup', views.interface_setup), # POST
    path('interface/reset', views.interface_reset), # POST

    # PATIENT DATA
    path('patient', views.patient) # GET and POST
    ]
