from django.shortcuts import render
from django.views.generic.edit import CreateView
from . import models, forms

# Create your views here.

from django.http import HttpResponse

class NeueTeilnahme(CreateView):
    """ Erstellt Teilnahme """
    model = models.Teilnahme
    form_class = forms.TeilnahmeForm
    template_name = 'Anmeldung/neue_teilnahme.html'
    context_object_name = 'teilnahme'
    success_url='/danke'

