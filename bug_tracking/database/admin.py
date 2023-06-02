from typing import Optional
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http.request import HttpRequest
from .models import *
from django.db.models import Count
# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Usuario)
class ReporteBugAdmin(admin.ModelAdmin):
    def has_add_permission(self, request,obj=None):
        return True

    def has_change_permission(self, request,obj=None):
        return False


@admin.register(Programador)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('user',)
    # exclude      = ('nombre_programador', 'correo_programador')


admin.site.register(Proyecto)


@admin.register(Cargo)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_programador', 'cargo', 'id_proyecto')
    
    fieldsets = (
        ('Proyecto', {
            'fields': ('id_proyecto',)
        }),
        ('Información del programador', {
            'fields': ('id_programador', 'cargo')
        })
    )


@admin.register(Bug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display  = ('id_bug', 'titulo', 'id_proyecto',
                    'estado', 'prioridad', 'id_programador')
    
    search_fields = ('id_proyecto', 'id_programador')
    
    list_filter   = ('id_proyecto', 'estado')

    fieldsets     = (
        ('Informacion del Bug', {
            'fields': ('titulo', 'descripcion', 'id_proyecto', 'estado', 'prioridad')
        }),
        ('Personal encargado', {
            'fields': ('id_programador',)
        })
    )


@admin.register(ReporteBug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_reporte','titulo', 'fecha_reporte', 'id_proyecto', 'estado', 'id_bug')
    
    list_filter  = ('estado', 'id_proyecto')
    
    fieldsets    = (
        ('Información entregada por el usuario', {
            'fields': ('titulo', 'reporte', 'id_usuario')
        }),
        ('Información extra', {
            'fields': ('estado', 'id_proyecto', 'id_bug')
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado='PENDIENTE')

    
    def has_add_permission(self, request,obj=None):      
        return True
    
    def has_change_permission(self, request,obj=None):
        return False
    

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):
        return False
    
    
@admin.register(Avances)
class AvancesAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):
        return False
    
    
@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    
    def has_change_permission(self, request,obj=None):
        return False
   
@admin.register(Reasignacion)
class ReasignacionBugAdmin(admin.ModelAdmin):
    list_display = ('id_reasignacion', 'id_bug',
                    'id_programador_inicial', 'id_programador_final', 'fecha_reasignacion')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado='PENDIENTE')
    
    

