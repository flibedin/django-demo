from django.contrib import admin
from banco.models import  Cliente, Transaccion


# Register your models here.
admin.site.register( Cliente )
admin.site.register( Transaccion )
