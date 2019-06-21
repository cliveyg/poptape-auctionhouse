from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_unixdatetimefield import UnixDateTimeField
from djmoney.models.fields import MoneyField

from auctionhouse.validators import validate_currency, validate_uuid_from_model

# -----------------------------------------------------------------------------
# a u c t i o n    m o d e l s
# -----------------------------------------------------------------------------
# i've made the design decision that an item can appear in more than one auction
# and have different prices in different auctions - i'm not 100% sure of this. 
# it may be better to make items unique to an auction with only one price. 
# an item can only be in one live auction at a time. probably revisit. 

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
    items = ArrayField(models.CharField(max_length=36, 
                                        blank=False, null=False,
                                        validators=[validate_uuid_from_model]),
                       size=500)
    type = models.CharField(max_length=15, 
                            choices=AuctionType.AUCTION_CHOICES) 
    start_time = UnixDateTimeField()
    end_time = UnixDateTimeField()
    status = models.CharField(max_length=20, blank=False)
    active = models.BooleanField(default=True)

# -----------------------------------------------------------------------------

class AuctionLot(models.Model):
    item_id = models.CharField(max_length=36, blank=False, unique=True, 
                               validators=[validate_uuid_from_model])
    lot_status = models.CharField(max_length=20, blank=False)
    lot_active = models.BooleanField(default=True)
    # i'm putting start and end times at both the item level and auction level
    # as live auctions have an ordered list of items to go through and the 
    # start time is when the lot comes up under the auctioneers hammer so is 
    # likely to be set at 'run' time
    lot_start_time = UnixDateTimeField()
    lot_end_time = UnixDateTimeField()
    winning_bid = MoneyField(max_digits=19, 
                             decimal_places=4, 
                             null=True, 
                             default_currency=None) 
    # not sure i need currency field if using MoneyField
    currency = models.CharField(max_length=3, blank=False,
                                validators=[validate_currency]) 
    quantity = models.IntegerField(default=1)

# -----------------------------------------------------------------------------

class EnglishAuction(AuctionLot): 
    start_price = MoneyField(max_digits=19,
                             decimal_places=4,
                             null=True,
                             default_currency=None) 
    reserve_price = MoneyField(max_digits=19,
                               decimal_places=4,
                               null=True,
                               default_currency=None)
    min_increment = MoneyField(max_digits=19,
                               decimal_places=4,
                               null=True,
                               default_currency=None)

# -----------------------------------------------------------------------------

class BuyNowAuction(EnglishAuction):
    buy_now_price = MoneyField(max_digits=19,
                               decimal_places=4,
                               null=True,
                               default_currency=None)

# -----------------------------------------------------------------------------

