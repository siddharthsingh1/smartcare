# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class patient_data(models.Model):
    patient_name = models.CharField(max_length=50)
    device_id = models.CharField(max_length=100 , unique=True)
    patient_email = models.EmailField(max_length=100)
    patient_age = models.IntegerField()
    patient_relatives = models.CharField(max_length=500 , default="")

class patient_medicines(models.Model):
    patient_device_id = models.CharField(max_length=100)
    medicines = models.CharField(max_length=500)
