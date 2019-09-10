# Generated by Django 2.2.4 on 2019-09-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anmeldung', '0008_teilnahme_datum_eingegangen'),
    ]

    operations = [
        migrations.AddField(
            model_name='teilnahme',
            name='notfallkontakt',
            field=models.CharField(default=' ', max_length=144, verbose_name='Ansprechperson für Notfälle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teilnahme',
            name='notfallnummer',
            field=models.CharField(max_length=144, verbose_name='Telefonnummer der Ansprechperson für Notfälle'),
        ),
        migrations.AlterField(
            model_name='teilnahme',
            name='telefon',
            field=models.CharField(blank=True, max_length=144, verbose_name='Telefonnummer zur Erreichbarkeit während der Anreise'),
        ),
    ]