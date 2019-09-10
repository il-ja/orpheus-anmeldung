from django.contrib import admin
from . import models

# Register your models here.

class ThemenwahlAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'nachname', 'code', 'seminarort')
    readonly_fields = ['code']
    list_filter = ('seminarort', )

admin.site.register(models.Person, ThemenwahlAdmin)
