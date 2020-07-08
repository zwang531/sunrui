from django.db import models


class Project(models.Model):
    name = models.CharField(verbose_name="项目名称", max_length=200)
    contractor = models.CharField(verbose_name="合同方", max_length=200)
    create_date = models.DateField("创建时间")
    total_paid = models.FloatField(verbose_name="已收款", default=0)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.name

    def total_receivables(self):
        total_receivables = 0
        for sub_project in self.sub_projects.all():
            total_receivables += sub_project.receivables
        return total_receivables
    total_receivables.short_description = '应收款'

    # def total_paid(self):
    #     total_paid = 0
    #     for sub_project in self.sub_projects.all():
    #         total_paid += sub_project.paid
    #     return total_paid
    # total_paid.short_description = '已收款'

    def num_sub_projects(self):
        return len(self.sub_projects.all())
    num_sub_projects.short_description = '子项目数量'

    def status(self):
        status = '创建成功'
        started = False
        finished = True
        for sub_project in self.sub_projects.all():
            amount = sub_project.construction_amount
            started = started or sub_project.finished_amount > 0
            if sub_project.updated:
                amount += sub_project.updated_amount
            finished = finished and sub_project.finished_amount >= amount
        if started and finished:
            status = '施工完成'
            if self.total_paid >= self.total_receivables():
                status = '项目完成'
            # collected_all = True
            # collected = False
            # for sub_project in self.sub_projects.all():
            #     collected = collected or sub_project.paid > 0
            #     collected_all = collected_all and sub_project.paid >= sub_project.receivables
            # if collected and collected_all:
            #     status = '项目完成'
        elif started and not finished:
            status = '施工中'
        return status
    status.short_description = '状态'

    def status_color(self):
        status_color = 'blue'
        if self.status() == '施工中':
            status_color = 'orange'
        elif self.status() == '施工完成':
            status_color = 'green'
        elif self.status() == '项目完成':
            status_color = 'grey'
        return status_color

    def status_icon(self):
        status_icon = 'assignment'
        if self.status() == '施工中':
            status_icon = 'build'
        elif self.status() == '施工完成':
            status_icon = 'attach_money'
        elif self.status() == '项目完成':
            status_icon = 'check'
        return status_icon


class SubProject(models.Model):
    project_name = models.ForeignKey(Project, related_name='sub_projects', on_delete=models.CASCADE, verbose_name="所属项目")
    name = models.CharField(verbose_name="子项目名称", max_length=200)
    unit = models.CharField(verbose_name="单位", max_length=200)
    contract_amount = models.FloatField(verbose_name="合同数量")
    construction_amount = models.FloatField(verbose_name="施工图数量")
    updated = models.BooleanField(verbose_name="变改设计", default=False)
    updated_amount = models.FloatField(verbose_name="变改数量", default=0)
    finished_amount = models.FloatField(verbose_name="已完成数量", default=0)
    receivables = models.FloatField(verbose_name="应收款")
    # paid = models.FloatField(verbose_name="已收款", default=0)

    class Meta:
        verbose_name = '子项目'
        verbose_name_plural = '子项目'

    def __str__(self):
        return self.name
