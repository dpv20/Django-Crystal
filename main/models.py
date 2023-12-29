from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import os
from django.utils import timezone


# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
    
class Laguna(models.Model):
    idLagunas = models.CharField(max_length=10, primary_key=True)
    Nombre = models.CharField(max_length=255, blank=True, null=True)
    Codigo = models.CharField(max_length=255, blank=True, null=True)
    Identificador = models.IntegerField(blank=True, null=True)  # Changed to IntegerField
    Estado = models.BooleanField(blank=True, null=True)
    Rend = models.BooleanField(blank=True, null=True)
    Nombre_Proyecto = models.CharField(max_length=255, blank=True, null=True)
    idplatanus = models.IntegerField(blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)  # Changed to IntegerField
    idioma = models.CharField(max_length=255, blank=True, null=True)
    mailcontacto = models.EmailField(blank=True, null=True)
    subjectr = models.CharField(max_length=255, blank=True, null=True)
    mailcontacto2 = models.EmailField(blank=True, null=True)
    horariocorte = models.TimeField(blank=True, null=True)
    Water_analysis = models.BooleanField(blank=True, null=True)
    Region = models.IntegerField(blank=True, null=True)
    filtroreporte = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.Nombre

def image_upload_to(upload_date):
    def wrapper(instance, filename):
        extension = os.path.splitext(filename)[1]
        formatted_date = upload_date.strftime('%Y_%m_%d')
        count = LagunaImage.objects.filter(
            laguna=instance.laguna, 
            date=upload_date
        ).count()

        new_filename = f"{formatted_date}_{count + 1}{extension}"
        return f"laguna_images/{instance.laguna.idLagunas}/{new_filename}"
    return wrapper

class LagunaImage(models.Model):
    laguna = models.ForeignKey(Laguna, on_delete=models.CASCADE, related_name="images")
    photo = models.ImageField(upload_to='upload_to_placeholder')
    date = models.DateField()
    selected = models.BooleanField(default=False)
    _upload_date = None

    def set_upload_date(self, date):
        self._upload_date = date
    def __str__(self):
        return f"Image for {self.laguna.Nombre} on {self.date}"
    def save(self, *args, **kwargs):
        if self._upload_date is not None:
            self.photo.field.upload_to = image_upload_to(self._upload_date)
        super().save(*args, **kwargs)

######################

class BaseChecklist(models.Model):
    date = models.DateField()
    supervisor = models.CharField(max_length=200)
    lagoon = models.ForeignKey(Laguna, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True

class PersonalDeLaLaguna(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien?")
    cantidad = models.CharField(max_length=200, blank=True, null=True)
    dotacion_incompleta = models.BooleanField(default=False)
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.cantidad = ""
            self.dotacion_incompleta = False
            self.nota = 5
            # self.comentario remains unchanged
        super().save(*args, **kwargs)

class OperacionLimpiezaDeFondo(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien?")
    
    # Motor fuera de borda (bote)
    en_mantencion = models.BooleanField(default=False, verbose_name="En mantención", help_text="Motor fuera de borda (bote)")
    sin_combustible = models.BooleanField(default=False)
    falla_mecanica = models.BooleanField(default=False)
    problemas_en_piolas = models.BooleanField(default=False)
    alarma_de_recalentamiento = models.BooleanField(default=False)
    otro_motor_fuera_de_borda = models.CharField(max_length=200, blank=True)
    motor_fuera_de_borda_comentario = models.CharField(max_length=200, blank=True)
    
    # Manguera de Limpieza de Fondo
    filtracion_en_cuerpo = models.BooleanField(default=False, help_text="Manguera de Limpieza de Fondo")
    filtracion_en_union_muro = models.BooleanField(default=False)
    filtracion_en_union_carro = models.BooleanField(default=False)
    filtracion_en_union_Y = models.BooleanField(default=False)
    otro_tipo_de_filtracion = models.CharField(max_length=200, blank=True)
    manguera_comentarios = models.CharField(max_length=200, blank=True)

    # Bomba de Limpieza de Fondo
    bomba_en_mantencion = models.BooleanField(default=False, help_text="Bomba de Limpieza de Fondo")
    no_funciona_energia = models.BooleanField(default=False)
    no_funciona_electrico = models.BooleanField(default=False)
    otro_bomba = models.CharField(max_length=200, blank=True)
    bomba_comentarios = models.CharField(max_length=200, blank=True)

    # Secuencia de Limpieza
    no_optima = models.BooleanField(default=False, help_text="Secuencia de Limpieza")
    velocidad_excesiva = models.BooleanField(default=False)
    otro_secuencia = models.CharField(max_length=200, blank=True)
    secuencia_comentarios = models.CharField(max_length=200, blank=True)

    # Carro de aspiración(Antiguo)
    cepillos_gastados_antiguo = models.BooleanField(default=False, help_text="Carro de aspiración(Antiguo)")
    valvula_mal_estado_antiguo = models.BooleanField(default=False)
    plancha_acero_rota = models.BooleanField(default=False)
    ruedas_mal_estado = models.BooleanField(default=False)
    faldon_externo_gastado = models.BooleanField(default=False)
    faldon_interno_gastado = models.BooleanField(default=False)
    otro_carro_antiguo = models.CharField(max_length=200, blank=True)
    carro_antiguo_comentarios = models.CharField(max_length=200, blank=True)

    # Carro de aspiración (Nuevo)
    cepillos_gastados_nuevo = models.BooleanField(default=False, help_text="Carro de aspiración (Nuevo)")
    gomas_gastadas = models.BooleanField(default=False)
    valvula_mal_estado_nuevo = models.BooleanField(default=False)
    otro_carro_nuevo = models.CharField(max_length=200, blank=True)
    carro_nuevo_comentarios = models.CharField(max_length=200, blank=True)

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentarios = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)
            
            # Clear other specific fields
            self.otro_motor_fuera_de_borda = ""
            self.motor_fuera_de_borda_comentario = ""
            self.otro_tipo_de_filtracion = ""
            self.manguera_comentarios = ""
            self.otro_bomba = ""
            self.bomba_comentarios = ""
            self.otro_secuencia = ""
            self.secuencia_comentarios = ""
            self.otro_carro_antiguo = ""
            self.carro_antiguo_comentarios = ""
            self.otro_carro_nuevo = ""
            self.carro_nuevo_comentarios = ""
            # self.evaluacion_comentarios remains unchanged

        super().save(*args, **kwargs)

class OperacionLimpiezaManual(BaseChecklist):
    # 1) ¿Operando todo bien?
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien?")

    # 2) Equipamiento
    equipamiento_incompleto = models.BooleanField(default=False, verbose_name="Incompleto",help_text="Equipamiento")
    equipamiento_defectuoso = models.BooleanField(default=False, verbose_name="Defectuoso")
    Equipamiento_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Equipamiento Comentarios")
    # 3) Bomba Limpieza Manual
    bomba_en_mantencion = models.BooleanField(default=False, verbose_name="En mantención o reparación",help_text="Bomba Limpieza Manual")
    no_funciona_energia = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    no_funciona_electrico = models.BooleanField(default=False, verbose_name="No funciona por problema eléctrico o mecánico")
    problemas_en_manguera = models.BooleanField(default=False, verbose_name="Problemas en la manguera")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    bomba_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Bomba Limpieza Manual Comentarios")

    # 4) Secuencia de Limpieza
    no_optima = models.BooleanField(default=False, verbose_name="No óptima",help_text="Secuencia de Limpieza")
    otro_secuencia = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    secuencia_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Secuencia de Limpieza Comentarios")

    # 5) Limpieza de Liner
    suciedad_en_uniones = models.BooleanField(default=False, verbose_name="Suciedad en las uniones de liner, arrugas y baches",help_text="Limpieza de Liner")

    # 6) Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentarios = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)
            
            # Clear other specific fields
            self.otro_bomba = ""
            self.bomba_comentarios = ""
            self.otro_secuencia = ""
            self.secuencia_comentarios = ""
            # self.evaluacion_comentarios remains unchanged

        super().save(*args, **kwargs)

class OperacionFiltro(BaseChecklist):
    # ¿Operando todo bien?
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Calidad Agua de Salida(Visual)
    turbidez_media = models.BooleanField(default=False, verbose_name="Turbidez media")
    sucia = models.BooleanField(default=False, verbose_name="Sucia")
    otro_calidad_salida = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    calidad_salida_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Filtro
    lecho_saturado = models.BooleanField(default=False, verbose_name="El lecho filtrante está saturado")
    valvulas_no_funcionan = models.BooleanField(default=False, verbose_name="Las válvulas no abren y/o cierran bien")
    filtracion_tuberias = models.BooleanField(default=False, verbose_name="Filtración de tuberías")
    otro_filtro = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    filtro_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Calidad de agua cámara de LF
    turbidez_baja = models.BooleanField(default=False, verbose_name="Turbidez baja")
    turbidez_media_camara = models.BooleanField(default=False, verbose_name="Turbidez media")
    turbidez_alta = models.BooleanField(default=False, verbose_name="Turbidez alta")
    otro_calidad_camara = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    calidad_camara_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Sensores de nivel cámara LF
    sensores_no_funcionan = models.BooleanField(default=False, verbose_name="Sensores no funcionan")
    otro_sensores = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    sensores_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Bomba Filtro
    bomba_en_mantencion = models.BooleanField(default=False, verbose_name="En mantención")
    no_funciona_energia_bomba = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    no_funciona_electrico_bomba = models.BooleanField(default=False, verbose_name="No funciona por problema eléctrico o mecánico")
    problemas_variador = models.BooleanField(default=False, verbose_name="Problemas variador de frecuencia /Partidor Suave")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    bomba_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentarios = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)
            
            # Clear other specific fields
            self.otro_calidad_salida = ""
            self.calidad_salida_comentarios = ""
            self.otro_filtro = ""
            self.filtro_comentarios = ""
            self.otro_calidad_camara = ""
            self.calidad_camara_comentarios = ""
            self.otro_sensores = ""
            self.sensores_comentarios = ""
            self.otro_bomba = ""
            self.bomba_comentarios = ""
            # self.evaluacion_comentarios remains unchanged

        super().save(*args, **kwargs)

class OperacionSistemaDosificacion(BaseChecklist):
    # ¿Operando todo bien?
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Nivel de inventario de aditivos
    nivel_bajo = models.BooleanField(default=False, verbose_name="Bajo")
    nivel_critico = models.BooleanField(default=False, verbose_name="Crítico")
    nivel_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Bombas Dosificadoras
    bomba_en_mantencion = models.BooleanField(default=False, verbose_name="En mantención")
    bomba_no_funciona_energia = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    bomba_no_funciona_electrico = models.BooleanField(default=False, verbose_name="No funciona por problemas eléctrico o mecánico")
    bomba_no_marca_presion = models.BooleanField(default=False, verbose_name="No marca presión")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    bomba_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Estanques de aditivos
    filtracion_estanque = models.BooleanField(default=False, verbose_name="Filtración en estanque")
    valvula_corte_dañadas = models.BooleanField(default=False, verbose_name="Vávula de corte dañadas")
    otro_estanque = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    estanque_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Succión de Venturis
    caudal_insuficiente = models.BooleanField(default=False, verbose_name="Insuficiente caudal bomba dosificadora")
    valvulas_tapadas = models.BooleanField(default=False, verbose_name="Válvulas retención tapadas o defectuosas")
    mangueras_incrustaciones = models.BooleanField(default=False, verbose_name="Mangueras o tuberías con incrustaciones")
    venturi_mal_estado = models.BooleanField(default=False, verbose_name="Venturi en mal estado")
    otro_venturi = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    venturi_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Bomba Dosificadora de playa
    bomba_playa_en_mantencion = models.BooleanField(default=False, verbose_name="En mantención")
    bomba_playa_no_funciona_energia = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    bomba_playa_no_funciona_electrico = models.BooleanField(default=False, verbose_name="No funciona por problemas eléctrico o mecánico")
    otro_bomba_playa = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    bomba_playa_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Dosificación telemetría
    discordancia_telemetria = models.BooleanField(default=False, verbose_name="Discordancia entre la dosificación por telemetría y la real")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentarios = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5 
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)
            
            # Clear other specific fields
            self.otro_bomba = ""
            self.bomba_comentarios = ""
            self.otro_estanque = ""
            self.estanque_comentarios = ""
            self.otro_venturi = ""
            self.venturi_comentarios = ""
            self.otro_bomba_playa = ""
            self.bomba_playa_comentarios = ""
            # self.evaluacion_comentarios remains unchanged

        super().save(*args, **kwargs)

class OperacionSistemaRecirculacion(BaseChecklist):
    # ¿Operando todo bien?
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Bomba de Recirculación
    bomba_en_mantencion = models.BooleanField(default=False, verbose_name="En mantención")
    no_funciona_energia = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    no_funciona_electrico = models.BooleanField(default=False, verbose_name="No funciona por problemas eléctricos o mecánicos")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    bomba_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Estado de inyectores
    inyectores_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    caudal_bajo = models.BooleanField(default=False, verbose_name="Caudal bajo")
    faltan_inyectores = models.BooleanField(default=False, verbose_name="Faltan inyectores por instalar")
    otro_inyectores = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    inyectores_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Manifold
    manifold_no_cierra = models.BooleanField(default=False, verbose_name="No cierra correctamente")
    manifold_filtraciones = models.BooleanField(default=False, verbose_name="Con filtraciones")
    otro_manifold = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    manifold_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Cámara de aditivos
    camara_filtraciones = models.BooleanField(default=False, verbose_name="Presenta filtraciones")
    otro_camara = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    camara_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentario = models.TextField(blank=True, verbose_name="Comentario")

    def save(self, *args, **kwargs):
        # If everything is fine, reset other fields to their defaults
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

            # Clear other specific fields
            self.otro_bomba = ""
            self.bomba_comentarios = ""
            self.otro_inyectores = ""
            self.inyectores_comentarios = ""
            self.otro_manifold = ""
            self.manifold_comentarios = ""
            self.otro_camara = ""
            self.camara_comentarios = ""
            # self.evaluacion_comentario remains unchanged

        super().save(*args, **kwargs)

class FuncionamientoTelemetria(BaseChecklist):
    # ¿Operando todo bien?
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Comunicación
    conexion_problemas = models.BooleanField(default=False, verbose_name="Conexión con problemas")
    otro_comunicacion = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Internet
    sin_conexion = models.BooleanField(default=False, verbose_name="Sin conexión")
    velocidad_baja = models.BooleanField(default=False, verbose_name="Velocidad baja")
    otro_internet = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Sensor de temperatura
    circuito_agua = models.BooleanField(default=False, verbose_name="Circuito eléctrico con agua")
    sensor_temp_danado = models.BooleanField(default=False, verbose_name="Dañado")
    sensor_temp_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    sensor_temp_fuera_rango = models.BooleanField(default=False, verbose_name="Fuera de rango")
    otro_sensor_temp = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Sensor de ORP
    sensor_orp_danado = models.BooleanField(default=False, verbose_name="Dañado")
    sensor_orp_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    sensor_orp_fuera_rango = models.BooleanField(default=False, verbose_name="Fuera de rango")
    otro_sensor_orp = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Turbidímetro
    turbidimetro_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    turbidimetro_danado = models.BooleanField(default=False, verbose_name="Dañado")
    turbidimetro_fuera_rango = models.BooleanField(default=False, verbose_name="Fuera de rango")
    otro_turbidimetro = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Bomba de turbidímetro
    bomba_potencia_insuficiente = models.BooleanField(default=False, verbose_name="No tiene la potencia necesaria")
    bomba_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Monitor Telemetría
    pantalla_touch_no_funciona = models.BooleanField(default=False, verbose_name="Pantalla touch no funciona")
    monitor_apagado = models.BooleanField(default=False, verbose_name="Apagado")
    otro_monitor = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # El panel de control
    panel_no_energizado = models.BooleanField(default=False, verbose_name="No energizado")
    panel_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    otro_panel = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentario = models.TextField(blank=True, verbose_name="Comentario")

    def save(self, *args, **kwargs):
        # If everything is fine, reset other fields to their defaults
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

            # Clear other specific fields
            self.otro_comunicacion = ""
            self.otro_internet = ""
            self.otro_sensor_temp = ""
            self.otro_sensor_orp = ""
            self.otro_turbidimetro = ""
            self.otro_bomba = ""
            self.otro_monitor = ""
            self.otro_panel = ""


        super().save(*args, **kwargs)

class OperacionSkimmers(BaseChecklist):
    # ¿Operando todo bien?
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Bomba Skimmers
    bomba_mantencion = models.BooleanField(default=False, verbose_name="En mantención")
    bomba_no_energia = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    bomba_problemas_electricos = models.BooleanField(default=False, verbose_name="No funciona por problemas eléctricos o mecánicos")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Sensores de nivel
    sensores_no_funciona = models.BooleanField(default=False, verbose_name="No funciona")
    otro_sensores = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    sensores_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Calidad Agua de Salida (Visual)
    agua_limpia = models.BooleanField(default=False, verbose_name="Limpia")
    agua_turbidez_media = models.BooleanField(default=False, verbose_name="Turbidez media")
    agua_sucia = models.BooleanField(default=False, verbose_name="Sucia")
    otro_agua = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    agua_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Filtro de anillas
    filtro_desgaste = models.BooleanField(default=False, verbose_name="Desgaste")
    filtro_carcasa_no_cierra = models.BooleanField(default=False, verbose_name="Carcasa no cierra bien")
    filtro_carcasa_rota = models.BooleanField(default=False, verbose_name="Carcasa rota")
    otro_filtro = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    filtro_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Manguera de impulsión
    manguera_fisuras = models.BooleanField(default=False, verbose_name="Fisuras")
    otro_manguera = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    manguera_comentarios = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    evaluacion_comentario = models.TextField(blank=True, verbose_name="Comentarios")

    def save(self, *args, **kwargs):
        # If everything is fine, reset other fields to their defaults
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

            # Clear other specific fields
            self.otro_bomba = ""
            self.otro_sensores = ""
            self.sensores_comentarios = ""
            self.otro_agua = ""
            self.agua_comentarios = ""
            self.otro_filtro = ""
            self.filtro_comentarios = ""
            self.otro_manguera = ""
            self.manguera_comentarios = ""
            # self.evaluacion_comentario remains unchanged

        super().save(*args, **kwargs)

class OperacionUltrasonido(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Ultrasonidos
    equipo_electronico_defectuoso = models.BooleanField(default=False, verbose_name="Equipo electrónico defectuoso")
    agua_no_llega_transductores = models.BooleanField(default=False, verbose_name="El agua no llega a los transductores")
    falta_energia = models.BooleanField(default=False, verbose_name="Falta de energía")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class Infraestructura(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Entradas de playa
    pintura_desgastada_playa = models.BooleanField(default=False, verbose_name="Pintura Desgastada")
    focos_oxido_playa = models.BooleanField(default=False, verbose_name="Presencia de focos de óxido")
    sucio_manchas_playa = models.BooleanField(default=False, verbose_name="Sucio/Manchas")
    otro_playa = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    comentarios_playa = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Muros
    pintura_desgastada_muros = models.BooleanField(default=False, verbose_name="Pintura Desgastada")
    sucio_manchas_muros = models.BooleanField(default=False, verbose_name="Sucio/Manchas")
    otro_muros = models.CharField(max_length=200, blank=True, verbose_name="Otro")
    comentarios_muros = models.CharField(max_length=200, blank=True, verbose_name="Comentarios")

    # Sensores y bomba
    sensores_mal_estado = models.BooleanField(default=False, verbose_name="Sensores de nivel en mal estado")
    bomba_mal_estado = models.BooleanField(default=False, verbose_name="Bomba sentina en mal estado o no tienen")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class CondicionLiner(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Liner conditions
    perforaciones_cortes = models.BooleanField(default=False, verbose_name="Liner con perforaciones y/o cortes")
    carbonato = models.BooleanField(default=False, verbose_name="Liner con carbonato")
    algas = models.BooleanField(default=False, verbose_name="Liner con algas")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class CondicionVisualLaguna(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Turbidez
    opacidad_leve = models.BooleanField(default=False, verbose_name="Opacidad leve - turbidez media")
    sucia_alta = models.BooleanField(default=False, verbose_name="Sucia - turbidez alta")
    otro_turbidez = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Color
    verdoso = models.BooleanField(default=False, verbose_name="Verdoso")
    verde = models.BooleanField(default=False, verbose_name="Verde")
    lechoso = models.BooleanField(default=False, verbose_name="Lechoso")
    otro_color = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Liner
    liner_sedimento = models.BooleanField(default=False, verbose_name="Liner con sedimento")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class FuncionamientoAguaRelleno(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Bomba Agua de relleno
    bomba_mantencion = models.BooleanField(default=False, verbose_name="En mantención")
    no_funciona_energia = models.BooleanField(default=False, verbose_name="No funciona por falta de energía")
    no_funciona_electrico = models.BooleanField(default=False, verbose_name="No funciona por problema eléctrico o mecánico")
    otro_bomba = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Fuente de agua
    sequia = models.BooleanField(default=False, verbose_name="Sequía")
    cuentas_impagas = models.BooleanField(default=False, verbose_name="Cuentas de agua potable impagas")
    calidad_no_cumple = models.BooleanField(default=False, verbose_name="Calidad de agua no cumple estándar de Crystal Lagoons")
    otro_fuente = models.CharField(max_length=200, blank=True, verbose_name="Otro")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class NivelDeLaLaguna(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Nivel
    nivel_bajo = models.BooleanField(default=False, verbose_name="Nivel bajo")
    nivel_alto = models.BooleanField(default=False, verbose_name="Nivel alto")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class MedidasDeMitigacion(BaseChecklist):
    todo_bien = models.BooleanField(default=False, verbose_name="¿Operando todo bien? Sí")

    # Medidas
    medidas_ineficientes = models.BooleanField(default=False, verbose_name="Medidas Ineficientes")
    no_tienen = models.BooleanField(default=False, verbose_name="No tienen")

    # Evaluación general
    nota = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.todo_bien:
            self.nota = 5
            # Set all boolean fields to False except "todo_bien"
            for field in self._meta.fields:
                if isinstance(field, models.BooleanField) and field.name != "todo_bien":
                    setattr(self, field.name, False)

        super().save(*args, **kwargs)

class Supervisor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lagunas = models.ManyToManyField(Laguna, through='SupervisorLaguna', related_name='supervisors')

    def __str__(self):
        return self.name

class SupervisorLaguna(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    laguna = models.ForeignKey(Laguna, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('supervisor', 'laguna')

    def __str__(self):
        return f'{self.supervisor.name} - {self.laguna.Nombre}'

class LagoonDetail(models.Model):
    idLagunas = models.ForeignKey('Laguna', on_delete=models.CASCADE, verbose_name="Lagoon ID")
    date = models.DateField(verbose_name="Date")
    comentrelevant = models.TextField(verbose_name="Relevant Matters", blank=True, null=True)
    comentqw = models.TextField(verbose_name="Comments on Water Quality", blank=True, null=True)
    comentlgm = models.TextField(verbose_name="Comments on Lagoon Maintenance", blank=True, null=True)
    milestone = models.TextField(verbose_name="Milestones", blank=True, null=True)
    
    RESPONSIBILITY_CHOICES = [
        ('Operations', 'Operations'),
        ('Engineering', 'Engineering')
    ]
    responsible = models.CharField(max_length=20, choices=RESPONSIBILITY_CHOICES, verbose_name="Responsibility of the Milestone", blank=True, null=True)
    
    STATUS_CHOICES = [
        ('Normal Operation', 'Normal Operation'),
        ('Quarantine', 'Quarantine'),
        ('Emptying process', 'Emptying process'),
        ('Filling on going', 'Filling on going'),
        ('Quarantine/ Emptying process', 'Quarantine/ Emptying process'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Status", blank=True, null=True)
    showroom = models.BooleanField(verbose_name="Showroom Lagoon", default=False)

    class Meta:
        unique_together = ['idLagunas', 'date']

    def __str__(self):
        return f"{self.idLagunas} - {self.date} - {self.status}"

class Laguna_Stock(models.Model):
    # Choice for stock or supply
    STOCK_OR_SUPPLY_CHOICES = [
        ('stock', 'Stock'),
        ('supply', 'Supply'),
    ]

    # Fields
    date = models.DateField()
    laguna = models.ForeignKey(Laguna, on_delete=models.CASCADE, verbose_name="Project")
    stock_or_supply = models.CharField(max_length=6, choices=STOCK_OR_SUPPLY_CHOICES)
    
    # Stock items
    cl_ap2hi_tank = models.IntegerField()  # Number of tanks
    cl_ap2hi_storage = models.DecimalField(max_digits=10, decimal_places=2)  # Storage capacity

    cl_fh1lo_tank = models.IntegerField()
    cl_fh1lo_storage = models.DecimalField(max_digits=10, decimal_places=2)

    cl_flo12_tank = models.IntegerField()
    cl_flo12_storage = models.DecimalField(max_digits=10, decimal_places=2)

    cl_cotflo_tank = models.IntegerField()
    cl_cotflo_storage = models.DecimalField(max_digits=10, decimal_places=2)

    cl_mb010_tank = models.IntegerField()
    cl_mb010_storage = models.DecimalField(max_digits=10, decimal_places=2)

    # Add more fields as needed for each stock item

    def __str__(self):
        return f"{self.laguna.Nombre} - {self.date}"
    
class RelevantMatters(models.Model):
    laguna = models.ForeignKey(Laguna, on_delete=models.CASCADE, related_name="relevant_matters")
    text = models.TextField()  # Text field for the content
    date = models.DateField()  # Date field

    class Meta:
        unique_together = ('laguna', 'date')  # Ensures uniqueness for each laguna and date

    def __str__(self):
        return f"Relevant Matters for {self.laguna.Nombre} on {self.date}"

def get_default_laguna():
    return Laguna.objects.first().idLagunas  # Adjust this to return a default Laguna id

class AditivosLaguna(models.Model):
    proyecto = models.ForeignKey(Laguna, on_delete=models.CASCADE, related_name='aditivos_laguna')
    leadtime = models.CharField(max_length=255)
    ddaDiaLts_AP2 = models.CharField(max_length=255)
    ddaDiaLts_FH1 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.proyecto.Nombre} - {self.leadtime}"
    


class IMOP(models.Model):
    laguna = models.ForeignKey('Laguna', on_delete=models.CASCADE)
    generated_id = models.CharField(max_length=255, editable=False, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    resumen_ejecutivo = models.TextField()
    last_resumen_ejecutivo_date = models.DateField(editable=True, null=True)
    recomendaciones = models.TextField()
    last_recomendaciones_date = models.DateField(editable=True, null=True)
    temas_pendientes = models.TextField()
    last_temas_pendientes_date = models.DateField(editable=True, null=True)

    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Keep the update logic for other fields but remove the ID generation logic
        if self.pk:
            old_instance = IMOP.objects.get(pk=self.pk)
            if old_instance.resumen_ejecutivo != self.resumen_ejecutivo:
                self.last_resumen_ejecutivo_date = timezone.now().date()
            if old_instance.recomendaciones != self.recomendaciones:
                self.last_recomendaciones_date = timezone.now().date()
            if old_instance.temas_pendientes != self.temas_pendientes:
                self.last_temas_pendientes_date = timezone.now().date()

        super(IMOP, self).save(*args, **kwargs)

    def generate_id(self):
        selected_month_year = self.date.strftime("%m%y")
        num_imops = IMOP.objects.filter(laguna=self.laguna).count()
        self.generated_id = f"{self.laguna.idLagunas}-{num_imops + 1}-{selected_month_year}"
        self.save()