# Generated by Django 2.2.4 on 2019-10-06 10:41

import auctionhouse.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_auto_20191006_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buynowauctionlot',
            name='buy_now_price',
            field=models.FloatField(default=None, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='dutchauctionlot',
            name='min_decrement',
            field=models.FloatField(default=None, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='dutchauctionlot',
            name='start_price',
            field=models.FloatField(default=None, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='englishauctionlot',
            name='min_increment',
            field=models.FloatField(default=None, validators=[auctionhouse.validators.validate_decimals]),
        ),
    ]
