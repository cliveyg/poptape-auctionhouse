# Generated by Django 2.2.4 on 2019-10-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0026_auto_20191014_2154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidhistory',
            old_name='your_bid',
            new_name='bid_amount',
        ),
        migrations.AddField(
            model_name='bidhistory',
            name='reserve_message',
            field=models.CharField(default='No reserve', max_length=20),
            preserve_default=False,
        ),
    ]
