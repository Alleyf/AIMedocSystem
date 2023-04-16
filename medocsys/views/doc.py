# import json
import os
import random
import re
import time

import jieba
import requests
# from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page

from medocsys import models
from medocsys.utils import pagination, upload
from medocsys.utils.form import MeDocsModelForm, DocTxtModelForm, DocImgTxtModelForm
from medocsys.utils.upload import extract_img_info, extract_txt_info
from ..utils.del_img import del_img
from ..utils.doc_get_category import get_category
from ..utils.get_doc_title import get_doc_title
from ..utils.get_language_type import is_contains_chinese
from ..utils.learn_doc import get_keyinfo
from ..utils.query import query_elastics
from ..utils.zhiwang import get_zhiwang_data


@gzip_page
def doc_list(request):
    form = MeDocsModelForm()
    # 1.搜索参数初始化
    search_dict = {}
    user_id = models.User.objects.filter(username=request.session['info']['name']).first().pk
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
    # print(queryset)
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
    return render(request, "doc_list.html", context)


@gzip_page
@csrf_exempt
def doc_add(request):
    """添加文档"""
    # start = time.perf_counter()
    context = {
        'status': 500,
        'err': "内部服务出错"
    }
    try:
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
            # print(item)
            form.instance.name = item.name[:-4]
            form.instance.date = time.strftime("%Y-%m-%d", time.localtime())
            # 单独设置表单数据：将当前登录的用户作为该条信息的作者
            form.instance.user_id = request.session['info'].get("id")
            form.instance.cover = form.instance.name + ".png"
            # 设置文档语言
            # print("当前名字：" + form.instance.name)
            # tika获取文献标题
            doc_title = get_doc_title(doc_name=form.instance.name)
            # item.name = doc_title
            # print(item.name, doc_title)
            # 设置文献种类
            form.instance.category = get_category(title=doc_title)
            # 设置文献语言
            if is_contains_chinese(doc_title):
                # if is_contains_chinese(form.instance.name):
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
                # print(form.cleaned_data)
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
            # item.name = doc_title
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
                # print("文本库", doc_title, doc_txt_form, item.name)
                doc_txt_form.instance.page_id = page_id
                doc_txt_form.instance.txt_content = txt_ls[index].replace("\n", "")
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
                    # print("图片文本库", doc_title, doc_img_txt_form)
                    doc_img_txt_form.instance.page_id = txt_dict['filepage']
                    doc_img_txt_form.instance.img_content = txt_dict['content'].replace("\n", "")
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
        # end = time.perf_counter()
        # cost_time = end - start
        os.system('python ./manage.py update_index')
        context = {
            'status': 200,
            'info': upload_info,
            # 'cost_time': {
            # 'upload': "{}秒".format(upload_res[1]),
            # 'all': "{}秒".format(cost_time),
            # },
            'upload_num': {
                'fail': fail_num,
                'success': success_num,
                'all': fail_num + success_num
            }
        }
    except Exception as e:
        print(e)
    finally:
        return JsonResponse(context)


@gzip_page
def doc_del(request):
    uid = request.GET.get('uid')
    exist = models.MeDocs.objects.filter(id=uid).exists()
    if exist:
        obj = models.MeDocs.objects.filter(id=uid).first()
        content_obj = models.DocTxt.objects.filter(doc_name=obj.name).all()
        img_content_obj = models.DocImgTxt.objects.filter(doc_name=obj.name).all()
        doc_url = "./media/docs/" + obj.name + ".pdf"
        # 删除图片
        del_img(img_name=obj.name)
        # 删除文献
        if os.path.exists(doc_url):
            os.remove(doc_url)
        # 删除数据库doctxt记录
        if content_obj:
            content_obj.delete()
        # 删除数据库imgdoctxtx记录
        if img_content_obj:
            img_content_obj.delete()
        # 删数据库除medoc记录
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
        usrid = request.session["info"]['id']
        usrobj = models.User.objects.filter(id=usrid).first()
        new_read_num = usrobj.read_num + 1
        models.User.objects.filter(id=usrid).update(read_num=new_read_num)
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
        # url = "./media/docs/" + title + '.pdf'
        # page_info = spdfmkeyword(url=url, keyword=keyword)
        _, page_info = query_elastics(key=keyword, start=0, size=1000)
        # page_info = query_elastics_min_fragment(key=keyword, start=0, size=1000)
        new_page_info = []
        for item in page_info:
            # print(item['name'])
            if item['name'] == title:
                new_page_info.append(item)
        # 我们需要使用匿名函数，使用sort函数中的key这个参数，来指定字典比大小的方法
        new_page_info.sort(key=lambda x: x['page_id'])
        # print(len(new_page_info), "打开该文献的含有关键词的信息为", new_page_info)
        key_page_info = {}
        facetnum = []
        for item_dict in new_page_info:
            page_abstract = []
            for nape in item_dict["fragments"]:
                # 将未高亮的关键词高亮
                re_strong = r"<strong>(.*?)</strong>"
                key = re.findall(re_strong, nape)[0]
                nape = nape.replace(key, "<strong>" + key + "</strong>")
                # print("加粗：", key, "提取加粗", key[8:-8], "摘要类型", type(nape), "摘要为", nape)
                abstract = {'abstract': nape, 'source': item_dict['source'], 'keyword': keyword}
                page_abstract.append(abstract)
            # 去重同页中重复的摘要
            new_page_abstract = []
            for dictionary in page_abstract:
                if dictionary not in new_page_abstract:
                    new_page_abstract.append(dictionary)
            page_abstract = new_page_abstract
            # print("新摘要", page_abstract)
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
    start = 0
    if request.GET.get("keyword") is None:
        return render(request, "doc_search.html")
    keyword = request.GET.get("keyword")
    # print(request.GET.get("start"))
    if request.GET.get('start') not in ['', None]:
        start = int(request.GET.get('start'))
    # print("起始页为：" + str(start))
    request.session['info']['keyword'] = keyword
    request.session.set_expiry(60 * 60 * 24 * 7)
    # print(request.session['info']['keyword'])
    page_info = query_elastics(key=keyword, start=0, size=1000)
    # print(page_info)
    if len(page_info) == 0:
        context = {
            'search_data': keyword,
            'page_info': page_info,
            'code': 404
        }
        # print(context['code'])
        return JsonResponse(context)
    # print("{}秒".format(end - start))
    # print(page_info)
    for i, item in enumerate(page_info):
        # if i < len(page_info) - 1:
        repeate_ls = []
        # print("当前的下标为：", i)
        rel_score = item['rel_score']
        # print("每页的分数", rel_score)
        for j, _ in enumerate(page_info):
            # print(j)
            if i >= j:
                continue
            if page_info[i]['name'] == page_info[j]['name']:
                rel_score += page_info[j]['rel_score']
                repeate_ls.append(j)
                # print("剔除了" + str(j), page_info[i]['rel_score'])
            continue
        n = 0
        for k in repeate_ls:
            k -= n
            page_info.pop(k)
            n += 1
        # print("更新前的名字：" + page_info[i]['name'])
        # print("求和后的分数", rel_score)
        page_info[i]['id'] = models.MeDocs.objects.filter(name=page_info[i]['name']).first().id
        page_info[i]['name'] = get_doc_title(page_info[i]['name'])
        # print('更新后的名字：' + page_info[i]['name'])
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
    # for i, item in enumerate(page_info):
    #     item['num'] = i + 1
    # print("去除重复后的文献数", len(page_info))
    if start + 10 < len(page_info):
        page_info = page_info[start:start + 10]
        page_status = False
    else:
        page_info = page_info[start:len(page_info)]
        page_status = True
    for i, item in enumerate(page_info):
        # print("行号为", i)
        item['num'] = i + 1
    # print("分页后的文献数", len(page_info))
    # print(page_info)
    context = {
        'search_data': keyword,
        'page_info': page_info,
        'code': 200,
        'start': start,
        'final_page': page_status
    }
    return JsonResponse(context)


# @gzip_page
@csrf_exempt
def doc_query(request):
    """同步检索"""
    start = 0
    if request.GET.get("keyword") is None:
        return render(request, "doc_query.html")
    keyword = request.GET.get("keyword")
    # print(request.GET.get("start"))
    if request.GET.get('start') not in ['', None]:
        start = int(request.GET.get('start'))
    # print("起始页为：" + str(start))
    request.session['info']['keyword'] = keyword
    request.session.set_expiry(60 * 60 * 24 * 7)
    # print(request.session['info']['keyword'])
    cost_time, page_info = query_elastics(key=keyword, start=0, size=1000)
    # print(len(page_info))
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
        # print("当前的下标为：", i)
        rel_score = item['rel_score']
        # print("每页的分数", rel_score)
        for j, _ in enumerate(page_info):
            # print(j)
            if i >= j:
                continue
            if page_info[i]['name'] == page_info[j]['name']:
                rel_score += page_info[j]['rel_score']
                repeate_ls.append(j)
                # print("剔除了" + str(j), page_info[i]['rel_score'])
            continue
        n = 0
        for k in repeate_ls:
            k -= n
            page_info.pop(k)
            n += 1
        # print("更新前的名字：" + page_info[i]['name'])
        # print("求和后的分数", rel_score)
        # print(page_info[i])
        page_info[i]['id'] = models.MeDocs.objects.filter(name=page_info[i]['name']).first().id
        page_info[i]['name'] = get_doc_title(page_info[i]['name'])
        # print('更新后的名字：' + page_info[i]['name'])
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
    page_info_len = len(page_info)
    # print("剔除重复后的：", len(page_info), len(page_info) - len(repeate_ls))
    page_info = sorted(page_info, key=lambda x: x['allscore'], reverse=True)
    # for i, item in enumerate(page_info):
    #     item['num'] = i + 1
    # print("去除重复后的文献数", len(page_info))
    if start + 10 < len(page_info):
        page_info = page_info[start:start + 10]
        page_status = False
    else:
        page_info = page_info[start:len(page_info)]
        page_status = True
    for i, item in enumerate(page_info):
        # print("行号为", i)
        item['num'] = i + 1
    # print("分页后的文献数", len(page_info))
    # print(page_info)
    context = {
        'search_data': keyword,
        'page_info': page_info,
        'code': 200,
        'start': start,
        'final_page': page_status,
        'cost_time': cost_time,
        'doc_num': page_info_len
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
    # data = ""
    # while not data:
    status, data = get_zhiwang_data(keywords, start, end)
    print(data)
    res = {
        'status': status,
        'data': data
    }
    return JsonResponse(res)


def doc_img(request):
    doc_id = request.POST.get('uid', 98)
    doc_name = models.MeDocs.objects.filter(id=doc_id).first().name
    # print(doc_id, doc_name)
    names_list = []
    paths_list = []
    context = {
        'status': 200,
        'names': names_list,
        'paths': paths_list
    }
    path = "./media/docimgs"
    for parent, _, fileNames in os.walk(path):
        for name in fileNames:
            if doc_name in name:
                names_list.append(name[-7:-4])
                parent = parent.replace(".", '')
                paths_list.append(os.path.join(parent, name))
    if not names_list:  # 文件夹为空
        context['status'] = 403
        return JsonResponse(context)
    # print(context)
    return JsonResponse(context)


@gzip_page
def doc_keyinfo(request):
    try:
        doc_name = request.GET.get('doc_name', "")
        content = models.DocTxt.objects.filter(doc_name=doc_name, page_id=1).first().txt_content
        # content = query_leastic_firstpage(doc_name=doc_name)[2]
        if content != "":
            part_content = content[:1000] if len(content) > 1000 else content
            # print("耗时为：", time.perf_counter() - start)
            keyinfo = get_keyinfo(part_content)
            # print(len(part_content))
            # qas = get_qas(doc_txt=part_content)
            # qas = qas[:5] if len(qas) > 5 else qas
            # print(qas)
            # print("关键信息为：", keyinfo)
            context = {
                'status': 200,
                'keyinfo': keyinfo,
                # 'qas': qas
            }
        else:
            context = {
                'status': 403,
                'error': "抱歉，网络当前出错啦，请重试谢谢！"
            }
    except Exception as e:
        # print(e)
        context = {
            'status': 403,
            'error': "抱歉，网络当前出错啦，请重试谢谢！"
        }
    finally:
        return JsonResponse(context)


@csrf_exempt
@gzip_page
def doc_union(request):
    keyword = request.GET.get('keyword')
    keyword = list(jieba.cut(keyword))
    # print(keyword, type(keyword))
    res = {'wordres': []}
    url = "https://recom.cnki.net/api/recommendations/words/union"
    for item in keyword:
        formdata = {
            'w': item,
            'top': 10
        }
        result = requests.get(url=url, params=formdata).json()
        res['wordres'] += result['wordres'] if result else result
    random.shuffle(res['wordres'])
    res['wordres'] = res['wordres'][:10]
    return JsonResponse(res)


@csrf_exempt
def doc_get_random(request):
    baseurl = "/media/covers/"
    doc_queryset = models.MeDocs.objects.all().order_by('-allscore')
    doc_num = len(doc_queryset)
    current_id = request.GET.get('cid')
    # print(type(current_id), current_id, int(current_id) % doc_num)
    current_doc_obj = doc_queryset[int(current_id) % doc_num]
    doc_cover_url = baseurl + current_doc_obj.cover
    # print(request.method, doc_cover_url)
    context = {
        'doc_cover_url': doc_cover_url,
        'doc_cover_name': current_doc_obj.name
    }
    return JsonResponse(context)

# if __name__ == '__main__':
#     with PyCallGraph(output=GraphvizOutput()):
#         调用你要分析的函数
# doc_list()
