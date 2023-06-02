from typing import Optional
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http.request import HttpRequest
from .models import *
from django.db.models import Count
from django import forms
from django.forms import ModelChoiceField
# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Usuario)
class ReporteBugAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Programador)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('nombre_programador', 'correo_programador')
    # exclude      = ('nombre_programador', 'correo_programador')


admin.site.register(Proyecto)


@admin.register(Cargo)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_programador', 'id_proyecto')
    # exclude      = ('nombre_programador', 'correo_programador')


@admin.register(Bug)
class ReporteBugAdmin(admin.ModelAdmin):
    list_display = ('id_bug', 'descripcion', 'id_proyecto',
                    'id_programador', 'estado', 'prioridad')
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
    list_display = ('titulo', 'fecha_reporte', 'id_proyecto', 'id_bug', 'estado')
    list_filter = ('estado', 'id_proyecto')
    # exclude      = ('id_reporte','titulo','reporte','fecha_reporte','correo_usuario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado='PENDIENTE')

    
    def has_add_permission(self, request):      
        return True
    

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False
    
    
@admin.register(Avances)
class AvancesAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request):
        return False
    
    
@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    
    
    def has_change_permission(self, request):
        return False

class ProgramadorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        total_bugs = obj.bug_set.count()
        bugs_baja = obj.bug_set.filter(prioridad='BAJA').count()
        bugs_media = obj.bug_set.filter(prioridad='MEDIA').count()
        bugs_alta = obj.bug_set.filter(prioridad='ALTA').count()
        bugs_urgente = obj.bug_set.filter(prioridad='URGENTE').count()
        
        return f'{obj.nombre_programador} -  TOTAL BUGS: {total_bugs} | BAJA: {bugs_baja} | MEDIA: {bugs_media} | ALTA: {bugs_alta} | URGENTE: {bugs_urgente}'
        #return f'{obj.nombre_programador} ({obj.bug_set.count()} bugs asociados)'
    
class ReasignacionBugAdmin(admin.ModelAdmin):
    list_display = ('id_reasignacion', 'id_bug',
                    'id_programador_inicial', 'fecha_reasignacion')
    #'id_programador_final_display'
    #readonly_fields = ('id_programador_inicial','id_bug')


    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Programadores involucrados', {
                'fields': ('id_programador_inicial', 'id_programador_final')
            }),
        
            ('Estado solicitud', {
                'fields': ('estado', 'id_bug')
            })
        )
        return fieldsets
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado='PENDIENTE')
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'id_programador_final':
            kwargs['form_class'] = ProgramadorChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if obj.id_programador_final:
    
            bug_id = obj.id_bug.id_bug  # Obtener el id_bug del objeto Reasignacion
            try:
                bug = Bug.objects.get(id_bug=bug_id)
                bug.id_programador = obj.id_programador_final
                bug.save()
            except Bug.DoesNotExist:
                pass
            
    
admin.site.register(Reasignacion, ReasignacionBugAdmin)

