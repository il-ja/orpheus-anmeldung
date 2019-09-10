from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render, HttpResponse
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

    
thema_to_id = dict(zip(models.themen_kiel, range(100)))

text_geruest = """<?xml version="1.0" encoding="UTF-8" ?>
<nodes>
{nodes}
</nodes>
"""

text_node = """  <node>
    <Thema>{themaid}</Thema>
    <Benutzer>{personid}</Benutzer>
    <Wahl>{wahlprozent}</Wahl>
  </node>"""

def erzeuge_xml():
    personen = models.Person.objects.all()
    attrnamen = [f.name for f in models.Person._meta.fields if f.name in models.themen_kiel]
    daten_wahl = sorted([(thema_to_id[name], person.code, getattr(person, name)) for name in attrnamen for person in personen])
    nodetexte = [text_node.format(themaid=tripel[0], personid=tripel[1], wahlprozent=25*tripel[2]) for tripel in daten_wahl]
    gesamttext = text_geruest.format(nodes='\n'.join(nodetexte))
    return gesamttext


@staff_member_required
def runterladen(request):
    """ gibt xml mit Themenwahlen zurück """
    content = erzeuge_xml()

    filename = "themenwahlen.xml"
    response = HttpResponse(content, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

