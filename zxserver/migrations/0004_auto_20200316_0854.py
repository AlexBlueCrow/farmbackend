# Generated by Django 2.2.5 on 2020-03-16 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zxserver', '0003_auto_20200310_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Captain',
            fields=[
                ('captain_id', models.AutoField(primary_key=True, serialize=False)),
                ('longitude', models.DecimalField(decimal_places=4, default=0, max_digits=8)),
                ('latitude', models.DecimalField(decimal_places=4, default=0, max_digits=8)),
                ('addresss', models.CharField(max_length=40)),
                ('phonenumber', models.BigIntegerField(blank=True, default=0)),
                ('name', models.CharField(blank=True, default='', max_length=20)),
                ('active', models.BooleanField(default=False)),
                ('zxuser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='zxserver.ZxUser')),
            ],
        ),
        migrations.AddField(
            model_name='zxorder',
            name='captain',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, to='zxserver.Captain'),
        ),
        migrations.AddField(
            model_name='zxprepay_order',
            name='captain',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, to='zxserver.Captain'),
        ),
    ]