import json
import os
import time
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from haystack.views import SearchView
from django.views.decorators.gzip import gzip_page

from medocsys import models
from medocsys.utils import pagination, upload
from medocsys.utils.form import MeDocsModelForm, DocTxtModelForm, DocImgTxtModelForm
from medocsys.utils.upload import extract_img_info, extract_txt_info
from ..models import MeDocs
from ..utils.get_doc_title import get_pdf_title
from ..utils.query import query_elastics
from ..utils.search import spdfmkeyword, div_word
from ..utils.get_language_type import is_contains_chinese
from ..utils.wordCloud import get_word_cloud
from ..utils.zhiwang import get_zhiwang_data


# 一定要继承SearchView


# class MySearchView(SearchView):
#
#     # 重写人家的方法
#     def create_response(self):
#         # 人家的，就这样写，获取到的就是全部的东西
#         start = time.perf_counter()
#         context = self.get_context()
#         end = time.perf_counter()
#         print('-----------------------------------')
#         print("{}秒".format(end - start))
#         print('-----------------------------------')
#         data_list = []
#         #   context['page'].object_list   这样获取到的就是  数据的list集合
#         for sku in context['page'].object_list:
#             # 获取表里面的数据，就是前缀就是sku.object
#             # print(sku.object.status, sku.object.get_status_display())
#             data_list.append({
#                 'id': sku.object.id,
#                 'name': sku.object.name,
#                 'content': sku.object.content,
#                 'author': sku.object.author,
#                 'source': sku.object.get_source_display(),
#                 'relscore': sku.object.relscore,
#                 'clkscore': sku.object.clkscore,
#                 'fedbakscore': sku.object.fedbakscore,
#                 'allscore': sku.object.allscore,
#                 'status': sku.object.get_status_display(),
#                 'user': sku.object.user,
#             })
#         content = {}
#         if data_list:
#             content = {
#                 'status': True,
#                 'data': data_list,
#             }
#         else:
#             xw_list = MeDocs.objects.all()[0:1]
#             content = {
#                 'status': False,
#                 'data': xw_list,
#             }
#
#         # 渲染到我们自己写的页面
#         # return JsonResponse({"content": content}
#         print(content)
#         return render(self.request, 'doc_list_search.html', {"context": context, "content": content})

@gzip_page
def doc_list(request):
    form = MeDocsModelForm()
    # 1.搜索参数初始化
    search_dict = {}
    user_id = models.User.objects.filter(username=request.session['info']['name']).first().pk
    print(request.session['info']['name'], user_id)
    # 获取号码搜索参数
    search_data = request.GET.get(key="n", default='')
    if search_data:
        search_dict['name__contains'] = search_data
    search_dict['user_id__exact'] = user_id
    # 2.页码参数初始化
    pagesize = 10
    pageplus = 2
    # 3.筛选符合条件的数据
    queryset = models.MeDocs.objects.filter(**search_dict).order_by('-allscore')
    print(queryset)
    # print("{}秒".format(end - start))
    # 4.实例化页面对象
    page_obj = pagination.Pagination(request, query_set=queryset, page_size=pagesize, page_plus=pageplus)
    # 5.获取页面数据
    page_queryset = page_obj.page_queryset
    page_str = page_obj.htmlstr()
    context = {
        'form': form,
        #     页面数据信息
        'page_queryset': page_queryset,
        #     搜索参数
        'search_data': search_data,
        #     分页html字符串组件
        'page_str': page_str
    }
    # print(datetime.now().strftime('%Y%m%d%H%M%S'))
    return render(request, "doc_list.html", context)


@gzip_page
@csrf_exempt
def doc_add(request):
    """添加文档"""
    start = time.perf_counter()
    upload_info = []
    pop_doc = []
    fail_num = 0
    success_num = 0
    file_list = request.FILES.getlist("docfile")
    # print("可以上传的文档包括：" + str(file_list))
    if len(file_list) == 0:
        context = {
            'status': 402,
            'err': "上传文档为空"
        }
        return JsonResponse(context)
    upload_res = upload.upload_mul(file_list=file_list)
    for item in file_list:
        form = MeDocsModelForm(data=request.POST, files=None)
        # 设置文件名
        item.name = item.name.replace(" ", "_")
        # print(item, item.name)
        form.instance.name = item.name[:-4]
        form.instance.date = time.strftime("%Y-%m-%d", time.localtime())
        # 单独设置表单数据：将当前登录的用户作为该条信息的作者
        form.instance.user_id = request.session['info'].get("id")
        # 设置文档语言
        print("当前名字：" + form.instance.name)
        # tika获取文献标题
        # if is_contains_chinese(get_pdf_title(form.instance.name)):
        if is_contains_chinese(form.instance.name):
            form.instance.language = 1
        else:
            form.instance.language = 2
        if models.MeDocs.objects.filter(name=form.instance.name).exists():
            upload_info.append(form.instance.name + ':文档已存在,上传失败')
            pop_doc.append(file_list.index(item))
            fail_num += 1
            continue
        upload_info.append(form.instance.name + ',上传成功')
        success_num += 1
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
        if not form.is_valid():
            context = {
                'status': 403,
                'err': form.errors
            }
            return JsonResponse(context)
        # print(path)
        # for item in file_list:
        item.name = item.name[:-4].replace(" ", "_")
        txt_exist = models.DocTxt.objects.filter(doc_name=item.name).exists()
        img_txt_exist = models.DocImgTxt.objects.filter(doc_name=item.name).exists()
        # print(item.name, txt_exist, img_txt_exist)
        if txt_exist:
            upload_info.append(item.name + ':文本数据已存在,上传失败')
            pop_doc.append(file_list.index(item))
            fail_num += 1
            continue
        if img_txt_exist:
            upload_info.append(item.name + ':图片数据已存在,上传失败')
            pop_doc.append(file_list.index(item))
            fail_num += 1
            continue
        path = "./media/docs/" + item.name + ".pdf"
        txt_ls = extract_txt_info(url=path)
        img_txt_ls = extract_img_info(url=path, mul=False)
        # print(txt_ls, img_txt_ls, len(txt_ls))
        for index in range(len(txt_ls)):
            doc_txt_form = DocTxtModelForm(request.POST)
            page_id = index + 1
            doc_txt_form.instance.doc_name = item.name
            doc_txt_form.instance.page_id = page_id
            doc_txt_form.instance.txt_content = txt_ls[index]
            # print("成功写入文本内容")
            if doc_txt_form.is_valid():
                doc_txt_form.save()
            else:
                # print(doc_txt_form.errors)
                context = {
                    'status': 403,
                    'err': doc_txt_form.errors
                }
                return JsonResponse(context)
        if img_txt_ls:
            for txt_dict in img_txt_ls:
                doc_img_txt_form = DocImgTxtModelForm(request.POST)
                doc_img_txt_form.instance.doc_name = item.name
                doc_img_txt_form.instance.page_id = txt_dict['filepage']
                doc_img_txt_form.instance.img_content = txt_dict['content']
                doc_img_txt_form.instance.page_img_num = txt_dict['filepageimgnumber']
                # print("成功添加图片内容")
                if doc_img_txt_form.is_valid():
                    doc_img_txt_form.save()
                else:
                    # print(doc_img_txt_form.errors)
                    context = {
                        'status': 403,
                        'err': doc_img_txt_form.errors
                    }
                    return JsonResponse(context)
    end = time.perf_counter()
    cost_time = end - start
    context = {
        'status': 200,
        'info': upload_info,
        'cost_time': {
            'upload': "{}秒".format(upload_res[1]),
            'all': "{}秒".format(cost_time),
        },
        'upload_num': {
            'fail': fail_num,
            'success': success_num,
            'all': fail_num + success_num
        }
    }
    # return render(request, 'doc_list.html', context)
    return JsonResponse(context)


@gzip_page
def doc_del(request):
    uid = request.GET.get('uid')
    exist = models.MeDocs.objects.filter(id=uid).exists()
    if exist:
        obj = models.MeDocs.objects.filter(id=uid).first()
        content_obj = models.DocTxt.objects.filter(doc_name=obj.name).all()
        img_content_obj = models.DocImgTxt.objects.filter(doc_name=obj.name).all()
        url = "./media/docs/" + obj.name + ".pdf"
        # print(url, os.path.exists(url))
        if os.path.exists(url):
            os.remove(url)
        if content_obj:
            content_obj.delete()
        if img_content_obj:
            img_content_obj.delete()
        obj.delete()
        res = {
            'status': True,
        }
        return JsonResponse(res)
    res = {
        'status': False,
        'err': 'ID为' + uid + '的文件不存在,删除失败'
    }
    return JsonResponse(res)


@gzip_page
@csrf_exempt
def doc_edit(request):
    """编辑文献"""
    # 根据id获取文献信息
    uid = request.GET.get('uid')
    # 编辑文献
    rowobj = models.MeDocs.objects.filter(id=uid).first()
    if not rowobj:
        res = {
            'status': False,
            'tips': 'ID为' + uid + '的文件不存在,请刷新重试'
        }
        return JsonResponse(res)
    form = MeDocsModelForm(data=request.POST, instance=rowobj)
    if form.is_valid():
        form.save()
        res = {
            'status': True
        }
        return JsonResponse(res)
    context = {
        'status': False,
        'err': form.errors
    }
    return JsonResponse(context)


@gzip_page
def doc_edit_details(request):
    # 根据id获取文献信息
    uid = request.GET.get('uid')
    # 方法1获取对象
    # rowobj = models.MeDocs.objects.filter(id=uid).first()
    # if not rowobj:
    #     res = {
    #         'status': False,
    #         'err': 'ID为' + uid + '的文件不存在,打开失败'
    #     }
    #     return JsonResponse(res)
    # res = {
    #     'status': True,
    #     'data': {
    #         'name': rowobj.name,
    #         'author': rowobj.author,
    #         'clkscore': rowobj.clkscore,
    #         'fedbakscore': rowobj.fedbakscore,
    #         'status': rowobj.status,
    #         'user': rowobj.user.username
    #     }
    # }
    # return JsonResponse(res)
    # 方法2获取字典
    rowdic = models.MeDocs.objects.filter(id=uid).values('name', 'author', 'source').first()
    if not rowdic:
        res = {
            'status': False,
            'err': 'ID为' + uid + '的文件不存在,打开失败'
        }
        return JsonResponse(res)
    res = {
        'status': True,
        'data': rowdic
    }
    return JsonResponse(res)


@gzip_page
@csrf_exempt
def doc_view(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        rowobj = models.MeDocs.objects.filter(id=uid).first()
        docname = rowobj.name
        # print(docname)
        res = {
            'status': True,
            'docname': docname
        }
        # return render(request, 'pdfview.html', {'docname': docname})
        return JsonResponse(res)
    return render(request, 'pdfview.html')


@gzip_page
@csrf_exempt
def doc_details(request):
    """查看详情"""
    if request.method == 'GET':
        keyword = request.GET.get("text")
        uid = request.GET.get("uid")
        title = models.MeDocs.objects.filter(id=uid).first().name
        url = "./media/docs/" + title + '.pdf'
        # page_info = spdfmkeyword(url=url, keyword=keyword)
        page_info = query_elastics(key=keyword)
        new_page_info = []
        for item in page_info:
            if item['name'] == title:
                new_page_info.append(item)
        # 我们需要使用匿名函数，使用sort函数中的key这个参数，来指定字典比大小的方法
        new_page_info.sort(key=lambda x: x['page_id'])
        # print(new_page_info)
        key_page_info = {}
        facetnum = []
        for item_dict in new_page_info:
            page_abstract = []
            for nape in item_dict["fragments"]:
                abstract = {'abstract': nape, 'source': item_dict['source'], 'keyword': keyword}
                page_abstract.append(abstract)
            if item_dict["page_id"] not in key_page_info.keys():
                key_page_info[item_dict["page_id"]] = page_abstract
                facetnum.append(len(key_page_info[item_dict["page_id"]]))
            else:
                key_page_info[item_dict["page_id"]] += page_abstract
                # print("当前页码为：" + str(item_dict["page_id"]), len(facetnum))
                facetnum[len(facetnum) - 1] = len(key_page_info[item_dict["page_id"]])
        # title = get_pdf_title(title=title)
        page_info = {'total_page': len(key_page_info), 'key_page_info': key_page_info, 'id': uid, 'title': title,
                     'keyword': keyword, 'facet_num': facetnum}
        # print("总共项数为：" + str(facet_num))
        # print(len(page_info))
        return render(request, 'doc_detail.html', page_info)


@csrf_exempt
def doc_search(request):
    """异步检索"""
    if request.method == 'GET':
        return render(request, "doc_search.html")
    else:
        id_ls = []
        for i in range(len(request.POST)):
            id_ls.append(request.POST[str(i)])
        start = time.perf_counter()
        querysets = models.MeDocs.objects.filter(id__in=id_ls)
        end = time.perf_counter()
        # print("{}秒".format(end - start))
        # 2.页码参数初始化
        pagesize = 10
        pageplus = 2
        # 3.筛选符合条件的数据
        queryset = querysets
        # 4.实例化页面对象
        page_obj = pagination.Pagination(request, query_set=queryset, page_size=pagesize, page_plus=pageplus)
        # 5.获取页面数据
        page_queryset = page_obj.page_queryset
        page_str = page_obj.htmlstr()
        page_queryset = serializers.serialize("json", page_queryset)
        page_queryset = json.loads(page_queryset)
        i = 0
        for uid in id_ls:
            for index, item in enumerate(page_queryset):
                if str(item['pk']) == uid:
                    # temp = page_queryset[i]
                    page_queryset[i], page_queryset[index] = item, page_queryset[i]
                    # page_queryset[index] = temp
                    i += 1
                    break
        context = {
            #     页面数据信息
            'page_queryset': page_queryset,
            #     分页html字符串组件
            'page_str': page_str
        }
        return JsonResponse(context)
        # return render(request, "doc_search.html", context)
        # return redirect('/admin/list/')


@gzip_page
def doc_query(request):
    """同步检索"""
    if request.GET.get("keyword") is None:
        return render(request, "doc_query.html")
    keyword = request.GET.get("keyword")
    request.session['info']['keyword'] = keyword
    request.session.set_expiry(60 * 60 * 24 * 7)
    # print(request.session['info']['keyword'])
    page_info = query_elastics(keyword)
    if len(page_info) == 0:
        context = {
            'search_data': keyword,
            'page_info': page_info,
            'code': 404
        }
        # print(context['code'])
        return render(request, "doc_query.html", context)
    # print("{}秒".format(end - start))
    # print(page_info)
    for i, item in enumerate(page_info):
        # if i < len(page_info) - 1:
        repeate_ls = []
        rel_score = page_info[i]['rel_score']
        for j, _ in enumerate(page_info):
            # print(j)
            if i >= j:
                continue
            if page_info[i]['name'] == page_info[j]['name']:
                rel_score += page_info[j]['rel_score']
                repeate_ls.append(j)
                print("剔除了" + str(j) + page_info[i]['name'])
            continue
        n = 0
        for k in repeate_ls:
            k -= n
            page_info.pop(k)
            n += 1
        print("更新前的名字：" + page_info[i]['name'])
        page_info[i]['id'] = models.MeDocs.objects.filter(name=page_info[i]['name']).first().id
        # page_info[i]['name'] = get_pdf_title(page_info[i]['name'])
        print('更新后的名字：' + page_info[i]['name'])
        uid = page_info[i]['id']
        rel_score = round(rel_score, 2)
        models.MeDocs.objects.filter(id=uid).update(relscore=rel_score)
        page_info[i]['relscore'] = rel_score
        page_info[i]['fedbakscore'] = models.MeDocs.objects.filter(id=uid).first().fedbakscore
        page_info[i]['clkscore'] = models.MeDocs.objects.filter(id=uid).first().clkscore
        allscore = round(page_info[i]['fedbakscore'] + page_info[i]['clkscore'] + rel_score, 2)
        models.MeDocs.objects.filter(id=uid).update(allscore=allscore)
        page_info[i]['allscore'] = models.MeDocs.objects.filter(id=uid).first().allscore
    # 对文档结果按照总分进行排序
    page_info = sorted(page_info, key=lambda x: x['allscore'], reverse=True)
    for i, item in enumerate(page_info):
        item['num'] = i + 1
    context = {
        'search_data': keyword,
        'page_info': page_info,
        'code': 200
    }
    return render(request, "doc_query.html", context)
    # return redirect('/admin/list/')


@gzip_page
def doc_thumbup(request, nid):
    """
    点赞
    :param request: http请求
    :param nid: 文档id
    :return: 状态，id，反馈分数
    """
    allscore = 0
    for item in models.MeDocs.objects.all():
        feedbackscore = item.fedbakscore
        allscore += feedbackscore
    # print(allscore)
    fedbakscore = models.MeDocs.objects.filter(id=nid).first().fedbakscore
    fedbakscore = round(((fedbakscore + 1) / allscore) * 10, 2)
    models.MeDocs.objects.filter(id=nid).update(fedbakscore=fedbakscore)
    res = {
        'status': 200,
        'doc_id': nid,
        'fedbakscore': fedbakscore
    }
    return JsonResponse(res)


@gzip_page
def doc_thumbdown(request, nid):
    """
    点踩
    :param request: http请求
    :param nid: 文档id
    :return: 状态,id,反馈分数
    """
    allscore = 0
    for item in models.MeDocs.objects.all():
        feedbackscore = item.fedbakscore
        allscore += feedbackscore
    # print(allscore)
    fedbakscore = models.MeDocs.objects.filter(id=nid).first().fedbakscore
    if fedbakscore - 1 > 0:
        fedbakscore = round(((fedbakscore - 1) / allscore) * 10, 2)
    else:
        fedbakscore = 0
    models.MeDocs.objects.filter(id=nid).update(fedbakscore=fedbakscore)
    res = {
        'status': 200,
        'doc_id': nid,
        'fedbakscore': fedbakscore
    }
    return JsonResponse(res)


@gzip_page
def doc_clk(request, nid):
    """
    点击接口
    :param request: http请求
    :param nid: 文档id
    :return: 状态，id，点击分数
    """
    allscore = 0
    for item in models.MeDocs.objects.all():
        clkscore = item.clkscore
        allscore += clkscore
    clkscore = models.MeDocs.objects.filter(id=nid).first().clkscore
    clkscore = round(((clkscore + 1) / allscore) * 30, 2)
    # print("总分为" + str(allscore) + "点击后的分：" + str(clkscore))
    models.MeDocs.objects.filter(id=nid).update(clkscore=clkscore)
    res = {
        'status': 200,
        'doc_id': nid,
        'clkscore': clkscore
    }
    return JsonResponse(res)


@gzip_page
def doc_external(request):
    """
    获取知网数据接口
    :param request:
    :return: 知网数据（列表）
    """
    keywords = request.GET.get("keywords")
    start = int(request.GET.get("start"))
    end = int(request.GET.get("end"))
    data = ""
    while not data:
        data = get_zhiwang_data(keywords, start, end)
    res = {
        'status': 200,
        'data': data
    }
    return JsonResponse(res)
