from django_extensions.db.models import TimeStampedModel
from django.db import models 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import EmailMessage

import os, string, random

themen_dresden = [name for name in """
Spezielle Funktionen und Vektorrechnung
Einführung ins Differenzieren
Näherungsmethoden
Experimentieren und Auswerten
Einführung ins Integrieren
Gewöhnliche Differentialgleichungen
Fouriertransformation
Erzwungene/Gedämpfte Schwingungen

Aufgabenseminar klassische Mechanik
Harmonische Schwingungen

Reversionspendel
Gravitationsbeschleunigung

Klassische Mechanik
Rotationsbewegungen
Theoretische Mechanik
Minimalprinzip
Himmelsmechanik

Aufgabenseminar Elektrodynamik
Elektrische Blackboxen
Erdmagnetisches Feld
Passiver Zweipol

Elektrische Schlatungen
Elektronik
Elektrodynamik 1
Komplexe Wechselstromrechnung
Elektrodynamik 2

Aufgabenseminar Wärmelehre

Adiabatische Zustandsänderung
Oberflächenspannung
Stehende Wellen
Strömung im Rohr

Thermodynamik 1
Fluiddynamik
Thermodynamik 2

Aufgabenseminar Quanten- und Atomphysik und Struktur der Materie
Aufgabenseminar SRT

Spezielle Relativitätstheorie
Kosmologie und Astrophysik
Kernphysik
Quanten- und Atomphysik I
Quanten- und Atomphysik II
Relativistische Teilchenphysik

Bestimmung des Brechungskoeffizienten von Plexiglas
Bestimmung des Brechungskoeffizienten von Wasser
Geometrische Optik
Wellenoptik

Hygienemuseum
Mathematisch-Physikalischer Salon
Spiel und Spaß im Großen Garten
Stadtführung
Wandern
""".splitlines() if name]

themen_kiel = [name for name in """
Spezielle Funktionen und Vektorrechnung
Einführung ins Differenzieren
Näherungsmethoden
Experimentieren und Auswerten
Einführung ins Integrieren
Gewöhnliche Differentialgleichungen

Aufgabenseminar klassische Mechanik

Zylindrische Körper im Wasser
Gravitationsbeschleunigung

Klassische Mechanik
Rotationsbewegungen
Theoretische Mechanik
Himmelsmechanik

Aufgabenseminar Elektrodynamik
Elektrische Blackboxen

Energie im Kondensator
Grundlagen der Elektrik
Elektrodynamik 1
Komplexe Wechselstromrechnung
Elektrodynamik 2

Aufgabenseminar Wärmelehre

Thermodynamik 1
Fluiddynamik

Aufgabenseminar Quanten- und Atomphysik und Struktur der Materie
Aufgabenseminar SRT

Leuchtdioden und Plancksches Winkumsquantum

Spezielle Relativitätstheorie
Kernphysik
Quanten- und Atomphysik I
Relativistische Teilchenphysik

Bestimmung des Brechungskoeffizienten von Plexiglas
Bestimmung des Brechungskoeffizienten von Wasser
Geometrische Optik
Wellenoptik

Halleffekt
Ideales Gas
Reversionspendel
Schallgeschwindigkeit in Metallen
Torsionsschwingung
Pohlsches Rad
Wechselstrombrücke
Fallender Doppler-Effekt
Hören
Thermographie an einem Modellhaus
Videoanalyse von Stößen ausgedehnter Körper auf einem Luftkissentisch

Marieneehrenmal
Mediendom/Computermuseum
Stadtführung
""".splitlines() if name]

themen = set(themen_kiel + themen_dresden)

class Person(TimeStampedModel):
    email = models.EmailField(max_length=144, verbose_name="eMail", unique=True, blank=False)
    vorname = models.CharField(max_length=144, verbose_name="Vorname", blank=False)
    nachname = models.CharField(max_length=144, verbose_name="Nachname", blank=False)
    code = models.CharField(max_length=8, verbose_name="Zugangscode", blank=False, null=False, primary_key=True)
    seminarort = models.CharField(max_length=144, verbose_name="Seminarort", choices=(('Kiel', 'Kiel, 19.-22.9.19'), ('Dresden', 'Dresden, 3.-6.10.19')), blank=False)
    
    @classmethod
    def code_generieren(cls):
        auswahl = string.ascii_letters + 2*string.digits + '_____'
        return ''.join(random.sample(auswahl, 8))
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.code_generieren()
        super().save(*args, **kwargs)

    def mail_versenden(self):
        """ versendet Mail mit der Bitte, Themen zu wählen """
        email = EmailMessage(
            '[orpheus-verein.de] Themenwahl für Seminar in %s' % self.seminarort,
            """Guten Tag, {vorname} {nachname},

Bitte besuche den Link https://anmeldung.orpheus-verein.de/{code}/ um deine Themen auszuwählen
Die Beschreibungen der Themen findest du unter https://www.orpheus-verein.de/node/{ortid}/themen

Danke für deine Mithilfe zur Erstellung unseres Stundenplans!
der Orpheus e.V.
            """.format(
                vorname=self.vorname,
                nachname=self.nachname,
                code=self.code,
                ortid=1491 if self.seminarort=='Kiel' else 1492,
            ),
            'seminar@orpheus-verein.de',
            [self.email],
            ['ilja1988@gmail.com'],
            reply_to=['seminar@orpheus-verein.de'],
            headers={'Message-ID': '%s' % self.code },
        )

        email.send()
    
    @classmethod
    def personen_eintragen(cls, daten):
        """ nimmt Liste von Daten (dicts) und legt Personen an """
        for zeile in daten:
            person = Person.objects.create(**zeile)
            person.mail_versenden()

for thema in themen:
    Person.add_to_class(
        thema,
        models.IntegerField(
            blank=True,
            default=0,
            null=True,
            validators=[MinValueValidator(0, message='Bitte Wert 0-4 eingeben'), MaxValueValidator(4, message='Bitte Wert 0-4 eingeben')]
        ),
    )
