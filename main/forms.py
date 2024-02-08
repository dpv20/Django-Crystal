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
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = PersonalDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': '¿Operando todo bien?',
            'cantidad': 'Cantidad',
            'dotacion_incompleta': 'Dotación Incompleta',
            'comentario': 'Comentario',
        }

class PersonalDeLaLagunaForm_EN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    
    class Meta:
        model = PersonalDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': 'Everything operating well?',
            'cantidad': 'Quantity',
            'dotacion_incompleta': 'Incomplete provision',
            'comentario': 'Comment',
        }
    
class OperacionLimpiezaDeFondoForm(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')

    class Meta:
        model = OperacionLimpiezaDeFondo
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': '¿Operando todo bien?',
            'en_mantencion': 'En mantención',
            'sin_combustible': 'Sin combustible',
            'falla_mecanica': 'Falla mecánica',
            'problemas_en_piolas': 'Problemas en piolas',
            'alarma_de_recalentamiento': 'Alarma de recalientamiento',
            'otro_motor_fuera_de_borda': 'Otro problema con motor fuera de borda',
            'motor_fuera_de_borda_comentario': 'Comentario sobre motor fuera de borda',
            'filtracion_en_cuerpo': 'Filtración en cuerpo',
            'filtracion_en_union_muro': 'Filtración en unión con muro',
            'filtracion_en_union_carro': 'Filtración en unión con carro',
            'filtracion_en_union_Y': 'Filtración en unión en Y',
            'otro_tipo_de_filtracion': 'Otro tipo de filtración',
            'manguera_comentarios': 'Comentarios sobre manguera',
            'bomba_en_mantencion': 'Bomba en mantención',
            'no_funciona_energia': 'No funciona por problema de energía',
            'no_funciona_electrico': 'No funciona por problema eléctrico',
            'otro_bomba': 'Otro problema con la bomba',
            'bomba_comentarios': 'Comentarios sobre la bomba',
            'no_optima': 'Secuencia no óptima',
            'velocidad_excesiva': 'Velocidad excesiva',
            'otro_secuencia': 'Otro problema con la secuencia',
            'secuencia_comentarios': 'Comentarios sobre la secuencia',
            'cepillos_gastados_antiguo': 'Cepillos gastados (antiguo)',
            'valvula_mal_estado_antiguo': 'Válvula en mal estado (antiguo)',
            'plancha_acero_rota': 'Plancha de acero rota',
            'ruedas_mal_estado': 'Ruedas en mal estado',
            'faldon_externo_gastado': 'Faldón externo gastado',
            'faldon_interno_gastado': 'Faldón interno gastado',
            'otro_carro_antiguo': 'Otro problema con el carro antiguo',
            'carro_antiguo_comentarios': 'Comentarios sobre el carro antiguo',
            'cepillos_gastados_nuevo': 'Cepillos gastados (nuevo)',
            'gomas_gastadas': 'Gomas gastadas',
            'valvula_mal_estado_nuevo': 'Válvula en mal estado (nuevo)',
            'otro_carro_nuevo': 'Otro problema con el carro nuevo',
            'carro_nuevo_comentarios': 'Comentarios sobre el carro nuevo',
            'evaluacion_comentarios': 'Comentarios sobre la evaluación',
        }

class OperacionLimpiezaDeFondoFormEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')

    class Meta:
        model = OperacionLimpiezaDeFondo
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': 'Everything operating well?',
            'en_mantencion': 'Under maintenance',
            'sin_combustible': 'Out of fuel',
            'falla_mecanica': 'Mechanical failure',
            'problemas_en_piolas': 'Problems with ropes',
            'alarma_de_recalentamiento': 'Overheating alarm',
            'otro_motor_fuera_de_borda': 'Other outboard motor issue',
            'motor_fuera_de_borda_comentario': 'Outboard motor comments',
            'filtracion_en_cuerpo': 'Leakage in body',
            'filtracion_en_union_muro': 'Leakage at wall joint',
            'filtracion_en_union_carro': 'Leakage at cart joint',
            'filtracion_en_union_Y': 'Leakage at Y joint',
            'otro_tipo_de_filtracion': 'Other type of leakage',
            'manguera_comentarios': 'Hose comments',
            'bomba_en_mantencion': 'Pump under maintenance',
            'no_funciona_energia': 'Not working due to power issue',
            'no_funciona_electrico': 'Not working due to electrical issue',
            'otro_bomba': 'Other pump issue',
            'bomba_comentarios': 'Pump comments',
            'no_optima': 'Not optimal',
            'velocidad_excesiva': 'Excessive speed',
            'otro_secuencia': 'Other sequence issue',
            'secuencia_comentarios': 'Sequence comments',
            'cepillos_gastados_antiguo': 'Worn brushes (old)',
            'valvula_mal_estado_antiguo': 'Valve in poor condition (old)',
            'plancha_acero_rota': 'Broken steel plate',
            'ruedas_mal_estado': 'Wheels in poor condition',
            'faldon_externo_gastado': 'Worn external skirt',
            'faldon_interno_gastado': 'Worn internal skirt',
            'otro_carro_antiguo': 'Other issue with old cart',
            'carro_antiguo_comentarios': 'Old cart comments',
            'cepillos_gastados_nuevo': 'Worn brushes (new)',
            'gomas_gastadas': 'Worn rubbers',
            'valvula_mal_estado_nuevo': 'Valve in poor condition (new)',
            'otro_carro_nuevo': 'Other issue with new cart',
            'carro_nuevo_comentarios': 'New cart comments',
            'evaluacion_comentarios': 'Evaluation comments',
        }











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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)