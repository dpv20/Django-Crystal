from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from datetime import datetime, timedelta 
from datetime import date, timedelta
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models import Count, Q, Case, When, Value, BooleanField
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from itertools import groupby
from operator import attrgetter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from xhtml2pdf import pisa
import calendar
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from calendar import monthrange
from django.contrib.auth import authenticate, login
import requests
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
#import matplotlib.pyplot as plt
from django.conf import settings
import numpy as np
import os
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string, get_template
from io import BytesIO


from .models import (
    ToDoList,
    Item,
    Supervisor,
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
    SupervisorLaguna,
    AditivosLaguna,
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
    RelevantMatterForm,
    LoginForm,
    FeedbackForm,
    )

from .forms import (
    PersonalDeLaLagunaFormEN,  
    OperacionLimpiezaDeFondoFormEN,
    OperacionLimpiezaManualFormEN,
    OperacionFiltroFormsEN,
    OperacionSistemaDosificacionFormsEN,
    OperacionSistemaRecirculacionFormsEN,
    FuncionamientoTelemetriaFormsEN,
    OperacionSkimmersFormsEN,
    OperacionUltrasonidoFormsEN,
    InfraestructuraFormsEN,
    CondicionLinerFormsEN,
    CondicionVisualLagunaFormsEN,
    FuncionamientoAguaRellenoFormsEN,
    NivelDeLaLagunaFormsEN,
    MedidasDeMitigacionFormsEN,
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

@login_required
def home(request):
    lagunas = Laguna.objects.all()
    
    # Check the language cookie
    language = request.COOKIES.get('language', 'en')  # Default to English if the cookie is not set
    
    # Choose the template based on the language preference
    if language == 'es':
        template_name = 'main/home.html'
    else:  # Assuming 'en' or any other value defaults to English
        template_name = 'main/english/home_en.html'
    
    return render(request, template_name, {'lagunas': lagunas, 'full_width': True})

@login_required
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

@login_required
def testing(response):
    return render(response, "main/testing.html", {})

@login_required
def view(response):
    return render(response, "main/view.html", {})

@login_required
def laguna_database(request):
    lagunas = Laguna.objects.all()
    return render(request, 'main/laguna_database.html', {'lagunas': lagunas, 'full_width': True})

@login_required
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

@login_required
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
            language = request.COOKIES.get('language')
            request.session['fecha'] = str(form.cleaned_data['fecha'])
            request.session['supervisor'] = str(form.cleaned_data['supervisor'])
            request.session['lagoons'] = str(form.cleaned_data['lagoons'])
            if language == 'en':
                return redirect('results_EN')
            else:
                return redirect('results')

    personal_entries = PersonalDeLaLaguna.objects.all()  # Query the database
    return render(request, "main/initial_form.html", {"form": form, "personal_entries": personal_entries})

@login_required
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

@login_required
def results_EN_view(request):
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
    personal_form = PersonalDeLaLagunaFormEN()
    limpieza_form = OperacionLimpiezaDeFondoFormEN()
    limpiezamanual_form = OperacionLimpiezaManualFormEN()
    operacionfiltro_form = OperacionFiltroFormsEN()
    operacionsistemadosificacion_form = OperacionSistemaDosificacionFormsEN()
    operacionsistemarecirculacion_form = OperacionSistemaRecirculacionFormsEN()
    funcionamientotelemetria_form = FuncionamientoTelemetriaFormsEN()
    operacionskimmers_form = OperacionSkimmersFormsEN()
    operacionultrasonido_form = OperacionUltrasonidoFormsEN()
    infraestructura_form = InfraestructuraFormsEN()
    condicionliner_form = CondicionLinerFormsEN()
    condicionvisuallaguna_form = CondicionVisualLagunaFormsEN()
    funcionamientoaguarelleno_form = FuncionamientoAguaRellenoFormsEN()
    niveldelalaguna_form = NivelDeLaLagunaFormsEN()
    medidasdemitigacion_form = MedidasDeMitigacionFormsEN()






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
            personal_form = PersonalDeLaLagunaFormEN(request.POST)
            if personal_form.is_valid(): 
                if existing_personal:
                    existing_personal.delete()
                personal_form.instance.date = date
                personal_form.instance.supervisor = supervisor
                personal_form.instance.lagoon = lagoon
                personal_form.save()
                request.session['personal_form_submitted'] = True
        elif 'limpieza_submit' in request.POST:
            limpieza_form = OperacionLimpiezaDeFondoFormEN(request.POST)
            if limpieza_form.is_valid():
                if existing_limpieza: 
                    existing_limpieza.delete()
                limpieza_form.instance.date = date
                limpieza_form.instance.supervisor = supervisor
                limpieza_form.instance.lagoon = lagoon
                limpieza_form.save()
                request.session['limpieza_form_submitted'] = True
        elif 'limpiezamanual_submit' in request.POST:
            limpiezamanual_form = OperacionLimpiezaManualFormEN(request.POST)
            if limpiezamanual_form.is_valid():
                if existing_limpiezamanual: 
                    existing_limpiezamanual.delete()
                limpiezamanual_form.instance.date = date
                limpiezamanual_form.instance.supervisor = supervisor
                limpiezamanual_form.instance.lagoon = lagoon
                limpiezamanual_form.save()
                request.session['limpiezamanual_form_submitted'] = True
        elif 'operacionfiltro_submit' in request.POST:
            operacionfiltro_form = OperacionFiltroFormsEN(request.POST)
            if operacionfiltro_form.is_valid():
                if existing_operacionfiltro: 
                    existing_operacionfiltro.delete()
                operacionfiltro_form.instance.date = date
                operacionfiltro_form.instance.supervisor = supervisor
                operacionfiltro_form.instance.lagoon = lagoon
                operacionfiltro_form.save()
                request.session['operacionfiltro_form_submitted'] = True
        elif 'operacionsistemadosificacion_submit' in request.POST:
            operacionsistemadosificacion_form = OperacionSistemaDosificacionFormsEN(request.POST)
            if operacionsistemadosificacion_form.is_valid():
                if existing_operacionsistemadosificacion: 
                    existing_operacionsistemadosificacion.delete()
                operacionsistemadosificacion_form.instance.date = date
                operacionsistemadosificacion_form.instance.supervisor = supervisor
                operacionsistemadosificacion_form.instance.lagoon = lagoon
                operacionsistemadosificacion_form.save()
                request.session['operacionsistemadosificacion_form_submitted'] = True
        elif 'operacionsistemarecirculacion_submit' in request.POST:
            operacionsistemarecirculacion_form = OperacionSistemaRecirculacionFormsEN(request.POST)
            if operacionsistemarecirculacion_form.is_valid():
                if existing_operacionsistemarecirculacion: 
                    existing_operacionsistemarecirculacion.delete()
                operacionsistemarecirculacion_form.instance.date = date
                operacionsistemarecirculacion_form.instance.supervisor = supervisor
                operacionsistemarecirculacion_form.instance.lagoon = lagoon
                operacionsistemarecirculacion_form.save()
                request.session['operacionsistemarecirculacion_form_submitted'] = True
        elif 'funcionamientotelemetria_submit' in request.POST:
            funcionamientotelemetria_form = FuncionamientoTelemetriaFormsEN(request.POST)
            if funcionamientotelemetria_form.is_valid():
                if existing_funcionamientotelemetria: 
                    existing_funcionamientotelemetria.delete()
                funcionamientotelemetria_form.instance.date = date
                funcionamientotelemetria_form.instance.supervisor = supervisor
                funcionamientotelemetria_form.instance.lagoon = lagoon
                funcionamientotelemetria_form.save()
                request.session['funcionamientotelemetria_form_submitted'] = True
        elif 'operacionskimmers_submit' in request.POST:
            operacionskimmers_form = OperacionSkimmersFormsEN(request.POST)
            if operacionskimmers_form.is_valid():
                if existing_operacionskimmers: 
                    existing_operacionskimmers.delete()
                operacionskimmers_form.instance.date = date
                operacionskimmers_form.instance.supervisor = supervisor
                operacionskimmers_form.instance.lagoon = lagoon
                operacionskimmers_form.save()
                request.session['operacionskimmers_form_submitted'] = True
        elif 'operacionultrasonido_submit' in request.POST:
            operacionultrasonido_form = OperacionUltrasonidoFormsEN(request.POST)
            if operacionultrasonido_form.is_valid():
                if existing_operacionultrasonido: 
                    existing_operacionultrasonido.delete()
                operacionultrasonido_form.instance.date = date
                operacionultrasonido_form.instance.supervisor = supervisor
                operacionultrasonido_form.instance.lagoon = lagoon
                operacionultrasonido_form.save()
                request.session['operacionultrasonido_form_submitted'] = True
        elif 'infraestructura_submit' in request.POST:
            infraestructura_form = InfraestructuraFormsEN(request.POST)
            if infraestructura_form.is_valid():
                if existing_infraestructura: 
                    existing_infraestructura.delete()
                infraestructura_form.instance.date = date
                infraestructura_form.instance.supervisor = supervisor
                infraestructura_form.instance.lagoon = lagoon
                infraestructura_form.save()
                request.session['infraestructura_form_submitted'] = True
        elif 'condicionliner_submit' in request.POST:
            condicionliner_form = CondicionLinerFormsEN(request.POST)
            if condicionliner_form.is_valid():
                if existing_condicionliner: 
                    existing_condicionliner.delete()
                condicionliner_form.instance.date = date
                condicionliner_form.instance.supervisor = supervisor
                condicionliner_form.instance.lagoon = lagoon
                condicionliner_form.save()
                request.session['condicionliner_form_submitted'] = True
        elif 'condicionvisuallaguna_submit' in request.POST:
            condicionvisuallaguna_form = CondicionVisualLagunaFormsEN(request.POST)
            if condicionvisuallaguna_form.is_valid():
                if existing_condicionvisuallaguna: 
                    existing_condicionvisuallaguna.delete()
                condicionvisuallaguna_form.instance.date = date
                condicionvisuallaguna_form.instance.supervisor = supervisor
                condicionvisuallaguna_form.instance.lagoon = lagoon
                condicionvisuallaguna_form.save()
                request.session['condicionvisuallaguna_form_submitted'] = True
        elif 'funcionamientoaguarelleno_submit' in request.POST:
            funcionamientoaguarelleno_form = FuncionamientoAguaRellenoFormsEN(request.POST)
            if funcionamientoaguarelleno_form.is_valid():
                if existing_funcionamientoaguarelleno: 
                    existing_funcionamientoaguarelleno.delete()
                funcionamientoaguarelleno_form.instance.date = date
                funcionamientoaguarelleno_form.instance.supervisor = supervisor
                funcionamientoaguarelleno_form.instance.lagoon = lagoon
                funcionamientoaguarelleno_form.save()
                request.session['funcionamientoaguarelleno_form_submitted'] = True
        elif 'niveldelalaguna_submit' in request.POST:
            niveldelalaguna_form = NivelDeLaLagunaFormsEN(request.POST)
            if niveldelalaguna_form.is_valid():
                if existing_niveldelalaguna: 
                    existing_niveldelalaguna.delete()
                niveldelalaguna_form.instance.date = date
                niveldelalaguna_form.instance.supervisor = supervisor
                niveldelalaguna_form.instance.lagoon = lagoon
                niveldelalaguna_form.save()
                request.session['niveldelalaguna_form_submitted'] = True
        elif 'medidasdemitigacion_submit' in request.POST:
            medidasdemitigacion_form = MedidasDeMitigacionFormsEN(request.POST)
            if medidasdemitigacion_form.is_valid():
                if existing_medidasdemitigacion: 
                    existing_medidasdemitigacion.delete()
                medidasdemitigacion_form.instance.date = date
                medidasdemitigacion_form.instance.supervisor = supervisor
                medidasdemitigacion_form.instance.lagoon = lagoon
                medidasdemitigacion_form.save()
                request.session['medidasdemitigacion_form_submitted'] = True
    else:
        personal_form = PersonalDeLaLagunaFormEN(instance=latest_personal) if latest_personal else PersonalDeLaLagunaFormEN()
        limpieza_form = OperacionLimpiezaDeFondoFormEN(instance=latest_limpieza) if latest_limpieza else OperacionLimpiezaDeFondoFormEN()
        limpiezamanual_form = OperacionLimpiezaManualFormEN(instance=latest_limpiezamanual) if latest_limpiezamanual else OperacionLimpiezaManualFormEN()
        operacionfiltro_form = OperacionFiltroFormsEN(instance=latest_operacionfiltro) if latest_operacionfiltro else OperacionFiltroFormsEN()
        operacionsistemadosificacion_form = OperacionSistemaDosificacionFormsEN(instance=latest_operacionsistemadosificacion) if latest_operacionsistemadosificacion else OperacionSistemaDosificacionFormsEN()
        operacionsistemarecirculacion_form = OperacionSistemaRecirculacionFormsEN(instance=latest_operacionsistemarecirculacion) if latest_operacionsistemarecirculacion else OperacionSistemaRecirculacionFormsEN()
        funcionamientotelemetria_form = FuncionamientoTelemetriaFormsEN(instance=latest_funcionamientotelemetria) if latest_funcionamientotelemetria else FuncionamientoTelemetriaFormsEN()
        operacionskimmers_form = OperacionSkimmersFormsEN(instance=latest_operacionskimmers) if latest_operacionskimmers else OperacionSkimmersFormsEN()
        operacionultrasonido_form = OperacionUltrasonidoFormsEN(instance=latest_operacionultrasonido) if latest_operacionultrasonido else OperacionUltrasonidoFormsEN()
        infraestructura_form = InfraestructuraFormsEN(instance=latest_infraestructura) if latest_infraestructura else InfraestructuraFormsEN()
        condicionliner_form = CondicionLinerFormsEN(instance=latest_condicionliner) if latest_condicionliner else CondicionLinerFormsEN()
        condicionvisuallaguna_form = CondicionVisualLagunaFormsEN(instance=latest_condicionvisuallaguna) if latest_condicionvisuallaguna else CondicionVisualLagunaFormsEN()
        funcionamientoaguarelleno_form = FuncionamientoAguaRellenoFormsEN(instance=latest_funcionamientoaguarelleno) if latest_funcionamientoaguarelleno else FuncionamientoAguaRellenoFormsEN()
        niveldelalaguna_form = NivelDeLaLagunaFormsEN(instance=latest_niveldelalaguna) if latest_niveldelalaguna else NivelDeLaLagunaFormsEN()
        medidasdemitigacion_form = MedidasDeMitigacionFormsEN(instance=latest_medidasdemitigacion) if latest_medidasdemitigacion else MedidasDeMitigacionFormsEN()

    return render(request, 'main/english/results_EN.html', {
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def select_laguna_view(request):
    lagunas = Laguna.objects.all()
    return render(request, 'main/select_laguna.html', {'lagunas': lagunas})

@login_required
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

@login_required
def semanal_selection_view(request):
    lagunas = Laguna.objects.all()
    return render(request, 'main/select_laguna_2.html', {'lagunas': lagunas})

@login_required
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

@login_required
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
    
@login_required
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

@login_required
def semanal_selection_view2(request):
    lagunas = Laguna.objects.all()
    supervisors = Supervisor.objects.all()  # Query all supervisors
    return render(request, 'main/select_laguna_3.html', {'lagunas': lagunas, 'supervisors': supervisors})

@login_required
def imops_view(request):
    if request.method == 'POST':
        form = LagunaSelectionForm(request.POST)
        if form.is_valid():
            selected_laguna = form.cleaned_data['laguna']
            month_year = form.cleaned_data['date']
            selected_laguna_id = selected_laguna.id  # Assuming 'laguna' field is a model instance
            

            year, month = month_year.year, month_year.month

            _, last_day = calendar.monthrange(year, month)
            date_str = f"{year}-{month:02d}-{last_day}"

            # Redirect to the 'create_imop_view' with the selected laguna ID and the last day of the selected month
            return redirect('create_imop_view', id_laguna=selected_laguna_id, date=date_str)
    else:
        form = LagunaSelectionForm()

    completed_imops = IMOP.objects.filter(is_completed=True)
    incomplete_imops = IMOP.objects.filter(is_completed=False)

    language = request.COOKIES.get('language', 'es')  # Default to 'es' if the cookie is not set
    template_name = 'main/english/imops_EN.html' if language == 'en' else 'main/imops.html'

    return render(request, template_name, {
        'form': form,
        'completed_imops': completed_imops,
        'incomplete_imops': incomplete_imops
    })

@login_required
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

@login_required
def supervisor_relevant_matters_page2(request, supervisor_name):
    supervisor = get_object_or_404(Supervisor, name=supervisor_name)
    lagunas = supervisor.lagunas.all()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)

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

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_image_selection(request):
    try:
        data = json.loads(request.body)
        image_id = data.get('image_id')
        selected = data.get('selected', False)

        image = LagunaImage.objects.get(id=image_id)
        image.selected = selected
        image.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@login_required
def supervisor_report(request, supervisor_name):
    supervisor = get_object_or_404(Supervisor, name=supervisor_name)

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    all_lagunas = supervisor.lagunas.all()

    lagunas_with_pictures = []
    lagunas_without_pictures = []

    for laguna in all_lagunas:
        images = LagunaImage.objects.filter(
            laguna=laguna,
            date__range=(start_date, end_date)
        )

        if images.exists():
            lagunas_with_pictures.append(laguna)
        else:
            lagunas_without_pictures.append(laguna)

    total_lagunas = len(all_lagunas)
    lagunas_with_pictures_count = len(lagunas_with_pictures)

    if total_lagunas > 0:
        percentage_with_pictures = (lagunas_with_pictures_count / total_lagunas) * 100
    else:
        percentage_with_pictures = 0

    return render(request, 'main/supervisor_report.html', {
        'supervisor': supervisor,
        'lagunas_with_pictures': lagunas_with_pictures,
        'lagunas_without_pictures': lagunas_without_pictures,
        'report_date': end_date,
        'percentage_with_pictures': percentage_with_pictures
    })

@login_required
def generate_pdf(request, supervisor_name):
    try:
        supervisor = get_object_or_404(Supervisor, name=supervisor_name)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)

        all_lagunas = supervisor.lagunas.all()
        lagunas_with_pictures = []
        lagunas_without_pictures = []

        for laguna in all_lagunas:
            images = LagunaImage.objects.filter(
                laguna=laguna,
                date__range=(start_date, end_date)
            )

            if images.exists():
                lagunas_with_pictures.append(laguna)
            else:
                lagunas_without_pictures.append(laguna)

        total_lagunas = len(all_lagunas)
        percentage_with_pictures = (len(lagunas_with_pictures) / total_lagunas) * 100 if total_lagunas > 0 else 0

        pdf_directory = 'C:\\code\\Djangopage\\PDF'
        pdf_filename = "supervisor_report.pdf"
        pdf_filepath = os.path.join(pdf_directory, pdf_filename)

        html_content = render_to_string('PDFs/supervisor_report_pdf.html', {
            'supervisor': supervisor,
            'lagunas_with_pictures': lagunas_with_pictures,
            'lagunas_without_pictures': lagunas_without_pictures,
            'report_date': end_date,
            'percentage_with_pictures': percentage_with_pictures,
            'is_pdf': True
        })

        with open(pdf_filepath, "w+b") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

            if pisa_status.err:
                raise Exception('PDF generation error')

        return JsonResponse({'status': 'success', 'message': f'PDF successfully saved at {pdf_filepath}'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@csrf_exempt
def generate_imop_id(request):
    try:
        data = json.loads(request.body)
        laguna_idLagunas = data.get('laguna_idLagunas')
        selected_date_str = data.get('selected_date')

        # Convert the date string to a datetime object
        selected_date = datetime.strptime(selected_date_str, '%b. %d, %Y').date()

        # Fetch the Laguna instance using idLagunas
        laguna = Laguna.objects.get(idLagunas=laguna_idLagunas)

        # Create a new IMOP instance
        imop = IMOP(laguna=laguna, date=selected_date, is_completed=False)
        imop.generate_id()

        return JsonResponse({'status': 'success', 'generated_id': imop.generated_id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def viernes_view(request, name="1"):
    image_path = f"media/viernes/{name}.png"
    return render(request, 'main/viernes.html', {'image_path': image_path})

def login_view(request):
    # Check if the user is already logged in
    if request.user.is_authenticated:
        # Optionally, redirect to home page if already logged in
        return redirect('home')
        # Or, you can render a different message/template if you prefer not to redirect
        # return render(request, 'main/already_logged_in.html')

    if request.method == 'POST':
        form = LoginForm(request.POST)  # Instantiate the form with submitted data
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard
            else:
                # Invalid login, add an error to the form
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()  # Instantiate a blank form for GET request

    # Check the language cookie to determine which template to render
    language = request.COOKIES.get('language', 'en')
    template_name = 'main/login.html' if language == 'es' else 'main/english/login_en.html'
    return render(request, template_name, {'form': form})

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Set the user to the currently logged-in user
            feedback.save()
            # Redirect or indicate success without redirecting, as preferred
            return render(request, 'main/submit_feedback.html', {'form_submitted': True})
    else:
        form = FeedbackForm()
    return render(request, 'main/submit_feedback.html', {'form': form, 'form_submitted': False})

@login_required    
def create_imop_view(request, id_laguna, date):
    laguna = get_object_or_404(Laguna, pk=id_laguna)
    year, month, day = map(int, date.split('-'))
    selected_date = timezone.datetime(year, month, day).date()
    date_from = selected_date - relativedelta(months=5)

    _, end_day = calendar.monthrange(year, month)

    start_date = timezone.datetime(year, month, 1).date()
    end_date = (timezone.datetime(year, month, end_day) + timedelta(days=1)).date()
    
    images = LagunaImage.objects.filter(
        laguna=laguna, 
        date__range=[start_date, end_date]
    )

    language = request.COOKIES.get('language', 'es')  # Default to 'es' if the cookie is not set
    template_name = 'main/english/imops_2_EN.html' if language == 'en' else 'main/imops_2.html'

    return render(request, template_name, {
        'laguna': laguna,
        'selected_date': selected_date,
        'date_from': date_from,
        'images': images,
        # ... other context variables if needed ...
    })

def download_lagoon_reports(idplatanus, year, month):
    downloads_dir = 'descargas'
    downloads_path = os.path.join(settings.MEDIA_ROOT, downloads_dir)
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)
    
    base_url = "https://infocenter.crystal-lagoons.com/api/reports"
    report_types = ['cleaning', 'connectivity']
    report_paths = {}

    for report_type in report_types:
        url = f"{base_url}/{report_type}/{idplatanus}?month={year}-{month}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"{report_type}_{idplatanus}_{year}-{month}.png"
                file_path = os.path.join(downloads_path, filename)
                
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {report_type} report for Laguna {idplatanus} to {file_path}.")
                
                # Calculate the relative web path
                web_path = os.path.join(settings.MEDIA_URL, downloads_dir, filename).replace('\\', '/')
                report_paths[f'{report_type}_url'] = web_path
            else:
                print(f"Failed to download {report_type} report for Laguna {idplatanus}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {report_type} report for Laguna {idplatanus}. Error: {e}")
    
    return report_paths
def get_last_instance(model, laguna):
        #print(f"Querying {model.__name__} with lagoon={laguna.idLagunas}")  # Use idLagunas instead of id
        return model.objects.filter(lagoon=laguna).order_by('-date').values('nota', 'comentario').first()
def generate_bar_graph(last_instances):
    column_names = [
        "PER", "BC", "MC", "FIL", "DOS", "REC",
        "TEL", "SKI", "ULT", "INF", "LIN", "VISUAL",
        "WAT", "LVL", "ENV"
    ]
    weights = {
        "PER": 0.05, "BC": 0.1, "MC": 0.1, "FIL": 0.1, "DOS": 0.07, "REC": 0.07,
        "TEL": 0.1, "SKI": 0.04, "ULT": 0.04, "INF": 0.03, "LIN": 0.08,
        "VIS": 0.14, "WAT": 0.02, "LVL": 0.04, "ENV": 0.02
    }

    #values = [instance.get('nota', 0) for instance in last_instances.values()]
    values = [instance.get('nota', 0) if instance is not None else 0 for instance in last_instances.values()]

    final_value = sum(values[i] * weight for i, (model, weight) in enumerate(weights.items()))

    colors = ['red' if value <= 3 else '#00AFC9' for value in values]
    final_color = 'red' if final_value <= 3 else '#00AFC9' 

    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.8
    positions = np.arange(len(column_names))
    gap = 1
    final_position = positions[-1] + gap + 1

    bars = ax.bar(positions, values, width=bar_width, label='Models', color=colors)
    final_bar = ax.bar(final_position, final_value, width=bar_width * 2, label='FINAL', color=final_color)

    # Draw dim grey lines across the graph for each rating number
    for rating in range(1, 6):  # For numbers 1 to 5
        ax.axhline(y=rating, color='dimgray', linewidth=1, linestyle='--')

    # Adjusting text insertion for value inside the bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height - 0.05, f'{value}',
                ha='center', va='top', color='white', fontsize=15, fontweight='bold')  # Added fontweight='bold'

    # For the final bar, adjust if you expect its value to be similarly displayed
    height = final_bar[0].get_height()
    ax.text(final_bar[0].get_x() + final_bar[0].get_width() / 2., height - 0.05, f'{final_value:.2f}',
            ha='center', va='top', color='white', fontsize=15, fontweight='bold')  # Added fontweight='bold'

    plt.title('NOTAS POR SECCIÓN', fontsize=16, fontweight='bold', fontname='arial', color='#00AFC9')
    all_positions = np.append(positions, final_position)
    ax.set_xticks(all_positions)
    ax.set_xticklabels(column_names + ["FINAL"], rotation=45, ha='right', fontsize=15)
    ax.set_ylim(0, max(values + [final_value]) * 1.1)
    plt.tight_layout()

    graph_path = os.path.join(settings.MEDIA_ROOT, 'model_ratings_bar_chart_with_final_gap.png')
    plt.savefig(graph_path)
    plt.close()

    return os.path.join(settings.MEDIA_URL, 'model_ratings_bar_chart_with_final_gap.png')
def graph_line_1(results, final_grade_nota, date_str):
    input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    dates = [input_date - relativedelta(months=i) for i in range(5, -1, -1)]
    values = [result[2] for result in results] + [final_grade_nota]
    date_labels = [date.strftime('%m/%y') for date in dates]
    
    turquoise = (64/255, 224/255, 208/255)
    plt.figure(figsize=(10, 6))
    plt.plot(date_labels, values, marker='o', linestyle='-', color='#00AFC9', linewidth=5)
    plt.title('EVALUACIÓN GENERAL', fontsize=15, fontweight='bold', fontname='arial', color='#00AFC9')
    plt.ylim(0, 5)  
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=1)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    

    graph_path = os.path.join(settings.MEDIA_ROOT, 'model_line_chart.png')
    plt.savefig(graph_path)
    plt.close()

    return os.path.join(settings.MEDIA_URL, 'model_line_chart.png')
def get_previous_imops(id_laguna, date_str):
    input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    laguna = get_object_or_404(Laguna, pk=id_laguna)
    results = []

    for i in range(1, 6):
        first_day_of_current_month = input_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        input_date = last_day_of_previous_month

        try:
            imop = IMOP.objects.filter(laguna=laguna, date=last_day_of_previous_month).first()
            if imop:
                results.append([float(imop.var_FH1LO), float(imop.var_AP2HI), float(imop.nota_final)])
            else:
                raise IMOP.DoesNotExist
        except IMOP.DoesNotExist:
            results.append([0, 0, 0])

    results = results[::-1]

    return results
def get_last_laguna_stock_data(idLagunas, date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    year, month = date_obj.year, date_obj.month

    last_entry = Laguna_Stock.objects.filter(
        laguna__idLagunas=idLagunas,
        date__year=year,
        date__month=month
    ).order_by('-date').first()  
    
    if not last_entry:
        return [0,0]

    cl_fh1lo_sum = last_entry.cl_fh1lo_tank + float(last_entry.cl_fh1lo_storage)
    cl_ap2hi_sum = last_entry.cl_ap2hi_tank + float(last_entry.cl_ap2hi_storage)
    #return [90, 80]
    return [cl_fh1lo_sum, cl_ap2hi_sum]
def get_leadtime_by_laguna(idLagunas):
    aditivo = AditivosLaguna.objects.filter(proyecto__idLagunas=idLagunas).first()
    if aditivo is None:
        return 0
    return aditivo.leadtime
def get_AP2_by_laguna(idLagunas):
    aditivo = AditivosLaguna.objects.filter(proyecto__idLagunas=idLagunas).first()
    if aditivo is None:
        return 0
    return aditivo.ddaDiaLts_AP2
def get_FH1_by_laguna(idLagunas):
    aditivo = AditivosLaguna.objects.filter(proyecto__idLagunas=idLagunas).first()
    if aditivo is None:
        return 0
    return aditivo.ddaDiaLts_FH1
def graph_line_2(values_fh1lo, values_ap2hi, Leadtime, date_str):
    from matplotlib.font_manager import FontProperties
    
    input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    dates = [input_date - relativedelta(months=i) for i in range(5, -1, -1)]
    
    date_labels = [date.strftime('%m/%y') for date in dates]
    
    leadtime_values = [Leadtime] * len(date_labels)
    
    # Specify figsize here, doubling the default width (6.4*2) and keeping the default height (4.8)
    fig, ax = plt.subplots(figsize=(12.8, 4.8))
    
    ax.plot(date_labels, values_fh1lo, label='CL-FH1LO', marker='o', color='#00AFC9', linewidth=2, markersize=10)
    ax.plot(date_labels, values_ap2hi, label='CL-AP2HI', marker='o', color='red', linewidth=2, markersize=10)
    
    ax.plot(date_labels, leadtime_values, label='Leadtime', linestyle='-', color='orange', linewidth=3)
    
    ax.set_xlabel('Fecha Reportada')
    ax.set_ylabel('Stock en Días')
    #ax.set_title('STOCK DE ADITIVOS', fontproperties=gotham_font, size=20, color='skyblue')

    all_values = values_fh1lo + values_ap2hi + leadtime_values
    # Set the minimum of the y-axis to 0, and let the maximum adjust dynamically
    ax.set_ylim(0, max(all_values) + 10)  

    plt.xticks(rotation=45)
    
    ax.legend()
    
    ax.grid(True)
    
    graph_path = os.path.join(settings.MEDIA_ROOT, 'model_line_chart_2.png')
    plt.savefig(graph_path)
    
    plt.close(fig)
    
    return os.path.join(settings.MEDIA_URL, 'model_line_chart_2.png')







@login_required
@require_http_methods(["GET", "POST"])
def imop_view(request, id_laguna, date):
    default_date = datetime.strptime(date, '%Y-%m-%d').date()
    laguna = get_object_or_404(Laguna, pk=id_laguna)
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    report_paths = None
    if laguna.idplatanus is None:
        print(f"Laguna {id_laguna} does not have an associated idplatanus.")
    else:
        year, month = selected_date.strftime("%Y"), selected_date.strftime("%m")
        report_paths = download_lagoon_reports(laguna.idplatanus, year, month)

    last_imop = IMOP.objects.filter(laguna=laguna).order_by('-date').first()

    if not last_imop:
        last_imop = IMOP(laguna=laguna, date=timezone.now())  
        last_imop.save()
    
    acros_and_values = [
        ('PER:', last_imop.PER),
        ('BC:', last_imop.BC),
        ('MC:', last_imop.MC),
        ('FIL:', last_imop.FIL),
        ('DOS:', last_imop.DOS),
        ('REC:', last_imop.REC),
        ('TEL:', last_imop.TEL),
        ('SKI:', last_imop.SKI),
        ('ULT:', last_imop.ULT),
        ('INF:', last_imop.INF),
        ('LIN:', last_imop.LIN),
        ('VISUAL:', last_imop.VISUAL),
        ('WAT:', last_imop.WAT),
        ('LVL:', last_imop.LVL),
        ('ENV:', last_imop.ENV),]

    models = [PersonalDeLaLaguna, OperacionLimpiezaDeFondo, OperacionLimpiezaManual, OperacionFiltro,
              OperacionSistemaDosificacion, OperacionSistemaRecirculacion, FuncionamientoTelemetria,
              OperacionSkimmers, OperacionUltrasonido, Infraestructura, CondicionLiner,
              CondicionVisualLaguna, FuncionamientoAguaRelleno, NivelDeLaLaguna, MedidasDeMitigacion]
    last_instances = {model.__name__: get_last_instance(model, laguna) for model in models}
    #valuesss = [instance.get('nota', 0) for instance in last_instances.values()]
    valuesss = [instance.get('nota', 0) if instance is not None else 0 for instance in last_instances.values()]

    weights_list = [0.05, 0.1, 0.1, 0.1, 0.07, 0.07, 0.1, 0.04, 0.04, 0.03, 0.08, 0.14, 0.02, 0.04, 0.02]
    final_grade_nota = sum(value * weight for value, weight in zip(valuesss, weights_list))


    year, month = selected_date.year, selected_date.month
    first_day, last_day = monthrange(year, month)
    laguna_images = LagunaImage.objects.filter(
        laguna=laguna,
        date__range=[datetime(year, month, 1).date(), datetime(year, month, last_day).date()],
        selected=True  
    )
    placeholders_needed = 8 - laguna_images.count()
    placeholder_path = os.path.join(settings.MEDIA_URL, 'placeholder_imop.jpg')
    placeholder_images = [{'photo': {'url': placeholder_path}} for _ in range(placeholders_needed)]
    combined_images = list(laguna_images) + placeholder_images
    laguna_images = combined_images

    resultss = get_previous_imops(id_laguna, date)

    graph_url = graph_line_1(resultss, final_grade_nota, date)
    graph_url_2 = generate_bar_graph(last_instances)
    #comentarios = {model.__name__: instance.get('comentario', '') for model in models for instance in [get_last_instance(model, laguna)]}
    comentarios = {model.__name__: (instance.get('comentario', '') if instance is not None else '') for model in models for instance in [get_last_instance(model, laguna)]}

    acros = ["PER:", "BC:", "MC:", "FIL:", "DOS:", "REC:", "TEL:", "SKI:", "ULT:", "INF:", "LIN:", "VISUAL:", "WAT:", "LVL:", "ENV:"]
    comentarios_acros = {acro: comentarios[model.__name__] for acro, model in zip(acros, models)}
    supervisor_name = f"{request.user.first_name} {request.user.last_name}"



    stocks_mes = get_last_laguna_stock_data(id_laguna, date)
    FH1_DECAI = float(get_FH1_by_laguna(id_laguna))
    AP2_DECAI = float(get_AP2_by_laguna(id_laguna))

    stocks_mes[0] = float(stocks_mes[0]/FH1_DECAI)
    stocks_mes[1] = float(stocks_mes[1]/AP2_DECAI)

    values_fh1lo = [result[0] for result in resultss] + [stocks_mes[0]]
    values_ap2hi = [result[1] for result in resultss] + [stocks_mes[1]]
    Leadtime =  float(get_leadtime_by_laguna(id_laguna))

    
    #values_fh1lo = [60, 70, 80, 90, 100, 110]
    #values_ap2hi = [50, 60, 70, 80, 90, 100]

    graph_url_3 = graph_line_2(values_fh1lo,values_ap2hi, Leadtime, date)

    

    context = {
        'laguna': laguna,
        'selected_date': selected_date,
        'supervisor_name': supervisor_name,
        'last_imop': last_imop,
        'acros': acros,
        'comentarios_acros': comentarios_acros,
        'acros_and_values': acros_and_values,
        'last_instances': last_instances,
        'laguna_images': laguna_images,  
        'graph_url': graph_url,
        'graph_url_2': graph_url_2,
        'graph_url_3': graph_url_3,
        'report_paths': report_paths,
    }

    if request.method == 'POST':
        resumen_ejecutivo = request.POST.get('resumen_ejecutivo', '')
        recomendaciones = request.POST.get('recomendaciones', '')
        temas_pendientes = request.POST.get('temas_pendientes', '')
        recomendaciones = request.POST.get('recomendaciones', '')
        temas_pendientes = request.POST.get('temas_pendientes', '')
        texts_list = [resumen_ejecutivo, recomendaciones, temas_pendientes]
        acronyms = ['PER', 'BC', 'MC', 'FIL', 'DOS', 'REC', 'TEL', 'SKI', 'ULT', 'INF', 'LIN', 'VISUAL', 'WAT', 'LVL', 'ENV']
        for acronym in acronyms:
                value = request.POST.get(acronym, '')
                if value: 
                    texts_list.append(value)
                if not value:
                    texts_list.append("")
        if last_imop is not None:
                resumen_ejecutivo_past = last_imop.resumen_ejecutivo
                resumen_ejecutivo_past_date = last_imop.resumen_ejecutivo_date
                recomendaciones_past = last_imop.recomendaciones
                recomendaciones_past_date = last_imop.recomendaciones_date
                temas_pendientes_past = last_imop.temas_pendientes
                temas_pendientes_past_date = last_imop.temas_pendientes_date
        else:
                resumen_ejecutivo_past = ""
                resumen_ejecutivo_past_date = default_date
                recomendaciones_past = ""
                recomendaciones_past_date = default_date
                temas_pendientes_past = ""
                temas_pendientes_past_date = default_date
        resumen_ejecutivo_date = resumen_ejecutivo_past_date if resumen_ejecutivo == resumen_ejecutivo_past else default_date
        recomendaciones_date = recomendaciones_past_date if recomendaciones == recomendaciones_past else default_date
        temas_pendientes_date = temas_pendientes_past_date if temas_pendientes == temas_pendientes_past else default_date
        acros_and_values_2 = [
                ('PER:', texts_list[3]),
                ('BC:', texts_list[4]),
                ('MC:', texts_list[5]),
                ('FIL:', texts_list[6]),
                ('DOS:', texts_list[7]),
                ('REC:', texts_list[8]),
                ('TEL:', texts_list[9]),
                ('SKI:', texts_list[10]),
                ('ULT:', texts_list[11]),
                ('INF:', texts_list[12]),
                ('LIN:', texts_list[13]),
                ('VISUAL:', texts_list[14]),
                ('WAT:', texts_list[15]),
                ('LVL:', texts_list[16]),
                ('ENV:', texts_list[17]),]
        IMOP.objects.filter(laguna=laguna, date=default_date).delete()
        new_imop = IMOP(
                laguna=laguna,
                date=default_date,
                resumen_ejecutivo=texts_list[0],
                resumen_ejecutivo_date=resumen_ejecutivo_date,
                recomendaciones=texts_list[1],
                recomendaciones_date=recomendaciones_date,
                temas_pendientes=texts_list[2],
                temas_pendientes_date=temas_pendientes_date,
                var_FH1LO = round(values_fh1lo[-1], 2),
                var_AP2HI = round(values_ap2hi[-1], 2),
                nota_final = round(final_grade_nota, 2),
                is_completed=True,
                PER=texts_list[3],
                BC=texts_list[4],
                MC=texts_list[5],
                FIL=texts_list[6],
                DOS=texts_list[7],
                REC=texts_list[8],
                TEL=texts_list[9],
                SKI=texts_list[10],
                ULT=texts_list[11],
                INF=texts_list[12],
                LIN=texts_list[13],
                VISUAL=texts_list[14],
                WAT=texts_list[15],
                LVL=texts_list[16],
                ENV=texts_list[17],
            )
        new_imop.generate_id()

        if 'submit_form' in request.POST and request.POST['submit_form'] == 'update_info':  
            context = {
            'laguna': laguna,
            'selected_date': selected_date,
            'supervisor_name': supervisor_name,
            'last_imop': new_imop,
            'acros': acros,
            'comentarios_acros': comentarios_acros,
            'acros_and_values': acros_and_values_2,
            'last_instances': last_instances,
            'laguna_images': laguna_images,  
            'graph_url': graph_url,
            'graph_url_2': graph_url_2,
            'graph_url_3': graph_url_3,
            'report_paths': report_paths,
            }
            return render(request, 'main/imops_3.html', context)

        elif request.POST.get('action') == 'generate_pdf':
            return redirect(reverse('imop_pdf_view', kwargs={'id_laguna': id_laguna, 'date': date}))
        



    return render(request, 'main/imops_3.html', context)


def link_callback(uri, rel):
    print(f"Resolving URI: {uri}")

    # use settings.MEDIA_ROOT and settings.STATIC_ROOT to construct absolute paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        return uri  # return as is for absolute URIs

    # Make sure the file exists
    if not os.path.isfile(path):
        raise Exception(f'Media or static file not found: {path}')
    return path
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
def imop_pdf_view(request, id_laguna, date):
    laguna = get_object_or_404(Laguna, pk=id_laguna)
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    if laguna.idplatanus is None:
        print(f"Laguna {id_laguna} does not have an associated idplatanus.")
    else:
        year, month = selected_date.strftime("%Y"), selected_date.strftime("%m")
        report_paths = download_lagoon_reports(laguna.idplatanus, year, month)
    last_imop = IMOP.objects.filter(laguna=laguna).order_by('-date').first()
    acros_and_values = [
        ('PER:', last_imop.PER),
        ('BC:', last_imop.BC),
        ('MC:', last_imop.MC),
        ('FIL:', last_imop.FIL),
        ('DOS:', last_imop.DOS),
        ('REC:', last_imop.REC),
        ('TEL:', last_imop.TEL),
        ('SKI:', last_imop.SKI),
        ('ULT:', last_imop.ULT),
        ('INF:', last_imop.INF),
        ('LIN:', last_imop.LIN),
        ('VISUAL:', last_imop.VISUAL),
        ('WAT:', last_imop.WAT),
        ('LVL:', last_imop.LVL),
        ('ENV:', last_imop.ENV),]
    models = [PersonalDeLaLaguna, OperacionLimpiezaDeFondo, OperacionLimpiezaManual, OperacionFiltro,
              OperacionSistemaDosificacion, OperacionSistemaRecirculacion, FuncionamientoTelemetria,
              OperacionSkimmers, OperacionUltrasonido, Infraestructura, CondicionLiner,
              CondicionVisualLaguna, FuncionamientoAguaRelleno, NivelDeLaLaguna, MedidasDeMitigacion]
    last_instances = {model.__name__: get_last_instance(model, laguna) for model in models}
    valuesss = [instance.get('nota', 0) for instance in last_instances.values()]
    valuesss = [instance.get('nota', 0) for instance in last_instances.values()]
    weights_list = [0.05, 0.1, 0.1, 0.1, 0.07, 0.07, 0.1, 0.04, 0.04, 0.03, 0.08, 0.14, 0.02, 0.04, 0.02]
    final_grade_nota = sum(value * weight for value, weight in zip(valuesss, weights_list))
    year, month = selected_date.year, selected_date.month
    first_day, last_day = monthrange(year, month)
    laguna_images = LagunaImage.objects.filter(
        laguna=laguna,
        date__range=[datetime(year, month, 1).date(), datetime(year, month, last_day).date()],
        selected=True  
    )
    placeholders_needed = 8 - laguna_images.count()
    placeholder_path = os.path.join(settings.MEDIA_URL, 'placeholder_imop.jpg')
    placeholder_images = [{'photo': {'url': placeholder_path}} for _ in range(placeholders_needed)]
    combined_images = list(laguna_images) + placeholder_images
    laguna_images = combined_images
    resultss = get_previous_imops(id_laguna, date)
    graph_url = graph_line_1(resultss, final_grade_nota, date)
    graph_url_2 = generate_bar_graph(last_instances)
    comentarios = {model.__name__: instance.get('comentario', '') for model in models for instance in [get_last_instance(model, laguna)]}
    acros = ["PER:", "BC:", "MC:", "FIL:", "DOS:", "REC:", "TEL:", "SKI:", "ULT:", "INF:", "LIN:", "VISUAL:", "WAT:", "LVL:", "ENV:"]
    comentarios_acros = {acro: comentarios[model.__name__] for acro, model in zip(acros, models)}
    supervisor_name = f"{request.user.first_name} {request.user.last_name}"
    stocks_mes = get_last_laguna_stock_data(id_laguna, date)
    FH1_DECAI = float(get_FH1_by_laguna(id_laguna))
    AP2_DECAI = float(get_AP2_by_laguna(id_laguna))
    stocks_mes[0] = float(stocks_mes[0]/FH1_DECAI)
    stocks_mes[1] = float(stocks_mes[1]/AP2_DECAI)
    values_fh1lo = [result[0] for result in resultss] + [stocks_mes[0]]
    values_ap2hi = [result[1] for result in resultss] + [stocks_mes[1]]
    Leadtime =  float(get_leadtime_by_laguna(id_laguna))
    graph_url_3 = graph_line_2(values_fh1lo,values_ap2hi, Leadtime, date)
    context = {
        'laguna': laguna,
        'selected_date': selected_date,
        'supervisor_name': supervisor_name,
        'last_imop': last_imop,
        'acros': acros,
        'comentarios_acros': comentarios_acros,
        'acros_and_values': acros_and_values,
        'last_instances': last_instances,
        'laguna_images': laguna_images,  
        'graph_url': graph_url,
        'graph_url_2': graph_url_2,
        'graph_url_3': graph_url_3,
        'report_paths': report_paths,
    }
    return render_to_pdf('main/imops_3_pdf.html', context)