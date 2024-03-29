from django.urls import path, include
from .views import initial_form_view, results_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views

from .views import (
    manuals_view, 
    stock_view, 
    notas_view, 
    select_laguna_view, 
    semanal_selection_view, 
    display_images_view, 
    upload_image_view,
    imops_view,
    index_page,
    supervisor_relevant_matters_view,
    update_image_selection,
    supervisor_report,
    generate_pdf,
    generate_imop_id,
    viernes_view,
    login_view,
    results_EN_view,
    submit_feedback,
    imop_view,
)

urlpatterns = [
    path("", views.index_page, name="indexpage"),
    path("home/", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("<int:id>", views.index, name="index"),
    path("testing/", views.testing, name="testing"),
    path("view/", views.view, name="view"),
    path('database/', views.laguna_database, name='laguna_database'),
    path('edit-laguna/<str:idLagunas>/', views.edit_laguna, name='edit_laguna'),
    path('initial/', initial_form_view, name='initial_form'),
    path('results/', results_view, name='results'),
    path('results_EN/', results_EN_view, name='results_EN'),

    path('daily-report/', views.daily_report, name='daily_report'),
    path('daily-report/monday/<str:idLagunas>/', views.lagoon_detail, name='monday'),
    path('daily-report/friday/<str:idLagunas>/', views.lagoon_detail, name='friday'),
    path('manuals/', manuals_view, name='manuals'),
    path('stock/', stock_view, name='stock'),
    path('select-laguna/', select_laguna_view, name='select_laguna'),
    path('notas/<str:nombre_laguna>/', notas_view, name='notas'),
    path('semanal/', semanal_selection_view, name='semanal-select_laguna'),
    path('semanal/<str:idLagunas>/<str:fecha>/', display_images_view, name='display_images'),
    path('semanal/upload/<str:idLagunas>/<str:fecha>/', upload_image_view, name='upload_image'),
    path('update_image_status/', views.update_image_status, name='update_image_status'),
    path('semanal_selection/', views.semanal_selection_view2, name='semanal_selection'),
    path('imops/', views.imops_view, name='imops_view'),
    path('supervisor/<str:supervisor_name>/', views.supervisor_relevant_matters_view, name='supervisor_relevant_matters'),
    path('supervisor/<str:supervisor_name>/2', views.supervisor_relevant_matters_page2, name='supervisor_relevant_matters_page2'),
    path('update_image_selection/', update_image_selection, name='update_image_selection'),
    path('supervisor/<str:supervisor_name>/3', supervisor_report, name='supervisor_report'),
    path('supervisor/<str:supervisor_name>/report_pdf', generate_pdf, name='generate_pdf'),
    
    path('generate_imop_id/', views.generate_imop_id, name='generate_imop_id'),
    path('imops/<str:id_laguna>/<str:date>/', views.create_imop_view, name='create_imop_view'),
    path('imops/<str:id_laguna>/<str:date>/info', views.imop_view, name='imop_info_view'),
    path('imops/<str:id_laguna>/<str:date>/info/pdf', views.imop_pdf_view, name='imop_pdf_view'),

    
    path('viernes/', viernes_view, name='viernes'),
    path('viernes/<str:name>/', viernes_view, name='viernes_with_name'),

    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('feedback/submit/', submit_feedback, name='submit_feedback'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


