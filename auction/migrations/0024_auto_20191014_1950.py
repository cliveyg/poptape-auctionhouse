# Generated by Django 2.2.4 on 2019-10-14 19:50

import auctionhouse.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0023_bidhistory_lot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dutchauctionlot',
            name='min_decrement',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=10, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='englishauctionlot',
            name='min_increment',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=10, validators=[auctionhouse.validators.validate_decimals]),
        ),
    ]