# Generated by Django 2.2.5 on 2019-10-20 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0003_auto_20191020_0805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='Answer',
            new_name='correct_answer',
        ),
    ]
