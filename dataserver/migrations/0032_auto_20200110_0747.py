# Generated by Django 2.2.5 on 2020-01-10 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0031_auto_20200108_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collectiveorder',
            old_name='username',
            new_name='contact',
        ),
        migrations.RenameField(
            model_name='collectiveorder',
            old_name='phonenumber',
            new_name='phone_num',
        ),
        migrations.RenameField(
            model_name='giftcode',
            old_name='itemId',
            new_name='item_id',
        ),
        migrations.AddField(
            model_name='giftcode',
            name='ip_line',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='giftcode',
            name='ip_row',
            field=models.IntegerField(default=0),
        ),
    ]
