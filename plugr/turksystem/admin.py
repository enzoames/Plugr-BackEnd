# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


# Register your model

class TurkUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lastname', 'email', 'credential', 'accepted', 'pending', 'warning', 'warning_count',
                    'rating', 'money', 'completed_projects']


admin.site.register(TurkUser, TurkUserAdmin)


class SystemDemandAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'precondition', 'postcondition', 'description', 'deadline', 'reward', 'created_at',
                    'client', 'status']


admin.site.register(SystemDemand, SystemDemandAdmin)


class BidAdmin(admin.ModelAdmin):
    list_display = ['id', 'bid_created', 'price', 'developer', 'systemdemand', 'is_chosen']


admin.site.register(Bid, BidAdmin)


class BlackListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'reason', 'blacklisted_date']


admin.site.register(BlackList, BlackListAdmin)


class ChoosenDeveloperAdmin(admin.ModelAdmin):
    list_display = ['id', 'result', 'developer', 'client', 'sysdemand', 'is_completed', 'delivered']


admin.site.register(ChoosenDeveloper, ChoosenDeveloperAdmin)
