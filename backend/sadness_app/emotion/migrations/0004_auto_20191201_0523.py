# Generated by Django 2.1.5 on 2019-12-01 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotion', '0003_auto_20191019_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
