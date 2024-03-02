from django.urls import path
from . import views

urlpatterns = [
    path('get_hematuria/', views.get_hematuria, name='get_hematuria'),
    path('get_supply/', views.get_supply, name='get_supply'),
]
