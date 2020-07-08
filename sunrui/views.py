import time
from datetime import datetime
import pytz
import json

import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker

from sunrui.Crawler import GetDetail, GetPurchaseList

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Project, Record


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def line2d(data):
    amounts = []
    intervals = []
    for record in data:
        amounts.append("{:.2f}".format(float(record["total"])))
        t = time.strftime('%H:%M', time.localtime(int(record["timestamp"])))
        intervals.append(t)
    c = (
        Line()
        .add_xaxis(intervals)
        .add_yaxis("SunRui", amounts)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")]
        )
    )
    return c


def index(request):
    # print(GetDetail(5320))
    # print(GetPurchaseList(5320))
    proj = GetDetail(5126)
    proj2 = GetDetail(5765)

    try:
        project = Project.objects.get(project_id=proj.pro_id)
    except ObjectDoesNotExist:
        project = Project()

    try:
        project2 = Project.objects.get(project_id=proj2.pro_id)
    except ObjectDoesNotExist:
        project2 = Project()

    project.project_id = proj.pro_id
    project.project_title = proj.title
    project.current_funding = proj.current
    project.sold_num = proj.support_num
    timezone = pytz.timezone("Asia/Shanghai")
    project.start_date = datetime.fromtimestamp(proj.starttime, timezone)
    project.end_date = datetime.fromtimestamp(proj.endtime, timezone)
    project.save()
    starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.starttime))
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.endtime))

    project2.project_id = proj2.pro_id
    project2.project_title = proj2.title
    project2.current_funding = proj.current
    project2.sold_num = proj2.support_num
    timezone = pytz.timezone("Asia/Shanghai")
    project2.start_date = datetime.fromtimestamp(proj2.starttime, timezone)
    project2.end_date = datetime.fromtimestamp(proj2.endtime, timezone)
    project2.save()
    starttime2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.starttime))
    endtime2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proj.endtime))

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = list()
    with open("sunrui/sunrui102.md") as f:
        for line in f:
            record = json.loads(line)
            data.append(record)

    l2d = line2d(data)
    context = dict(
        myechart=l2d.render_embed(),
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
