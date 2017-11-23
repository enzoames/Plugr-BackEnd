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

# ========================================================================================================================
# ========================================================================================================================
# ==================================================== ROHAN =============================================================
# ========================================================================================================================
# ========================================================================================================================

class SystemDemand(models.Model):
    NONE = "None"
    POSTED = "Posted"
    DELIVERED = "Delivered"
    TIMED_OUT = "Timed-out"
    STATUS = "Inprogress"
    CANCELED = "Canceled"

    status_list = ((POSTED, "Posted"),
               (DELIVERED, "Delivered"),
               (TIMED_OUT, "Timed-out"),
               (STATUS, "Inprogress"),
               (CANCELED, "Canceled"),
               (NONE, "None"))

    title = models.CharField(max_length=20, blank=True, null=True, verbose_name="Title")
    precondition = models.TextField(blank=True, null=True, verbose_name="Precondition")
    postcondition = models.TextField(blank=True, null=True, verbose_name="Postcondition")
    description = models.TextField(blank=True, null=True, verbose_name="description")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Deadline")
    reward = models.IntegerField(default=0, verbose_name="Reward")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    client = models.ForeignKey(TurkUser, blank=True, null=True)
    status = models.CharField(max_length=10, choices=status_list, default=NONE)

    # NOTE:::
    # cant reference bid table and bid table reference system demand simultaniously | logically incorrent, causes loop
    # winning_bid = models.ForeignKey(Bid,blank=True,null = True) 

    def __str__(self):
        return str(self.title) + "        [ " + str(self.status) + " ]"

class Bid(models.Model):
    bid_created = models.DateTimeField(auto_now_add=True, verbose_name="Bid Created" )
    price = models.IntegerField(default=0, verbose_name="Price")
    developer = models.ForeignKey(TurkUser, blank=True, null=True, verbose_name="Developer")
    systemdemand = models.ForeignKey(SystemDemand, blank=True, null=True, verbose_name="System Demand")
    is_chosen = models.BooleanField(default=False, verbose_name="Chosen?")

    def __str__(self):
        return str(self.id)


# ========================================================================================================================
# ========================================================================================================================
# ==================================================== SAMMIE ============================================================
# ========================================================================================================================
# ========================================================================================================================


















# ========================================================================================================================
# ========================================================================================================================
# ================================================ ENZO ==================================================================
# ========================================================================================================================
# ========================================================================================================================



class BlackList(models.Model):
    user = models.ForeignKey(TurkUser, verbose_name="User", blank=True, null=True)
    reason = models.TextField(verbose_name="Reason", blank=True, null=True)
    blacklisted_date = models.DateTimeField(auto_now_add=True, verbose_name="Blacklisted Date")


















