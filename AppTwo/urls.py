from django.urls import path
from AppTwo import views

app_name = 'AppTwo'

urlpatterns = [
    path('', views.users, name='users'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('edit/', views.edit, name='edit'),
    path('special/', views.special, name='views.special'),
    ]
