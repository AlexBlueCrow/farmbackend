# Generated by Django 2.2.5 on 2019-10-20 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0002_auto_20191011_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_item',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dataserver.Item'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
