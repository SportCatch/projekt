# Generated by Django 2.1.3 on 2019-01-05 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20190105_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miejsce',
            name='godzina_otwarcia',
        ),
        migrations.RemoveField(
            model_name='miejsce',
            name='godzina_zamkniecia',
        ),
        migrations.AddField(
            model_name='miejsce',
            name='miasto',
            field=models.CharField(default='Białystok', max_length=100),
        ),
        migrations.AlterField(
            model_name='miejsce',
            name='nazwa',
            field=models.CharField(max_length=100),
        ),
    ]
