# Generated by Django 2.1.7 on 2019-06-15 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0020_wydarzenie_srednia_ocen'),
    ]

    operations = [
        migrations.AddField(
            model_name='ogloszenie',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]
