from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta 
from datetime import date, timedelta
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from itertools import groupby
from operator import attrgetter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import (
    ToDoList,
    Item,
    LagoonDetail,
    LagunaImage,
    Laguna, 
    Laguna_Stock,

    PersonalDeLaLaguna, 
    OperacionLimpiezaDeFondo, 
    OperacionLimpiezaManual, 
    OperacionFiltro, 
    OperacionSistemaDosificacion, 
    OperacionSistemaRecirculacion, 
    FuncionamientoTelemetria, 
    OperacionSkimmers, 
    OperacionUltrasonido, 
    Infraestructura, 
    CondicionLiner, 
    CondicionVisualLaguna, 
    FuncionamientoAguaRelleno, 
    NivelDeLaLaguna, 
    MedidasDeMitigacion,
    RelevantMatters,
    IMOP,
    Supervisor,
    SupervisorLaguna
    )
from .forms import (
    CreateNewList,
    LagoonDetailForm,
    LagunaForm,
    ChecklistForm,
    StockForm,

    PersonalDeLaLagunaForm,  
    OperacionLimpiezaDeFondoForm,
    OperacionLimpiezaManualForm,
    OperacionFiltroForms,
    OperacionSistemaDosificacionForms,
    OperacionSistemaRecirculacionForms,
    FuncionamientoTelemetriaForms,
    OperacionSkimmersForms,
    OperacionUltrasonidoForms,
    InfraestructuraForms,
    CondicionLinerForms,
    CondicionVisualLagunaForms,
    FuncionamientoAguaRellenoForms,
    NivelDeLaLagunaForms,
    MedidasDeMitigacionForms,
    LagunaSelectionForm,
    RelevantMatterForm
    )


def index_page(request):
    return render(request, 'main/indexpage.html')


def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
    
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")

        return render(response, "main/list.html", {"ls":ls})
    return render(response, "main/view.html", {})

def home(request):
    lagunas = Laguna.objects.all()
    return render(request, "main/home.html", {'lagunas': lagunas, 'full_width': True})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)
        
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})

def testing(response):
    return render(response, "main/testing.html", {})

def view(response):
    return render(response, "main/view.html", {})

def laguna_database(request):
    lagunas = Laguna.objects.all()
    return render(request, 'main/laguna_database.html', {'lagunas': lagunas, 'full_width': True})

def edit_laguna(request, idLagunas):
    laguna = get_object_or_404(Laguna, idLagunas=idLagunas)
    
    if request.method == "POST":
        form = LagunaForm(request.POST, instance=laguna)
        if form.is_valid():
            form.save()
            return redirect('laguna_database')  # Redirect to the database view after saving
    else:
        form = LagunaForm(instance=laguna)
    
    return render(request, 'main/edit_laguna.html', {'form': form})

def initial_form_view(request):
    request.session['personal_form_submitted'] = False
    request.session['limpieza_form_submitted'] = False
    request.session['limpiezamanual_form_submitted'] = False
    request.session['operacionfiltro_form_submitted'] = False
    request.session['operacionsistemadosificacion_form_submitted'] = False
    request.session['operacionsistemarecirculacion_form_submitted'] = False
    request.session['funcionamientotelemetria_form_submitted'] = False
    request.session['operacionskimmers_form_submitted'] = False
    request.session['operacionultrasonido_form_submitted'] = False
    request.session['infraestructura_form_submitted'] = False
    request.session['condicionliner_form_submitted'] = False
    request.session['condicionvisuallaguna_form_submitted'] = False
    request.session['funcionamientoaguarelleno_form_submitted'] = False
    request.session['niveldelalaguna_form_submitted'] = False
    request.session['medidasdemitigacion_form_submitted'] = False
    form = ChecklistForm()
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        if form.is_valid():
            request.session['fecha'] = str(form.cleaned_data['fecha'])
            request.session['supervisor'] = str(form.cleaned_data['supervisor'])
            request.session['lagoons'] = str(form.cleaned_data['lagoons'])

            return redirect('results')

    personal_entries = PersonalDeLaLaguna.objects.all()  # Query the database
    return render(request, "main/initial_form.html", {"form": form, "personal_entries": personal_entries})

def results_view(request):
    date = request.session.get('fecha')
    supervisor = request.session.get('supervisor')
    lagoon_name = request.session.get('lagoons')
    try:
        lagoon = Laguna.objects.get(Nombre=lagoon_name)
    except Laguna.DoesNotExist:
        lagoon = None



    latest_personal = PersonalDeLaLaguna.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_limpieza = OperacionLimpiezaDeFondo.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_limpiezamanual = OperacionLimpiezaManual.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_operacionfiltro = OperacionFiltro.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_operacionsistemadosificacion = OperacionSistemaDosificacion.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_operacionsistemarecirculacion = OperacionSistemaRecirculacion.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_funcionamientotelemetria = FuncionamientoTelemetria.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_operacionskimmers = OperacionSkimmers.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_operacionultrasonido = OperacionUltrasonido.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_infraestructura = Infraestructura.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_condicionliner = CondicionLiner.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_condicionvisuallaguna = CondicionVisualLaguna.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_funcionamientoaguarelleno = FuncionamientoAguaRelleno.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_niveldelalaguna = NivelDeLaLaguna.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None
    latest_medidasdemitigacion = MedidasDeMitigacion.objects.filter(lagoon=lagoon).order_by('-date').first() if lagoon else None





    # Initialize all forms
    personal_form = PersonalDeLaLagunaForm()
    limpieza_form = OperacionLimpiezaDeFondoForm()
    limpiezamanual_form = OperacionLimpiezaManualForm()
    operacionfiltro_form = OperacionFiltroForms()
    operacionsistemadosificacion_form = OperacionSistemaDosificacionForms()
    operacionsistemarecirculacion_form = OperacionSistemaRecirculacionForms()
    funcionamientotelemetria_form = FuncionamientoTelemetriaForms()
    operacionskimmers_form = OperacionSkimmersForms()
    operacionultrasonido_form = OperacionUltrasonidoForms()
    infraestructura_form = InfraestructuraForms()
    condicionliner_form = CondicionLinerForms()
    condicionvisuallaguna_form = CondicionVisualLagunaForms()
    funcionamientoaguarelleno_form = FuncionamientoAguaRellenoForms()
    niveldelalaguna_form = NivelDeLaLagunaForms()
    medidasdemitigacion_form = MedidasDeMitigacionForms()






    if request.method == 'POST':
        # Replace with a series of if/elif statements
        ####
        existing_personal = PersonalDeLaLaguna.objects.filter(lagoon=lagoon, date=date).first() ####test
        existing_limpieza = OperacionLimpiezaDeFondo.objects.filter(lagoon=lagoon, date=date).first()
        existing_limpiezamanual = OperacionLimpiezaManual.objects.filter(lagoon=lagoon, date=date).first()
        existing_operacionfiltro = OperacionFiltro.objects.filter(lagoon=lagoon, date=date).first()
        existing_operacionsistemadosificacion = OperacionSistemaDosificacion.objects.filter(lagoon=lagoon, date=date).first()
        existing_operacionsistemarecirculacion = OperacionSistemaRecirculacion.objects.filter(lagoon=lagoon, date=date).first()
        existing_funcionamientotelemetria = FuncionamientoTelemetria.objects.filter(lagoon=lagoon, date=date).first()
        existing_operacionskimmers = OperacionSkimmers.objects.filter(lagoon=lagoon, date=date).first()
        existing_operacionultrasonido = OperacionUltrasonido.objects.filter(lagoon=lagoon, date=date).first()
        existing_infraestructura = Infraestructura.objects.filter(lagoon=lagoon, date=date).first()
        existing_condicionliner = CondicionLiner.objects.filter(lagoon=lagoon, date=date).first()
        existing_condicionvisuallaguna = CondicionVisualLaguna.objects.filter(lagoon=lagoon, date=date).first()
        existing_funcionamientoaguarelleno = FuncionamientoAguaRelleno.objects.filter(lagoon=lagoon, date=date).first()
        existing_niveldelalaguna = NivelDeLaLaguna.objects.filter(lagoon=lagoon, date=date).first()
        existing_medidasdemitigacion = MedidasDeMitigacion.objects.filter(lagoon=lagoon, date=date).first()

        ####
        if 'personal_submit' in request.POST:
            personal_form = PersonalDeLaLagunaForm(request.POST)
            if personal_form.is_valid(): 
                if existing_personal:
                    existing_personal.delete()
                personal_form.instance.date = date
                personal_form.instance.supervisor = supervisor
                personal_form.instance.lagoon = lagoon
                personal_form.save()
                request.session['personal_form_submitted'] = True
        elif 'limpieza_submit' in request.POST:
            limpieza_form = OperacionLimpiezaDeFondoForm(request.POST)
            if limpieza_form.is_valid():
                if existing_limpieza: 
                    existing_limpieza.delete()
                limpieza_form.instance.date = date
                limpieza_form.instance.supervisor = supervisor
                limpieza_form.instance.lagoon = lagoon
                limpieza_form.save()
                request.session['limpieza_form_submitted'] = True
        elif 'limpiezamanual_submit' in request.POST:
            limpiezamanual_form = OperacionLimpiezaManualForm(request.POST)
            if limpiezamanual_form.is_valid():
                if existing_limpiezamanual: 
                    existing_limpiezamanual.delete()
                limpiezamanual_form.instance.date = date
                limpiezamanual_form.instance.supervisor = supervisor
                limpiezamanual_form.instance.lagoon = lagoon
                limpiezamanual_form.save()
                request.session['limpiezamanual_form_submitted'] = True
        elif 'operacionfiltro_submit' in request.POST:
            operacionfiltro_form = OperacionFiltroForms(request.POST)
            if operacionfiltro_form.is_valid():
                if existing_operacionfiltro: 
                    existing_operacionfiltro.delete()
                operacionfiltro_form.instance.date = date
                operacionfiltro_form.instance.supervisor = supervisor
                operacionfiltro_form.instance.lagoon = lagoon
                operacionfiltro_form.save()
                request.session['operacionfiltro_form_submitted'] = True
        elif 'operacionsistemadosificacion_submit' in request.POST:
            operacionsistemadosificacion_form = OperacionSistemaDosificacionForms(request.POST)
            if operacionsistemadosificacion_form.is_valid():
                if existing_operacionsistemadosificacion: 
                    existing_operacionsistemadosificacion.delete()
                operacionsistemadosificacion_form.instance.date = date
                operacionsistemadosificacion_form.instance.supervisor = supervisor
                operacionsistemadosificacion_form.instance.lagoon = lagoon
                operacionsistemadosificacion_form.save()
                request.session['operacionsistemadosificacion_form_submitted'] = True
        elif 'operacionsistemarecirculacion_submit' in request.POST:
            operacionsistemarecirculacion_form = OperacionSistemaRecirculacionForms(request.POST)
            if operacionsistemarecirculacion_form.is_valid():
                if existing_operacionsistemarecirculacion: 
                    existing_operacionsistemarecirculacion.delete()
                operacionsistemarecirculacion_form.instance.date = date
                operacionsistemarecirculacion_form.instance.supervisor = supervisor
                operacionsistemarecirculacion_form.instance.lagoon = lagoon
                operacionsistemarecirculacion_form.save()
                request.session['operacionsistemarecirculacion_form_submitted'] = True
        elif 'funcionamientotelemetria_submit' in request.POST:
            funcionamientotelemetria_form = FuncionamientoTelemetriaForms(request.POST)
            if funcionamientotelemetria_form.is_valid():
                if existing_funcionamientotelemetria: 
                    existing_funcionamientotelemetria.delete()
                funcionamientotelemetria_form.instance.date = date
                funcionamientotelemetria_form.instance.supervisor = supervisor
                funcionamientotelemetria_form.instance.lagoon = lagoon
                funcionamientotelemetria_form.save()
                request.session['funcionamientotelemetria_form_submitted'] = True
        elif 'operacionskimmers_submit' in request.POST:
            operacionskimmers_form = OperacionSkimmersForms(request.POST)
            if operacionskimmers_form.is_valid():
                if existing_operacionskimmers: 
                    existing_operacionskimmers.delete()
                operacionskimmers_form.instance.date = date
                operacionskimmers_form.instance.supervisor = supervisor
                operacionskimmers_form.instance.lagoon = lagoon
                operacionskimmers_form.save()
                request.session['operacionskimmers_form_submitted'] = True
        elif 'operacionultrasonido_submit' in request.POST:
            operacionultrasonido_form = OperacionUltrasonidoForms(request.POST)
            if operacionultrasonido_form.is_valid():
                if existing_operacionultrasonido: 
                    existing_operacionultrasonido.delete()
                operacionultrasonido_form.instance.date = date
                operacionultrasonido_form.instance.supervisor = supervisor
                operacionultrasonido_form.instance.lagoon = lagoon
                operacionultrasonido_form.save()
                request.session['operacionultrasonido_form_submitted'] = True
        elif 'infraestructura_submit' in request.POST:
            infraestructura_form = InfraestructuraForms(request.POST)
            if infraestructura_form.is_valid():
                if existing_infraestructura: 
                    existing_infraestructura.delete()
                infraestructura_form.instance.date = date
                infraestructura_form.instance.supervisor = supervisor
                infraestructura_form.instance.lagoon = lagoon
                infraestructura_form.save()
                request.session['infraestructura_form_submitted'] = True
        elif 'condicionliner_submit' in request.POST:
            condicionliner_form = CondicionLinerForms(request.POST)
            if condicionliner_form.is_valid():
                if existing_condicionliner: 
                    existing_condicionliner.delete()
                condicionliner_form.instance.date = date
                condicionliner_form.instance.supervisor = supervisor
                condicionliner_form.instance.lagoon = lagoon
                condicionliner_form.save()
                request.session['condicionliner_form_submitted'] = True
        elif 'condicionvisuallaguna_submit' in request.POST:
            condicionvisuallaguna_form = CondicionVisualLagunaForms(request.POST)
            if condicionvisuallaguna_form.is_valid():
                if existing_condicionvisuallaguna: 
                    existing_condicionvisuallaguna.delete()
                condicionvisuallaguna_form.instance.date = date
                condicionvisuallaguna_form.instance.supervisor = supervisor
                condicionvisuallaguna_form.instance.lagoon = lagoon
                condicionvisuallaguna_form.save()
                request.session['condicionvisuallaguna_form_submitted'] = True
        elif 'funcionamientoaguarelleno_submit' in request.POST:
            funcionamientoaguarelleno_form = FuncionamientoAguaRellenoForms(request.POST)
            if funcionamientoaguarelleno_form.is_valid():
                if existing_funcionamientoaguarelleno: 
                    existing_funcionamientoaguarelleno.delete()
                funcionamientoaguarelleno_form.instance.date = date
                funcionamientoaguarelleno_form.instance.supervisor = supervisor
                funcionamientoaguarelleno_form.instance.lagoon = lagoon
                funcionamientoaguarelleno_form.save()
                request.session['funcionamientoaguarelleno_form_submitted'] = True
        elif 'niveldelalaguna_submit' in request.POST:
            niveldelalaguna_form = NivelDeLaLagunaForms(request.POST)
            if niveldelalaguna_form.is_valid():
                if existing_niveldelalaguna: 
                    existing_niveldelalaguna.delete()
                niveldelalaguna_form.instance.date = date
                niveldelalaguna_form.instance.supervisor = supervisor
                niveldelalaguna_form.instance.lagoon = lagoon
                niveldelalaguna_form.save()
                request.session['niveldelalaguna_form_submitted'] = True
        elif 'medidasdemitigacion_submit' in request.POST:
            medidasdemitigacion_form = MedidasDeMitigacionForms(request.POST)
            if medidasdemitigacion_form.is_valid():
                if existing_medidasdemitigacion: 
                    existing_medidasdemitigacion.delete()
                medidasdemitigacion_form.instance.date = date
                medidasdemitigacion_form.instance.supervisor = supervisor
                medidasdemitigacion_form.instance.lagoon = lagoon
                medidasdemitigacion_form.save()
                request.session['medidasdemitigacion_form_submitted'] = True
    else:
        personal_form = PersonalDeLaLagunaForm(instance=latest_personal) if latest_personal else PersonalDeLaLagunaForm()
        limpieza_form = OperacionLimpiezaDeFondoForm(instance=latest_limpieza) if latest_limpieza else OperacionLimpiezaDeFondoForm()
        limpiezamanual_form = OperacionLimpiezaManualForm(instance=latest_limpiezamanual) if latest_limpiezamanual else OperacionLimpiezaManualForm()
        operacionfiltro_form = OperacionFiltroForms(instance=latest_operacionfiltro) if latest_operacionfiltro else OperacionFiltroForms()
        operacionsistemadosificacion_form = OperacionSistemaDosificacionForms(instance=latest_operacionsistemadosificacion) if latest_operacionsistemadosificacion else OperacionSistemaDosificacionForms()
        operacionsistemarecirculacion_form = OperacionSistemaRecirculacionForms(instance=latest_operacionsistemarecirculacion) if latest_operacionsistemarecirculacion else OperacionSistemaRecirculacionForms()
        funcionamientotelemetria_form = FuncionamientoTelemetriaForms(instance=latest_funcionamientotelemetria) if latest_funcionamientotelemetria else FuncionamientoTelemetriaForms()
        operacionskimmers_form = OperacionSkimmersForms(instance=latest_operacionskimmers) if latest_operacionskimmers else OperacionSkimmersForms()
        operacionultrasonido_form = OperacionUltrasonidoForms(instance=latest_operacionultrasonido) if latest_operacionultrasonido else OperacionUltrasonidoForms()
        infraestructura_form = InfraestructuraForms(instance=latest_infraestructura) if latest_infraestructura else InfraestructuraForms()
        condicionliner_form = CondicionLinerForms(instance=latest_condicionliner) if latest_condicionliner else CondicionLinerForms()
        condicionvisuallaguna_form = CondicionVisualLagunaForms(instance=latest_condicionvisuallaguna) if latest_condicionvisuallaguna else CondicionVisualLagunaForms()
        funcionamientoaguarelleno_form = FuncionamientoAguaRellenoForms(instance=latest_funcionamientoaguarelleno) if latest_funcionamientoaguarelleno else FuncionamientoAguaRellenoForms()
        niveldelalaguna_form = NivelDeLaLagunaForms(instance=latest_niveldelalaguna) if latest_niveldelalaguna else NivelDeLaLagunaForms()
        medidasdemitigacion_form = MedidasDeMitigacionForms(instance=latest_medidasdemitigacion) if latest_medidasdemitigacion else MedidasDeMitigacionForms()

    return render(request, 'main/results.html', {
    'personal_form': personal_form,
    'limpieza_form': limpieza_form,
    'limpiezamanual_form': limpiezamanual_form,
    'operacionfiltro_form': operacionfiltro_form,
    'operacionsistemadosificacion_form': operacionsistemadosificacion_form,
    'operacionsistemarecirculacion_form': operacionsistemarecirculacion_form,
    'funcionamientotelemetria_form': funcionamientotelemetria_form,
    'operacionskimmers_form': operacionskimmers_form,
    'operacionultrasonido_form': operacionultrasonido_form,
    'infraestructura_form': infraestructura_form,
    'condicionliner_form': condicionliner_form,
    'condicionvisuallaguna_form': condicionvisuallaguna_form,
    'funcionamientoaguarelleno_form': funcionamientoaguarelleno_form,
    'niveldelalaguna_form': niveldelalaguna_form,
    'medidasdemitigacion_form': medidasdemitigacion_form,
    })

def daily_report(request):
    import datetime

    today = datetime.date.today()
    weekday = today.weekday()

    # Determine Monday's date
    if weekday == 0:  # Monday
        monday_date = today
    else:
        monday_date = today - datetime.timedelta(days=weekday)

    # Determine Friday's date
    if weekday <= 3:  # Monday to Thursday
        friday_date = monday_date + datetime.timedelta(days=4)
    elif weekday == 4:  # Friday
        friday_date = today
    else:  # Saturday and Sunday
        friday_date = today - datetime.timedelta(days=(weekday - 4))

    # Calculate image counts for Monday column (previous Friday, Saturday, Sunday)
    start_date_monday = monday_date - datetime.timedelta(days=3)
    end_date_monday = monday_date - datetime.timedelta(days=1)
    
    # Calculate image counts for Friday column (previous Monday to Thursday)
    start_date_friday = friday_date - datetime.timedelta(days=4)
    end_date_friday = friday_date - datetime.timedelta(days=1)

    lagoons = Laguna.objects.all().annotate(
        total_images_monday=Count(
            'images',
            filter=Q(images__date__range=(start_date_monday, end_date_monday))
        ),
        selected_images_monday=Count(
            'images',
            filter=Q(images__date__range=(start_date_monday, end_date_monday), images__selected=True)
        ),
        total_images_friday=Count(
            'images',
            filter=Q(images__date__range=(start_date_friday, end_date_friday))
        ),
        selected_images_friday=Count(
            'images',
            filter=Q(images__date__range=(start_date_friday, end_date_friday), images__selected=True)
        )
    )

    context = {
        'lagoons': lagoons,
        'monday_date': monday_date,
        'friday_date': friday_date
    }
    return render(request, 'main/daily_report.html', context)

def lagoon_detail(request, idLagunas):
    date_today = date.today()

    date_str = 'monday' if 'monday' in request.path else 'friday'
    date_obj = datetime.date.today()

    # Determine the start and end dates for the images
    start_date = date_obj - timedelta(days=date_obj.weekday())  # This will give the last Monday
    end_date = date_obj

    # Fetch the images for the lagoon between these dates
    images = LagunaImage.objects.filter(laguna_id=idLagunas, date__range=(start_date, end_date))

    detail = LagoonDetail.objects.filter(idLagunas_id=idLagunas).order_by('-date').first()
    lagoon_name = Laguna.objects.get(idLagunas=idLagunas).Nombre
    laguna_instance = Laguna.objects.get(idLagunas=idLagunas)

    if request.method == 'POST':
        if detail and detail.date == date_today:
            pass  
        else:
            detail = LagoonDetail(idLagunas_id=idLagunas, date=date_today)

        uploaded_files = request.FILES.getlist('userfile[]')
        for uploaded_file in uploaded_files:
            image = LagunaImage()
            image.laguna_id = idLagunas
            image.photo = uploaded_file
            image.date = timezone.now().date()
            image.save()

        detail.comentrelevant = request.POST.get('comentrelevant')
        detail.comentqw = request.POST.get('comentqw')
        detail.comentlgm = request.POST.get('comentlgm')  # Update Comments on Lagoon Maintenance
        detail.milestone = request.POST.get('milestone')  # Update Milestones
        detail.responsible = request.POST.get('responsible')  # Update Responsibility of the Milestone dropdown
        detail.status = request.POST.get('status')  # Update Status dropdown
        detail.showroom = 'showroom' in request.POST  # Update Showroom Lagoon checkbox

        detail.save()

    context = {
        'images': images,  # Add the images to the context
        'Laguna': laguna_instance,
        'idLagunas': idLagunas,
        'lagoon_name': lagoon_name,
        'date': date_str,
        'detail': detail,
        'date_today': date_today
    }
    return render(request, 'main/idlagoon.html', context)

def manuals_view(request):
    manuals = [
        {'file_url': 'varios/manuales/2015-05-04_Procedure_For_Working_On_Confined.pdf', 'name': '2015-05-04 Procedure For Working On Confined'},
        {'file_url': 'varios/manuales/2015-12-02_ProcedimientoDeTrabajoEnEspaciosCo.pdf', 'name': '2015-12-02 ProcedimientoDeTrabajoEnEspaciosCo'},
        {'file_url': 'varios/manuales/Manual Mantenimiento y Operaciones.pdf', 'name': 'Manual Mantenimiento y Operaciones'},
        {'file_url': 'varios/manuales/Manual_Imops.pdf', 'name': 'Manual_Imops'},
        {'file_url': 'varios/manuales/PhotographicProcedures_ForLagoonMonitoring.pd.pdf', 'name': 'PhotographicProcedures_ForLagoonMonitoring.pd'},
        {'file_url': 'varios/manuales/Presentacion Portal Operaciones v.1.pdf', 'name': 'Presentacion Portal Operaciones v.1'},
        {'file_url': 'varios/manuales/Procedimiento Cambio de Cepillos.pdf', 'name': 'Procedimiento Cambio de Cepillos'},
        {'file_url': 'varios/manuales/Procedimiento Enjuague Linea Refrigeracion MO.pdf', 'name': 'Procedimiento Enjuague Linea Refrigeracion MO'},
        {'file_url': 'varios/manuales/Procedimiento Limpieza Liner con Acido.pdf', 'name': 'Procedimiento Limpieza Liner con Acido'},
        {'file_url': 'varios/manuales/ProcedimientoFotografico_Paramonitoreodelagun.pdf', 'name': 'Procedimiento Fotografico Para monitoreo de la laguna'},
    ]

    return render(request, 'main/manuals.html', {'manuals': manuals})

def stock_view(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            new_entry = Laguna_Stock(
                date=form.cleaned_data['date'],
                laguna=form.cleaned_data['laguna'],
                stock_or_supply=form.cleaned_data['stock_or_supply'],
                cl_ap2hi_tank=form.cleaned_data['cl_ap2hi_tank'],
                cl_ap2hi_storage=form.cleaned_data['cl_ap2hi_storage'],
                cl_fh1lo_tank=form.cleaned_data['cl_fh1lo_tank'],
                cl_fh1lo_storage=form.cleaned_data['cl_fh1lo_storage'],
                cl_flo12_tank=form.cleaned_data['cl_flo12_tank'],
                cl_flo12_storage=form.cleaned_data['cl_flo12_storage'],
                cl_cotflo_tank=form.cleaned_data['cl_cotflo_tank'],
                cl_cotflo_storage=form.cleaned_data['cl_cotflo_storage'],
                cl_mb010_tank=form.cleaned_data['cl_mb010_tank'],
                cl_mb010_storage=form.cleaned_data['cl_mb010_storage'],
            )
            new_entry.save()
            messages.success(request, "Stock successfully added.")
            return redirect('/stock/')  # Replace 'stock_view' with your view's name if it's different

        else:
            messages.error(request, "Ingresa todos los campos preguntados")
    else:
        form = StockForm()  # Initialize an empty form for a GET request
   
    lagunas = Laguna.objects.all()
    return render(request, 'main/stock.html', {'form': form, 'lagunas': lagunas})

def select_laguna_view(request):
    lagunas = Laguna.objects.all()
    return render(request, 'main/select_laguna.html', {'lagunas': lagunas})

def notas_view(request, nombre_laguna):
    lagoon = get_object_or_404(Laguna, Nombre=nombre_laguna)
    id_laguna = lagoon.idLagunas

    modelos = [
        (PersonalDeLaLaguna, 'nota_personal'),
        (OperacionLimpiezaDeFondo, 'nota_limpieza_fondo'),
        (OperacionLimpiezaManual, 'nota_limpieza_manual'),
        (OperacionFiltro, 'nota_filtro'),
        (OperacionSistemaDosificacion, 'nota_sistema_dosificacion'),
        (OperacionSistemaRecirculacion, 'nota_sistema_recirculacion'),
        (FuncionamientoTelemetria, 'nota_telemetria'),
        (OperacionSkimmers, 'nota_skimmers'),
        (OperacionUltrasonido, 'nota_ultrasonido'),
        (Infraestructura, 'nota_infraestructura'),
        (CondicionLiner, 'nota_condicion_liner'),
        (CondicionVisualLaguna, 'nota_condicion_visual'),
        (FuncionamientoAguaRelleno, 'nota_agua_relleno'),
        (NivelDeLaLaguna, 'nota_nivel_laguna'),
        (MedidasDeMitigacion, 'nota_mitigacion')
    ]

    notas_combinadas = {}
    promedios = []

    for modelo, clave_nota in modelos:
        for obj in modelo.objects.filter(lagoon_id=id_laguna):
            fecha = obj.date
            if fecha not in notas_combinadas:
                notas_combinadas[fecha] = {'supervisor': obj.supervisor, 'notas': {}}
            notas_combinadas[fecha]['notas'][clave_nota] = getattr(obj, 'nota', None)

    for fecha, datos in notas_combinadas.items():
        notas_numericas = [nota for nota in datos['notas'].values() if isinstance(nota, (int, float))]
        notas = [nota for nota in datos['notas'].values() if nota is not None]
        promedio = sum(notas_numericas) / len(notas_numericas) if notas_numericas else None
        datos['promedio'] = promedio

    # Preparar lista para la plantilla
    notas_lista = [{'fecha': fecha, **datos} for fecha, datos in notas_combinadas.items()]
     
    return render(request, 'main/notas.html', {
        'notas': notas_lista, 
        'nombre_laguna': nombre_laguna,
        'full_width': True
    })

def semanal_selection_view(request):
    lagunas = Laguna.objects.all()
    return render(request, 'main/select_laguna_2.html', {'lagunas': lagunas})

def display_images_view(request, idLagunas, fecha):
    date_format = "%Y-%m-%d"
    end_date = datetime.strptime(fecha, date_format).date()
    start_date = end_date - timedelta(days=7)

    laguna = Laguna.objects.get(idLagunas=idLagunas)

    # Retrieve images for this Laguna between the start_date and end_date
    images = LagunaImage.objects.filter(
        laguna=laguna,
        date__range=(start_date, end_date)
    ).order_by('date', 'photo')  # Images are ordered by date

    # Group images by date
    grouped_images = {k: list(v) for k, v in groupby(images, key=attrgetter('date'))}
    latest_relevant_matter = RelevantMatters.objects.filter(laguna=laguna).order_by('-date').first()

    if request.method == 'POST':
        new_text = request.POST.get('relevant_matter_text')
        if new_text:
            RelevantMatters.objects.filter(laguna=laguna, date=end_date).delete()
            RelevantMatters.objects.create(laguna=laguna, text=new_text, date=end_date)
            return redirect('display_images', idLagunas=idLagunas, fecha=fecha)

    return render(request, 'main/display_images.html', {
        'grouped_images': grouped_images,
        'laguna': laguna,
        'fecha': fecha,
        'latest_relevant_matter': latest_relevant_matter
    })

@require_http_methods(["POST"])
def upload_image_view(request, idLagunas, fecha):
    laguna = Laguna.objects.get(idLagunas=idLagunas)
    date = parse_date(fecha)
    
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        image_instance = LagunaImage(laguna=laguna, photo=photo, date=date)
        image_instance.set_upload_date(date)
        image_instance.save()


    return redirect('display_images', idLagunas=idLagunas, fecha=fecha)
    
@csrf_exempt
def update_image_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_id = data.get('image_id')
        selected = data.get('selected', False)
        
        try:
            image = LagunaImage.objects.get(id=image_id)
            image.selected = selected
            image.save()
            return JsonResponse({'status': 'success'})
        except LagunaImage.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def semanal_selection_view2(request):
    lagunas = Laguna.objects.all()
    supervisors = Supervisor.objects.all()  # Query all supervisors
    return render(request, 'main/select_laguna_3.html', {'lagunas': lagunas, 'supervisors': supervisors})

def imops_view(request):
    if request.method == 'POST':
        form = LagunaSelectionForm(request.POST)
        if form.is_valid():
            selected_laguna = form.cleaned_data['laguna']
            num_imops = IMOP.objects.filter(laguna=selected_laguna).count()
            month_year = form.cleaned_data['date']
            selected_laguna = form.cleaned_data['laguna']
            
            # Additional logic to handle the selected data
            # For example, redirecting to another page or passing data to another function
            
            return redirect('some_view_name')  # Replace with your desired redirect
    else:
        form = LagunaSelectionForm()
    
    completed_imops = IMOP.objects.filter(is_completed=True)
    incomplete_imops = IMOP.objects.filter(is_completed=False)

    return render(request, 'main/imops.html', {
        'form': form,
        'completed_imops': completed_imops,
        'incomplete_imops': incomplete_imops
    })

def supervisor_relevant_matters_view(request, supervisor_name):
    supervisor = get_object_or_404(Supervisor, name=supervisor_name)
    lagunas = supervisor.lagunas.all()

    lagunas_with_matters = {laguna: [] for laguna in lagunas}
    for laguna in lagunas:
        relevant_matters = RelevantMatters.objects.filter(laguna=laguna).order_by('date')
        lagunas_with_matters[laguna] = relevant_matters if relevant_matters.exists() else None

    if request.method == 'POST':
        if 'update_matter' in request.POST:
            matter_id = request.POST.get('matter_id')
            if matter_id:  # Existing matter
                matter = get_object_or_404(RelevantMatters, id=matter_id)
                matter.date = timezone.now().date()
                matter.text = request.POST.get('text', matter.text)
                matter.save()
            else:  # New matter
                laguna_id = request.POST.get('laguna_id')
                laguna = get_object_or_404(Laguna, idLagunas=laguna_id)
                new_text = request.POST.get('text', '')
                new_matter = RelevantMatters(laguna=laguna, text=new_text, date=timezone.now().date())
                new_matter.save()

            return redirect('supervisor_relevant_matters', supervisor_name=supervisor_name)

    return render(request, 'main/supervisor_relevant_matters.html', {
        'supervisor': supervisor,
        'lagunas_with_matters': lagunas_with_matters,
    })

def supervisor_relevant_matters_page2(request, supervisor_name):
    supervisor = get_object_or_404(Supervisor, name=supervisor_name)
    lagunas = supervisor.lagunas.all()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    lagunas_with_images = {}
    for laguna in lagunas:
        images = LagunaImage.objects.filter(
            laguna=laguna,
            date__range=(start_date, end_date)
        ).order_by('date', 'photo')
        lagunas_with_images[laguna] = images

    return render(request, 'main/supp_relevant_2.html', {
        'supervisor': supervisor,
        'lagunas_with_images': lagunas_with_images,
        'start_date': start_date,
        'end_date': end_date
    })