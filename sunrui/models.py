import time

from django.db import models


class Project(models.Model):
    project_id = models.CharField(max_length=200)
    project_title = models.CharField(max_length=200)
    project_nickname = models.CharField(max_length=200)
    target_amount = models.FloatField(default=0)
    current_amount = models.FloatField(default=0)
    sold = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    num_participants = models.IntegerField(default=0)
    start_str = models.CharField(max_length=200, default='')
    end_str = models.CharField(max_length=200, default='')
    start_time = models.DateTimeField('time started', null=True)
    end_time = models.DateTimeField('time ended', null=True)
    # is_progress = models.BooleanField(default=False)
    is_expire = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        status = '进行中'
        if self.is_expire:
            status = '已结束'
        profiles = '项目ID:' + str(self.project_id) + '\n'
        profiles += '项目名称:' + str(self.project_title) + '\n'
        profiles += '当前金额:' + str(self.current_amount) + '\n'
        profiles += '销售件数:' + str(self.sold) + '\n'
        profiles += '开始日期:' + str(self.start_str) + '\n'
        profiles += '结束日期:' + str(self.end_str) + '\n'
        profiles += '状态:' + status
        return profiles


class SaleRecord(models.Model):
    project = models.ForeignKey(Project, related_name='sale_list', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200)
    user_nickname = models.CharField(max_length=200)
    amount = models.FloatField(default=0)
    record_time = models.DateTimeField('record time', null=True)

    class Meta:
        verbose_name = 'Sale Record'
        verbose_name_plural = 'Sale Records'


class UserRecord(models.Model):
    project = models.ForeignKey(Project, related_name='user_list', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200)
    user_nickname = models.CharField(max_length=200)
    amount = models.FloatField(default=0)

    class Meta:
        verbose_name = 'User Record'
        verbose_name_plural = 'User Records'
