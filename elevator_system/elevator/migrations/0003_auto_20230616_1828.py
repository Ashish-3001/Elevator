# Generated by Django 3.0.5 on 2023-06-16 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elevator', '0002_auto_20230615_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elevator',
            old_name='is_door_open',
            new_name='is_door_opens',
        ),
    ]
