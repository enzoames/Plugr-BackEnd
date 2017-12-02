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
    resume = models.TextField(verbose_name="Resume", blank=True, null=True)
    technical_skills = models.TextField(verbose_name="Technical Skills", blank=True, null=True)
    project_experience = models.TextField(verbose_name="Project Experience", blank=True, null=True)
    interests = models.TextField(verbose_name="Interests", blank=True, null=True)
    recent_work = models.TextField(verbose_name="Recent Work", blank=True, null=True)
    business_credential = models.TextField(verbose_name="Business Credential", blank=True, null=True)

    def __unicode__(self):
        return self.email or u''


# ========================================================================================================================
# ========================================================================================================================
# ==================================================== ROHAN =============================================================
# ========================================================================================================================
# ========================================================================================================================

class SystemDemand(models.Model):
    OPEN = "Open"
    CLOSED = "Closed"

    status_list = ((OPEN, "Open"),
                   (CLOSED, "Closed"))

    title = models.CharField(max_length=20, blank=True, null=True, verbose_name="Title")
    precondition = models.TextField(blank=True, null=True, verbose_name="Precondition")
    postcondition = models.TextField(blank=True, null=True, verbose_name="Postcondition")
    description = models.TextField(blank=True, null=True, verbose_name="description")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Deadline")
    reward = models.IntegerField(default=0, verbose_name="Reward")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    client = models.ForeignKey(TurkUser, blank=True, null=True)
    status = models.CharField(max_length=10, choices=status_list, default=OPEN)

    def __str__(self):
        return str(self.title) + "        [ " + str(self.status) + " ]"


class Bid(models.Model):
    bid_created = models.DateTimeField(auto_now_add=True, verbose_name="Bid Created")
    price = models.IntegerField(default=0, verbose_name="Price")
    developer = models.ForeignKey(TurkUser, blank=True, null=True, verbose_name="Developer")
    systemdemand = models.ForeignKey(SystemDemand, blank=True, null=True, verbose_name="System Demand")
    is_chosen = models.BooleanField(default=False, verbose_name="Chosen?")

    def __str__(self):
        return str(self.id)


class ChosenDeveloper(models.Model):
    """This model is to record Developers how have been choosen by clients"""
    result = models.TextField(blank=True, null=True, verbose_name="results")
    developer = models.ForeignKey(TurkUser, blank=True, null=True, related_name="developer")
    sysdemand = models.ForeignKey(SystemDemand, blank=True, null=True)
    is_completed = models.BooleanField(default=False, verbose_name="Completed?")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="delivered")
    front_fee = models.IntegerField(default=0, blank=True, null=True, verbose_name="front_fee")


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
