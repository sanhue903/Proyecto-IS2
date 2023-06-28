from django.shortcuts import render
from django.core.paginator import Paginator
from database.models import Bug, ReporteBug, Proyecto
from django.db.models import Q

def index(request):
    bug_order = request.GET.get('bug_order', '')
    report_order = request.GET.get('report_order', '')

    bug_order_direction = request.GET.get('bug_order_direction', '')
    report_order_direction = request.GET.get('report_order_direction', '')

    bug_search = request.GET.get('bug_search', '')
    report_search = request.GET.get('report_search', '')

    bug_list = Bug.objects.all()
    report_list = ReporteBug.objects.all()

    if bug_order == 'id':
        bug_list = bug_list.order_by("id_bug" if bug_order_direction == 'asc' else "-id_bug")
    elif bug_order == 'titulo':
        bug_list = bug_list.order_by("titulo" if bug_order_direction == 'asc' else "-titulo")
    elif bug_order == 'fecha':
        bug_list = bug_list.order_by("fecha_reporte" if bug_order_direction == 'asc' else "-fecha_reporte")
    elif bug_order == 'estado':
        bug_list = bug_list.order_by("estado" if bug_order_direction == 'asc' else "-estado")
    elif bug_order == 'proyecto':
        bug_list = bug_list.order_by("id_proyecto__nombre_proyecto" if bug_order_direction == 'asc' else "-id_proyecto__nombre_proyecto")
    else:
        bug_list = bug_list.order_by("-fecha_reporte")

    if report_order == 'id':
        report_list = report_list.order_by("id_reporte" if report_order_direction == 'asc' else "-id_reporte")
    elif report_order == 'titulo':
        report_list = report_list.order_by("titulo" if report_order_direction == 'asc' else "-titulo")
    elif report_order == 'fecha':
        report_list = report_list.order_by("fecha_reporte" if report_order_direction == 'asc' else "-fecha_reporte")
    elif report_order == 'estado':
        report_list = report_list.order_by("estado" if report_order_direction == 'asc' else "-estado")
    elif report_order == 'proyecto':
        report_list = report_list.order_by("id_proyecto__nombre_proyecto" if report_order_direction == 'asc' else "-id_proyecto__nombre_proyecto")
    else:
        report_list = report_list.order_by("-fecha_reporte")

    if bug_search:
        bug_list = bug_list.filter(
            Q(id_bug__icontains=bug_search) |
            Q(titulo__icontains=bug_search) |
            Q(estado__icontains=bug_search) |
            Q(id_proyecto__nombre_proyecto__icontains=bug_search)
        )

    if report_search:
        report_list = report_list.filter(
            Q(id_reporte__icontains=report_search) |
            Q(titulo__icontains=report_search) |
            Q(estado__icontains=report_search) |
            Q(id_proyecto__nombre_proyecto__icontains=report_search)
        )

    bug_paginator = Paginator(bug_list, 5)
    bug_page_number = request.GET.get('bug_page')
    bug_page_obj = bug_paginator.get_page(bug_page_number)
    bug_page_obj.adjusted_elided_pages = bug_paginator.get_elided_page_range(bug_page_obj.number, on_each_side=1, on_ends=1)

    report_paginator = Paginator(report_list, 5)
    report_page_number = request.GET.get('report_page')
    report_page_obj = report_paginator.get_page(report_page_number)
    report_page_obj.adjusted_elided_pages = report_paginator.get_elided_page_range(report_page_obj.number, on_each_side=1, on_ends=1)

    context = {
        'bug_page_obj': bug_page_obj,
        'report_page_obj': report_page_obj,
        'bug_order': bug_order,
        'report_order': report_order,
    }
    return render(request, 'buglist/buglist.html', context)
