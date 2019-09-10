from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'Themenwahl'

urlpatterns = [
    path('<str:pk>/', views.WahlEditieren.as_view(), name='wahl'),
]
