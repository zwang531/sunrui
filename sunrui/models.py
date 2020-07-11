import time

from django.db import models


class Project(models.Model):
    project_id = models.CharField(max_length=200)
    project_title = models.CharField(max_length=200)
    project_nickname = models.CharField(max_length=200)
    target_funding = models.FloatField(default=0)
    current_funding = models.FloatField(default=0)
    sold_num = models.IntegerField(default=0)
    stock_num = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', null=True)
    start_date = models.DateTimeField('date started', null=True)
    end_date = models.DateTimeField('date ended', null=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Record(models.Model):
    project = models.ForeignKey(Project, related_name='record_list', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200)
    user_nickname = models.CharField(max_length=200)
    amount = models.FloatField(default=0)
    time = models.DateTimeField('record time', null=True)

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = 'Records'
