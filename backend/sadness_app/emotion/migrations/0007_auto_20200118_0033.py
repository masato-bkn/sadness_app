# Generated by Django 2.1.5 on 2020-01-18 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emotion', '0006_auto_20200117_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='display_name',
            new_name='displayName',
        ),
        migrations.RenameField(
            model_name='appuser',
            old_name='user_name',
            new_name='username',
        ),
    ]