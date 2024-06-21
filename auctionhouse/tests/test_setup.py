# auctionhouse/tests/test_setup.py

from auction.models import Auction, AuctionLot
from django.contrib.auth.models import User
from auction.models import Testy
import uuid
from datetime import datetime, timedelta
# from django_unixdatetimefield import UnixDateTimeField


def create_auction_and_lots(cls):

    auction_id = str(uuid.uuid4())
    public_id = str(uuid.uuid4())
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    lot1_id = str(uuid.uuid4())
    lot2_id = str(uuid.uuid4())

    cls.Auction1 = Auction.objects.create(
        auction_id = auction_id,
        public_id = public_id,
        status = "created",
        lots = [lot1_id, lot2_id],
        type = "Buy Now",
        name = "Auction 1",
        multiple = False,
        active = True,
        start_time = now,
        end_time = tomorrow,
        currency = "GBP"
    )

    cls.AucLot1 = AuctionLot.objects.create(
        lot_id = lot1_id,
        item_id = str(uuid.uuid4()),
        status = "created",
        active = False,
        start_time = now,
        end_time = tomorrow,
        quantity = 1
    )

    cls.AucLot2 = AuctionLot.objects.create(
        lot_id = lot2_id,
        item_id = str(uuid.uuid4()),
        status = "created",
        active = False,
        start_time = now,
        end_time = tomorrow,
        quantity = 1
    )

    return auction_id
