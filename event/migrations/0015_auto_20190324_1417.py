# Generated by Django 2.1.3 on 2019-03-24 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_wydarzenie_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miejsce',
            name='photo',
            field=models.ImageField(blank=True, default='miejsca/Default.jpg', upload_to='miejsca/'),
        ),
    ]
