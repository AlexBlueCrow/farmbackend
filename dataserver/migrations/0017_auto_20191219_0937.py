# Generated by Django 2.2.5 on 2019-12-19 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0016_auto_20191218_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_benifits',
            new_name='order_benefit',
        ),
    ]
