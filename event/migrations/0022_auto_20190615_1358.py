# Generated by Django 2.1.7 on 2019-06-15 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0021_ogloszenie_is_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='ogloszenie',
            name='liczba_wyswietlen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wydarzenie',
            name='liczba_wyswietlen',
            field=models.IntegerField(default=0),
        ),
    ]
