# Generated by Django 2.2.4 on 2019-10-14 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0018_auto_20191013_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlot',
            name='auction',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='auction.Auction'),
            preserve_default=False,
        ),
    ]
