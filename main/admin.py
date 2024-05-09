from django.contrib import admin

from .models import (
    ToDoList, 
    Item, 
    Supervisor, 
    Laguna, 
    LagunaImage, 
    LagoonDetail, 
    IMOP, 
    SupervisorLaguna, 
    Laguna_Stock, 
    AditivosLaguna,
    Feedback,
)
# Register your models here.

# admin.site.register(ToDoList)
#admin.site.register(Item)


from .models import Laguna

admin.site.register(Laguna)


from .models import (
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


class SupervisorLagunaInline(admin.TabularInline):
    model = SupervisorLaguna
    extra = 1

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [SupervisorLagunaInline]

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


class LagunaStockAdmin(admin.ModelAdmin):
    list_display = [
        'laguna', 'date', 'stock_or_supply', 
        'cl_ap2hi_tank', 'cl_ap2hi_storage', 
        'cl_fh1lo_tank', 'cl_fh1lo_storage', 
        'cl_flo12_tank', 'cl_flo12_storage', 
        'cl_cotflo_tank', 'cl_cotflo_storage', 
        'cl_mb010_tank', 'cl_mb010_storage'
    ]
    list_filter = ['date', 'laguna', 'stock_or_supply']
    search_fields = ['laguna__Nombre']
admin.site.register(Laguna_Stock, LagunaStockAdmin)


class RelevantMattersAdmin(admin.ModelAdmin):
    list_display = ('laguna', 'date', 'text_preview')

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'

admin.site.register(RelevantMatters, RelevantMattersAdmin)


class AditivosLagunaAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'leadtime', 'ddaDiaLts_AP2', 'ddaDiaLts_FH1')
    search_fields = ('proyecto__Nombre', 'leadtime', 'ddaDiaLts_AP2', 'ddaDiaLts_FH1')
    list_filter = ('proyecto', 'leadtime', 'ddaDiaLts_AP2', 'ddaDiaLts_FH1')

admin.site.register(AditivosLaguna, AditivosLagunaAdmin)






class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_feedback_type_display', 'short_description')

    def short_description(self, obj):
        """A method to return the first 50 characters of the description."""
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    short_description.short_description = 'Description'  # Sets column header

admin.site.register(Feedback, FeedbackAdmin)


class IMOPAdmin(admin.ModelAdmin):
    list_display = ('laguna', 'generated_id', 'date', 'is_completed')  # Customize as needed
    list_filter = ('laguna', 'date', 'is_completed')  # Customize as needed
    search_fields = ('laguna__Nombre', 'generated_id')  # Adjust 'laguna__name' if your Laguna model has a different field to search by
    readonly_fields = ('generated_id', 'var_FH1LO', 'var_AP2HI', 'nota_final')  # Fields that should not be editable
    fieldsets = (
        (None, {
            'fields': ('laguna', 'date', 'is_completed')
        }),
        ('Resumen y Recomendaciones', {
            'fields': ('resumen_ejecutivo', 'resumen_ejecutivo_date', 'recomendaciones', 'recomendaciones_date', 'temas_pendientes', 'temas_pendientes_date'),
        }),
        ('Comentarios de la Operación', {
            'fields': ('PER', 'BC', 'MC', 'FIL', 'DOS', 'REC', 'TEL', 'SKI', 'ULT', 'INF', 'LIN', 'VISUAL', 'WAT', 'LVL', 'ENV'),
        }),
        ('Variables y Nota Final', {
            'classes': ('collapse',),
            'fields': ('var_FH1LO', 'var_AP2HI', 'nota_final'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.generated_id:
            obj.generate_id()
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(IMOP, IMOPAdmin)