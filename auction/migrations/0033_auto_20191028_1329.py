# Generated by Django 2.2.4 on 2019-10-28 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0032_bidhistory_public_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryoptions',
            old_name='lot_id',
            new_name='auction_id',
        ),
    ]
