from django.shortcuts import render, HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.admin.views.decorators import staff_member_required

import csv, io

from . import models, forms

class NeueTeilnahme(CreateView):
    """ Erstellt Teilnahme """
    model = models.Teilnahme
    form_class = forms.TeilnahmeForm
    template_name = 'Anmeldung/neue_teilnahme.html'
    context_object_name = 'teilnahme'
    success_url='/danke'

@staff_member_required
def runterladen(request):
    neueitems = models.Teilnahme.objects.filter(runtergeladen=False)
    datenlisten = []
    for item in neueitems:
        daten = item.datenzeile()
        datenlisten.append(daten)
    
    csv_columns = [paar[0] for paar in daten]
    dict_data = [
        dict(daten)
        for daten in datenlisten
    ]
    
    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for zeile in dict_data:
        writer.writerow(zeile)

    filename = "daten.csv"
    content = f.getvalue()
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

