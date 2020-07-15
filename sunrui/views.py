import time
from datetime import datetime
import pytz
import json

import pyecharts.options as opts
from pyecharts.charts import Line, Pie, Bar

from sunrui.Crawler import GetDetail, GetRecords, GetAllProjects

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Project, SaleRecord, UserRecord


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def index(request):
    # print(GetDetail(5320))

    proj = GetDetail(5126)
    proj2 = GetDetail(5765)
    proj3 = GetDetail(5952)

    # project = update(proj)
    # project2 = update(proj2)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.starttime))
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.endtime))

    starttime2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj2.starttime))
    endtime2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj2.endtime))

    starttime3 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj3.starttime))
    endtime3 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj3.endtime))

    data = list()
    with open("sunrui/sunrui0627.md") as f:
        for line in f:
            record = json.loads(line)
            data.append(record)

    data2 = list()
    with open("sunrui/sunrui0708.md") as f:
        for line in f:
            record = json.loads(line)
            data2.append(record)

    data3 = list()
    with open("sunrui/sunrui0712.md") as f:
        for line in f:
            record = json.loads(line)
            data3.append(record)

    # data = project.record_list.all()
    # data2 = project2.record_list.all()
    # data2 = GetRecords(5765)

    l2d = line2d(data, data2, data3)

    distribution2 = {'>1000': 125, '501-1000': 80, '101-500': 615, '51-101': 1317, '11-50': 3079, '<10': 6923}
    distribution = {'>1000': 86, '501-1000': 160, '101-500': 844, '51-101': 1691, '11-50': 4392, '<10': 8168}
    distribution3 = {'>1000': 124, '501-1000': 95, '101-500': 622, '51-101': 1160, '11-50': 2761, '<10': 6044}

    p2d = pie2d(distribution.keys(), distribution2.values(), "SunRui0708")
    p2d_6 = pie2d(distribution.keys(), distribution.values(), "SunRui0627")
    p2d_12 = pie2d(distribution.keys(), distribution3.values(), "SunRui0712")

    b2d = bar2d(distribution.keys(), distribution.values(), distribution2.values(), distribution3.values())

    context = dict(
        myechart_line=l2d.render_embed(),
        myechart_pie=p2d.render_embed(),
        myechart_pie_6=p2d_6.render_embed(),
        myechart_pie_12=p2d_12.render_embed(),
        myechart_bar=b2d.render_embed(),
        host=REMOTE_HOST,
        current_time=current_time,
        project=proj,
        project2=proj2,
        project3=proj3,
        starttime=starttime,
        endtime=endtime,
        starttime2=starttime2,
        endtime2=endtime2,
        starttime3=starttime3,
        endtime3=endtime3
    )
    return render(request, 'sunrui/index.html', context)


def line2d(data, data2, data3):
    amounts = []
    amounts2 = []
    amounts3 = []
    intervals = []
    for record in data:
        amounts.append("{:.2f}".format(float(record["total"])))
        t = time.strftime('%H:%M', time.localtime(int(record["timestamp"])))
        intervals.append(t)
    if data2:
        for record in data2:
            amounts2.append("{:.2f}".format(float(record["total"])))
    if data3:
        for record in data3:
            amounts3.append("{:.2f}".format(float(record["total"])))
    c = (
        Line()
        .add_xaxis(intervals)
        .add_yaxis("SunRui0627", amounts)
        .add_yaxis("SunRui0708", amounts2)
        .add_yaxis("SunRui0712", amounts3)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")]
        )
    )
    return c


def pie2d(options, values, title):
    c = (
        Pie()
        .add("", [list(z) for z in zip(options, values)])
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def bar2d(options, values1, values2, values3):
    c = (
        Bar()
        .add_xaxis(list(options))
        .add_yaxis("SunRui0627", list(values1))
        .add_yaxis("SunRui0708", list(values2))
        .add_yaxis("SunRui0712", list(values3))
        .set_global_opts(title_opts=opts.TitleOpts(title="", subtitle=""))
    )
    return c


def birthday(request):
    return render(request, 'sunrui/birthday.html')


def riceranking(request):
    projects = GetAllProjects('孙芮')
    project_list = []
    for proj in projects:
        p = updateProject(proj)
        project_list.append(p)
    context = dict(
        project_list=project_list,
    )
    return render(request, 'sunrui/riceranking.html', context)


def updateProject(proj):
    need_update = True
    try:
        project = Project.objects.get(project_id=proj['id'])
        if project.is_expire:
            need_update = False
    except ObjectDoesNotExist:
        project = Project()

    if need_update:
        project.project_id = proj['id']
        project.project_title = proj['title']
        project.project_nickname = proj['nickname']
        project.current_amount = float(proj['money'])
        project.sold = int(proj['value'])
        project.start_str = proj['start']
        project.end_str = proj['expire']
        # project.is_progress = proj['isprogress']=='0'
        project.is_expire = proj['isexpire']=='1'
        project.save()

    return project
