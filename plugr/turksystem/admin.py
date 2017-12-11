# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


# Register your model

class TurkUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lastname', 'email', 'credential', 'accepted', 'pending', 'warning', 'warning_count',
                    'rating', 'money', 'completed_projects','aveRating_every5']


admin.site.register(TurkUser, TurkUserAdmin)


class SystemDemandAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'precondition', 'postcondition', 'description', 'deadline','failed','reward', 'created_at',
                    'client', 'status']


admin.site.register(SystemDemand, SystemDemandAdmin)


class BidAdmin(admin.ModelAdmin):
    list_display = ['id', 'bid_created', 'price', 'developer', 'systemdemand', 'is_chosen']


admin.site.register(Bid, BidAdmin)


class BlackListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'reason', 'blacklisted_date']


admin.site.register(BlackList, BlackListAdmin)


class ChosenDeveloperAdmin(admin.ModelAdmin):
    list_display = ['id', 'result', 'developer', 'cli_rating','sysdemand','system_rating','client_note', 'is_completed','front_fee', 'delivered_at']


admin.site.register(ChosenDeveloper, ChosenDeveloperAdmin)


class SUmessagesAdmin(admin.ModelAdmin):
    list_display = ['sender','complaint']

admin.site.register(SUmessages,SUmessagesAdmin)