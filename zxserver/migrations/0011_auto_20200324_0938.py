# Generated by Django 2.2.5 on 2020-03-24 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zxserver', '0010_auto_20200324_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captain',
            name='zxuser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='zxserver.ZxUser'),
        ),
    ]
