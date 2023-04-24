from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Usuario)

@admin.register(Programador)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('nombre_programador', 'correo_programador')
    #exclude      = ('nombre_programador', 'correo_programador')

admin.site.register(Proyecto)

@admin.register(Cargo)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('programador', 'proyecto')
    #exclude      = ('nombre_programador', 'correo_programador')

@admin.register(ReporteBug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('titulo','fecha_reporte','bug')
    #exclude      = ('id_reporte','titulo','reporte','fecha_reporte','usuario')

@admin.register(Bug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_bug', 'descripcion', 'proyecto', 'programador', 'estado', 'prioridad')
    search_fields = ('proyecto', 'programador')
    #exclude      = ('id_bug', 'descripcion', 'id_proyecto', 'id_programador')
