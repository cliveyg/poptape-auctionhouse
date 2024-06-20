# auctionhouse/tests/test_setup.py

from auction.models import Auction
from auction.models import Testy
import uuid
from datetime import datetime, timedelta
# from django_unixdatetimefield import UnixDateTimeField


def create_auction(cls):

    auction_id = str(uuid.uuid4())
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    cls.Auction1 = Auction.objects.create(
        auction_id = auction_id,
        public_id = str(uuid.uuid4()),
        status = "created",
        lots = [str(uuid.uuid4()), str(uuid.uuid4())],
        type = "Buy Now",
        name = "Auction 1",
        multiple = False,
        active = True,
        start_time = now,
        end_time = tomorrow,
        currency = "GBP"
    )
    return auction_id