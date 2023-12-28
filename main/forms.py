from django import forms
import datetime
from django.forms.widgets import SelectDateWidget
from .models import (
    Laguna, 
    LagoonDetail, 
    Laguna_Stock,
    Supervisor,
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
    RelevantMatters
    )


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    #check = forms.BooleanField(required=False)

class LagunaForm(forms.ModelForm):
    class Meta:
        model = Laguna
        fields = '__all__'  # This will include all fields from the Laguna model in the form

class ChecklistForm(forms.Form):
    fecha = forms.DateField(label='Date of visit', widget=forms.DateInput(attrs={'type': 'date'}))
    supervisor = forms.ModelChoiceField(label='Supervisor', queryset=Supervisor.objects.all())
    lagoons = forms.ModelChoiceField(label='Lagoon', queryset=Laguna.objects.all())

class PersonalDeLaLagunaForm(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = PersonalDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionLimpiezaDeFondoForm(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionLimpiezaDeFondo
        exclude = ['date', 'supervisor', 'lagoon']
        
class OperacionLimpiezaManualForm(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionLimpiezaManual
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionFiltroForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionFiltro
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionSistemaDosificacionForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionSistemaDosificacion
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionSistemaRecirculacionForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionSistemaRecirculacion
        exclude = ['date', 'supervisor', 'lagoon']

class FuncionamientoTelemetriaForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = FuncionamientoTelemetria
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionSkimmersForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionSkimmers
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionUltrasonidoForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = OperacionUltrasonido
        exclude = ['date', 'supervisor', 'lagoon']

class InfraestructuraForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = Infraestructura
        exclude = ['date', 'supervisor', 'lagoon']

class CondicionLinerForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = CondicionLiner
        exclude = ['date', 'supervisor', 'lagoon']

class CondicionVisualLagunaForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = CondicionVisualLaguna
        exclude = ['date', 'supervisor', 'lagoon']

class FuncionamientoAguaRellenoForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = FuncionamientoAguaRelleno
        exclude = ['date', 'supervisor', 'lagoon']

class NivelDeLaLagunaForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = NivelDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']

class MedidasDeMitigacionForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='')
    class Meta:
        model = MedidasDeMitigacion
        exclude = ['date', 'supervisor', 'lagoon']

class LagoonDetailForm(forms.ModelForm):
    class Meta:
        model = LagoonDetail
        fields = '__all__'

#################################################################################
#################################################################################
#################################################################################

class StockForm(forms.ModelForm):
    class Meta:
        model = Laguna_Stock
        fields = [
            'date', 
            'laguna', 
            'stock_or_supply', 
            'cl_ap2hi_tank', 'cl_ap2hi_storage', 
            'cl_fh1lo_tank', 'cl_fh1lo_storage', 
            'cl_flo12_tank', 'cl_flo12_storage', 
            'cl_cotflo_tank', 'cl_cotflo_storage', 
            'cl_mb010_tank', 'cl_mb010_storage'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'stock_or_supply': forms.RadioSelect
        }

class LagunaSelectionForm(forms.Form):
    today = datetime.date.today()
    years = range(2020, today.year + 1)

    date = forms.DateField(widget=SelectDateWidget(years=years, empty_label=("Choose Year", "Choose Month", None)))
    laguna = forms.ModelChoiceField(queryset=Laguna.objects.all(), to_field_name="Codigo", empty_label="Select Laguna")

class RelevantMatterForm(forms.ModelForm):
    class Meta:
        model = RelevantMatters
        fields = ['text', 'date']