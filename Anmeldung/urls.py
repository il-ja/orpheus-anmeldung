from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.NeueTeilnahme.as_view(), name='index'),
    path('danke', TemplateView.as_view(template_name='Anmeldung/danke.html')),
]
