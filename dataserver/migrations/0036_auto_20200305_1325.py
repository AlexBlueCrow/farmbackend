# Generated by Django 2.2.5 on 2020-03-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0035_item_m_word'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mchinfo',
            name='id',
        ),
        migrations.AddField(
            model_name='mchinfo',
            name='appcode',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]