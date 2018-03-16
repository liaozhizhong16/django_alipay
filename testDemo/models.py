# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
class Alipay(models.Model):
	pay_ment_id = models.CharField(max_length=50,primary_key=True,unique=True)
	phone_number = models.CharField(max_length=15)
	amount = models.CharField(max_length=15)
	is_operate=models.CharField(max_length=5)
	pay_time=models.CharField(max_length=20)

# Create your models here.
