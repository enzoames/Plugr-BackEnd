# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from .models import *


# Create your tests here.


class ModelTestCase(TestCase):
    """Here we will write test the Turksystem Models"""

    def setUp(self):
        pass  #

    def TestCreateSystemDemand(self):
        pass


class ViewTestCase(TestCase):
    def setUp(self):
        pass

    def TestCreateSxystemDemand(self):
        pass
