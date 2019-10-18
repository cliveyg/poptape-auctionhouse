# Generated by Django 2.2.4 on 2019-10-14 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0020_remove_auctionlot_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlot',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='auction.Auction'),
            preserve_default=False,
        ),
    ]
