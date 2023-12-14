from django.contrib import admin
from .models import ToDoList, Item, Supervisor, Laguna, LagunaImage, LagoonDetail
# Register your models here.

# admin.site.register(ToDoList)
#admin.site.register(Item)


from .models import Laguna

admin.site.register(Laguna)


from .models import PersonalDeLaLaguna, OperacionLimpiezaDeFondo, OperacionLimpiezaManual, OperacionFiltro, OperacionSistemaDosificacion, OperacionSistemaRecirculacion, FuncionamientoTelemetria, OperacionSkimmers, OperacionUltrasonido, Infraestructura, CondicionLiner, CondicionVisualLaguna, FuncionamientoAguaRelleno, NivelDeLaLaguna, MedidasDeMitigacion
@admin.register(OperacionLimpiezaDeFondo)
class OperacionLimpiezaDeFondoAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']  # Add more fields here if you want them to be displayed in the list view
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']   # Filters for the right sidebar
    search_fields = ['supervisor', 'lagoon']  # Fields by which you can search

@admin.register(PersonalDeLaLaguna)
class PersonalDeLaLagunaAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(OperacionLimpiezaManual)
class OperacionLimpiezaManualAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(OperacionFiltro)
class OperacionFiltroAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(OperacionSistemaDosificacion)
class OperacionSistemaDosificacionAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(OperacionSistemaRecirculacion)
class OperacionSistemaRecirculacionAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(FuncionamientoTelemetria)
class FuncionamientoTelemetriaAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(OperacionSkimmers)
class OperacionSkimmersAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(OperacionUltrasonido)
class OperacionUltrasonidoAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(Infraestructura)
class InfraestructuraAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(CondicionLiner)
class CondicionLinerAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(CondicionVisualLaguna)
class CondicionVisualLagunaAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(FuncionamientoAguaRelleno)
class FuncionamientoAguaRellenoAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(NivelDeLaLaguna)
class NivelDeLaLagunaAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(MedidasDeMitigacion)
class MedidasDeMitigacionAdmin(admin.ModelAdmin):
    list_display = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    list_filter = ['date', 'supervisor', 'lagoon', 'todo_bien', 'nota']
    search_fields = ['supervisor', 'lagoon']

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class LagunaImageAdmin(admin.ModelAdmin):
    list_display = ['laguna', 'date', 'selected']
    search_fields = ['laguna__Nombre', 'date']
    list_filter = ['selected', 'date']

admin.site.register(LagunaImage, LagunaImageAdmin)

class LagoonDetailAdmin(admin.ModelAdmin):
    list_display = ('idLagunas', 'date', 'status')
    search_fields = ('idLagunas__Nombre', 'status')  # Assuming you want to search by Laguna's Nombre field
    list_filter = ('status', 'responsible', 'showroom')
    ordering = ['date', 'idLagunas']
    date_hierarchy = 'date'

admin.site.register(LagoonDetail, LagoonDetailAdmin)
