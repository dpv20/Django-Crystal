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
    RelevantMatters,
    Feedback,
    )


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    #check = forms.BooleanField(required=False)

class LagunaForm(forms.ModelForm):
    class Meta:
        model = Laguna
        fields = '__all__'  # This will include all fields from the Laguna model in the form


#################################################################################
#################################################################################
#################################################################################

class ChecklistForm(forms.Form):
    fecha = forms.DateField(label='Date of visit / Fecha de visita', widget=forms.DateInput(attrs={'type': 'date'}))
    supervisor = forms.ModelChoiceField(label='Supervisor', queryset=Supervisor.objects.all())
    lagoons = forms.ModelChoiceField(label='Lagoon / Laguna', queryset=Laguna.objects.all())

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

class PersonalDeLaLagunaFormEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    
    class Meta:
        model = PersonalDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': 'Is everything going all right?',
            'cantidad': 'Quantity:',
            'dotacion_incompleta': 'Incomplete personal',
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
            'comentario': 'Comentarios sobre la evaluación',
        }
        help_texts = {
            'en_mantencion': 'Motor fuera de borda (bote)1',
            'filtracion_en_cuerpo': 'Manguera de Limpieza de Fondo1',
            'bomba_en_mantencion': 'Bomba de Limpieza de Fondo1',
            'no_optima': 'Secuencia de Limpieza1',
            'cepillos_gastados_antiguo': 'Carro de aspiración(Antiguo)1',
            'cepillos_gastados_nuevo': 'Carro de aspiración (Nuevo)1',
        }

class OperacionLimpiezaDeFondoFormEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')

    class Meta:
        model = OperacionLimpiezaDeFondo
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': 'Is everything going all right?',
            'en_mantencion': 'Under maintenance',
            'sin_combustible': 'Out of fuel',
            'falla_mecanica': 'Mechanical failure',
            'problemas_en_piolas': 'Problems in the controls',
            'alarma_de_recalentamiento': 'Overheating alarm',
            'otro_motor_fuera_de_borda': 'Other Outboard motor (boat) issue',
            'motor_fuera_de_borda_comentario': 'Outboard motor (boat) comments',
            'filtracion_en_cuerpo': 'Leakage in the body of the hose',
            'filtracion_en_union_muro': 'Leakage at the junction of the wall',
            'filtracion_en_union_carro': 'Leakage at the junction of the suction cart',
            'filtracion_en_union_Y': 'Leakage in Y connector',
            'otro_tipo_de_filtracion': 'Other type of leakage',
            'manguera_comentarios': 'Hose comments',
            'bomba_en_mantencion': 'Pump under maintenance',
            'no_funciona_energia': 'Not working due to power issue',
            'no_funciona_electrico': 'Not working due to electrical or mechanical issue',
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
            'faldon_externo_gastado': 'Worn white external rubber strip',
            'faldon_interno_gastado': 'Worn black internal rubber strip',
            'otro_carro_antiguo': 'Other issue with old cart',
            'carro_antiguo_comentarios': 'Old cart comments',
            'cepillos_gastados_nuevo': 'Worn brushes (new)',
            'gomas_gastadas': 'Worn rubbers strip',
            'valvula_mal_estado_nuevo': 'Valve in poor condition (new)',
            'otro_carro_nuevo': 'Other issue with new cart',
            'carro_nuevo_comentarios': 'New cart comments',
            'comentario': 'Evaluation comments',
        }
        help_texts = {
            'en_mantencion': 'Outboard motor (boat)',
            'filtracion_en_cuerpo': 'Bottom Cleaning Hose',
            'bomba_en_mantencion': 'Bottom Cleaning Pump',
            'no_optima': 'Cleaning Sequence',
            'cepillos_gastados_antiguo': 'Suction Cart (Old)',
            'cepillos_gastados_nuevo': 'Suction Cart (New)',
        }

class OperacionLimpiezaManualForm(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    
    class Meta:
        model = OperacionLimpiezaManual
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': '¿Operando todo bien?',
            'equipamiento_incompleto': 'Incompleto',
            'equipamiento_defectuoso': 'Defectuoso',
            'Equipamiento_comentarios': 'Comentarios sobre el Equipamiento',
            'bomba_en_mantencion': 'En mantención o reparación',
            'no_funciona_energia': 'No funciona por falta de energía',
            'no_funciona_electrico': 'No funciona por problema eléctrico o mecánico',
            'problemas_en_manguera': 'Problemas en la manguera',
            'otro_bomba': 'Otro (Bomba Limpieza Manual)',
            'bomba_comentarios': 'Comentarios sobre la Bomba de Limpieza Manual',
            'no_optima': 'No óptima',
            'otro_secuencia': 'Otro (Secuencia de Limpieza)',
            'secuencia_comentarios': 'Comentarios sobre la Secuencia de Limpieza',
            'suciedad_en_uniones': 'Suciedad en las uniones de liner, arrugas y baches',
            'comentario': 'Comentarios de la Evaluación General',
        }
        
        help_texts = {
            'equipamiento_incompleto': 'Equipamento',
            'bomba_en_mantencion': 'Bomba Limpieza Manual',
            'no_optima': 'Secuencia de Limpieza',
            'suciedad_en_uniones': 'Limpieza de Liner',
        }

class OperacionLimpiezaManualFormEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    
    class Meta:
        model = OperacionLimpiezaManual
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': 'Is everything operating well?',
            'equipamiento_incompleto': 'Equipment Incomplete',
            'equipamiento_defectuoso': 'Equipment Defective',
            'Equipamiento_comentarios': 'Equipment Comments',
            'bomba_en_mantencion': 'Under Maintenance or Repair',
            'no_funciona_energia': 'Not Working Due to Lack of Energy',
            'no_funciona_electrico': 'Not Working Due to Electrical or Mechanical Issue',
            'problemas_en_manguera': 'Problems in the Hose',
            'otro_bomba': 'Other',
            'bomba_comentarios': 'Manual Cleaning Pump Comments',
            'no_optima': 'Not Optimal',
            'otro_secuencia': 'Other',
            'secuencia_comentarios': 'Cleaning Sequence Comments',
            'suciedad_en_uniones': 'Dirt at the Liner Joints, Wrinkles, and Potholes',
            'comentario': 'General Evaluation Comments',
        }
        help_texts = {
            'equipamiento_incompleto': 'Equipment/Gear',
            'bomba_en_mantencion': 'Manual Cleaning Pump',
            'no_optima': 'Cleaning Sequence',
            'suciedad_en_uniones': 'Liner Cleaning',
        }

class OperacionFiltroForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')

    class Meta:
        model = OperacionFiltro
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'turbidez_media': "Turbidez media",
            'sucia': "Sucia",
            'otro_calidad_salida': "Otro (Calidad Agua de Salida)",
            'calidad_salida_comentarios': "Comentarios (Calidad Agua de Salida)",
            'lecho_saturado': "El lecho filtrante está saturado",
            'valvulas_no_funcionan': "Las válvulas no abren y/o cierran bien",
            'filtracion_tuberias': "Filtración de tuberías",
            'otro_filtro': "Otro (Filtro)",
            'filtro_comentarios': "Comentarios (Filtro)",
            'turbidez_baja': "Turbidez baja (Calidad de agua cámara de LF)",
            'turbidez_media_camara': "Turbidez media (Calidad de agua cámara de LF)",
            'turbidez_alta': "Turbidez alta (Calidad de agua cámara de LF)",
            'otro_calidad_camara': "Otro (Calidad de agua cámara de LF)",
            'calidad_camara_comentarios': "Comentarios (Calidad de agua cámara de LF)",
            'sensores_no_funcionan': "Sensores no funcionan",
            'otro_sensores': "Otro (Sensores de nivel cámara LF)",
            'sensores_comentarios': "Comentarios (Sensores de nivel cámara LF)",
            'bomba_en_mantencion': "En mantención (Bomba Filtro)",
            'no_funciona_energia_bomba': "No funciona por falta de energía",
            'no_funciona_electrico_bomba': "No funciona por problema eléctrico o mecánico",
            'problemas_variador': "Problemas variador de frecuencia / Partidor Suave",
            'otro_bomba': "Otro (Bomba Filtro)",
            'bomba_comentarios': "Comentarios (Bomba Filtro)",
            'comentario': "Comentarios (Evaluación general)",
        }
        help_texts = {
            'turbidez_media': "Calidad Agua de Salida(Visual)",
            'lecho_saturado': "Filtro",
            'turbidez_baja': "Calidad de agua cámara de LF",
            'sensores_no_funcionan': "Sensores de nivel cámara LF",
            'bomba_en_mantencion': "Bomba Filtro",

        }

class OperacionFiltroFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')

    class Meta:
        model = OperacionFiltro
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well? ",
            'turbidez_media': "Medium Turbidity",
            'sucia': "Dirty",
            'otro_calidad_salida': "Other (Water Output Quality)",
            'calidad_salida_comentarios': "Comments (Water Output Quality)",

            'lecho_saturado': "Filter media is saturated",
            'valvulas_no_funcionan': "The valves do not open and/or close properly",
            'filtracion_tuberias': "Pipe leak",
            'otro_filtro': "Other (Filter)",
            'filtro_comentarios': "Comments (Filter)",

            'turbidez_baja': "Low Turbidity",
            'turbidez_media_camara': "Medium Turbidity",
            'turbidez_alta': "High Turbidity",
            'otro_calidad_camara': "Other (Water quality in BC chamber)",
            'calidad_camara_comentarios': "Comments (Water quality in BC chamber)",


            'sensores_no_funcionan': "Sensors do not work",
            'otro_sensores': "Other (LF Chamber Level Sensors)",
            'sensores_comentarios': "Comments (LF Chamber Level Sensors)",


            'bomba_en_mantencion': "Under Maintenance",
            'no_funciona_energia_bomba': "Does not work due to lack of energy",
            'no_funciona_electrico_bomba': "Does not work due to electrical or mechanical problem",
            'problemas_variador': "Frequency variator / Soft Start problems",
            'otro_bomba': "Other (Filter Pump)",
            'bomba_comentarios': "Comments (Filter Pump)",
            'comentario': "Comments (General Evaluation)",
        }
        help_texts = {
            'turbidez_media': "Water Output Quality (Visual)",
            'lecho_saturado': "Filter",
            'turbidez_baja': "Water quality in BC chamber",
            'sensores_no_funcionan': "Level sensors in BC Chamber",
            'bomba_en_mantencion': "Filter Pump",
        }

class OperacionSistemaDosificacionForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')

    class Meta:
        model = OperacionSistemaDosificacion
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'nivel_bajo': "Bajo",
            'nivel_critico': "Crítico",
            'nivel_comentarios': "Comentarios (Nivel de inventario de aditivos)",
            'bomba_en_mantencion': "En mantención",
            'bomba_no_funciona_energia': "No funciona por falta de energía",
            'bomba_no_funciona_electrico': "No funciona por problemas eléctrico o mecánico",
            'bomba_no_marca_presion': "No marca presión",
            'otro_bomba': "Otro (Bombas Dosificadoras)",
            'bomba_comentarios': "Comentarios (Bombas Dosificadoras)",
            'filtracion_estanque': "Filtración en estanque",
            'valvula_corte_dañadas': "Válvula de corte dañadas",
            'otro_estanque': "Otro (Estanques de aditivos)",
            'estanque_comentarios': "Comentarios (Estanques de aditivos)",
            'caudal_insuficiente': "Insuficiente caudal bomba dosificadora",
            'valvulas_tapadas': "Válvulas retención tapadas o defectuosas",
            'mangueras_incrustaciones': "Mangueras o tuberías con incrustaciones",
            'venturi_mal_estado': "Venturi en mal estado",
            'otro_venturi': "Otro (Succión de Venturis)",
            'venturi_comentarios': "Comentarios (Succión de Venturis)",
            'bomba_playa_en_mantencion': "En mantención",
            'bomba_playa_no_funciona_energia': "No funciona por falta de energía",
            'bomba_playa_no_funciona_electrico': "No funciona por problemas eléctrico o mecánico",
            'otro_bomba_playa': "Otro (Bomba Dosificadora de playa)",
            'bomba_playa_comentarios': "Comentarios (Bomba Dosificadora de playa)",
            'discordancia_telemetria': "Discordancia entre la dosificación por telemetría y la real",
            'comentario': "Comentarios (Evaluación general)",
        }

class OperacionSistemaDosificacionFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')

    class Meta:
        model = OperacionSistemaDosificacion
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'nivel_bajo': "Low",
            'nivel_critico': "Critical",
            'nivel_comentarios': "Comments (Stock of additives)",
            'bomba_en_mantencion': "Under maintenance",
            'bomba_no_funciona_energia': "Not working due to lack of energy",
            'bomba_no_funciona_electrico': "Not working due to electrical or mechanical issues",
            'bomba_no_marca_presion': "No pressure indication",
            'otro_bomba': "Other (Dosing pumps)",
            'bomba_comentarios': "Comments (Dosing pumps)",
            'filtracion_estanque': "Tank leak",
            'valvula_corte_dañadas': "Damaged shut-off valve",
            'otro_estanque': "Other (Additive Tanks)",
            'estanque_comentarios': "Comments (Additive Tanks)",
            'caudal_insuficiente': "Insufficient flow",
            'valvulas_tapadas': "Clogged or faulty check valves",
            'mangueras_incrustaciones': "Hoses or pipes with inlays",
            'venturi_mal_estado': "Venturi in bad condition",
            'otro_venturi': "Other (Venturis suction)",
            'venturi_comentarios': "Comments (Venturis suction)",
            'bomba_playa_en_mantencion': "Under maintenance",
            'bomba_playa_no_funciona_energia': "Not working due to lack of energy",
            'bomba_playa_no_funciona_electrico': "Not working due to electrical or mechanical issues",
            'otro_bomba_playa': "Other (Pump Dosing of beach)",
            'bomba_playa_comentarios': "Comments (Pump Dosing of beach)",
            'discordancia_telemetria': "Discrepancy between telemetry and actual dosing",
            'comentario': "Comments (General Evaluation)",
        }

class OperacionSistemaRecirculacionForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = OperacionSistemaRecirculacion
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'bomba_en_mantencion': "En mantención",
            'no_funciona_energia': "No funciona por falta de energía",
            'no_funciona_electrico': "No funciona por problemas eléctricos o mecánicos",
            'otro_bomba': "Otro (Bomba de Recirculación)",
            'bomba_comentarios': "Comentarios (Bomba de Recirculación)",
            'inyectores_no_funciona': "No funciona",
            'caudal_bajo': "Caudal bajo",
            'faltan_inyectores': "Faltan inyectores por instalar",
            'otro_inyectores': "Otro (Estado de inyectores)",
            'inyectores_comentarios': "Comentarios (Estado de inyectores)",
            'manifold_no_cierra': "No cierra correctamente",
            'manifold_filtraciones': "Con filtraciones",
            'otro_manifold': "Otro (Manifold)",
            'manifold_comentarios': "Comentarios (Manifold)",
            'camara_filtraciones': "Presenta filtraciones",
            'otro_camara': "Otro (Cámara de aditivos)",
            'camara_comentarios': "Comentarios (Cámara de aditivos)",
            'comentario': "Comentario (Evaluación general)",
        }

class OperacionSistemaRecirculacionFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = OperacionSistemaRecirculacion
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'bomba_en_mantencion': "Under maintenance",
            'no_funciona_energia': "Not working due to lack of energy",
            'no_funciona_electrico': "Not working due to electrical or mechanical issues",
            'otro_bomba': "Other (Recirculation Pump)",
            'bomba_comentarios': "Comments (Recirculation Pump)",
            'inyectores_no_funciona': "Not working",
            'caudal_bajo': "Low flow",
            'faltan_inyectores': "Injectors missing for installation",
            'otro_inyectores': "Other (Injectors status)",
            'inyectores_comentarios': "Comments (Injectors status)",
            'manifold_no_cierra': "Does not close properly",
            'manifold_filtraciones': "With leaks",
            'otro_manifold': "Other (Manifold)",
            'manifold_comentarios': "Comments (Manifold)",
            'camara_filtraciones': "Presents leaks",
            'otro_camara': "Other (Additive Chamber)",
            'camara_comentarios': "Comments (Additive Chamber)",
            'comentario': "Comment (General Evaluation)",
        }

class FuncionamientoTelemetriaForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = FuncionamientoTelemetria
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'conexion_problemas': "Conexión con problemas",
            'otro_comunicacion': "Otro (Comunicación)",
            'sin_conexion': "Sin conexión",
            'velocidad_baja': "Velocidad baja",
            'otro_internet': "Otro (Internet)",
            'circuito_agua': "Circuito eléctrico con agua",
            'sensor_temp_danado': "Dañado",
            'sensor_temp_no_funciona': "No funciona",
            'sensor_temp_fuera_rango': "Fuera de rango",
            'otro_sensor_temp': "Otro (Sensor de temperatura)",
            'sensor_orp_danado': "Dañado",
            'sensor_orp_no_funciona': "No funciona",
            'sensor_orp_fuera_rango': "Fuera de rango",
            'otro_sensor_orp': "Otro (Sensor de ORP)",
            'turbidimetro_no_funciona': "No funciona",
            'turbidimetro_danado': "Dañado",
            'turbidimetro_fuera_rango': "Fuera de rango",
            'otro_turbidimetro': "Otro (Turbidímetro)",
            'bomba_potencia_insuficiente': "No tiene la potencia necesaria",
            'bomba_no_funciona': "No funciona",
            'otro_bomba': "Otro (Bomba de turbidímetro)",
            'pantalla_touch_no_funciona': "Pantalla touch no funciona",
            'monitor_apagado': "Apagado",
            'otro_monitor': "Otro (Monitor Telemetría)",
            'panel_no_energizado': "No energizado",
            'panel_no_funciona': "No funciona",
            'otro_panel': "Otro (El panel de control)",
            'comentario': "Comentario (Evaluación general)",
        }

class FuncionamientoTelemetriaFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = FuncionamientoTelemetria
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'conexion_problemas': "Connection with problems",
            'otro_comunicacion': "Other (Communication)",
            'sin_conexion': "No connection",
            'velocidad_baja': "Low speed",
            'otro_internet': "Other (Internet)",
            'circuito_agua': "Electrical circuit with water",
            'sensor_temp_danado': "Damaged",
            'sensor_temp_no_funciona': "Not working",
            'sensor_temp_fuera_rango': "Out of range",
            'otro_sensor_temp': "Other (Temperature sensor)",
            'sensor_orp_danado': "Damaged",
            'sensor_orp_no_funciona': "Not working",
            'sensor_orp_fuera_rango': "Out of range",
            'otro_sensor_orp': "Other (ORP Sensor)",
            'turbidimetro_no_funciona': "Not working",
            'turbidimetro_danado': "Damaged",
            'turbidimetro_fuera_rango': "Out of range",
            'otro_turbidimetro': "Other (Turbidimeter)",
            'bomba_potencia_insuficiente': "Lacks necessary power",
            'bomba_no_funciona': "Not working",
            'otro_bomba': "Other (Turbidimeter Pump)",
            'pantalla_touch_no_funciona': "Touch screen not working",
            'monitor_apagado': "Off",
            'otro_monitor': "Other (Telemetry Monitor)",
            'panel_no_energizado': "Not energized",
            'panel_no_funciona': "Not working",
            'otro_panel': "Other (Control Panel)",
            'comentario': "Comment (General Evaluation)",
        }

class OperacionSkimmersForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = OperacionSkimmers
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien? Sí",
            'bomba_mantencion': "En mantención",
            'bomba_no_energia': "No funciona por falta de energía",
            'bomba_problemas_electricos': "No funciona por problemas eléctricos o mecánicos",
            'otro_bomba': "Otro (Bomba de Skimmers)",
            'sensores_no_funciona': "No funciona (Sensores de nivel)",
            'otro_sensores': "Otro (Sensores de nivel)",
            'sensores_comentarios': "Comentarios (Sensores de nivel)",
            'agua_limpia': "Limpia (Calidad Agua de Salida)",
            'agua_turbidez_media': "Turbidez media (Calidad Agua de Salida)",
            'agua_sucia': "Sucia (Calidad Agua de Salida)",
            'otro_agua': "Otro (Calidad Agua de Salida)",
            'agua_comentarios': "Comentarios (Calidad Agua de Salida)",
            'filtro_desgaste': "Desgaste (Filtro de anillas)",
            'filtro_carcasa_no_cierra': "Carcasa no cierra bien (Filtro de anillas)",
            'filtro_carcasa_rota': "Carcasa rota (Filtro de anillas)",
            'otro_filtro': "Otro (Filtro de anillas)",
            'filtro_comentarios': "Comentarios (Filtro de anillas)",
            'manguera_fisuras': "Fisuras (Manguera de impulsión)",
            'otro_manguera': "Otro (Manguera de impulsión)",
            'manguera_comentarios': "Comentarios (Manguera de impulsión)",
            'comentario': "Comentarios (Evaluación general)",
        }

class OperacionSkimmersFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = OperacionSkimmers
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'bomba_mantencion': "Under maintenance",
            'bomba_no_energia': "Not working due to lack of energy",
            'bomba_problemas_electricos': "Not working due to electrical or mechanical issues",
            'otro_bomba': "Other (Skimmers Pump)",
            'sensores_no_funciona': "Not working",
            'otro_sensores': "Other (Level Sensors)",
            'sensores_comentarios': "Comments (Level Sensors)",
            'agua_limpia': "Clean",
            'agua_turbidez_media': "Medium turbidity",
            'agua_sucia': "Dirty",
            'otro_agua': "Other (Water Output Quality)",
            'agua_comentarios': "Comments (Water Output Quality)",
            'filtro_desgaste': "Worn out",
            'filtro_carcasa_no_cierra': "Casing does not close well",
            'filtro_carcasa_rota': "Broken casing",
            'otro_filtro': "Other (Ring Filter)",
            'filtro_comentarios': "Comments (Ring Filter)",
            'manguera_fisuras': "Fissures",
            'otro_manguera': "Other (Discharge Hose)",
            'manguera_comentarios': "Comments (Discharge Hose)",
            'comentario': "Comments (General Evaluation)",
        }

class OperacionUltrasonidoForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = OperacionUltrasonido
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'equipo_electronico_defectuoso': "Equipo electrónico defectuoso",
            'agua_no_llega_transductores': "El agua no llega a los transductores",
            'falta_energia': "Falta de energía",
            'nota': "Nota",
            'comentario': "Comentario (General)",
        }

class OperacionUltrasonidoFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = OperacionUltrasonido
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'equipo_electronico_defectuoso': "Electronic equipment is defective",
            'agua_no_llega_transductores': "Water does not reach the transducers",
            'falta_energia': "Lack of energy",
            'nota': "Grade",
            'comentario': "Comment (General)",
        }

class InfraestructuraForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = Infraestructura
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'pintura_desgastada_playa': "Pintura Desgastada",
            'focos_oxido_playa': "Presencia de focos de óxido",
            'sucio_manchas_playa': "Sucio/Manchas",
            'otro_playa': "Otro (Entradas de playa)",
            'comentarios_playa': "Comentarios (Entradas de playa)",
            'pintura_desgastada_muros': "Pintura Desgastada",
            'sucio_manchas_muros': "Sucio/Manchas",
            'otro_muros': "Otro (Muros)",
            'comentarios_muros': "Comentarios (Muros)",
            'sensores_mal_estado': "Sensores de nivel en mal estado",
            'bomba_mal_estado': "Bomba sentina en mal estado o no tienen",
            'comentario': "Comentario (General)",
        }

class InfraestructuraFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = Infraestructura
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'pintura_desgastada_playa': "Worn out Paint",
            'focos_oxido_playa': "Presence of rust",
            'sucio_manchas_playa': "Dirty/Stains",
            'otro_playa': "Other (Beach Entrances)",
            'comentarios_playa': "Comments (Beach Entrances)",
            'pintura_desgastada_muros': "Worn out Paint",
            'sucio_manchas_muros': "Dirty/Stains",
            'otro_muros': "Other (Walls)",
            'comentarios_muros': "Comments (Walls)",
            'sensores_mal_estado': "Level sensors in poor condition",
            'bomba_mal_estado': "Bilge pump in poor condition or missing",
            'comentario': "Comment (General)",
        }

class CondicionLinerForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = CondicionLiner
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'perforaciones_cortes': "Liner con perforaciones y/o cortes",
            'carbonato': "Liner con carbonato",
            'algas': "Liner con algas",
            'nota': "Nota",
            'comentario': "Comentario (General)",
        }

class CondicionLinerFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = CondicionLiner
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'perforaciones_cortes': "Liner with perforations and/or cuts",
            'carbonato': "Liner with carbonate",
            'algas': "Liner with algae",
            'nota': "Grade",
            'comentario': "Comment (General)",
        }

class CondicionVisualLagunaForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = CondicionVisualLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'opacidad_leve': "Opacidad leve - turbidez media",
            'sucia_alta': "Sucia - turbidez alta",
            'otro_turbidez': "Otro (Turbidez)",
            'verdoso': "Verdoso",
            'verde': "Verde",
            'lechoso': "Lechoso",
            'otro_color': "Otro (Color)",
            'liner_sedimento': "Liner con sedimento",
            'nota': "Nota",
            'comentario': "Comentario (General)",
        }

class CondicionVisualLagunaFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = CondicionVisualLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'opacidad_leve': "Slight opacity - medium turbidity",
            'sucia_alta': "Dirty - high turbidity",
            'otro_turbidez': "Other (Turbidity)",
            'verdoso': "Greenish",
            'verde': "Green",
            'lechoso': "Milky",
            'otro_color': "Other (Color)",
            'liner_sedimento': "Liner with sediment",
            'nota': "Grade",
            'comentario': "Comment (General)",
        }

class FuncionamientoAguaRellenoForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label="Nota")
    class Meta:
        model = FuncionamientoAguaRelleno
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'bomba_mantencion': "En mantención",
            'no_funciona_energia': "No funciona por falta de energía",
            'no_funciona_electrico': "No funciona por problema eléctrico o mecánico",
            'otro_bomba': "Otro (Bomba Agua de relleno)",
            'sequia': "Sequía",
            'cuentas_impagas': "Cuentas de agua potable impagas",
            'calidad_no_cumple': "Calidad de agua no cumple estándar de Crystal Lagoons",
            'otro_fuente': "Otro (Fuente de agua)",
            'nota': "Nota",
            'comentario': "Comentario (General)",
        }

class FuncionamientoAguaRellenoFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label="Grade")
    class Meta:
        model = FuncionamientoAguaRelleno
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'bomba_mantencion': "Under maintenance",
            'no_funciona_energia': "Not working due to lack of energy",
            'no_funciona_electrico': "Not working due to electrical or mechanical issue",
            'otro_bomba': "Other (Refilling water pump)",
            'sequia': "Drought",
            'cuentas_impagas': "Unpaid water bills",
            'calidad_no_cumple': "Water quality does not meet Crystal Lagoons standard",
            'otro_fuente': "Other (Water Source)",
            'nota': "Grade",
            'comentario': "Comment (General)",
        }

class NivelDeLaLagunaForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = NivelDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'nivel_bajo': "Nivel bajo",
            'nivel_alto': "Nivel alto",
            'nota': "Nota",
            'comentario': "Comentario (General)",
        }

class NivelDeLaLagunaFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = NivelDeLaLaguna
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'nivel_bajo': "Low level",
            'nivel_alto': "High level",
            'nota': "Grade",
            'comentario': "Comment (General)",
        }

class MedidasDeMitigacionForms(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Nota')
    class Meta:
        model = MedidasDeMitigacion
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "¿Operando todo bien?",
            'medidas_ineficientes': "Medidas Ineficientes",
            'no_tienen': "No tienen",
            'nota': "Nota",
            'comentario': "Comentario (General)",
        }

class MedidasDeMitigacionFormsEN(forms.ModelForm):
    nota = forms.ChoiceField(choices=[('', '------')] + [(i, i) for i in range(1, 5)], required=False, initial='', label='Grade')
    class Meta:
        model = MedidasDeMitigacion
        exclude = ['date', 'supervisor', 'lagoon']
        labels = {
            'todo_bien': "Is everything operating well?",
            'medidas_ineficientes': "Inefficient measures",
            'no_tienen': "Doesn't have any",
            'nota': "Grade",
            'comentario': "Comment (General)",
        }

#################################################################################
#################################################################################
#################################################################################

class LagoonDetailForm(forms.ModelForm):
    class Meta:
        model = LagoonDetail
        fields = '__all__'

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

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['user']  # Exclude the user field from the form
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Describe the issue or suggestion...'}),
        }
        help_texts = {
            'screenshot': 'Windows button + Shift + S allow you to take a screenshot of a particular area, you can paste it on paint and attach it here after.',
        }
