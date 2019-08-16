from django_extensions.db.models import TimeStampedModel
from django.db import models 


class Teilnahme(TimeStampedModel):
    """ Klasse für Teilnahme eines Schülers """
    vorname = models.CharField(max_length=144, verbose_name="Vorname", blank=False)
    nachname = models.CharField(max_length=144, verbose_name="Nachname", blank=False)
    geschlecht = models.CharField(max_length=1, verbose_name="Geschlecht", choices=(('m', 'm'), ('w', 'w')), blank=False)
    email = models.EmailField(max_length=144, verbose_name="eMail", unique=True, blank=False)
    geburtsdatum = models.DateField(blank=False)
    telefon = models.CharField(max_length=144, verbose_name="Telefonnummer zur Planung der Anreise", blank=True)
    notfallnummer = models.CharField(max_length=144, verbose_name="Telefonnummer der Eltern für Notfälle", blank=False)
    essenswünsche = models.TextField(verbose_name="Besondere Essenswünsche (vegan, koscher, etc)", blank=True)
    beeinträchtigungen = models.TextField(verbose_name="Körperliche Beeinträchtigugen (z.B. Rollstuhl)", blank=True)
    weitere_hinweise = models.TextField(verbose_name="Weitere Hinweise", blank=True)


    def __str__(self):
        return "%s %s, %s" % (self.vorname, self.nachname, self.email)

    @property
    def bestaetigungstext(self):
        """ für Mailversand """
        felder = [
            self._meta.get_field(name)
            for name in 'vorname, nachname, geburtsdatum, telefon, notfallnummer, essenswünsche, beeinträchtigungen, weitere_hinweise'.split(', ')
        ]
        daten = '\n'.join([
            " - %s: %s" % (feld.verbose_name, getattr(self, feld.attname))
            for feld in felder
        ])

        return """Guten Tag, {vorname} {nachname},

Wir haben die folgenden Daten deiner Anmeldung gespeichert.
Wenn du noch Fragen hast, oder sich etwas ändern sollte, antworte bitte auf diese eMail!

Deine Anmeldung:

{daten}

Viele Grüße vom Orpheus e.V.
""".format(
            vorname=self.vorname,
            nachname=self.nachname,
            daten=daten)
