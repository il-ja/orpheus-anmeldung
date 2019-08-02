from django_extensions.db.models import TimeStampedModel
from django.db import models 


class Teilnahme(TimeStampedModel):
    """ Klasse für Teilnahme eines Schülers """
    vorname = models.CharField(max_length=144, blank=False)
    nachname = models.CharField(max_length=144, blank=False)
    geschlecht = models.CharField(max_length=1, choices=(('m', 'm'), ('w', 'w')), blank=False)
    email = models.EmailField(max_length=144, unique=True, blank=False)
    geburtsdatum = models.DateField(blank=False)
    telefon = models.CharField(max_length=144, verbose_name="Telefonnummer zur Planung der Anreise", blank=True)
    notfallnummer = models.CharField(max_length=144, verbose_name="Telefonnummer der Eltern für Notfälle", blank=False)
    essenswünsche = models.TextField(verbose_name="Besondere Essenswünsche (vegan, koscher, etc)", blank=True)
    beeinträchtigungen = models.TextField(verbose_name="Körperliche Beeinträchtigugen (z.B. Rollstuhl)", blank=True)
    weitere_hinweise = models.TextField(verbose_name="Weitere Hinweise", blank=True)


    def __str__(self):
        return "%s %s" % (self.vorname, self.nachname)
