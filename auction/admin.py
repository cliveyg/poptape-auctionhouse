# auction/admin.py
from django.contrib import admin
from auction.models import Auction

admin.site.register(Auction)

class FlatPageAdmin(admin.ModelAdmin):
    fields = ('auction_id', 'owner', 'items', 'type'
              'start_time', 'end_time', 'status', 'active',
              'created', 'modified')
