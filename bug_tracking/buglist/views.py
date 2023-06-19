from django.shortcuts import render
from django.core.paginator import Paginator
from database.models import Bug, ReporteBug, Proyecto

def index(request, order=''):  # Agregamos el parámetro de ordenamiento con un valor predeterminado vacío

    # Obtener el parámetro de dirección del ordenamiento
    order_direction = request.GET.get('order')

    # Ordenar la lista de bugs por ID
    if order == 'id':
        if order_direction == 'asc':
            bug_list = Bug.objects.order_by("id_bug")
        else:
            bug_list = Bug.objects.order_by("-id_bug")
    elif order == 'titulo':
        if order_direction == 'asc':
            bug_list = Bug.objects.order_by("titulo")
        else:
            bug_list = Bug.objects.order_by("-titulo")
    elif order == 'fecha':
        if order_direction == 'asc':
            bug_list = Bug.objects.order_by("fecha_reporte")
        else:
            bug_list = Bug.objects.order_by("-fecha_reporte")
    elif order == 'estado':
        if order_direction == 'asc':
            bug_list = Bug.objects.order_by("estado")
        else:
            bug_list = Bug.objects.order_by("-estado") 
    elif order == 'proyecto':
        if order_direction == 'asc':
            bug_list = Bug.objects.order_by("id_proyecto__nombre_proyecto")
        else:
            bug_list = Bug.objects.order_by("-id_proyecto__nombre_proyecto")
    else:
        bug_list = Bug.objects.order_by("-fecha_reporte")
    
    # Ordenar la lista de reportes por ID
    if order == 'id':
        if order_direction == 'asc':
            report_list = ReporteBug.objects.order_by("id_reporte")
        else:
            report_list = ReporteBug.objects.order_by("-id_reporte")
    elif order == 'titulo':
        if order_direction == 'asc':
            report_list = ReporteBug.objects.order_by("titulo")
        else:
            report_list = ReporteBug.objects.order_by("-titulo")
    elif order == 'fecha':
        if order_direction == 'asc':
            report_list = ReporteBug.objects.order_by("fecha_reporte")
        else:
            report_list = ReporteBug.objects.order_by("-fecha_reporte")
    elif order == 'proyecto':
        if order_direction == 'asc':
            report_list = ReporteBug.objects.order_by("id_proyecto__nombre_proyecto")
        else:
            report_list = ReporteBug.objects.order_by("-id_proyecto__nombre_proyecto")
    else:
        report_list = ReporteBug.objects.order_by("-fecha_reporte").select_related("id_proyecto")

    bug_paginator = Paginator(bug_list, 5)  # Paginación para la lista de bugs
    report_paginator = Paginator(report_list, 5)  # Paginación para los reportes

    bug_page_number = request.GET.get('bug_page')
    bug_page_obj = bug_paginator.get_page(bug_page_number)
    bug_page_obj.adjusted_elided_pages = bug_paginator.get_elided_page_range(bug_page_obj.number, on_each_side=1, on_ends=1)

    report_page_number = request.GET.get('report_page')
    report_page_obj = report_paginator.get_page(report_page_number)
    report_page_obj.adjusted_elided_pages = report_paginator.get_elided_page_range(report_page_obj.number, on_each_side=1, on_ends=1)

    context = {
        "bug_page_obj": bug_page_obj,
        "report_page_obj": report_page_obj,
        "order": order  # Agregamos la variable de ordenamiento al contexto
    }
    return render(request, "buglist/buglist.html", context)
