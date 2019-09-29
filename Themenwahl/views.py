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

 
thema_to_id = {
"Spezielle Funktionen und Vektorrechnung": 285,
"Einführung ins Differenzieren": 180,
"Näherungsmethoden": 182,
"Experimentieren und Auswerten": 184,
"Einführung ins Integrieren": 181,
"Gewöhnliche Differentialgleichungen": 200,
"Aufgabenseminar klassische Mechanik": 189,
"Zylindrische Körper im Wasser": 1558,
"Gravitationsbeschleunigung": 214,
"Klassische Mechanik": 216,
"Rotationsbewegungen": 190,
"Theoretische Mechanik": 197,
"Himmelsmechanik": 168,
"Aufgabenseminar Elektrodynamik": 198,
"Elektrische Blackboxen": 213,
"Energie im Kondensator (Exp)": 1556,
"Energie im Kondensator": 1555,
"Grundlagen der Elektrik": 1563,
"Elektrodynamik 1": 186,
"Komplexe Wechselstromrechnung": 183,
"Elektrodynamik 2": 187,
"Aufgabenseminar Wärmelehre": 1256,
"Thermodynamik 1": 167,
"Fluiddynamik": 283,
"Thermodynamik 2 - Statistische Physik": 257,
"Aufgabenseminar Quanten- und Atomphysik und Struktur der Materie": 199,
"Aufgabenseminar SRT": 1409,
"Leuchtdioden und Plancksches Winkumsquantum": 1557,
"Spezielle Relativitätstheorie": 170,
"Kernphysik": 171,
"Quanten- und Atomphysik I": 169,
"Relativistische Teilchenphysik": 331,
"Bestimmung des Brechungskoeffizienten von Plexiglas": 654,
"Bestimmung des Brechungskoeffizienten von Wasser": 332,
"Geometrische Optik": 188,
"Wellenoptik": 185,
"Marieneehrenmal": 1569,
"Mediendom/Computermuseum": 1570,
"Stadtführung": 1568,
"Halleffekt": 1552,
"Ideales Gas": 1554,
"Reversionspendel": 1548,
"Schallgeschwindigkeit in Metallen": 1550,
"Torsionsschwingung": 1549,
"Pohlsches Rad": 1551,
"Wechselstrombrücke": 1553,
"Fallender Doppler-Effekt": 1559,
"Hören": 1560,
"Thermographie an einem Modellhaus": 1561,
"Videoanalyse von Stößen ausgedehnter Körper auf einem Luftkissentisch": 1562,
}

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

def erzeuge_xml_themen():
    personen = models.Person.objects.all()
    attrnamen = [f.name for f in models.Person._meta.fields if f.name in models.themen_kiel]
    daten_wahl = sorted([(thema_to_id[name], person.code, getattr(person, name)) for name in attrnamen for person in personen])
    nodetexte = [text_node.format(themaid=tripel[0], personid=tripel[1], wahlprozent=25*tripel[2]) for tripel in daten_wahl]
    gesamttext = text_geruest.format(nodes='\n'.join(nodetexte))
    return gesamttext

def erzeuge_xml_personen():
    personen = models.Person.objects.all()
    users_geruest = """<?xml version="1.0" encoding="UTF-8" ?>
  <users>
{nodes}
  </users>
"""
    nodetemplate = "  <user>\n    <id>{code}</id>\n    <Name>{vorname} {nachname}</Name>\n    <Vorname>{vorname}</Vorname>\n    <Nachname>{nachname}</Nachname>\n  </user>"
    nodetexte = [nodetemplate.format(code=p.code, vorname=p.vorname, nachname=p.nachname) for p in personen]
    gesamttext = users_geruest.format(nodes='\n'.join(nodetexte))
    return gesamttext


@staff_member_required
def runterladen(request):
    """ gibt xml mit Themenwahlen zurück """
    themen = erzeuge_xml_themen()

    filename = "themenwahlen.xml"
    response = HttpResponse(themen, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

@staff_member_required
def runterladen_users(request):
    """ gibt xml mit Themenwahlen zurück """
    themen = erzeuge_xml_personen()

    filename = "teilnehmer-und-betreuer.xml"
    response = HttpResponse(themen, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

