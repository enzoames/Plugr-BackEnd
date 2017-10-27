# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from photologue.models import Photo
from django.db import models

# Create your models here.

class EnzoGallery(models.Model):
	gallery_name = models.CharField(max_length=120, verbose_name="Gallery Name", blank=True, null=True)
	photo = models.ForeignKey(Photo, related_name="enzo_photo", verbose_name="Photo", blank=True, null=True)
	photo_name = models.CharField(max_length=120, verbose_name="Photo Name", blank=True, null=True)
	photo_description = models.TextField(verbose_name="Photo Description", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
	orientation = models.CharField(max_length=15, verbose_name="Orientation", help_text="Horizontal or Vertical?", blank=True, null=True)

	def __unicode__(self):
		return self.gallery_name


class ContactEnzoAmes(models.Model):
	firstname = models.CharField(max_length=120, verbose_name="First Name", blank=True, null=True)
	lastname = models.CharField(max_length=120, verbose_name="Last Name", blank=True, null=True)
	company = models.CharField(max_length=120, verbose_name="Company", blank=True, null=True)
	email = models.CharField(max_length=120, verbose_name="email", blank=True, null=True)
	message = models.TextField(verbose_name="Message", blank=True, null=True)
	datesent = models.DateTimeField(auto_now_add=True, verbose_name="Date")