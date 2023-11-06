# auctionhouse/auction/janitor.py
from background_task import background
from auction.models import Auction  # , EnglishAuctionLot, BuyNowAuctionLot
"""from auction.models import AuctionLot, DutchAuctionLot, BidHistory
from auction.models import DeliveryOptions, PaymentOptions
from auction.serializers import AuctionSerializer, EnglishAuctionLotSerializer
from auction.serializers import DutchAuctionLotSerializer, BuyNowAuctionLotSerializer
from auction.serializers import BidHistorySerializer
from auction.serializers import PaymentOptionsSerializer, DeliveryOptionsSerializer"""
import time

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')


@background()
def process_finished_single_auctions():

    unixnow = int(time.time())
    auctions = None
    try:
        # auctions = Auction.objects.filter(active=True)\
        #                           .filter(multiple=False)\
        #                           .filter(end_time__lte=unixnow)
        auctions = Auction.objects.filter(multiple=False)\
                                  .filter(end_time__lte=unixnow)
    except Exception as e:
        logger.error("Auction get fail! [%s]", e)

    for auction in auctions:
        logger.error("------------------------")
        logger.error("Auction ID is [%s]", auction.auction_id)

        # auction.active = False
        # auction.status = "Finished"
        # lots = auction.lots
        # lot_id = lots[0]
        lot_id = auction.lots[0]
        logger.error("Lot ID is [%s]", lot_id)

        # for bid in bids:
        #   bid_serializer = BidHistorySerializer(bid)

    logger.info("woopy - process_finished_auctions")

    
