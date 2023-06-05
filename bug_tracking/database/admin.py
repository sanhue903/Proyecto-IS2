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
    
class ProgramadorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):

        total_bugs = obj.bug_set.count()
        bugs_baja = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad='BAJA').count()
        bugs_media = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad='MEDIA').count()
        bugs_alta = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad='ALTA').count()
        bugs_urgente = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad='URGENTE').count()

        return f'{obj.user.username} -  TOTAL BUGS: {total_bugs} | BAJA: {bugs_baja} | MEDIA: {bugs_media} | ALTA: {bugs_alta} | URGENTE: {bugs_urgente}'
        # return f'{obj.nombre_programador} ({obj.bug_set.count()} bugs asociados)'


# def rechazar_reasignacion(modeladmin, request, queryset):
#     queryset.update(estado='DESAPROBADO')
# class DesaprobarAction(admin.Action):
#     """
#     Acción personalizada para cambiar el estado a 'DESAPROBADO'.
#     """
#     short_description = 'DESAPROBAR'  # Texto del botón

#     def __init__(self, func=None, name=None, short_description=None):
#         super().__init__(func, name, short_description)
#         self.short_description = short_description or self.short_description

#     def delete_models(self, modeladmin, request, queryset):
#         # Cambiar el estado a 'DESAPROBADO' para todos los objetos seleccionados
#         queryset.update(estado='DESAPROBADO')

#     def get_success_message(self, queryset):
#         count = queryset.count()
#         return f"{count} reasignaciones fueron desaprobadas."

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             # Eliminar la acción predeterminada de eliminar
#             del actions['delete_selected']
#         return actions

#     # Texto para el mensaje de confirmación
#     delete_models.short_description = 'DESAPROBAR'


class ReasignacionBugAdmin(admin.ModelAdmin):
    list_display = ('id_reasignacion', 'id_bug',
                    'id_programador_inicial', 'fecha_reasignacion')
    # 'id_programador_final_display'
    readonly_fields = ('id_programador_inicial', 'id_bug')
    # actions = [DesaprobarAction.delete_models]

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
            kwargs['queryset'] = Programador.objects.all()
            kwargs['form_class'] = ProgramadorChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):

        if obj.id_programador_final and obj.id_programador_inicial == obj.id_programador_final:
            messages.error(
                request, "No se puede reasignar a la misma persona.")
        else:
            if obj.id_programador_final:
                bug_id = obj.id_bug.id_bug  # Obtener el id_bug del objeto Reasignacion
                try:
                    bug = Bug.objects.get(id_bug=bug_id)
                    bug.id_programador = obj.id_programador_final
                    bug.save()
                    obj.estado = 'APROBADO'
                except Bug.DoesNotExist:
                    pass
        super().save_model(request, obj, form, change)

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         # Eliminar la acción predeterminada de eliminar
    #         del actions['delete_selected']
    #     return actions

    # actions = ['desaprobar_reasignacion']

    # def desaprobar_reasignacion(self, request, queryset):
    #     queryset.update(estado='desaprobado')
    # desaprobar_reasignacion.short_description = 'Desaprobar'

    # def get_actions(self, request):
    #     actions = super().get_actions(request)

    #     if 'delete_selected' in actions:
    #         actions['delete_selected'].short_description = 'Desaprobar'

    #     return actions

    # PERMITE QUE AL PRESIONAR EL BOTÓN ELIMINAR SE CAMBIE EL ESTADO

    def delete_model(self, request, obj):
        obj.estado = 'DESAPROBADO'
        obj.save()

    def has_add_permission(self, request):
        return False


admin.site.register(Reasignacion, ReasignacionBugAdmin)

