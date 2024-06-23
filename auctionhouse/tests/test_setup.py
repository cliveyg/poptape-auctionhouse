# auctionhouse/tests/test_setup.py

from auction.models import Auction, EnglishAuctionLot
# from django.contrib.auth.models import User
# from auction.models import Testy
import uuid
from datetime import datetime, timedelta
# from django_unixdatetimefield import UnixDateTimeField
import logging

logger = logging.getLogger(__name__)


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

    logger.info("LENGTH OF LOTS IS: %d", len(lots))
    logger.info("LOTS :[%s]", lots)

    return cls.Auction1, lots
