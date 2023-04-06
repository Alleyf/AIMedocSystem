import os
import json

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
# from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page

from ..models import MeDocs  # 位置不能放错，否则报错
from ..utils.query import query_elastics_fulltext
from ..utils.wordCloud import get_word_cloud
from py2neo import *


@gzip_page
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
    # print(type(request.session['info']), request.session['info'])
    if 'keyword' in request.session['info']:
        keyword = request.session['info']['keyword']
        status, doc_name, content = query_elastics_fulltext(key=keyword)
        if status:
            if not os.path.exists(base_path + doc_name + '.png'):
                get_word_cloud(doc_name=doc_name, content=content)
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


@gzip_page
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
    # print(data2)
    res = {
        'status': True,
        'data1': data1,
        'data2': data2
    }
    return JsonResponse(res)


@gzip_page
def chart_pie(request):
    """饼状图数据接口"""
    queryset = MeDocs.objects.all()
    data = {}
    for item in queryset:
        # if item.user.username in data.keys():
        #     data[item.user.username] += 1
        # else:
        #     data[item.user.username] = 1
        if item.category in data.keys():
            data[item.category] += 1
        else:
            data[item.category] = 1
    # print(data)
    # data_list = [
    #     {"value": 1048, "name": '研发部'},
    #     {"value": 735, "name": '后勤部'},
    #     {"value": 580, "name": '运营部'},
    #     {"value": 484, "name": '销售部'},
    #     {"value": 300, "name": '售后部'}
    # ]
    res = {
        'status': True,
        'data': data
    }
    return JsonResponse(res)


@gzip_page
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


# 连接数据库
def medicine_search_all():
    graph = Graph('http://47.120.0.133:7474/', auth=("neo4j", "password"))
    # 定义data数组，存放节点信息
    data = []
    # 定义关系数组，存放节点间的关系
    links = []
    # 查询所有节点，并将节点信息取出存放在data数组中
    for n in graph.nodes:
        # 将节点信息转化为json格式，否则中文会不显示
        # print(n)
        nodesStr = json.dumps(graph.nodes[n], ensure_ascii=False)
        # 取出节点的name
        node_name = json.loads(nodesStr)['name']

        # 构造字典，存储单个节点信息
        dict = {
            # 'id':str(n), # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': '对象'
        }
        # 将单个节点信息存放在data数组中
        data.append(dict)
    # 查询所有关系，并将所有的关系信息存放在links数组中
    rps = graph.relationships
    for r in rps:
        # 取出开始节点的name
        source = str(rps[r].start_node['name'])
        # for i in data: #需要使用ID
        #     if source == i['name']:
        #         source = i['id']
        # 取出结束节点的name
        target = str(rps[r].end_node['name'])
        # for i in data: #需要使用ID
        #     if target == i['name']:
        #         target = i['id']
        # 取出开始节点的结束节点之间的关系
        name = str(type(rps[r]).__name__)
        # 构造字典存储单个关系信息
        dict = {
            'source': source,
            'target': target,
            'name': name
        }
        # 将单个关系信息存放进links数组中
        links.append(dict)
    # 输出所有节点信息
    # for item in data:
    #     print(item)
    # 输出所有关系信息
    # for item in links:
    #     print(item)
    # 将所有的节点信息和关系信息存放在一个字典中
    neo4j_data = {
        'data': data,
        'links': links
    }
    neo4j_data = json.dumps(neo4j_data)
    return neo4j_data


# @csrf_exempt
def medicine_search_all_category():
    """医学知识图谱"""
    graph = Graph('http://47.120.0.133:7474/', auth=("neo4j", "password"))
    data = []  # 定义data数组，存放节点信息
    links = []  # 定义关系数组，存放节点间的关系
    # 节点分类
    node_Disease = graph.run('MATCH (n:Disease) RETURN n').data()
    node_Check = graph.run('MATCH (n:Check) RETURN n').data()
    node_Department = graph.run('MATCH (n:Department) RETURN n').data()
    node_Drug = graph.run('MATCH (n:Drug) RETURN n').data()
    node_Food = graph.run('MATCH (n:Food) RETURN n').data()
    node_Producer = graph.run('MATCH (n:Producer) RETURN n').data()
    node_Symptom = graph.run('MATCH (n:Symptom) RETURN n').data()

    for n in node_Disease:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Disease'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中
    for n in node_Check:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Check'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中
    for n in node_Department:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Department'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中
    for n in node_Drug:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Drug'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中
    for n in node_Food:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Food'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中
    for n in node_Producer:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Producer'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中
    for n in node_Symptom:
        nodesStr = json.dumps(n, ensure_ascii=False)  # 将节点信息转化为json格式，否则中文会不显示
        node_name = json.loads(nodesStr)
        node_name = node_name['n']['name']  # 取出节点的name
        # print(node_name)
        dict = {
            'id': str(n),  # 防止重复节点
            'name': node_name,
            'symbolSize': 50,
            'category': 'Symptom'
        }
        data.append(dict)  # 将单个节点信息存放在data数组中

    # 查询所有关系，并将所有的关系信息存放在links数组中
    rps = graph.relationships
    for r in rps:
        source = str(rps[r].start_node['name'])  # 取出开始节点的name
        target = str(rps[r].end_node['name'])
        name = str(type(rps[r]).__name__)  # 取出开始节点的结束节点之间的关系
        # 构造字典存储单个关系信息
        dict = {
            'source': source,
            'target': target,
            'name': name
        }
        links.append(dict)  # 将单个关系信息存放进links数组中
    neo4j_data = {
        'data': data,
        'links': links
    }
    neo4j_data = json.dumps(neo4j_data)
    return neo4j_data


def medicine_search_one(value="百日咳"):
    graph = Graph('http://47.120.0.133:7474/', auth=("neo4j", "password"))
    # 定义data数组存储节点信息
    rel_label = ['Disease', 'Check', 'Department', 'Drug', 'Food', 'Producer', 'Symptom']
    data = []
    # 定义links数组存储关系信息
    links = []
    # 查询节点是否存在
    node = graph.run('MATCH(n:Disease{name:"' + value + '"}) return n').data()
    # print(node)
    # 如果节点存在len(node)的值为1不存在的话len(node)的值为0
    if len(node):
        # 如果该节点存在将该节点存入data数组中
        # 构造字典存放节点信息
        dict = {
            # 'id': str(n),  # 防止重复节点
            'name': value,
            'symbolSize': 50,
            'category': 'Disease'
        }
        data.append(dict)
        # 查询与该节点有关的节点，无向，步长为1，并返回这些节点
        for rel in rel_label:
            nodes = graph.run('MATCH(n:Disease{name:"' + value + '"})<-->(m:' + rel + ') return m').data()
            # 处理节点信息
            for n in nodes:
                # 将节点信息的格式转化为json
                node = json.dumps(n, ensure_ascii=False)
                node = json.loads(node)
                # 取出节点信息中person的name
                name = str(node['m']['name'])
                # print(name)
                # 构造字典存放单个节点信息
                dict = {
                    # 'id': str(n),  # 防止重复节点
                    'id': name,  # 防止重复节点
                    'name': name,
                    'symbolSize': 50,
                    'category': rel
                }
                # 将单个节点信息存储进data数组中
                data.append(dict)
        # 处理relationship
        for rel in rel_label:
            # 查询该节点所涉及的所有relationship，无向，步长为1，并返回这些relationship
            reps = graph.run('MATCH(n:Disease{name:"' + value + '"})<-[rel]->(m:' + rel + ') return rel').data()
            for r in reps:
                source = str(r['rel'].start_node['name'])
                target = str(r['rel'].end_node['name'])
                name = str(type(r['rel']).__name__)
                # print(name, str(reps.index(r)), str(r))
                dict = {
                    'id': str(r),  # 防止重复节点
                    # 'id': name,  # 防止重复节点
                    'source': source,
                    'target': target,
                    'name': name
                }
                links.append(dict)
        # 构造字典存储data和links
        res = {
            'status': 200,
            'data': data,
            'links': links,
            'error': '成功找到\"' + value + "\"疾病"
        }
    else:
        # print("查无此人")
        if value:
            error = value + ",疾病不存在,返回默认节点"
        else:
            error = "当前输入为空，请重新搜索,返回默认节点"
        res = {
            'status': 404,
            'error': error
        }
    res = json.dumps(res)
    return res
    # return JsonResponse(res)


@csrf_exempt
# @cache_page(60 * 30)
def index(request):
    cache_data = cache.get('neo4j_default_data')
    # print(type(cache_data))
    if request.method == 'POST':
        # 接收前端传过来的查询值
        node_name = request.POST.get('disease_node')
        cache_search_data = cache.get('neo4j_' + node_name)
        # print(node_name, cache_search_data)
        # print(cache_data, type(cache_data))
        if not cache_search_data:
            # print(node_name)
            # 查询结果
            search_neo4j_data = medicine_search_one(value=node_name)
            cache.set('neo4j_' + node_name, search_neo4j_data, 60 * 60 * 24 * 7)
            cache_search_data = cache.get('neo4j_' + node_name)
            # print(json.loads(search_neo4j_data)['error'])

            # 未查询到该节点
            if json.loads(cache_search_data)['status'] == 404:
                # print(json.loads(search_neo4j_data)['error'])
                # return redirect('/chart/graph/')
                # ctx = {'title': '数据库中暂未添加该实体'}
                # neo4j_data = medicine_search_all_category()
                # neo4j_data = medicine_search_one()
                return render(request, "medicine_graph.html",
                              {'neo4j_data': cache_data, 'ctx': json.loads(search_neo4j_data)['error']})
            # 查询到了该节点
            else:
                # neo4j_data = medicine_search_all_category()
                return render(request, 'medicine_graph.html',
                              {'neo4j_data': cache_search_data, 'ctx': json.loads(cache_search_data)['error']})
        else:
            if json.loads(cache_search_data)['status'] == 404:
                return render(request, 'medicine_graph.html',
                              {'neo4j_data': cache_data, 'ctx': json.loads(cache_search_data)['error']})
            else:
                return render(request, 'medicine_graph.html',
                              {'neo4j_data': cache_search_data, 'ctx': json.loads(cache_search_data)['error']})
    if not cache_data:
        # if cache_data:
        neo4j_data = medicine_search_one()
        cache.set('neo4j_default_data', neo4j_data, 60 * 60 * 24 * 7)
        cache_data = cache.get('neo4j_data')
        # print(cache_data, type(cache_data))
    # print(type(cache_data))
    return render(request, 'medicine_graph.html', {'neo4j_data': cache_data, 'ctx': json.loads(cache_data)['error']})
    # return render(request, 'medicine_graph.html', {'neo4j_data': neo4j_data, 'ctx': json.loads(neo4j_data)['error']})
