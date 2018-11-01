from django.urls import path
from . import views

app_name = 'banco'

urlpatterns = [
    path('', views.ClienteList.as_view(), name='list'),
    path('query/', views.Query, name='query'),
    path('<int:pk>', views.BancoDetailView, name='detail'),
    path('pdf/<int:pk>', views.BancoPDF, name='cliente_pdf'),
    path('hipotecario/<int:pk>', views.HipotecarioView, name='hipotecario'),

]
