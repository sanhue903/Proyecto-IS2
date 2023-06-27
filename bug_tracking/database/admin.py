from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from .models import *
from django.urls import reverse
from django.forms import ModelChoiceField
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _


# Register your models here.


admin.site.unregister(User)
admin.site.unregister(Group)


def notificar(obj,change=False):
    obj_type = type(obj)
    
    if obj_type == ReporteBug:
        Notificaciones.objects.create(
            id_user     = obj.id_usuario.id_user,
            descripcion = 'Ticket {0.id_reporte}: su reporte ha sido {0.estado}'.format(obj),
        )
    
    elif obj_type == Bug:
        if not change:
            Notificaciones.objects.create(
                id_user     = obj.id_programador.id_user,
                descripcion = 'Caso {0.id_bug}: nuevo caso asignado'.format(obj),
            )
        
        tickets_relacionados = ReporteBug.objects.all().filter(id_bug=obj.id_bug)
        
        for ticket in tickets_relacionados:
            Notificaciones.objects.create(
                id_user     = ticket.id_usuario.id_user,
                descripcion = 'Caso {0.id_bug}: estado del caso cambio a {0.estado}'.format(obj),
            )
    
    elif obj_type == Reasignacion:
        Notificaciones.objects.create(
            id_user     = obj.id_programador_inicial.id_user,
            descripcion = 'Caso {0.id_bug.id_bug}: estado de reasignacion cambio a {0.estado}'.format(obj),
        )
        
        if obj.id_programador_final:
            notificacion_programador_final = Notificaciones.objects.create(
                id_user     =obj.id_programador_final.id_user,
                descripcion ='Caso {0.id_bug.id_bug}: nuevo caso asignado'.format(obj),
            )
            
            notificacion_programador_final.save()    


class general(admin.ModelAdmin):
    def render_change_form(self, request, context, add, change, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
        })
        
        return super().render_change_form(request, context, add, change, form_url, obj)


#TODO ver tema de no poder editar usuarios
#al crear usuarios tengan por defecto is_staff=True, especificar que al registrarse desde la pagina se tiene que especificar is_staff=False
@admin.register(User)
class UserAdmin(UserAdmin):
    def has_change_permissions(self, request, obj=None):
        return False
    
    list_display = ('username', 'email', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff',),
        }),
    )
    
 

@admin.register(Usuario)
class UsuarioAdmin(general):
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):
        return False
    
    def has_delete_permission(self, request,obj=None):
        return False
    
    

class CargoInline(admin.TabularInline):
    model = Proyecto.programadores.through
    
    extra = 0
    
    list_display = ('id_programador', 'cargo')
    
    def has_change_permissions(self, request, obj=None):
        return False



@admin.register(Programador)
class ProgramadorAdmin(general):
    @admin.display(description='Nombre')
    def get_name(self,obj=None):
        return obj.id_user.first_name + ' ' + obj.id_user.last_name

    @admin.display(description='Email')
    def get_email(self,obj=None):
        return obj.id_user.email
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    readonly_fields = ['get_name', 'get_email']
    
    list_display = ('get_name', 'get_email')
    
    inlines = [
        CargoInline,
    ]
    
    fieldsets = [
        ('Información personal', {
            'fields': readonly_fields
        }),
    ]
    
    

@admin.register(Proyecto)
class ProyectoAdmin(general):
    list_display = ('nombre_proyecto',)
    
    exclude = ('programadores',)
    
    inlines = [
        CargoInline,
    ]
    
    

@admin.register(Cargo)
class CargoAdmin(general):
    list_display = ('id_programador', 'cargo', 'id_proyecto')
    
    fieldsets = [
        ('Proyecto', {
            'fields': ['id_proyecto',]
        }),
        ('Información del programador', {
            'fields': ['id_programador', 'cargo']
        })
    ]



class AvancesInline(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    model = Avances
    
    readonly_fields = ['titulo', 'fecha_avance']
    
    exclude = ['descripcion',]
    
    show_change_link = True

    

#TODO definir que fields dejar en readonly (id_proyecto si logro pasara información de reporteBug a Bug)
#TODO ver forma de pasar información de reporteBug a Bug(necesario para que se puedan filtar los programadores)
@admin.register(Bug)
class BugAdmin(general):
    def get_form(self, request, obj=None, **kwargs):
        self.instance = None## eso hace que funcione por ahora
        if obj:
            self.instance = obj
            
        #signal with the value of id_proyecto
            
        return super(BugAdmin, self).get_form(request, obj, **kwargs)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.instance:
            if db_field.name == 'id_programador':
                kwargs['queryset'] = Programador.objects.filter(cargo__id_proyecto=self.instance.id_proyecto)
                
                kwargs['form_class'] = ProgramadorChoiceField
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        notificar(obj, change)
    
    def has_delete_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):
        return False
    
    def response_change(self, request, obj):
        if '_save' in request.POST:
            redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
            
            return HttpResponseRedirect(reverse(redirect_url))
        elif '_solucionado' in request.POST:
            obj.estado = Bug.ESTADOS_CHOICES[2][0]
            obj.save()
            
            notificar(obj)
            
            
            redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
            
            return HttpResponseRedirect(reverse(redirect_url))
       
    
    list_display  = ('id_bug', 'titulo', 'id_proyecto',
                    'estado', 'prioridad', 'id_programador')
    
    search_fields = ('id_proyecto', 'id_programador')
    
    list_filter   = ('id_proyecto', 'estado')
    
    fieldsets     = [
        ('Informacion del Bug', {
            'fields': ['titulo', 'descripcion', 'id_proyecto', 'estado', 'prioridad']
        }),
        ('Personal encargado', {
            'fields': ['id_programador',]
        })
    ]
    
    inlines       = [
        AvancesInline,
    ]
    

#TODO cambiar forma de asignar un caso de bug a reporteBug
@admin.register(ReporteBug)
class ReporteBugAdmin(general):
    def get_form(self, request, obj=None, **kwargs):
        self.instance = None
        if obj:
            self.instance = obj
            
        return super(ReporteBugAdmin, self).get_form(request, obj, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado=ReporteBug.ESTADOS_CHOICES[0][0])

    def save_model(self, request, obj, form, change):
        if obj.id_bug:
            aux = obj.estado
            obj.estado = ReporteBug.ESTADOS_CHOICES[1][0]
            
            if aux != obj.estado:
                notificar(obj)
            
        super().save_model(request, obj, form, change)
        
    
    def has_add_permission(self, request,obj=None):      
        return False
    
    def has_delete_permission(self, request,obj=None):
        return False
    
    def response_change(self, request, obj):
        if '_save' in request.POST:
            redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
            
            return HttpResponseRedirect(reverse(redirect_url))
        elif '_desaprobar' in request.POST:
            obj.estado = ReporteBug.ESTADOS_CHOICES[2][0]
            obj.save()
            
            notificar(obj)
            
            
            redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
            
            return HttpResponseRedirect(reverse(redirect_url))
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.instance:
            if db_field.name == 'id_bug':
                kwargs['queryset'] = Bug.objects.filter(id_proyecto=self.instance.id_proyecto)
      
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    """  
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "id_bug":
            widget = super(BugAdmin, self.instance).formfield_for_dbfield(db_field, request, **kwargs).widget
            widget.template_name = 'admin/reportebug/widgets/related_widget_wrapper_with_id.html'
            widget.attrs.update({'id_proyecto': 1})
        
            return db_field.formfield(widget=widget)
        return super(BugAdmin, self.instance).formfield_for_dbfield(db_field, request, **kwargs)

    """
    list_display = ('id_reporte','titulo', 'fecha_reporte', 'id_proyecto', 'estado', 'id_bug')
    
    readonly_fields = ['titulo', 'reporte', 'id_usuario', 'estado' , 'id_proyecto']
    
    fieldsets    = [
        ('Información entregada por el usuario', {
            'fields': ['titulo', 'reporte', 'id_usuario']
        }),
        ('Información extra', {
            'fields': ['estado', 'id_proyecto', 'id_bug']
        })
    ]



@admin.register(Avances)
class AvancesAdmin(general):
    @admin.display(ordering='id_bug__proyecto', description='Proyecto')
    def get_proyecto(self,obj = None):
        return obj.id_bug.id_proyecto
    
    def has_add_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):
        return False
            
    def has_delete_permission(self, request,obj=None):
        return False
            
    list_display = ('titulo', 'id_bug', 'get_proyecto','fecha_avance')
    
    

@admin.register(Notificaciones)
class NotificacionesAdmin(general):
    def has_change_permission(self, request,obj=None):
        return False
    
    def has_delete_permission(self, request,obj=None):
        return False
    
    list_display = ('id_notificacion', 'descripcion', 'id_user')
    
    

@admin.register(Reasignacion)
class ReasignacionBugAdmin(general):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado=Reasignacion.ESTADOS_CHOICES[0][0])
    
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.instance = obj
        return super(ReasignacionBugAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'id_programador_final':
            kwargs['queryset'] = Programador.objects.filter(cargo__id_proyecto=self.instance.id_bug.id_proyecto).exclude(id_user=self.instance.id_programador_inicial)
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
                    obj.estado = Reasignacion.ESTADOS_CHOICES[1][0]
                    
                    notificar(obj)

                except Bug.DoesNotExist:
                    pass
        
        
             
        obj = super().save_model(request, obj, form, change)
        
        

    def has_add_permission(self, request,obj=None):
        return False
    
    def has_delete_permission(self, request,obj=None):
        return False
    
    def response_change(self, request, obj):
        if '_save' in request.POST:
            redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
            
            return HttpResponseRedirect(reverse(redirect_url))
        
        elif '_desaprobar' in request.POST:
            obj.estado = Reasignacion.ESTADOS_CHOICES[2][0]
            obj.save()
            
            notificar(obj)
            
            redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
            
            return HttpResponseRedirect(reverse(redirect_url))
    
    
    change_form_template = 'admin/database/reasignacion/change_form.html'
    
    list_display    = ('id_reasignacion', 'id_bug','id_programador_inicial', 'fecha_reasignacion')
    
    readonly_fields = ('id_programador_inicial', 'id_bug', 'estado')
    
    fieldsets       = [
        ('Programadores involucrados', {
            'fields': ['id_programador_inicial', 'id_programador_final']
        }),
        ('Estado solicitud', {
            'fields': ['estado', 'id_bug']
        })
    ]

    

class ProgramadorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        total_bugs = obj.bug_set.count()
        
        bugs_baja = obj.bug_set.filter(
            id_programador=obj).filter(prioridad=Bug.PRIORIDADES_CHOICES[0][0]).count()
        
        bugs_media = obj.bug_set.filter(
            id_programador=obj).filter(prioridad=Bug.PRIORIDADES_CHOICES[1][0]).count()
        
        bugs_alta = obj.bug_set.filter(
            id_programador=obj).filter(prioridad=Bug.PRIORIDADES_CHOICES[2][0]).count()
        
        bugs_urgente = obj.bug_set.filter(
            id_programador=obj).filter(prioridad=Bug.PRIORIDADES_CHOICES[3][0]).count()

        return f'{obj.id_user.username} -  TOTAL BUGS: {total_bugs} | BAJA: {bugs_baja} | MEDIA: {bugs_media} | ALTA: {bugs_alta} | URGENTE: {bugs_urgente}'