# Generated by Django 2.2.5 on 2020-01-05 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0024_auto_20200102_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_num',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='prepay_order',
            name='phone_num',
            field=models.IntegerField(default=0),
        ),
    ]
