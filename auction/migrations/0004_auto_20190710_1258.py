# Generated by Django 2.2.2 on 2019-07-10 12:58

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20190709_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buynowauctionlot',
            name='buy_now_price',
            field=djmoney.models.fields.MoneyField(decimal_places=4, max_digits=19),
        ),
        migrations.AlterField(
            model_name='englishauctionlot',
            name='start_price',
            field=djmoney.models.fields.MoneyField(decimal_places=4, max_digits=19),
        ),
    ]
