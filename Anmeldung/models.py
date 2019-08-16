from django_extensions.db.models import TimeStampedModel
from django.db import models 

import os

class Teilnahme(TimeStampedModel):
    """ Klasse für Teilnahme eines Schülers """
    vorname = models.CharField(max_length=144, verbose_name="Vorname", blank=False)
    nachname = models.CharField(max_length=144, verbose_name="Nachname", blank=False)
    geschlecht = models.CharField(max_length=1, verbose_name="Geschlecht", choices=(('m', 'm'), ('w', 'w')), blank=False)
    email = models.EmailField(max_length=144, verbose_name="eMail", unique=True, blank=False)
    geburtsdatum = models.DateField(blank=False)
    telefon = models.CharField(max_length=144, verbose_name="Telefonnummer zur Planung der Anreise", blank=True)
    notfallnummer = models.CharField(max_length=144, verbose_name="Telefonnummer der Eltern für Notfälle", blank=False)
    schule = models.CharField(max_length=144, verbose_name="Schule", blank=False)
    bundesland = models.CharField(max_length=144, verbose_name="Bundesland", blank=False)
    essenswünsche = models.TextField(verbose_name="Besondere Essenswünsche (vegan, koscher, etc)", blank=True)
    beeinträchtigungen = models.TextField(verbose_name="Körperliche Beeinträchtigugen (z.B. Rollstuhl)", blank=True)
    weitere_hinweise = models.TextField(verbose_name="Weitere Hinweise", blank=True)


    def __str__(self):
        return "%s %s, %s" % (self.vorname, self.nachname, self.email)

    def erzeuge_formular(self):
        """ erzeugt und compiliert texdatei """
        with open('/home/olymp/orpheus-anmeldung_21/local_tex/formular_ilja_template.tex', 'r', encoding='utf-8') as f:
            template = f.read()

        text = template.format(
            code='',
            vorname=self.vorname,
            nachname=self.nachname,
            email=self.email,
            geburtsdatum=str(self.geburtsdatum),
            geschlecht=self.geschlecht,
            notfallnummer=self.notfallnummer,
            essenswuensche=self.essenswünsche,
            beeintraechtigungen=self.beeinträchtigungen,
            schule=self.schule, 
            bundesland=self.bundesland,
            informationen=self.weitere_hinweise,
            startbahnhof='',
            zielbahnhof='Kiel',
        )
 
        with open('/home/olymp/orpheus-anmeldung_21/local_tex/fertige_formulare/%s.tex' % self.pk, 'w', encoding='utf-8') as f:
            f.write(text)

        os.system('cd /home/olymp/orpheus-anmeldung_21/local_tex/fertige_formulare; pdflatex {0}.tex; pdflatex {0}.tex'.format(self.pk))

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

Danke für Dein Interesse, wir haben Deine Anmeldung bei uns gespeichert!
Im Anhang findest Du ein vorausgefülltes Formular. 
Bitte prüfe die Daten gründlich, trage eventuelle Ergänzungen ein, und sende es unterschrieben an die angegebene Adresse.
Wenn du noch Fragen hast, oder sich etwas ändern sollte, antworte bitte auf diese eMail!

Deine Anmeldung:

{daten}

Viele Grüße vom Orpheus e.V.
""".format(
            vorname=self.vorname,
            nachname=self.nachname,
            daten=daten)
