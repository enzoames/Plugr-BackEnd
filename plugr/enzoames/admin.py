# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import Photo
from .models import *
# Register your models here.

class EnzoGalleryAdmin(admin.ModelAdmin):
	list_display = ['id', 'gallery_name', 'photo', 'photo_name', 'orientation', 'photo_description', 'created_at']

admin.site.register(EnzoGallery, EnzoGalleryAdmin)


class ContactEnzoAmesAdmin(admin.ModelAdmin):
	list_display = ['id', 'firstname', 'lastname', 'company', 'email', 'message', 'datesent']

admin.site.register(ContactEnzoAmes, ContactEnzoAmesAdmin)

