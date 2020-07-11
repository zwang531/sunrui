import time
from datetime import datetime
import pytz
import json

import pyecharts.options as opts
from pyecharts.charts import Line, Pie, Bar

from sunrui.Crawler import GetDetail, GetRecords, GetPurchaseList

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Project, Record


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def update(proj):
    timezone = pytz.timezone("Asia/Shanghai")

    need_update = True
    try:
        project = Project.objects.get(project_id=proj.pro_id)
        if datetime.now(timezone) > datetime.fromtimestamp(proj.endtime, timezone):
            need_update = False
    except ObjectDoesNotExist:
        project = Project()

    if need_update:
        project.project_id = proj.pro_id
        project.project_title = proj.title
        project.current_funding = proj.current
        project.sold_num = proj.support_num
        project.start_date = datetime.fromtimestamp(proj.starttime, timezone)
        project.end_date = datetime.fromtimestamp(proj.endtime, timezone)
        project.save()

        records = GetRecords(proj.pro_id)
        for record in records:
            try:
                project.record_list.filter(time=datetime.fromtimestamp(record["timestamp"], timezone))
            except ObjectDoesNotExist:
                project.record_list.create(time=datetime.fromtimestamp(record["timestamp"], timezone),
                                           amount=record["total"])
    elif project.record_list.count() == 0:
        records = GetRecords(proj.pro_id)
        for record in records:
            try:
                project.record_list.filter(time=datetime.fromtimestamp(record["timestamp"], timezone))
            except ObjectDoesNotExist:
                project.record_list.create(time=datetime.fromtimestamp(record["timestamp"], timezone),
                                           amount=record["total"])

    return project


def index(request):
    # print(GetDetail(5320))

    proj = GetDetail(5126)
    proj2 = GetDetail(5765)

    # project = update(proj)
    # project2 = update(proj2)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.starttime))
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.endtime))

    starttime2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj2.starttime))
    endtime2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj2.endtime))

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

    # data = project.record_list.all()
    # data2 = project2.record_list.all()
    # data2 = GetRecords(5765)

    l2d = line2d(data, data2)

    distribution2 = {'>1000': 125, '501-1000': 80, '101-500': 615, '51-101': 1317, '11-50': 3079, '<10': 6923}
    distribution = {'>1000': 86, '501-1000': 160, '101-500': 844, '51-101': 1691, '11-50': 4392, '<10': 8168}

    p2d = pie2d(distribution.keys(), distribution2.values(), "SunRui0708")
    p2d_6 = pie2d(distribution.keys(), distribution.values(), "SunRui0627")

    b2d = bar2d(distribution.keys(), distribution.values(), distribution2.values())

    context = dict(
        myechart_line=l2d.render_embed(),
        myechart_pie=p2d.render_embed(),
        myechart_pie_6=p2d_6.render_embed(),
        myechart_bar=b2d.render_embed(),
        host=REMOTE_HOST,
        current_time=current_time,
        project=proj,
        project2=proj2,
        starttime=starttime,
        endtime=endtime,
        starttime2=starttime2,
        endtime2=endtime2
    )
    return render(request, 'sunrui/index.html', context)


def line2d(data, data2):
    amounts = []
    amounts2 = []
    intervals = []
    for record in data:
        amounts.append("{:.2f}".format(float(record["total"])))
        t = time.strftime('%H:%M', time.localtime(int(record["timestamp"])))
        intervals.append(t)
    if data2:
        for record in data2:
            amounts2.append("{:.2f}".format(float(record["total"])))
    c = (
        Line()
        .add_xaxis(intervals)
        .add_yaxis("SunRui0627", amounts)
        .add_yaxis("SunRui0708", amounts2)
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


def bar2d(options, values1, values2):
    c = (
        Bar()
        .add_xaxis(list(options))
        .add_yaxis("SunRui0627", list(values1))
        .add_yaxis("SunRui0708", list(values2))
        .set_global_opts(title_opts=opts.TitleOpts(title="", subtitle=""))
    )
    return c


def birthday(request):
    return render(request, 'sunrui/birthday.html')