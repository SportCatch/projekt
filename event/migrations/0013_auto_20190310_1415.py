# Generated by Django 2.1.4 on 2019-03-10 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_friends'),
        ('event', '0012_auto_20190310_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zaproszenia',
            name='tresc',
        ),
        migrations.RemoveField(
            model_name='zaproszenia',
            name='uzytkownicyy',
        ),
        migrations.AddField(
            model_name='zaproszenia',
            name='uzytkownicyy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Zaproszony', to='account.Profile'),
        ),
    ]
