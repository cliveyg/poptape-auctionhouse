# auctionhouse/tests/test_setup.py

from auction.models import Auction, EnglishAuctionLot, PaymentOptions, DeliveryOptions
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def create_auction_and_lots(cls):

    auction_id = str(uuid.uuid4())
    public_id = str(uuid.uuid4())
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    lot1_id = str(uuid.uuid4())
    lot2_id = str(uuid.uuid4())

    cls.User1 = User.objects.create(
        username = public_id,
        first_name = "Blinky"
    )

    cls.Auction1 = Auction.objects.create(
        auction_id = auction_id,
        public_id = public_id,
        status = "created",
        lots = [lot1_id, lot2_id],
        type = "EN",
        name = "Auction 1",
        multiple = False,
        active = True,
        start_time = now,
        end_time = tomorrow,
        currency = "GBP"
    )

    cls.AucLot1 = EnglishAuctionLot.objects.create(
        lot_id = lot1_id,
        item_id = str(uuid.uuid4()),
        status = "created",
        active = False,
        start_time = now,
        end_time = tomorrow,
        quantity = 1,
        start_price = 1.00,
        reserve_price = 30.00,
        min_increment = 1.00
    )

    cls.AucLot2 = EnglishAuctionLot.objects.create(
        lot_id = lot2_id,
        item_id = str(uuid.uuid4()),
        status = "created",
        active = False,
        start_time = now,
        end_time = tomorrow,
        quantity = 1,
        start_price = 10.00,
        reserve_price = 500.00,
        min_increment = 15.00
    )
    lots = [cls.AucLot1, cls.AucLot2]

    cls.PayOpts = PaymentOptions.objects.create(
        auction_id = auction_id,
        mastercard = True
    )

    cls.DelivOpts1 = DeliveryOptions.objects.create(
        auction_id = auction_id,
        postage = False,
        delivery = False,
        collection = True
    )

    return cls.Auction1, lots
