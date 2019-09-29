from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'Themenwahl'

urlpatterns = [
    path('runterladen_themen/', views.runterladen, name='runterladen_themen'),
    path('runterladen_users/', views.runterladen_users, name='runterladen_users'),
    path('<str:pk>/', views.WahlEditieren.as_view(), name='wahl'),
]
