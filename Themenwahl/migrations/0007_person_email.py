# Generated by Django 2.2.4 on 2019-09-05 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Themenwahl', '0006_auto_20190904_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(default='a@b.de', max_length=144, unique=True, verbose_name='eMail'),
            preserve_default=False,
        ),
    ]