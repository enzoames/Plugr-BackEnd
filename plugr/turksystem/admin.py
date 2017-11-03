# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your model

class TurkUserAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'lastname', 'email', 'credential', 'accepted', 'pending', 'warning', 'warning_count', 'rating', 'money', 'completed_projects']

admin.site.register(TurkUser, TurkUserAdmin)

