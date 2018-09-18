# coding=utf-8
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone
#内存信息
class memory_info(models.Model):
	minion_id = models.CharField(max_length=20,null=False)
	memory_total = models.IntegerField(default=0)
	memory_used = models.IntegerField(default=0)
	memory_free = models.IntegerField(default=0)
	memory_share = models.IntegerField(default=0)
	memory_bu_ca = models.IntegerField(default=0)
	memory_available = models.IntegerField(default=0)
	memory_time = models.DateTimeField(default=timezone.now)

#网络流量监控
class network_info(models.Model):
	minion_id = models.CharField(max_length=20,null=False)
	network_key = models.CharField(max_length=20,null=False)
	network_in = models.IntegerField(default=0)
	network_out = models.IntegerField(default=0)
	network_time = models.DateTimeField(default=timezone.now)

#监控内容
#基本监控0，服务监控1
class monitor_info(models.Model):
	monitor_name = models.CharField(max_length=20,null=False)
	monitor_type = models.IntegerField(default=0)
	monitor_description = models.CharField(max_length=50,null=False)
# Create your models here.
