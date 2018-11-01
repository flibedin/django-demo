from django.contrib import admin
from banco.models import  Cliente, Transaccion, Hipotecario


# Register your models here.
admin.site.register( Cliente )
admin.site.register( Transaccion )
admin.site.register( Hipotecario )

