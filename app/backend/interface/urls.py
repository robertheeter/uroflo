from django.urls import path
from . import views

urlpatterns = [
    path('api/get_update/', views.get_update, name='get_update'),
    path('api/post_update/', views.post_update, name='post_update'),
]