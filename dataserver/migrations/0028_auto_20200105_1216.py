# Generated by Django 2.2.5 on 2020-01-05 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0027_auto_20200105_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prepay_order',
            name='phone_num',
            field=models.CharField(default='', max_length=15),
        ),
    ]