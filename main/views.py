from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, Laguna, LagoonDetail, LagunaImage
from .forms import CreateNewList, LagoonDetailForm  
import datetime 
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Count, Q
# Create your views here.


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

from django.http import HttpResponse
from .models import Laguna
from .forms import LagunaForm  # We'll create this form next

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






# views.py
from .forms import ChecklistForm
from .models import PersonalDeLaLaguna  # Import the model

def initial_form_view(request):
    request.session['personal_form_submitted'] = False
    form = ChecklistForm()
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        if form.is_valid():
            request.session['fecha'] = str(form.cleaned_data['fecha'])
            request.session['supervisor'] = str(form.cleaned_data['supervisor'])
            request.session['lagoons'] = str(form.cleaned_data['lagoons'])

            return redirect('results')  # 'results' should be the name of the view where you want to redirect

    personal_entries = PersonalDeLaLaguna.objects.all()  # Query the database
    return render(request, "main/initial_form.html", {"form": form, "personal_entries": personal_entries})



from .forms import (
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
    MedidasDeMitigacionForms
)



'''
def results_view(request):
    date = request.session.get('fecha')
    supervisor = request.session.get('supervisor')
    lagoon_name = request.session.get('lagoons')
    try:
        lagoon = Laguna.objects.get(Nombre=lagoon_name)
    except Laguna.DoesNotExist:
        lagoon = None
    
    personal_form = PersonalDeLaLagunaForm()
    limpieza_form = OperacionLimpiezaDeFondoForm()
    limpiezamanual_form = OperacionLimpiezaManualForm()

    if request.method == 'POST':
        if 'personal_submit' in request.POST:
            personal_form = PersonalDeLaLagunaForm(request.POST)
            if personal_form.is_valid():
                # Handle PersonalDeLaLagunaForm submission
                personal_form.instance.date = date
                personal_form.instance.supervisor = supervisor
                personal_form.instance.lagoon = lagoon
                personal_form.save()
                # Handle successful PersonalDeLaLagunaForm submission here.
        elif 'limpieza_submit' in request.POST:
            limpieza_form = OperacionLimpiezaDeFondoForm(request.POST)
            if limpieza_form.is_valid():
                limpieza_form.instance.date = date
                limpieza_form.instance.supervisor = supervisor
                limpieza_form.instance.lagoon = lagoon
                limpieza_form.save()
        elif 'limpiezamanual_submit' in request.POST:
            limpiezamanual_form = OperacionLimpiezaManualForm(request.POST)
            if limpiezamanual_form.is_valid():
                limpiezamanual_form.instance.date = date
                limpiezamanual_form.instance.supervisor = supervisor
                limpiezamanual_form.instance.lagoon = lagoon
                limpiezamanual_form.save()


    else:
        personal_form = PersonalDeLaLagunaForm()
        limpieza_form = OperacionLimpiezaDeFondoForm()
        limpiezamanual_form = OperacionLimpiezaManualForm()
    return render(request, 'main/results.html', {
        'personal_form': personal_form,
        'limpieza_form': limpieza_form,
        'limpiezamanual_form': limpiezamanual_form,
        'lagoon_name': lagoon_name,
    })
'''



def results_view(request):
    date = request.session.get('fecha')
    supervisor = request.session.get('supervisor')
    lagoon_name = request.session.get('lagoons')
    try:
        lagoon = Laguna.objects.get(Nombre=lagoon_name)
    except Laguna.DoesNotExist:
        lagoon = None

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
        if 'personal_submit' in request.POST:
            personal_form = PersonalDeLaLagunaForm(request.POST)
            if personal_form.is_valid():
                personal_form.instance.date = date
                personal_form.instance.supervisor = supervisor
                personal_form.instance.lagoon = lagoon
                personal_form.save()
                request.session['personal_form_submitted'] = True
        elif 'limpieza_submit' in request.POST:
            limpieza_form = OperacionLimpiezaDeFondoForm(request.POST)
            if limpieza_form.is_valid():
                limpieza_form.instance.date = date
                limpieza_form.instance.supervisor = supervisor
                limpieza_form.instance.lagoon = lagoon
                limpieza_form.save()

        elif 'limpiezamanual_submit' in request.POST:
            limpiezamanual_form = OperacionLimpiezaManualForm(request.POST)
            if limpiezamanual_form.is_valid():
                limpiezamanual_form.instance.date = date
                limpiezamanual_form.instance.supervisor = supervisor
                limpiezamanual_form.instance.lagoon = lagoon
                limpiezamanual_form.save()
        elif 'operacionfiltro_submit' in request.POST:
            operacionfiltro_form = OperacionFiltroForms(request.POST)
            if operacionfiltro_form.is_valid():
                operacionfiltro_form.instance.date = date
                operacionfiltro_form.instance.supervisor = supervisor
                operacionfiltro_form.instance.lagoon = lagoon
                operacionfiltro_form.save()
        elif 'operacionsistemadosificacion_submit' in request.POST:
            operacionsistemadosificacion_form = OperacionSistemaDosificacionForms(request.POST)
            if operacionsistemadosificacion_form.is_valid():
                operacionsistemadosificacion_form.instance.date = date
                operacionsistemadosificacion_form.instance.supervisor = supervisor
                operacionsistemadosificacion_form.instance.lagoon = lagoon
                operacionsistemadosificacion_form.save()
        elif 'operacionsistemarecirculacion_submit' in request.POST:
            operacionsistemarecirculacion_form = OperacionSistemaRecirculacionForms(request.POST)
            if operacionsistemarecirculacion_form.is_valid():
                operacionsistemarecirculacion_form.instance.date = date
                operacionsistemarecirculacion_form.instance.supervisor = supervisor
                operacionsistemarecirculacion_form.instance.lagoon = lagoon
                operacionsistemarecirculacion_form.save()

        elif 'funcionamientotelemetria_submit' in request.POST:
            funcionamientotelemetria_form = FuncionamientoTelemetriaForms(request.POST)
            if funcionamientotelemetria_form.is_valid():
                funcionamientotelemetria_form.instance.date = date
                funcionamientotelemetria_form.instance.supervisor = supervisor
                funcionamientotelemetria_form.instance.lagoon = lagoon
                funcionamientotelemetria_form.save()

        elif 'operacionskimmers_submit' in request.POST:
            operacionskimmers_form = OperacionSkimmersForms(request.POST)
            if operacionskimmers_form.is_valid():
                operacionskimmers_form.instance.date = date
                operacionskimmers_form.instance.supervisor = supervisor
                operacionskimmers_form.instance.lagoon = lagoon
                operacionskimmers_form.save()

        elif 'operacionultrasonido_submit' in request.POST:
            operacionultrasonido_form = OperacionUltrasonidoForms(request.POST)
            if operacionultrasonido_form.is_valid():
                operacionultrasonido_form.instance.date = date
                operacionultrasonido_form.instance.supervisor = supervisor
                operacionultrasonido_form.instance.lagoon = lagoon
                operacionultrasonido_form.save()

        elif 'infraestructura_submit' in request.POST:
            infraestructura_form = InfraestructuraForms(request.POST)
            if infraestructura_form.is_valid():
                infraestructura_form.instance.date = date
                infraestructura_form.instance.supervisor = supervisor
                infraestructura_form.instance.lagoon = lagoon
                infraestructura_form.save()
        elif 'condicionliner_submit' in request.POST:
            condicionliner_form = CondicionLinerForms(request.POST)
            if condicionliner_form.is_valid():
                condicionliner_form.instance.date = date
                condicionliner_form.instance.supervisor = supervisor
                condicionliner_form.instance.lagoon = lagoon
                condicionliner_form.save()

        elif 'condicionvisuallaguna_submit' in request.POST:
            condicionvisuallaguna_form = CondicionVisualLagunaForms(request.POST)
            if condicionvisuallaguna_form.is_valid():
                condicionvisuallaguna_form.instance.date = date
                condicionvisuallaguna_form.instance.supervisor = supervisor
                condicionvisuallaguna_form.instance.lagoon = lagoon
                condicionvisuallaguna_form.save()

        elif 'funcionamientoaguarelleno_submit' in request.POST:
            funcionamientoaguarelleno_form = FuncionamientoAguaRellenoForms(request.POST)
            if funcionamientoaguarelleno_form.is_valid():
                funcionamientoaguarelleno_form.instance.date = date
                funcionamientoaguarelleno_form.instance.supervisor = supervisor
                funcionamientoaguarelleno_form.instance.lagoon = lagoon
                funcionamientoaguarelleno_form.save()

        elif 'niveldelalaguna_submit' in request.POST:
            niveldelalaguna_form = NivelDeLaLagunaForms(request.POST)
            if niveldelalaguna_form.is_valid():
                niveldelalaguna_form.instance.date = date
                niveldelalaguna_form.instance.supervisor = supervisor
                niveldelalaguna_form.instance.lagoon = lagoon
                niveldelalaguna_form.save()

        elif 'medidasdemitigacion_submit' in request.POST:
            medidasdemitigacion_form = MedidasDeMitigacionForms(request.POST)
            if medidasdemitigacion_form.is_valid():
                medidasdemitigacion_form.instance.date = date
                medidasdemitigacion_form.instance.supervisor = supervisor
                medidasdemitigacion_form.instance.lagoon = lagoon
                medidasdemitigacion_form.save()



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
        'lagoon_name': lagoon_name,
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



from datetime import timedelta

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
