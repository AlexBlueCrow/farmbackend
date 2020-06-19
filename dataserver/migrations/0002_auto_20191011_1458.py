# Generated by Django 2.2.5 on 2019-10-11 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='oder_item',
            new_name='order_item',
        ),
        migrations.AddField(
            model_name='order',
            name='order_deliver_address',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='order_wxuser',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='dataserver.WxUser'),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_period',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]