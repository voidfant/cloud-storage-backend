from django.db import models


class Element(models.Model):
    id = models.CharField('ID', max_length=200, primary_key=True)
    parentId = models.CharField('Parent ID', max_length=200, blank=True, null=True)
    url = models.CharField(max_length=255, unique=True, null=True, blank=True)
    type = models.CharField('Element type', max_length=6)
    date = models.CharField('Current date', max_length=26, blank=True)
    size = models.IntegerField('File size', null=True, blank=True)
