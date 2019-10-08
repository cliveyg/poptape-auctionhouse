# Generated by Django 2.2.4 on 2019-10-08 16:05

import auctionhouse.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0014_auto_20191006_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlot',
            name='current_bid',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='auctionlot',
            name='starting_bid',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='auctionlot',
            name='winning_bid',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='buynowauctionlot',
            name='buy_now_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='dutchauctionlot',
            name='min_decrement',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='dutchauctionlot',
            name='reserve_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='dutchauctionlot',
            name='start_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='englishauctionlot',
            name='min_increment',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='englishauctionlot',
            name='reserve_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[auctionhouse.validators.validate_decimals]),
        ),
        migrations.AlterField(
            model_name='englishauctionlot',
            name='start_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[auctionhouse.validators.validate_decimals]),
        ),
    ]
