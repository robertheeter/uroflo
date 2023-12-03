# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_hematuria/', views.get_hematuria, name='get_hematuria'),
    path('get_saline_weight/', views.get_saline_weight, name='get_saline_weight'),
]
