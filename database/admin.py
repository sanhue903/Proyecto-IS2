from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Usuario)
admin.site.register(Programador)
admin.site.register(Proyecto)
admin.site.register(ReporteBug)
admin.site.register(Prioridad)
admin.site.register(Estado)
admin.site.register(Bug)