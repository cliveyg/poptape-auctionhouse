# auctionhouse/tests/test_setup.py

from auction.models import Auction
from auction.models import Testy
import uuid
from datetime import datetime, timedelta
#from django_unixdatetimefield import UnixDateTimeField


def create_test(cls):

    test_id = str(uuid.uuid4())
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    cls.Test1 = Testy.objects.create(
        test_id = test_id,
        public_id = str(uuid.uuid4()),
        type = "English",
        name = "Testttty",
        multiple = False,
        start_time = now.timestamp(),
        end_time = tomorrow.timestamp(),
        status = "created"
    )
    return test_id


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
        start_time = now.timestamp(),
        end_time = tomorrow.timestamp(),
        currency = "GBP"
    )
    return auction_id
#auction_id = models.CharField(max_length=36, blank=False, primary_key=True,
#                              validators=[validate_uuid_from_model])
#public_id = models.CharField(max_length=36, blank=False,
#                             validators=[validate_uuid_from_model])
#lots = ArrayField(models.CharField(max_length=36,
#                                   blank=False, null=False,
#                                   validators=[validate_uuid_from_model]), size=500)
#type = models.CharField(max_length=15,
#                        choices=AuctionType.AUCTION_CHOICES)
#name = models.CharField(max_length=100, blank=True)
#multiple = models.BooleanField(default=False, null=False)
#start_time = UnixDateTimeField(blank=True)
#end_time = UnixDateTimeField(blank=True)
#status = models.CharField(max_length=20, blank=False, default="created")
#active = models.BooleanField(default=False)
#created = models.DateTimeField(auto_now_add=True)
#modified = models.DateTimeField(auto_now=True)
#currency = models.CharField(max_length=3, blank=False)