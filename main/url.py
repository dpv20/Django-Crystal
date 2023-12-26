from django.urls import path, include
from .views import initial_form_view, results_view
from django.conf import settings
from django.conf.urls.static import static

from . import views

from .views import (
    manuals_view, 
    stock_view, 
    notas_view, 
    select_laguna_view, 
    semanal_selection_view, 
    display_images_view, 
    upload_image_view,
    semanal_selection_view2,
    display_latest_relevant_matter_view,
    imops_view
)

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("<int:id>", views.index, name="index"),
    path("testing/", views.testing, name="testing"),
    path("view/", views.view, name="view"),
    path('database/', views.laguna_database, name='laguna_database'),
    path('edit-laguna/<str:idLagunas>/', views.edit_laguna, name='edit_laguna'),
    path('initial/', initial_form_view, name='initial_form'),
    path('results/', results_view, name='results'),
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
    path('laguna/relevant_matters/<str:idLagunas>/<str:fecha>/', views.display_latest_relevant_matter_view, name='display_latest_relevant_matter'),
    path('imops/', imops_view, name='imops_view'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


