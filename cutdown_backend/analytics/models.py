from django import db
from django.db import models


class Browser(models.Model):
    name = models.CharField(max_length=50, default="unknown")
    version = models.CharField(max_length=10, default="unknown")
    created_at = models.DateTimeField(editable=False, auto_now_add=True)


class OS(models.Model):
    name = models.CharField(max_length=50, default="unknown")
    version = models.CharField(max_length=10, default="unknown")
    created_at = models.DateTimeField(editable=False, auto_now_add=True)


class Device(models.Model):
    name = models.CharField(max_length=50, default="unknown")
    created_at = models.DateTimeField(editable=False, auto_now_add=True)


# class Location(models.Model):


class ShortnerAnalytics(models.Model):
    browser = models.ForeignKey(Browser, on_delete=models.CASCADE)
    os = models.ForeignKey(OS, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
