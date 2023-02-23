import os

from django.core.checks.security import csrf
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from medocsys.utils.upload import upload
from ..models import MeDocs
from ..utils.query import query_elastics_fulltext
from ..utils.wordCloud import get_word_cloud


def chart_list(request):
    """数据可视化页面"""
    queryset = MeDocs.objects.all().order_by('-clkscore')
    # print(queryset)
    # print(queryset[0], len(queryset))
    rank_ls = []
    ch = len(MeDocs.objects.filter(language=1))
    en = len(MeDocs.objects.filter(language=2))
    total = ch + en
    data_num = [total, ch, en]
    for index in range(len(queryset)):
        if index < 10:
            data_dict = {
                'name': queryset[index].name,
                'fedbakscore': queryset[index].fedbakscore,
                'clkscore': queryset[index].clkscore,
                'id': queryset[index].id
            }
            rank_ls.append(data_dict)

    # return JsonResponse(context)
    word_cloud_ls = []
    # word_cloud_path = ''
    base_path = './media/wordcloud/'
    keyword = request.session['info']['keyword']
    status, doc_name, content = query_elastics_fulltext(key=keyword)
    if status:
        if not os.path.exists(base_path + doc_name + '.png'):
            print(get_word_cloud(doc_name=doc_name, content=content))
    # if keyword:
    #     print("当前关键词为" + keyword)
    #     word_cloud_path, status = get_word_cloud(keyword=keyword)
    #     if not status:
    #         word_cloud_path = base_path[1:] + os.listdir(base_path)[0]
    # else:
    #     word_cloud_path = base_path[1:] + os.listdir(base_path)[0]
    for item in os.listdir(base_path):
        word_cloud_path = base_path[1:] + item
        doc_name = item[:-4]
        word_cloud_ls.append({'word_cloud_path': word_cloud_path, 'doc_name': doc_name})
    # print(word_cloud_ls)
    context = {
        'status': 200,
        'data': rank_ls,
        'num': data_num,
        'word_cloud_ls': word_cloud_ls,
    }
    # print(context)
    return render(request, "chart_list.html", context)


def chart_bar(request):
    """柱状图数据接口"""
    # 去数据库中获取数据
    # global series_list
    ch = len(MeDocs.objects.filter(language="1"))
    en = len(MeDocs.objects.filter(language="1"))
    total = ch + en
    data1 = [total, ch, en]
    queryset = MeDocs.objects.all()
    data2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for index in range(len(queryset)):
        # print(queryset[index].date, type(queryset[index].date))
        dt = queryset[index].date
        # dt_str = dt.strftime('%Y-%m-%d')  # 转换成字符串
        dt_int = int(dt.strftime('%m'))  # 转换成字符串
        data2[dt_int - 1] += 1
    print(data2)
    res = {
        'status': True,
        'data1': data1,
        'data2': data2
    }
    return JsonResponse(res)


def chart_pie(request):
    """饼状图数据接口"""
    queryset = MeDocs.objects.all()
    data = {}
    for item in queryset:
        if item.user.username in data.keys():
            data[item.user.username] += 1
        else:
            data[item.user.username] = 1
    print(data)
    data_list = [
        {"value": 1048, "name": '研发部'},
        {"value": 735, "name": '后勤部'},
        {"value": 580, "name": '运营部'},
        {"value": 484, "name": '销售部'},
        {"value": 300, "name": '售后部'}
    ]
    res = {
        'status': True,
        'data': data
    }
    return JsonResponse(res)


def chart_line(request):
    """折线图数据接口"""
    legend = ['alleyf', 'chuiyugin']
    series_list = [
        {
            "name": legend[0],
            "type": 'line',
            "stack": 'Total',
            "data": [3, 5, 4, 8, 6, 10, 5],
            "smooth": True
        },
        {
            "name": legend[1],
            "type": 'line',
            "stack": 'Total',
            "data": [2, 5, 9, 3, 8, 12, 6],
            "smooth": True
        }
    ]
    res = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list
        }
    }
    return JsonResponse(res)
