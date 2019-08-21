from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.NeueTeilnahme.as_view(), name='index'),
    path('danke', TemplateView.as_view(template_name='Anmeldung/danke.html')),
    path('runterladen', views.runterladen),

]
