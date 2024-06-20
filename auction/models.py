from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_unixdatetimefield import UnixDateTimeField
# from djmoney.models.fields import MoneyField
# from auctionhouse.validators import validate_currency, validate_uuid_from_model
from auctionhouse.validators import validate_uuid_from_model
from auctionhouse.validators import validate_decimals

# -----------------------------------------------------------------------------
# a u c t i o n    m o d e l s
# -----------------------------------------------------------------------------
# i've made the design decision that an item cannot appear in more than one 
# auction. 
#
# also unsure of my choice for model design. i think having an auction item base
# class and then various child classes based on auction type works but again i
# may revisit this. it's a bit odd having auction type hanging off auction item
# but it's not strictly an auction type but valid fields for an item based on 
# auction type. naming stuff is hard :)
# 
# there are many different auction types such as:
# [1] english
# [2] dutch
# [3] sealed bid
# [4] vickery
# [5] reverse
# [6] bidding fee
# [7] buy it now
# [8] make me an offer - i'm treating this as 'buy it now' with a flag
#
# see https://en.wikipedia.org/wiki/Online_auction for more auction types
#
# i'm also using a fair amount of specialised django modules such as MoneyField
# as i know from experience that writing these can be a real pita. much 
# cleverer people than me have already written this stuff so why re-invent the
# wheel without a very good reason

# -----------------------------------------------------------------------------

# TODO: all the other auction types apart from english and buy now!


class AuctionType(models.Model):
    EN = 'EN'
    DU = 'DU'
    SB = 'SB'
    VK = 'VK'
    RV = 'RV'
    BF = 'BF'
    BN = 'BN'
    MO = 'MO'
    AUCTION_CHOICES = (
        (EN, 'English'),
        (DU, 'Dutch'),
        (SB, 'Sealed Bid'),
        (VK, 'Vickery'),
        (RV, 'Reverse'),
        (BF, 'Bidding Fee'),
        (BN, 'Buy Now'),
        (MO, 'Make Me An Offer'),
    )

# -----------------------------------------------------------------------------

class Testy(models.Model):
    test_id = models.CharField(max_length=36, blank=False, primary_key=True,
                               validators=[validate_uuid_from_model])
    public_id = models.CharField(max_length=36, blank=False,
                                 validators=[validate_uuid_from_model])
    type = models.CharField(max_length=15,
                            choices=AuctionType.AUCTION_CHOICES)
    name = models.CharField(max_length=100, blank=True)
    multiple = models.BooleanField(default=False, null=False)
    start_time = UnixDateTimeField(blank=True)
    end_time = UnixDateTimeField(blank=True)
    status = models.CharField(max_length=20, blank=False, default="created")

class Auction(models.Model):
    auction_id = models.CharField(max_length=36, blank=False, primary_key=True,
                                  validators=[validate_uuid_from_model])
    public_id = models.CharField(max_length=36, blank=False,
                                 validators=[validate_uuid_from_model])
    lots = ArrayField(models.CharField(max_length=36, 
                                       blank=False, null=False,
                                       validators=[validate_uuid_from_model]), size=500)
    type = models.CharField(max_length=15, 
                            choices=AuctionType.AUCTION_CHOICES) 
    name = models.CharField(max_length=100, blank=True)
    multiple = models.BooleanField(default=False, null=False)
    start_time = UnixDateTimeField(blank=True)
    end_time = UnixDateTimeField(blank=True)
    status = models.CharField(max_length=20, blank=False, default="created")
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=3, blank=False)

# -----------------------------------------------------------------------------


class AuctionLot(models.Model):
    lot_id = models.CharField(max_length=36, blank=False, primary_key=True,
                              validators=[validate_uuid_from_model])
    item_id = models.CharField(max_length=36, blank=False, unique=True, 
                               validators=[validate_uuid_from_model])
    status = models.CharField(max_length=20, blank=False, default="created")
    active = models.BooleanField(null=False, default=False)
    # i'm putting start and end times at both the item level and auction level
    # as live auctions have an ordered list of items to go through and the 
    # start time is when the lot comes up under the auctioneers hammer so is 
    # likely to be set at 'run' time - single item auctions will have both 
    # start times (and end times) set to teh same value
    start_time = UnixDateTimeField(blank=True, null=True)
    end_time = UnixDateTimeField(blank=True, null=True)
    quantity = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# -----------------------------------------------------------------------------

class BidHistory(models.Model):
    bid_id = models.CharField(max_length=36, blank=False, primary_key=True,
                              validators=[validate_uuid_from_model]) 
    lot = models.ForeignKey(AuctionLot, on_delete=models.CASCADE, related_name='lot')
    username = models.CharField(max_length=36, blank=False, null=False)
    public_id = models.CharField(max_length=36, blank=False,
                                 validators=[validate_uuid_from_model])
    bid_amount = models.DecimalField(null=True, blank=True, default=None,
                                     validators=[validate_decimals],
                                     max_digits=10, decimal_places=2)
    bid_status = models.CharField(max_length=10, blank=False, null=False)
    lot_status = models.CharField(max_length=10, blank=False, null=False)
    message = models.CharField(max_length=50, blank=False, null=False)
    reserve_message = models.CharField(max_length=20, blank=False, null=False)
    unixtime = models.BigIntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.bid_id, 
                self.username,
                self.public_id,
                self.bid_amount,
                self.bid_status,
                self.lot_status,
                self.message,
                self.reserve_message,
                self.unixtime)

    def __str__(self):
        return f'{self.bid_id}'

# -----------------------------------------------------------------------------


class EnglishAuctionLot(AuctionLot): 
    start_price = models.DecimalField(null=True, blank=True, default=None, 
                                      validators=[validate_decimals],
                                      max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(null=True, blank=True, default=None,
                                        validators=[validate_decimals],
                                        max_digits=10, decimal_places=2)
    min_increment = models.DecimalField(null=False, blank=False, default=0.01,
                                        validators=[validate_decimals],
                                        max_digits=10, decimal_places=2)

# -----------------------------------------------------------------------------


class BuyNowAuctionLot(EnglishAuctionLot):
    buy_now_price = models.DecimalField(null=False, blank=False, default=None,
                                        validators=[validate_decimals],
                                        max_digits=10, decimal_places=2)
    make_an_offer = models.BooleanField(null=False, default=False)

# -----------------------------------------------------------------------------


class DutchAuctionLot(AuctionLot):
    start_price = models.DecimalField(null=False, blank=False, default=None,
                                      validators=[validate_decimals],
                                      max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(null=True, blank=True, default=None,
                                        validators=[validate_decimals],
                                        max_digits=10, decimal_places=2)
    min_decrement = models.DecimalField(null=False, blank=False, default=0.01,
                                        validators=[validate_decimals],
                                        max_digits=10, decimal_places=2)

# -----------------------------------------------------------------------------


class PaymentOptions(models.Model):
    auction_id = models.CharField(max_length=36, blank=False, null=False)
    bank_transfer = models.BooleanField(null=False, default=False)
    mastercard = models.BooleanField(null=False, default=False)
    visa = models.BooleanField(null=False, default=False)
    amex = models.BooleanField(null=False, default=False)
    bitcoin = models.BooleanField(null=False, default=False)
    paypal = models.BooleanField(null=False, default=False)
    venmo = models.BooleanField(null=False, default=False)
    cash = models.BooleanField(null=False, default=False)
    cheque = models.BooleanField(null=False, default=False)

# -----------------------------------------------------------------------------


class DeliveryOptions(models.Model):
    auction_id = models.CharField(max_length=36, blank=False, null=False)
    postage = models.BooleanField(null=False, default=False)
    postage_cost = models.DecimalField(null=True, blank=True,
                                       validators=[validate_decimals],
                                       max_digits=10, decimal_places=2)
    collection = models.BooleanField(null=False, default=False)
    collection_cost = models.DecimalField(null=True, blank=True,
                                          validators=[validate_decimals],
                                          max_digits=10, decimal_places=2)
    delivery = models.BooleanField(null=False, default=False)
    delivery_cost = models.DecimalField(null=True, blank=True,
                                        validators=[validate_decimals],
                                        max_digits=10, decimal_places=2)
