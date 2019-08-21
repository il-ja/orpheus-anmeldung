from django import forms
from django.forms import ModelForm

from django.core.mail import EmailMessage

from .models import Teilnahme


class DateInput(forms.DateInput):
    input_type = 'date'

class TeilnahmeForm(ModelForm):
    class Meta:
        model = Teilnahme
        exclude = ['formulardatei', 'runtergeladen']
        widgets = {
            'geburtsdatum': DateInput(),
        }

    def save(self):
        """ Mail versenden beim Speichern """
        instance = super().save()
        instance.erzeuge_formular()

        email = EmailMessage(
            '[orpheus-verein.de] Deine Anmeldung zum Seminar in %s' % instance.seminarort,
            instance.bestaetigungstext,
            'seminar@orpheus-verein.de',
            [self.cleaned_data['email']],
            ['ilja1988@gmail.com'],
            reply_to=['seminar@orpheus-verein.de'],
            headers={'Message-ID': '%s' % instance.pk },
        )

        email.attach_file('local_tex/fertige_formulare/%s.pdf' % instance.pk)
        email.send()

        return instance
