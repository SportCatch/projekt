# Generated by Django 2.1.3 on 2019-03-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_auto_20190323_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miejsce',
            name='photo',
            field=models.ImageField(blank=True, default='miejsca/Default.jpg', upload_to=''),
        ),
    ]
