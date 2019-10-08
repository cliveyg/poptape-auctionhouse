# Generated by Django 2.2.4 on 2019-10-05 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_auto_20191005_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='DutchAuctionLot',
            fields=[
                ('auctionlot_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auction.AuctionLot')),
                ('start_price', models.FloatField(blank=True, default=None, null=True)),
                ('reserve_price', models.FloatField(blank=True, default=None, null=True)),
                ('min_decrement', models.FloatField(blank=True, default=None, null=True)),
            ],
            bases=('auction.auctionlot',),
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='owner',
            new_name='public_id',
        ),
    ]
