from django.db import models


class Project(models.Model):
    project_id = models.CharField(max_length=200)
    project_title = models.CharField(max_length=200)
    project_nickname = models.CharField(max_length=200)
    fund = models.FloatField(default=0)
    amount_sold = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended')


class Chunk(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    chunk_fund = models.FloatField(default=0)
    time = models.DateTimeField('record time')

