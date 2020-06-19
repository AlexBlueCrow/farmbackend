# Generated by Django 2.2.5 on 2019-12-18 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0012_remove_order_order_farm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prepay_Order',
            fields=[
                ('out_trade_no', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('sign', models.CharField(max_length=50)),
                ('noncestr', models.CharField(max_length=50)),
                ('openid', models.CharField(max_length=40)),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('itme_id', models.IntegerField()),
                ('deliver_address', models.CharField(default='', max_length=50)),
                ('quantity', models.IntegerField(default=1)),
                ('buyernickname', models.CharField(default='', max_length=20)),
                ('postsign', models.CharField(default='', max_length=50)),
            ],
        ),
    ]