from django.contrib import admin
from . import models

# Register your models here.

class AnmeldungAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'nachname', 'seminarort')
    list_filter = ('seminarort', 'runtergeladen')

admin.site.register(models.Teilnahme, AnmeldungAdmin)
