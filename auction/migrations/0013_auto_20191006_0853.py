# Generated by Django 2.2.4 on 2019-10-06 08:53

from django.db import migrations
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0012_auto_20191005_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlot',
            name='end_time',
            field=django_unixdatetimefield.fields.UnixDateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auctionlot',
            name='start_time',
            field=django_unixdatetimefield.fields.UnixDateTimeField(blank=True, null=True),
        ),
    ]
