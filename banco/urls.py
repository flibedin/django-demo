from django.urls import path
from . import views

app_name = 'banco'

urlpatterns = [
    path('', views.ClienteList.as_view(), name='list'),
    path('query/', views.Query, name='query'),
    path( '<int:pk>', views.BancoDetailView.as_view(), name='detail'),

    ]
