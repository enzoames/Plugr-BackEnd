# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# class TurkUserType(models.Model):
# 	usertype = models.CharField(max_length=120, verbose_name="User Type", blank=True, null=True)

# Create your models here.
class TurkUser(models.Model):
	name = models.CharField(max_length=120, verbose_name="Name", blank=True, null=True)
	lastname = models.CharField(max_length=120, verbose_name="Last Name", blank=True, null=True)
	email = models.CharField(max_length=120, verbose_name="Email", blank=True, null=True)
	password = models.CharField(max_length=120, verbose_name="Password", blank=True, null=True)
	# credential = models.ForeignKey(TurkUserType, verbose_name="Credential", blank=True, null=True)
	credential = models.CharField(max_length=120, verbose_name="User Type", blank=True, null=True)
	accepted = models.BooleanField(verbose_name="Accepted", default=False)
	pending = models.BooleanField(verbose_name="Pending", default=True)
	warning = models.BooleanField(verbose_name="Warning", default=False)
	warning_count = models.IntegerField(verbose_name="Warning Count", default=0)
	rating = models.IntegerField(verbose_name="Rating", default=0)
	message = models.TextField(verbose_name="Message", blank=True, null=True)
	money = models.IntegerField(verbose_name="Money", default=0)
	completed_projects = models.IntegerField(verbose_name="Completed Projects", default=0)

	def __unicode__(self):
		return self.email
