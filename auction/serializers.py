# auction/serializers.py
  
from rest_framework import serializers
#from auction.bidhistory import BuildBidHistory
from auction.models import Auction, AuctionLot, BidHistory
from auction.models import EnglishAuctionLot, BuyNowAuctionLot
from auction.models import DutchAuctionLot
from auction.models import DeliveryOptions, PaymentOptions

#TODO: write serializer for bid history

# -----------------------------------------------------------------------------

class AuctionSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = Auction
        fields = ('auction_id', 'public_id', 'lots', 'type',
                  'start_time', 'end_time', 'status', 'active',
                  'multiple', 'name', 'created', 'modified')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class AuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format
    #bids = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = AuctionLot
        fields = ('item_id', 'start_time', 'end_time', 'status', 'active',
                  'quantity', 'created', 'modified')
#        fields = ('item_id', 'starting_bid', 'current_bid', 'winning_bid',
#                  'start_time', 'end_time', 'status', 'active',
#                  'quantity', 'created', 'modified')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class BidHistorySerializer(serializers.ModelSerializer):

    class Meta: 
        model = BidHistory
        fields = ('bid_id', 'username', 'public_id', 'bid_amount', 'bid_status',
                  'lot_status', 'message', 'reserve_message', 'unixtime',
                  'created')
        read_only_fields = ('created',)

# -----------------------------------------------------------------------------

class EnglishAuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = EnglishAuctionLot
        fields = ('item_id', 'start_time', 'end_time', 'status', 'active',
                  'quantity', 'start_price', 'reserve_price',
                  'min_increment', 'created', 'modified', 'lot_id')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class BuyNowAuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = BuyNowAuctionLot
        fields = ('item_id', 'start_time', 'end_time', 'status', 'active',
                  'quantity', 'start_price', 'reserve_price', 'make_an_offer',
                  'min_increment', 'buy_now_price', 'created', 'modified')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class DutchAuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = DutchAuctionLot
        fields = ('item_id', 'start_time', 'end_time', 'status', 'active',
                  'quantity', 'start_price', 'reserve_price',
                  'min_decrement', 'created', 'modified', 'lot_id')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class PaymentOptionsSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = PaymentOptions
        fields = ('bank_transfer', 'mastercard', 'visa', 'amex', 'bitcoin',
                  'paypal', 'venmo', 'cash', 'cheque' )

# -----------------------------------------------------------------------------

class DeliveryOptionsSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = DeliveryOptions
        fields = ('postage', 'postage_cost', 'delivery', 'delivery_cost',
                  'collection', 'collection_cost')
