from django_extensions.db.models import TimeStampedModel
from django.db import models 

import os

class Teilnahme(TimeStampedModel):
    """ Klasse für Teilnahme eines Schülers """
    teilnehmercode = models.CharField(max_length=144, verbose_name="Teilnehmercode für die PhysikOlympiade (falls vorhanden)", blank=True)
    seminarort = models.CharField(max_length=144, verbose_name="Seminarort", choices=(('Kiel', 'Kiel, 19.-22.9.19'), ('Dresden', 'Dresden, 3.-6.10.19')), blank=False)
    vorname = models.CharField(max_length=144, verbose_name="Vorname", blank=False)
    nachname = models.CharField(max_length=144, verbose_name="Nachname", blank=False)
    geschlecht = models.CharField(max_length=1, verbose_name="Geschlecht", choices=(('m', 'm'), ('w', 'w')), blank=False)
    email = models.EmailField(max_length=144, verbose_name="eMail", unique=True, blank=False)
    geburtsdatum = models.DateField(blank=False)
    notfallkontakt = models.CharField(max_length=144, verbose_name="Ansprechperson für Notfälle", blank=False)
    notfallnummer = models.CharField(max_length=144, verbose_name="Telefonnummer der Ansprechperson für Notfälle", blank=False)
    telefon = models.CharField(max_length=144, verbose_name="Telefonnummer zur Erreichbarkeit während der Anreise", blank=True)
    schule = models.CharField(max_length=144, verbose_name="Schule", blank=False)
    bundesland = models.CharField(max_length=144, verbose_name="Bundesland", blank=False)
    essenswünsche = models.TextField(verbose_name="Besondere Essenswünsche (vegan, koscher, etc)", blank=True)
    beeinträchtigungen = models.TextField(verbose_name="Körperliche Beeinträchtigugen (z.B. Rollstuhl)", blank=True)
    weitere_hinweise = models.TextField(verbose_name="Weitere Hinweise", blank=True)
    formulardatei = models.FileField(null=True)
    runtergeladen = models.BooleanField(default=False)
    datum_eingegangen = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s %s, %s" % (self.vorname, self.nachname, self.email)

    def erzeuge_formular(self):
        """ erzeugt und compiliert texdatei """
        with open('/home/olymp/orpheus-anmeldung_21/local_tex/formular_%s_template.tex' % (self.seminarort.lower()), 'r', encoding='utf-8') as f:
            template = f.read()

        text = template.format(
            code=self.teilnehmercode,
            vorname=self.vorname,
            nachname=self.nachname,
            email=self.email,
            geburtsdatum=str(self.geburtsdatum),
            geschlecht=self.geschlecht,
            notfallnummer="%s, %s" % (self.notfallkontakt, self.notfallnummer),
            essenswuensche=self.essenswünsche,
            beeintraechtigungen=self.beeinträchtigungen,
            schule=self.schule, 
            bundesland=self.bundesland,
            informationen=self.weitere_hinweise,
            startbahnhof='',
            zielbahnhof='',
        ).replace('"', "'").replace('&', r'\&').replace('_', r'\_')
 
        with open('/home/olymp/orpheus-anmeldung_21/local_tex/fertige_formulare/%s.tex' % self.pk, 'w', encoding='utf-8') as f:
            f.write(text)

        os.system('cd /home/olymp/orpheus-anmeldung_21/local_tex/fertige_formulare; pdflatex {0}.tex; pdflatex {0}.tex'.format(self.pk))
        self.formulardatei.name = "/home/olymp/orpheus-anmeldung_21/local_tex/fertige_formulare/{0}.pdf".format(self.pk)
        self.save()

    @property
    def bestaetigungstext(self):
        """ für Mailversand """
        felder = [
            self._meta.get_field(name)
	    for name in 'teilnehmercode, vorname, nachname, geburtsdatum, geschlecht, notfallkontakt, notfallnummer, telefon, essenswünsche, beeinträchtigungen, weitere_hinweise'.split(', ')
        ]
        daten = '\n'.join([
            " - %s: %s" % (feld.verbose_name, getattr(self, feld.attname))
            for feld in felder
        ])

        return """Guten Tag, {vorname} {nachname},

Danke für Dein Interesse, wir haben Deine Anfrage gespeichert!
Bitte beachte, dass die Anmeldung erst durch Einsenden des ausgefüllten und unterschriebenen Formulars abgeschlossen ist.

Im Anhang findest Du dein vorausgefülltes Formular. 
Bitte prüfe die Daten gründlich, trage eventuelle Ergänzungen ein, und sende es unterschrieben an die angegebene Adresse.
Wenn du noch Fragen hast, oder sich etwas ändern sollte, antworte bitte auf diese eMail!

Deine Anmeldung:

{daten}

Viele Grüße vom Orpheus e.V.
""".format(
            vorname=self.vorname,
            nachname=self.nachname,
            daten=daten)

    def datenzeile(self):
        """ gibt dict mit daten für ipn-Tabelle aus """
        daten = (
            ('Seminarort', self.seminarort),
            ('Nr', ' '),
            ('Vorname', self.vorname),
            ('Nachname', self.nachname),
            ('TN-Code', self.teilnehmercode),
            ('Geburtsdat.', self.geburtsdatum),
            ('Geschlecht', self.geschlecht),
            ('Anmeldeformular', ''),
            ('Status', ''),
            ('Verpflegung', self.essenswünsche),
            ('Beeinträchtigt', self.beeinträchtigungen),
            ('Telefon-Nr.', self.telefon),
            ('E-Mailadresse', self.email),
            ('Notfallrufnr. (Kontakt)', self.notfallnummer),
            ('Notfallkontakt', self.notfallkontakt),
            ('Schule', self.schule),
            ('Bundesland', self.bundesland),
            ('Straße', ' '),
            ('Ort', ' '),
            ('Veranstaltungsticket', ' '),
            ('von', ' '),
            ('nach', ' '),
            ('Datum hin', '19.9.' if self.seminarort=='Kiel' else '3.10.'),
            ('Datum rück', '22.9.' if self.seminarort=='Kiel' else '6.10.'),
            ('Bahntix-Nr.', ' '),
            ('Storno-Nr.', ' '),
	    ('Datum Anmeldung', self.datum_eingegangen),
        )       
        return daten

    class Meta:
        verbose_name_plural = 'Anmeldungen'
