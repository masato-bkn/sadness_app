# Generated by Django 2.1.5 on 2019-10-19 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emotion', '0002_auto_20191019_0853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='usernamae',
            new_name='username',
        ),
    ]