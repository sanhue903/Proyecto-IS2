from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *
# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Usuario)
class ReporteBugAdmin(admin.ModelAdmin):
    #exclude      = ('correo_usuario',)
    pass


@admin.register(Programador)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('nombre_programador', 'correo_programador')
    #exclude      = ('nombre_programador', 'correo_programador')

admin.site.register(Proyecto)

@admin.register(Cargo)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_programador', 'id_proyecto')
    #exclude      = ('nombre_programador', 'correo_programador')

@admin.register(ReporteBug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('titulo','fecha_reporte','id_bug')
    #exclude      = ('id_reporte','titulo','reporte','fecha_reporte','usuario')

@admin.register(Bug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_bug', 'descripcion', 'id_proyecto', 'id_programador', 'estado', 'prioridad')
    search_fields = ('id_proyecto', 'id_programador') #'proyecto'
    #exclude      = ('id_bug', 'descripcion', 'id_proyecto', 'id_programador')

