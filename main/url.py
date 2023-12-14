from django.urls import path, include
from .views import initial_form_view, results_view
from django.conf import settings
from django.conf.urls.static import static

from . import views

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)