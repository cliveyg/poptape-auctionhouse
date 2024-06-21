from django.test import TestCase
from auction.models import EnglishAuctionLot, AuctionLot
import uuid
import pytz
from datetime import datetime, timedelta
from django.conf import settings

NOW = datetime.utcnow()
NOW_PLUS_TEN = NOW + timedelta(days=10)
timey = NOW
NOW_WITH_TZ = timey.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
LOT_ID = str(uuid.uuid4())
ITEM_ID = str(uuid.uuid4())


class ModelsTestCase(TestCase):

    def setUp(self):
        print('test_setUp')

        self.english_auc = EnglishAuctionLot.objects.create(lot_id = LOT_ID,
                                                            item_id = ITEM_ID,
                                                            start_time = NOW,
                                                            end_time = NOW_PLUS_TEN,
                                                            status = 'created',
                                                            active = True,
                                                            created = NOW_WITH_TZ,
                                                            modified = NOW_WITH_TZ,
                                                            quantity = 1,
                                                            start_price = 99.50,
                                                            reserve_price = 145.80,
                                                            min_increment = 0.50)

        self.english_auc = EnglishAuctionLot.objects.create(start_price = 99.50,
                                                            reserve_price = 145.80,
                                                            min_increment = 0.50)
'''
    def test_get_english_auction(self):
        # eng_auc_test = EnglishAuctionLot.objects.get(lot_id = LOT_ID)
        self.assertEqual(self.english_auc.start_price, 99.50)
'''
