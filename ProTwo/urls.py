"""ProTwo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from AppTwo import views, auth_views

urlpatterns = [
    path( '', views.index, name='views.index'),
    path( 'users/', include('AppTwo.urls')),
    path( 'school/', include('school.urls')),
    path( 'banco/', include('banco.urls')),

    path('admin/', admin.site.urls),
    path('register/', auth_views.register, name='views.register'),
    path('logout/', auth_views.user_logout, name='logout'),
    path('user_login/', auth_views.user_login, name='user_login'),
    path('user_detail/', auth_views.user_detail, name='user_detail'),
    path('user_edit/', auth_views.user_edit, name='user_edit'),
    path('empresa/',views.EmpresaView.as_view(),name='empresa'),
    path('productos/',views.ProductosView.as_view(),name='productos'),



]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
