# Generated by Django 2.1.7 on 2019-03-14 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bori', '0006_auto_20190308_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='rcmdnews',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='rcmdnews',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
