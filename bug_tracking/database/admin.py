from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *
# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Usuario)
class ReporteBugAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj= None):
        return False

#dasasdas
@admin.register(Programador)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('nombre_programador', 'correo_programador')
    #exclude      = ('nombre_programador', 'correo_programador') 

admin.site.register(Proyecto)

@admin.register(Cargo)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_programador', 'id_proyecto')
    #exclude      = ('nombre_programador', 'correo_programador')


@admin.register(Bug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_bug', 'descripcion', 'id_proyecto', 'id_programador', 'estado', 'prioridad')
    search_fields = ('id_proyecto', 'id_programador') 
    list_filter = ('id_proyecto', 'estado')
    
    fieldsets = (
        ('Informacion del Bug', {
            'fields': ('descripcion', 'id_proyecto', 'estado', 'prioridad')
        }),
        ('Personal encargado', {
            'fields': ('id_programador',)
        })
    )


@admin.register(ReporteBug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('titulo','fecha_reporte','id_bug')
    list_filter = ('estado',)
    #exclude      = ('id_reporte','titulo','reporte','fecha_reporte','correo_usuario')
    
    def has_add_permission(self, request):
        return False
    
    