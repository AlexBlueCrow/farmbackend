# Generated by Django 2.2.5 on 2019-11-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0007_comments_comment_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='item',
        ),
        migrations.AddField(
            model_name='comments',
            name='item_id',
            field=models.IntegerField(default=0),
        ),
    ]