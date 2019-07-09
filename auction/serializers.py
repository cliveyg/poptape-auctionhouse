# auction/serializers.py
  
from rest_framework import serializers
from auction.models import Auction, AuctionLot
from auction.models import EnglishAuctionLot, BuyNowAuctionLot

# -----------------------------------------------------------------------------

class AuctionSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = Auction
        fields = ('auction_id', 'owner', 'lots', 'type',
                  'start_time', 'end_time', 'status', 'active',
                  'created', 'modified')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class AuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = AuctionLot
        fields = ('item_id', 'starting_bid', 'current_bid', 'winning_bid',
                  'start_time', 'end_time', 'status', 'active',
                  'quantity', 'created', 'modified')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class EnglishAuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = EnglishAuctionLot
        fields = ('item_id', 'starting_bid', 'current_bid', 'winning_bid',
                  'start_time', 'end_time', 'status', 'active',
                  'quantity', 'start_price', 'reserve_price',
                  'min_increment', 'created', 'modified', 'lot_id')
        read_only_fields = ('created', 'modified')

# -----------------------------------------------------------------------------

class BuyNowAuctionLotSerializer(serializers.ModelSerializer):
    # serializer to map the model instance into JSON format

    class Meta:
        # meta class to map serializer's fields with the model fields.
        model = BuyNowAuctionLot
        fields = ('item_id', 'starting_bid', 'current_bid', 'winning_bid',
                  'start_time', 'end_time', 'status', 'active',
                  'quantity', 'start_price', 'reserve_price',
                  'min_increment', 'buy_now_price', 'created', 'modified')
        read_only_fields = ('created', 'modified')
