from typing import Optional
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http.request import HttpRequest
from .models import *
from django.db.models import Count
from django import forms
from django.urls import reverse, path
from django.shortcuts import redirect
from django.forms import ModelChoiceField
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

# Register your models here.


admin.site.unregister(User)
admin.site.unregister(Group)


class general(admin.ModelAdmin):
    def render_change_form(self, request, context, add, change, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
        })

        return super().render_change_form(request, context, add, change, form_url, obj)

# TODO ver tema de no poder editar usuarios
# al crear usuarios tengan por defecto is_staff=True, especificar que al registrarse desde la pagina se tiene que especificar is_staff=False


@admin.register(User)
class UserAdmin(general):
    def has_change_permissions(self, request, obj=None):
        return False

    list_display = ('username', 'email', 'is_staff')

    fieldsets = (
        ('Información de Usuario', {
            "fields": (
                'username', 'password',
            ),
        }),
        ('Información Personal', {
            "fields": (
                'first_name', 'last_name', 'is_staff'
            )
        })
    )


@admin.register(Usuario)
class UsuarioAdmin(general):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
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
    def get_name(self, obj=None):
        return obj.id_user.first_name + ' ' + obj.id_user.last_name

    @admin.display(description='Email')
    def get_email(self, obj=None):
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

# class ReasignacionInline(admin.TabularInline):


# class AvancesInlineForm(forms.ModelForm):
#     class Meta:
#         model = Avances
#         fields = ['titulo', 'descripcion']
#         widgets = {
#             'titulo': forms.TextInput(),
#             'descripcion': forms.Textarea(),
#         }

class AvancesInlineForm(forms.ModelForm):
    class Meta:
        model = Avances
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(),
            'descripcion': forms.Textarea(),
        }


class AvancesInline(admin.TabularInline):

    extra = 0
    show_change_link = True
    can_add_related = True
    model = Avances
    form = AvancesInlineForm

    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return True  # Permitir que el programador agregue avances
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False  # Modo de solo lectura para avances existentes
        return super().has_change_permission(request, obj)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = ['titulo', 'descripcion']
        return fields

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj is None:
            formset.can_order = False
            formset.can_delete = False
        return formset


class ReasignacionInlineForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super().__init__(*args, **kwargs)

    # id_programador_inicial = ModelChoiceField(
    #     queryset=Programador.objects.all(),
    #     disabled=False
    # )
    # id_programador_inicial = forms.ModelChoiceField(
    #     queryset=Programador.objects.none()

    # id_programador_inicial = forms.ModelChoiceField(
    #     queryset=Programador.objects.all(),
    #     disabled=False,
    #     required=False
    # )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            bug_instance = kwargs.get('instance')
            if bug_instance:
                programador_asociado = bug_instance.id_programador
                self.fields['id_programador_inicial'].choices = [
                    (programador_asociado.pk, str(programador_asociado))]
                self.fields['id_programador_inicial'].initial = programador_asociado.pk

    # ...

    # def clean_id_programador_inicial(self):
    #     return self.instance.id_programador_inicial

    # def has_changed(self):
    #     return False

    # def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        # super().__init__(*args, **kwargs)
        # if self.request and self.request.user.is_authenticated:
        #     bug_instance = kwargs.get('instance')
        #     if bug_instance:
        #         programador_asociado = bug_instance.id_programador
        #         self.fields['id_programador_inicial'].queryset = Programador.objects.filter(
        #             pk=programador_asociado.pk)

        # self.request = kwargs.pop('request', None)
        # super().__init__(*args, **kwargs)
        # if self.request and self.request.user.is_authenticated:
        #     bug_instance = kwargs.get('instance')
        #     if bug_instance:
        #         programador_asociado = bug_instance.id_programador
        #         self.initial['id_programador_inicial'] = programador_asociado

        # self.request = kwargs.pop('request', None)
        # super().__init__(*args, **kwargs)
        # if self.request and self.request.user.is_authenticated:
        #     programador = self.request.user.programador
        #     self.initial['id_programador_inicial'] = programador.nombre_completo()
        # self.request = kwargs.pop('request', None)
        # super().__init__(*args, **kwargs)
        # if self.request and self.request.user.is_authenticated:
        #     programador = self.request.user.programador
        #     self.initial['id_programador_inicial'] = programador

        # self.request = kwargs.pop('request', None)
        # super().__init__(*args, **kwargs)
        # if self.request and self.request.user.is_authenticated:
        #     programador = self.request.user.programador
        #     self.initial['id_programador_inicial'] = programador
        # self.fields['id_programador_inicial'].widget = forms.TextInput(
        #     attrs={'readonly': 'readonly'})
        # self.initial['id_programador_inicial'] = programador.id

        # Establecer valor inicial en el campo de comentario
        # self.fields['id_programador_inicial'].initial = self.request.user.programador
        # self.fields['id_programador_inicial'].initial = self.request.user

    def save_model(self, commit=True):
        instance = super().save(commit=False)
        if not instance.id_programador_inicial and self.request.user.is_authenticated:
            instance.id_programador_inicial = self.request.user.programador
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Reasignacion
        fields = ['id_programador_inicial', 'comment']
    # def save_model(self, commit=True):
    #     instance = super().save(commit=False)
    #     if not instance.id_programador_inicial:
    #         instance.id_programador_inicial = self.request.user.programador
    #     if commit:
    #         instance.save()
    #     return instance

    # class Meta:
    #     model = Reasignacion
    #     fields = ['comment']
    #     # widgets = {
    #     #     'comment': forms.Textarea(),
    #     # }


class ReasignacionInline(admin.TabularInline):

    extra = 0
    show_change_link = True
    can_add_related = True
    model = Reasignacion
    form = ReasignacionInlineForm
    fields = ['id_programador_inicial', 'comment']

    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return True  # Permitir que el programador agregue avances
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False  # Modo de solo lectura para avances existentes
        return super().has_change_permission(request, obj)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['id_programador_inicial'].queryset = Programador.objects.filter(
                id_user=user)
            self.fields['id_programador_inicial'].widget.attrs['disabled'] = 'disabled'

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.request = request
    #     # if obj is None:
    #     #     formset.can_order = False
    #     #     formset.can_delete = False
    #     #     programador = Programador.objects.get(user=request.user)
    #     #     formset.form.base_fields['id_programador_inicial'].initial = programador
    #     return formset

    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if obj is None:
    #         fields = ['comment']
    #     return fields
    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.request = request  # Pasar el objeto request al formulario
    #     return formset


class IdProyectoBugFilter(admin.SimpleListFilter):
    title = 'Proyecto'
    parameter_name = 'id_proyecto'

    def lookups(self, request, model_admin):
        # Obtener los proyectos disponibles para filtrar
        proyectos = model_admin.get_queryset(request).values_list(
            'id_proyecto', 'id_proyecto__nombre_proyecto').distinct()
        return proyectos

    def queryset(self, request, queryset):
        # Aplicar el filtro si se selecciona un proyecto
        if self.value():
            return queryset.filter(id_proyecto=self.value())
        return queryset

# TODO definir que fields dejar en readonly


@admin.register(Bug)
class BugAdmin(general):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.instance = obj

        return super(BugAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'id_programador':
            kwargs['queryset'] = Programador.objects.filter(
                cargo__id_proyecto=self.instance.id_proyecto)

            kwargs['form_class'] = ProgramadorChoiceField
        elif db_field.name == 'id_programador_inicial':
            if not request.user.is_superuser and request.user.is_staff:
                programador = Programador.objects.get(id_user=request.user)
                kwargs['queryset'] = Programador.objects.filter(
                    id_user=programador.id_user)
                kwargs['empty_label'] = None

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.is_staff:
            qs = qs.filter(id_programador__id_user=request.user)
        return qs

    def titulo_bug(self, obj):
        return obj.titulo

    def proyecto(self, obj):
        return obj.id_proyecto
    titulo_bug.short_description = 'Título'
    proyecto.short_description = 'Proyecto'

    def get_list_display(self, request):
        if not request.user.is_superuser and request.user.is_staff:
            return ('titulo_bug', 'proyecto', 'prioridad', 'estado')
        return super().get_list_display(request)

    def get_list_filter(self, request):

        if not request.user.is_superuser and request.user.is_staff:
            # Agregar el filtro personalizado IdProyectoFilter
            return {
                IdProyectoBugFilter: 'Proyecto',
                'prioridad': 'Prioridad',
                'estado': 'Estado'
            }
    # }(IdProyectoBugFilter, 'prioridad', 'estado')
        return super().get_list_filter(request)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            fieldsets = [
                ('Informacion del Bug', {
                    'fields': ['titulo', 'id_proyecto', 'descripcion',  'estado', 'prioridad']
                })
            ]
        else:
            fieldsets = self.fieldsets
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            if obj is not None:
                # Campos de solo lectura para programadores
                readonly_fields = ['titulo', 'descripcion',
                                   'id_proyecto', 'estado', 'prioridad']
            else:
                readonly_fields = []
        else:
            # Sin campos de solo lectura para administradores
            readonly_fields = []

        return readonly_fields

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return True  # Permitir que los programadores editen el bug
        return False

    list_display = ('id_bug', 'titulo', 'id_proyecto',
                    'estado', 'prioridad', 'id_programador')

    list_filter = ('id_proyecto', 'estado')

    fieldsets = [
        ('Informacion del Bug', {
            'fields': ['titulo', 'descripcion', 'id_proyecto', 'estado', 'prioridad']
        }),
        ('Personal encargado', {
            'fields': ['id_programador',]
        })
    ]

    inlines = [
        AvancesInline,
        ReasignacionInline,
    ]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj is not None:
            inline_instances.append(AvancesInline(self.model, self.admin_site))
            inline_instances.append(
                ReasignacionInline(self.model, self.admin_site))
        return inline_instances

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [AvancesInline, ReasignacionInline]
        return super().change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        bug = form.instance
        mensaje_exito = f"Se ha añadido correctamente un reporte para el caso de bug: {bug.titulo}"
        self.message_user(request, mensaje_exito, level=messages.SUCCESS)


# TODO cambiar forma de asignar un caso de bug a reporteBug


class CustomReporteBugForm(forms.ModelForm):
    class Meta:
        model = ReporteBug
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'titulo' in self.fields:
            self.fields['titulo'].label = 'Título'


@admin.register(ReporteBug)
class ReporteBugAdmin(general):

    def titulo_ticket(self, obj):
        return obj.titulo

    def caso_asociado(self, obj):
        return obj.id_bug

    def proyecto_ticket(self, obj):
        return obj.id_proyecto
    titulo_ticket.short_description = 'Título'
    caso_asociado.short_description = 'Caso asociado'
    proyecto_ticket.short_description = 'Proyecto'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.is_staff:
            return qs.filter(id_bug__id_programador__id_user=request.user)
        return qs.filter(estado=ReporteBug.ESTADOS_CHOICES[0][0])

    def save_model(self, request, obj, form, change):
        if obj.id_bug:
            obj.estado = ReporteBug.ESTADOS_CHOICES[1][0]

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj=None):
        obj.estado = ReporteBug.ESTADOS_CHOICES[2][0]
        obj.save()

    def has_add_permission(self, request, obj=None):
        return False

    def get_list_display(self, request):
        if not request.user.is_superuser and request.user.is_staff:
            return ('titulo_ticket', 'caso_asociado', 'id_proyecto')
        return super().get_list_display(request)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            # Fieldsets personalizados para el empleado
            fieldsets = [
                ('Información entregada por el usuario', {
                    'fields': ['titulo', 'reporte', 'id_usuario']
                }),
                ('Información extra', {
                    'fields': ['caso_asociado', 'id_proyecto']
                })
            ]
        else:
            # Fieldsets predeterminados para el administrador
            fieldsets = self.fieldsets

        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser and request.user.is_staff:
            kwargs['form'] = CustomReporteBugForm
        return super().get_form(request, obj, **kwargs)

    # def get_list_filter(self, request):
    #     if not request.user.is_superuser and request.user.is_staff:
    #         return ('id_proyecto', 'id_bug')
    #     return ()

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)

    #     class CustomForm(form):

    #         def __init__(self, *args, **kwargs):
    #             super().__init__(*args, **kwargs)
    #             if 'titulo' in self.fields:
    #                 self.fields['titulo'].label = 'Título'

    #     if not request.user.is_superuser and request.user.is_staff:
    #         return CustomForm
    #     return form

    list_display = ('id_reporte', 'titulo', 'fecha_reporte',
                    'id_proyecto', 'estado', 'id_bug')

    readonly_fields = ['titulo', 'reporte',
                       'id_usuario', 'estado', 'id_proyecto']

    fieldsets = [
        ('Información entregada por el usuario', {
            'fields': ['titulo', 'reporte', 'id_usuario']
        }),
        ('Información extra', {
            'fields': ['estado', 'id_proyecto', 'id_bug']
        })
    ]
    # list_filter = ('estado',)

# Clase para obtener proyectos asociados al programador


class IdProyectoFilter(admin.SimpleListFilter):
    title = 'Proyecto'
    parameter_name = 'id_proyecto'

    def lookups(self, request, model_admin):
        # Obtener los proyectos disponibles para filtrar
        proyectos = model_admin.get_queryset(request).values_list(
            'id_bug__id_proyecto', 'id_bug__id_proyecto__nombre_proyecto').distinct()
        return proyectos

    def queryset(self, request, queryset):
        # Aplicar el filtro si se selecciona un proyecto
        if self.value():
            return queryset.filter(id_bug__id_proyecto=self.value())
        return queryset

# Clase para obtener bug asociados al programador


class IdBugFilter(admin.SimpleListFilter):
    title = 'Bug'
    parameter_name = 'id_bug'

    def lookups(self, request, model_admin):
        # Obtener los bugs asociados al programador actual
        bugs = model_admin.get_queryset(request).values_list(
            'id_bug__id_bug', 'id_bug__titulo').distinct()
        return bugs

    def queryset(self, request, queryset):
        # Aplicar el filtro si se selecciona un bug
        if self.value():
            return queryset.filter(id_bug=self.value())
        return queryset


@admin.register(Avances)
class AvancesAdmin(general):
    @admin.display(ordering='id_bug__proyecto', description='Proyecto')
    def titulo_reporte(self, obj):
        return obj.titulo

    def bug(self, obj):
        return obj.id_bug.titulo

    def proyecto(self, obj):
        return obj.id_bug.id_proyecto.nombre_proyecto

    def get_proyecto(self, obj=None):
        return obj.id_bug.id_proyecto

    def formatted_fecha_avance(self, obj):
        return obj.fecha_avance.strftime('%Y-%m-%d %H:%M:%S')

    titulo_reporte.short_description = 'Título'
    bug.short_description = 'Caso asociado'
    proyecto.short_description = 'Proyecto'
    formatted_fecha_avance.short_description = 'Fecha'

    def has_add_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser

    def get_list_filter(self, request):
        if not request.user.is_superuser and request.user.is_staff:
            return (IdProyectoFilter, IdBugFilter)
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.is_staff:
            programador = Programador.objects.get(id_user=request.user)
            # qs = qs.filter(id_bug__id_programador=programador)
            qs = qs.filter(id_bug__id_programador=programador)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # if not request.user.is_superuser and request.user.is_staff:
        #     form.base_fields['id_bug'].queryset = Bug.objects.filter(
        #         id_programador__id_user=request.user)

        class CustomForm(form):
            # SIREVE PARA CAMBIAR LA ETIQUETA
            id_bug = forms.ModelChoiceField(
                # queryset=form.base_fields['id_bug'].queryset,
                queryset=Bug.objects.filter(
                    id_programador__id_user=request.user),
                label='Caso Asociado',
                # widget=forms.Select(
                #     attrs={'data-placeholder': 'Seleccione un bug'}),
                # to_field_name='id_bug',
                # empty_label=None,
            )
            titulo = forms.CharField(label='Título')
            descripcion = forms.CharField(
                label='Descripción', widget=forms.Textarea)

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['id_bug'].queryset = Bug.objects.filter(
                    id_programador__id_user=request.user)
                self.fields['id_bug'].label_from_instance = lambda obj: f'{obj.id_proyecto} - {obj.titulo}'

            class Meta:
                model = Avances
                fields = ('id_bug', 'titulo', 'descripcion')

        return CustomForm
        return form

    list_display = ('titulo_reporte', 'bug', 'proyecto',
                    'formatted_fecha_avance')


@admin.register(Notificaciones)
class NotificacionesAdmin(general):
    def has_change_permission(self, request, obj=None):
        return False


class ReasignacionProgramadorForm(forms.ModelForm):
    class Meta:
        model = Reasignacion
        fields = ['id_programador_inicial', 'id_bug', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['id_programador_inicial'].queryset = Programador.objects.filter(
                id_user=user)
            self.fields['id_programador_inicial'].widget.attrs['disabled'] = 'disabled'


def is_superuser(user):
    return user.is_superuser


@admin.register(Reasignacion)
class ReasignacionBugAdmin(general):
    form = ReasignacionProgramadorForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.is_staff:
            programador = Programador.objects.get(id_user=request.user)
            return qs.filter(id_programador_inicial=programador)
        else:
            return qs.filter(estado=Reasignacion.ESTADOS_CHOICES[0][0])

    def get_form(self, request, obj=None, **kwargs):
        # if obj:
        #     self.instance = obj
        # return super(ReasignacionBugAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            self.instance = obj
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser and request.user.is_staff:
            form.user = request.user
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'id_programador_final':
            kwargs['queryset'] = Programador.objects.filter(
                cargo__id_proyecto=self.instance.id_bug.id_proyecto).exclude(id_user=self.instance.id_programador_inicial)
            kwargs['form_class'] = ProgramadorChoiceField
        elif db_field.name == 'id_bug':
            if not request.user.is_superuser and request.user.is_staff:
                programador = Programador.objects.get(id_user=request.user)
                kwargs['queryset'] = Bug.objects.filter(
                    id_programador=programador)
                # Elimina la opción vacía del campo
                kwargs['empty_label'] = None
            else:
                kwargs['queryset'] = Bug.objects.all()
        elif db_field.name == 'id_programador_inicial':
            if not request.user.is_superuser and request.user.is_staff:
                programador = Programador.objects.get(id_user=request.user)
                kwargs['queryset'] = Programador.objects.filter(
                    id_user=programador.id_user)
                kwargs['empty_label'] = None
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
                except Bug.DoesNotExist:
                    pass
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def desaprobar(self, obj):
        url = reverse('admin:desaprobar_url', kwargs={
                      'id': obj.id_reasignacion})
        return format_html('<a href="{% url opts|admin_urlname:\'changelist\' %}" class="btn {{ jazzmin_ui.button_classes.danger }} form-control">{% trans \'Desaprobar\' %}</a>', url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('desaprobar/<int:id>', self.desaprobar_app, name='desaprobar_url')
        ]

        return custom_urls + urls

    def desaprobar_app(self, request, id):
        obj = Reasignacion.objects.get(id_reasignacion=id)

        obj.estado = Reasignacion.ESTADOS_CHOICES[2][0]
        obj.save()

        redirect_url = "admin:{}_{}_changelist".format(
            self.opts.app_label, self.opts.model_name)
        return redirect(reverse(redirect_url))

    def get_list_display(self, request):
        if not request.user.is_superuser and request.user.is_staff:
            return ('id_reasignacion', 'id_bug', 'estado')
        return super().get_list_display(request)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return ('estado')
        return super().get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return [
                ('Solicitud Reasignacion', {
                    'fields': ['id_programador_inicial', 'id_bug', 'comment']
                })
            ]
        else:
            return self.fieldsets

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser and request.user.is_staff:
            # Elimina la acción de desaprobar para los usuarios no superusuarios
            if 'desaprobar' in actions:
                del actions['desaprobar']
        return actions

    # change_form_template = 'admin/database/reasignacion/change_form.html'
    def get_change_form_template(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return 'admin/database/reasignacion/change_form.html'
        return super().get_change_form_template(request, obj, **kwargs)

    def get_list_filter(self, request):
        if not request.user.is_superuser and request.user.is_staff:
            return ('estado',)
        return ()

    list_display = ('id_reasignacion', 'id_bug',
                    'id_programador_inicial', 'fecha_reasignacion')

    readonly_fields = ('id_programador_inicial', 'id_bug', 'estado')

    fieldsets = [
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
