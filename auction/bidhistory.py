# auctionhouse/auction/bidhistory.py
from auction.models import Auction, AuctionLot
from auction.models import EnglishAuctionLot, BuyNowAuctionLot
from auction.models import DutchAuctionLot, BidHistory

from kombu import Consumer, Connection, Exchange, Queue
import socket
from django.conf import settings
import json

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')

model = {
    "EN": EnglishAuctionLot,
    "BN": BuyNowAuctionLot,
    "DU": DutchAuctionLot,
}

class LotQueueConsumer():

    def __init__(self, lot_id):
        self.lot_id = lot_id
        self.queue_name = lot_id + "_auctionhouse"
        self.messages = []

    def connected_to_exchange(self):
        # need to connect to rabbit server and queue

        try:
            AuctionLot.objects.get(lot_id=self.lot_id)
        except AuctionLot.DoesNotExist:
            return False

        try:
            self.connection = Connection(hostname = settings.RABBIT_IP, 
                                         userid = settings.RABBIT_USER, 
                                         password = settings.RABBIT_PASS, 
                                         virtual_host = settings.RABBIT_VHOST,
                                         port = int(settings.RABBIT_PORT))
            self.exchange = Exchange(self.lot_id,
                                     durable = False, 
                                     type = 'fanout')
            self.queue = Queue(name = self.queue_name, 
                               durable = True,
                               exchange = self.exchange)
            self.consumer = Consumer(self.connection, 
                                     queues = self.queue, 
                                     callbacks = [self.process_message], 
                                     accept = ['json'])
        except Exception as err:
            logger.info("Something went bang in the queue: [%s]",err)
            return False

        return True

    def get_messages(self):
        with self.consumer:
            try:
                self.connection.drain_events(timeout=1)
            except socket.timeout:
                pass
            except Exception as e:
                logger.error("Something went bang! [%s]",e)
                

    def okeydokey(self):
        return "Howdy neighbour!"

    def process_message(self, body, message):
        # get the message data and create BidHistory records
        bid_body = json.loads(body)

        self.auction_type = bid_body.get('auction_type').upper()

        bid_history = BidHistory(bid_id = bid_body.get('bid_id'),
                                 username = bid_body.get('username'),
                                 public_id = bid_body.get('public_id'),
                                 bid_amount = bid_body.get('bid_amount'),
                                 bid_status = bid_body.get('bid_status'),
                                 lot_status = bid_body.get('lot_status'),
                                 message = bid_body.get('message'),
                                 reserve_message = bid_body.get('reserve_message'),
                                 unixtime = int(bid_body.get('unixtime')))
        # push records onto an array for saving later
        self.messages.append(bid_history)
        message.ack()

    def save_messages_to_db(self):

        if len(self.messages) == 0:
            return False

        model_type = model.get(self.auction_type)
        lot = model_type.objects.get(lot_id = self.lot_id)

        saved = 0
        errors = 0
        for bid_history in self.messages:
            bid_history.lot = lot
            try:
                bid_history.save()
            except Exception as err:
                # i'm expecting a few errors for example when trying to save
                # a bid that has already been saved for some reason
                logger.error("Problem saving bid history [%s]",err)
                errors = errors + 1
            else:
                saved = saved + 1

        logger.info("Bid history records saved: [%d], errored: [%d]",saved, errors)
            
        return
        
