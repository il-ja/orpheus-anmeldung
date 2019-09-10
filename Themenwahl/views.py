from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse

from django.contrib.admin.views.decorators import staff_member_required

from . import models, forms

class WahlEditieren(UpdateView):
    """ Editiert eine Person mit dem aus der url übergebenen code """
    model = models.Person
    #form_class = forms.WahlForm
    fields = ['vorname']
    template_name = 'Themenwahl/bearbeiten.html'
    context_object_name = 'person'
    def get_success_url(self):
        messages.success(self.request, "Die Auswahl wurde gespeichert")
        return reverse('Themenwahl:wahl', kwargs={'pk': self.object.code})

    def dispatch(self, request, *args, **kwargs):
        # Check permissions for the request.user here
        objekt = models.Person.objects.get(code=self.kwargs['pk'])
        self.fields = models.themen_dresden if objekt.seminarort=='Dresden' else models.themen_kiel
        return super().dispatch(request, *args, **kwargs)


@staff_member_required
def runterladen(request):
    allewahlen = models.Person.objects.all()
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

"""
<?xml version="1.0" encoding="UTF-8" ?>
<nodes>
  <node>
    <Thema>1421</Thema>
    <Benutzer>2424</Benutzer>
    <Wahl>25</Wahl>
  </node>
"""
