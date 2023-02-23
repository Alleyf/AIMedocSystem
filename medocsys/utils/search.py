# 搜索指定文本内容
import difflib
import json
import os
import time
from os import path

import fitz
import jieba

from medocsys.utils.query import query_elastics

"""-------------------------------------------公共方法-------------------------------------------"""


def str_replace(old_str: str, str1, str2):
    new_str = old_str.replace(str1, str2)
    return new_str


def mstr_replace(old: str, str_ls: list, target: str) -> str:
    """
    :param old: 待替换的字符串
    :param str_ls: 被替换的字符串表
    :param target: 目标字符
    :return: 替换后的字符串
    """
    for item in str_ls:
        old = old.replace(item, target)
    return old


def div_word(keywords):
    # 关键词分词(分词和原始完整词一起搜)
    res = []
    keywords = mstr_replace(keywords, [',', '，', ';', '；', '-', '——'], ' ')
    keywords = keywords.split(' ')
    for i in range(len(keywords)):
        origin_keyword = keywords[i]
        participle_keywords = jieba.lcut_for_search(origin_keyword)
        keyword_dict = {"origin_word": origin_keyword, "participle_word": participle_keywords}
        keywords += participle_keywords
        res.append(keyword_dict)
    keyword = sorted(set(keywords), reverse=True)
    keyword = list(keyword)
    keyword.sort(key=len, reverse=True)
    return keyword, res


def str_merge(str1, str2, ):
    new_str = str1 + str2
    merge_str = "".join(set(new_str))
    return merge_str


def duplate_rate(text1, text2):
    """
            :param text1: 待比较的文本
            :param text2：待比较的文本
            :return: 返回两者重复的数目占文本2的比例
    """
    com = difflib.Differ()
    com = com.compare(text1, text2)
    text = "".join(com)
    # text1_total = len(text1)
    text2_total = len(text2)
    # text1_only = str.count("-")
    text2_only = text.count("+")
    # text1_repetitive_rate = (text1_total - text1_only) / text1_total * 100
    text2_repetitive_rate = (text2_total - text2_only) / text2_total * 100
    return text2_repetitive_rate


def dict_sort(origin: dict):
    """
        :param origin: 待排序的字典
        :return: 返回排序后字典
    """
    sorted_tuples = sorted(origin.items(), key=lambda item: item[0])
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict


"""-------------------------------------------分割线-------------------------------------------"""


def mpdfkeyword(url, search_term):
    file = os.listdir(url)
    for f in file:
        # 字符串拼接
        real_url = path.join(url, f)
        # filename = "G:/Desktop/服创/test/pdf/ciceri2019.pdf"
        pdf_document = fitz.open(real_url)
        pdf_name = pdf_document.name[14:]
        pdf_total_page = len(pdf_document)
        result = {'title': '', 'total_page': 0, 'key_page_num': []}
        for current_page in range(pdf_total_page):
            page = pdf_document.load_page(current_page)
            if page.search_for(search_term):
                result['title'] = pdf_name
                result['total_page'] = pdf_total_page
                result['key_page_num'].append(current_page)
                # print("%s found on page %i in %s" % (search_term, current_page, pdf_name))
                my_rect = page.search_for(search_term)
                my_text = page.get_text_blocks(
                    fitz.Rect(-2147483648, my_rect[0].y0 - (4 * my_rect[0].height), 2147483520, my_rect[0].y1) + (
                            4 * my_rect[0].height))
                my_text2 = my_text[0][4]
                my_text2 = my_text2.replace("\n", " ")
                # print(my_text2)
                # print("\n")
        # print(result)


def spdfkeyword(url, keyword):
    start = time.time()
    search_term = keyword
    doc_name = url[22:-4]
    # doc_name = url[14:-4]
    pdf_document = fitz.open(url)
    pdf_name = pdf_document.name[22:-4]
    # pdf_name = pdf_document.name[14:-4]
    pdf_total_page = len(pdf_document)
    result = {'title': '', 'total_page': 0, 'key_page_info': {}}
    # PDF文本搜索关键词
    for current_page in range(pdf_total_page):
        page = pdf_document.load_page(current_page)
        print(page, search_term)
        if page.search_for(search_term):
            result['title'] = pdf_name
            result['total_page'] = pdf_total_page
            result['key_page_info'][current_page + 1] = []
            my_rect = page.search_for(search_term)
            recite = []
            if len(my_rect) >= 2:
                for num in range(0, len(my_rect) - 2):
                    if my_rect[num].y0 == my_rect[num + 1].y0 or my_rect[num].y1 == my_rect[num + 1].y1 or my_rect[
                        num].x0 == my_rect[num + 1].x0 or my_rect[num].x1 == my_rect[num + 1].x1:
                        recite.append(num)
                my_rect = [my_rect[i] for i in range(len(my_rect)) if (i not in recite)]
            for obj in my_rect:
                my_text = page.get_text_blocks(
                    fitz.Rect(-2147483648, obj.y0 - (4 * obj.height), 2147483520, obj.y1) + (
                            4 * obj.height))
                my_text2 = ""
                for item in my_text:
                    my_text2 = my_text2 + item[4]
                    my_text2 = my_text2.replace("\u3000", ' ')
                    my_text2 = mstr_replace(my_text2, ['\n', '\r', '<r', '<u', '<', '>'], '')
                my_text2 = my_text2.replace(search_term, '<strong>' + search_term + '</strong>')
                context = {
                    'abstract': my_text2,
                    'source': "文本",
                    'keyword': search_term
                }
                result['key_page_info'][current_page + 1].append(context)
                # if current_page + 1 == 5:
                #     print(my_text2 + str(current_page + 1) + "\n")
    print(doc_name + " PDF文本搜索结果：" + json.dumps(result))
    # PDF图片搜索关键词
    img_info = query_elastics(keyword)
    print(img_info)
    for item in img_info:
        print(item)
        if "page_id" in item and item['name'] == doc_name:
            # if item['name'] == doc_name:
            print("图片中存在关键字")
            page_id = int(item['page_id'])
            text = item['text'][:-1].replace(search_term, '<strong>' + search_term + '</strong>')
            text = mstr_replace(text, ['\n', '\r', '<r', '<u', '<', '>'], '')
            text = text.replace("\u3000", " ")
            # 判断图片所在页码是否已存在,不存在则总页数加1
            if page_id not in result['key_page_info']:
                result['total_page'] += 1
                result['key_page_info'][page_id] = []
            context = {
                'abstract': text,
                'source': "图片",
                'keyword': search_term
            }
            result['key_page_info'][page_id].append(context)
            result['title'] = doc_name
    end = time.time()
    result['cost_time'] = end - start
    return result


def spdfmkeyword(url, keyword):
    start = time.time()
    # 关键词分词
    # search_terms = jieba.lcut_for_search(keyword)
    search_terms, participle_ls = div_word(keyword)
    print(search_terms)
    print(participle_ls)
    doc_name = url[22:-4]  # 实际
    # doc_name = url[14:-4]#测试
    pdf_document = fitz.open(url)
    pdf_name = pdf_document.name[22:-4]  # 实际
    # pdf_name = pdf_document.name[14:-4]#测试
    pdf_total_page = len(pdf_document)
    result = {'title': '', 'total_page': 0, 'key_page_info': {}}
    # PDF文本搜索关键词
    for current_page in range(pdf_total_page):
        page = pdf_document.load_page(current_page)
        # result['key_page_info'][current_page + 1] = []
        for search_term in search_terms:
            status = False
            if page.search_for(search_term):
                # 去除文章中已经加入了完整词的分词
                page_info_ls = result['key_page_info'][current_page + 1] if (current_page + 1) in result[
                    'key_page_info'] else False
                print("当前的页面信息", page_info_ls)
                if page_info_ls:
                    for item in page_info_ls:
                        if search_term in item['keyword']:
                            print(search_term + "被跳过")
                            status = True
                            break
                    if status:
                        continue
                # -----------------------------------分割线-----------------------------------
                print("第" + str(current_page + 1) + "页包含关键词：" + search_term)
                result['title'] = pdf_name
                result['total_page'] = pdf_total_page
                if (current_page + 1) not in result['key_page_info']:
                    result['key_page_info'][current_page + 1] = []
                my_rect = page.search_for(search_term)
                recite = []
                if len(my_rect) >= 2:
                    for num in range(0, len(my_rect) - 2):
                        if my_rect[num].y0 == my_rect[num + 1].y0 or my_rect[num].y1 == my_rect[num + 1].y1 or my_rect[
                            num].x0 == my_rect[num + 1].x0 or my_rect[num].x1 == my_rect[num + 1].x1:
                            recite.append(num)
                    my_rect = [my_rect[i] for i in range(len(my_rect)) if (i not in recite)]
                for obj in my_rect:
                    my_text = page.get_text_blocks(
                        fitz.Rect(-2147483648, obj.y0 - (4 * obj.height), 2147483520, obj.y1) + (
                                4 * obj.height))
                    my_text2 = ""
                    for item in my_text:
                        my_text2 = my_text2 + item[4]
                        my_text2 = mstr_replace(my_text2, ['\n', '\r', '<r', '<u', '<', '>'], '')
                        my_text2 = my_text2.replace("\u3000", ' ')
                    my_text2 = my_text2.replace(search_term, '<strong>' + search_term + '</strong>')
                    context = {
                        'abstract': my_text2,
                        'source': "文本",
                        'keyword': search_term
                    }
                    # 去除重复的摘要
                    part_prev = context.get('abstract')
                    facet_num = len(result['key_page_info'][current_page + 1])
                    if facet_num > 0:
                        part_next = result['key_page_info'][current_page + 1][-1]['abstract']
                        duplicate_rate = duplate_rate(part_prev, part_next)
                        if duplicate_rate > 30:
                            # print(duplicate_rate)
                            merge_str = str_merge(part_prev, part_next)
                            if merge_str:
                                # print(merge_str)
                                context['abstract'] = merge_str
                    # if "strong" in context['abstract']:
                    #     result['key_page_info'][current_page + 1].append(context)
                    if search_term in context['abstract']:
                        print("该部分包含关键字")
                        if "<strong>" or "</strong>" not in context["abstract"]:
                            print("添加" + search_term + "高亮")
                            # 去除混乱的字符
                            # context['abstract'] = str_replace(context['abstract'], "<strong>", '')
                            # context['abstract'] = str_replace(context['abstract'], "</strong>", '')
                            # context['abstract'] = str_replace(context['abstract'], "<", '')
                            # context['abstract'] = str_replace(context['abstract'], "/", '')
                            # context['abstract'] = str_replace(context['abstract'], ">", '')
                            context['abstract'] = mstr_replace(
                                context['abstract'], ["<strong>", "</strong>", "<", "/", ">"], ''
                            )
                            context["abstract"] = context["abstract"].replace(search_term,
                                                                              "<strong>" + search_term + "</strong>")
                            print("添加后：" + context['abstract'])
                        result['key_page_info'][current_page + 1].append(context)
                    # ----------------------分隔线--------------------------
                    # result['key_page_info'][current_page + 1].append(context)
                print(result)
                # if current_page + 1 == 5:
                #     print(my_text2 + str(current_page + 1) + "\n")
        # print(doc_name + " PDF文本搜索结果：" + json.dumps(result))
        # PDF图片搜索关键词
        # search_term = ''.join(keyword)
    for search_term in search_terms:
        # print("关键词为:" + search_term)
        status = False
        img_info = query_elastics(search_term)
        for item in img_info:
            print(doc_name, item['name'])
            if "page_id" in item and item['name'] == doc_name:
                # print(item)
                # print("图片中存在关键字" + search_term)
                page_id = int(item['page_id'])
                # 去除文章中已经加入了完整词的分词
                page_info_ls = result['key_page_info'][page_id] if (page_id in result[
                    'key_page_info'] and result['key_page_info'][page_id][-1]['source'] == "图片") else False
                # print("当前的页面信息", page_info_ls)
                if page_info_ls:
                    for info in page_info_ls:
                        if search_term in info['keyword']:
                            # print(search_term + "被跳过")
                            status = True
                            break
                    if status:
                        break
                # print(search_term + "被添加")
                text = item['fragments'][0]
                text = text.replace("\u3000", " ")
                text = mstr_replace(text, ['\n', '\r', '<r', '<u'], '')
                # 判断图片所在页码是否已存在,不存在则总页数加1
                if page_id not in result['key_page_info']:
                    result['total_page'] += 1
                    result['key_page_info'][page_id] = []
                context = {
                    'abstract': text,
                    'source': "图片",
                    'keyword': search_term
                }
                # 去除重复的摘要
                # part_next = context.get('abstract')
                # facet_num = len(result['key_page_info'][page_id])
                # if facet_num > 0:
                #     part_prev = result['key_page_info'][page_id][-1]['abstract']
                #     duplicate_rate = duplate_rate(part_prev, part_next)
                #     print(duplicate_rate)
                #     if duplicate_rate > 30:
                #         # print(duplicate_rate)
                #         merge_str = str_merge(part_prev, part_next)
                #         if merge_str:
                #             # print(merge_str)
                #             context['abstract'] = merge_str
                #             print(merge_str)
                if search_term in context['abstract']:
                    if "<strong>" or "</strong>" not in context["abstract"]:
                        context["abstract"] = context["abstract"].replace(search_term,
                                                                          "<strong>" + search_term + "</strong>")
                    result['key_page_info'][page_id].append(context)
                    result['title'] = doc_name
                # print("当前检索的关键词为：" + search_term)
    result['key_page_info'] = dict_sort(result['key_page_info'])
    end = time.time()
    result['cost_time'] = end - start
    return result


"""测试"""
if __name__ == "__main__":
    # all_info = spdfmkeyword(url="../static/doc/高效液相色谱法测定人血浆中百草枯浓度_孙斌.pdf", keyword='百草枯')
    # key_info = all_info['key_page_info']
    # print(key_info)
    print(mstr_replace('f\tc\ns|;~!', ['\t', '\n', '|', '~', ';', '!'], ''))
