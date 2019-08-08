from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_unixdatetimefield import UnixDateTimeField
#from djmoney.models.fields import MoneyField

from auctionhouse.validators import validate_currency, validate_uuid_from_model

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
# [8] make me an offer
#
# see https://en.wikipedia.org/wiki/Online_auction for more auction types
#
# i'm also using a fair amount of specialised django modules such as MoneyField
# as i know from experience that writing these can be a real pita. much 
# cleverer people than me have already written this stuff so why re-invent the
# wheel without a very good reason

# -----------------------------------------------------------------------------

#TODO: all the other auction types apart from english and buy now!

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

class Auction(models.Model):
    auction_id = models.CharField(max_length=36, blank=False, unique=True, 
                                  validators=[validate_uuid_from_model])
    owner = models.CharField(max_length=36, blank=False,
                             validators=[validate_uuid_from_model])
    lots = ArrayField(models.CharField(max_length=36, 
                                        blank=False, null=False,
                                        validators=[validate_uuid_from_model]),
                       size=500)
    type = models.CharField(max_length=15, 
                            choices=AuctionType.AUCTION_CHOICES) 
    start_time = UnixDateTimeField()
    end_time = UnixDateTimeField()
    status = models.CharField(max_length=20, blank=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=3)

# -----------------------------------------------------------------------------

class AuctionLot(models.Model):
    lot_id = models.CharField(max_length=36, blank=False, unique=True,
                               validators=[validate_uuid_from_model])
    item_id = models.CharField(max_length=36, blank=False, unique=True, 
                               validators=[validate_uuid_from_model])
    status = models.CharField(max_length=20, blank=False, default="created")
    active = models.BooleanField(null=False, default=False)
    # i'm putting start and end times at both the item level and auction level
    # as live auctions have an ordered list of items to go through and the 
    # start time is when the lot comes up under the auctioneers hammer so is 
    # likely to be set at 'run' time
    start_time = UnixDateTimeField()
    end_time = UnixDateTimeField()
    starting_bid = models.FloatField(null=True, blank=True, default=None)
    current_bid = models.FloatField(null=True, blank=True, default=None)
    winning_bid = models.FloatField(null=True, blank=True, default=None)
    quantity = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# -----------------------------------------------------------------------------

class EnglishAuctionLot(AuctionLot): 
    start_price = models.FloatField(null=True, blank=True, default=None)
    reserve_price = models.FloatField(null=True, blank=True, default=None)
    min_increment = models.FloatField(null=True, blank=True, default=None)

# -----------------------------------------------------------------------------

class BuyNowAuctionLot(EnglishAuctionLot):
    buy_now_price = models.FloatField(null=True, blank=True, default=None)

# -----------------------------------------------------------------------------

