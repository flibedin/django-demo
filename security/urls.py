from django.urls import path
from security import views

app_name = 'security'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('user_edit/', views.user_edit, name='user_edit'),

]
