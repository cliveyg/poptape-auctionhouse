# Generated by Django 2.2.2 on 2019-07-09 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auctionlot_lot_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='items',
            new_name='lots',
        ),
    ]
