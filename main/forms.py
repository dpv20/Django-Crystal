from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    #check = forms.BooleanField(required=False)


from django import forms
from .models import Laguna, LagoonDetail

class LagunaForm(forms.ModelForm):
    class Meta:
        model = Laguna
        fields = '__all__'  # This will include all fields from the Laguna model in the form


from django import forms
from .models import Supervisor, Laguna, PersonalDeLaLaguna

class ChecklistForm(forms.Form):
    fecha = forms.DateField(label='Date of visit', widget=forms.DateInput(attrs={'type': 'date'}))
    supervisor = forms.ModelChoiceField(label='Supervisor', queryset=Supervisor.objects.all())
    lagoons = forms.ModelChoiceField(label='Lagoon', queryset=Laguna.objects.all())

from django import forms
from .models import PersonalDeLaLaguna, OperacionLimpiezaDeFondo, OperacionLimpiezaManual, OperacionFiltro, OperacionSistemaDosificacion
from .models import OperacionSistemaRecirculacion, FuncionamientoTelemetria, OperacionSkimmers, OperacionUltrasonido, Infraestructura
from .models import CondicionLiner, CondicionVisualLaguna, FuncionamientoAguaRelleno, NivelDeLaLaguna, MedidasDeMitigacion



class PersonalDeLaLagunaForm(forms.ModelForm):
    class Meta:
        model = PersonalDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionLimpiezaDeFondoForm(forms.ModelForm):
    class Meta:
        model = OperacionLimpiezaDeFondo
        exclude = ['date', 'supervisor', 'lagoon']
        
class OperacionLimpiezaManualForm(forms.ModelForm):
    class Meta:
        model = OperacionLimpiezaManual
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionFiltroForms(forms.ModelForm):
    class Meta:
        model = OperacionFiltro
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionSistemaDosificacionForms(forms.ModelForm):
    class Meta:
        model = OperacionSistemaDosificacion
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionSistemaRecirculacionForms(forms.ModelForm):
    class Meta:
        model = OperacionSistemaRecirculacion
        exclude = ['date', 'supervisor', 'lagoon']

class FuncionamientoTelemetriaForms(forms.ModelForm):
    class Meta:
        model = FuncionamientoTelemetria
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionSkimmersForms(forms.ModelForm):
    class Meta:
        model = OperacionSkimmers
        exclude = ['date', 'supervisor', 'lagoon']

class OperacionUltrasonidoForms(forms.ModelForm):
    class Meta:
        model = OperacionUltrasonido
        exclude = ['date', 'supervisor', 'lagoon']

class InfraestructuraForms(forms.ModelForm):
    class Meta:
        model = Infraestructura
        exclude = ['date', 'supervisor', 'lagoon']

class CondicionLinerForms(forms.ModelForm):
    class Meta:
        model = CondicionLiner
        exclude = ['date', 'supervisor', 'lagoon']

class CondicionVisualLagunaForms(forms.ModelForm):
    class Meta:
        model = CondicionVisualLaguna
        exclude = ['date', 'supervisor', 'lagoon']

class FuncionamientoAguaRellenoForms(forms.ModelForm):
    class Meta:
        model = FuncionamientoAguaRelleno
        exclude = ['date', 'supervisor', 'lagoon']

class NivelDeLaLagunaForms(forms.ModelForm):
    class Meta:
        model = NivelDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']

class MedidasDeMitigacionForms(forms.ModelForm):
    class Meta:
        model = MedidasDeMitigacion
        exclude = ['date', 'supervisor', 'lagoon']


class LagoonDetailForm(forms.ModelForm):
    class Meta:
        model = LagoonDetail
        fields = '__all__'
