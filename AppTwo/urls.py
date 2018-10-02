from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='views.users'),
    path('<first_name>-<last_name>/edit/', views.edit, name='views.edit'),
    path('edit/', views.edit, name='views.edit'),
    path('special/', views.special, name='views.special'),
    ]
