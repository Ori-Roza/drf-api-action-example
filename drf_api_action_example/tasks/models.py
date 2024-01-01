from django.db import models


class Task(models.Model):
    assigned_by = models.CharField(max_length=32)
    notes = models.CharField(max_length=256)
