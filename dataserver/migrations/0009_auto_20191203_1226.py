# Generated by Django 2.2.5 on 2019-12-03 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0008_auto_20191119_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_farm',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='dataserver.FarmUser'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_postsign',
            field=models.CharField(default='', max_length=50),
        ),
    ]
