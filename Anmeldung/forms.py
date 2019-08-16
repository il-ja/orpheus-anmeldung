from django import forms
from django.forms import ModelForm

from django.core.mail import send_mail

from .models import Teilnahme


class DateInput(forms.DateInput):
    input_type = 'date'

class TeilnahmeForm(ModelForm):
    class Meta:
        model = Teilnahme
        fields = '__all__'
        widgets = {
            'geburtsdatum': DateInput(),
        }

    def save(self):
        """ Mail versenden beim Speichern """
        instance = super().save()
        send_mail(
            '[orpheus-verein.de] Deine Anmeldung',
            instance.bestaetigungstext,
            'seminar@orpheus-verein.de',
            [self.cleaned_data['email']],
            fail_silently=False,
        )
        return instance
