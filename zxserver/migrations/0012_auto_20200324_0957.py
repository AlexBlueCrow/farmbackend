# Generated by Django 2.2.5 on 2020-03-24 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zxserver', '0011_auto_20200324_0938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='captain',
            old_name='addresss',
            new_name='address',
        ),
    ]
