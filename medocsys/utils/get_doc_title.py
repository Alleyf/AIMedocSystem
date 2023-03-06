import re

import fitz
from tika import parser
import PyPDF2

from medocsys.utils.get_language_type import is_contains_chinese
from medocsys.utils.search import duplate_rate


def get_pdf_title(title: str):
    url = '../../media/docs/' + title  # 测试
    # url = './media/docs/' + title + '.pdf'  # 实际
    print(url)
    parsedPDF = parser.from_file(url)
    if "pdf:docinfo:title" in parsedPDF['metadata']:
        # return parsedPDF['metadata']["pdf:docinfo:title"]
        return parsedPDF['metadata']  # 测试
    else:
        return title


def get_doc_title_and_language(doc_name: str):
    # 1.使用PyPDF2库：PyPDF2是用来提取PDF文档内容的库，可以把PDF文档转换成文本，并且可以提取其中的文本，所以可以用它来提取PDF文档中的论文题目：
    # url = '../../media/docs/' + doc_name  # 测试
    url = './media/docs/' + doc_name + '.pdf'  # 实际
    print(url)
    pdf_document = fitz.open(url)
    # 获取pdf元信息
    document_info = pdf_document.metadata
    # 获取文档题目
    title = document_info['title']
    if not title:
        # 获取第一页
        title_ls = []
        no_signal = 0
        yes_signal = 0
        new_no_signal = 0
        pdf_document = fitz.open(url)
        first_page = pdf_document.load_page(0)
        # print("第一页的内容为", first_page)
        # 获取页面标题
        first_page_ls = first_page.get_text().split('\n')[:8]
        # print(first_page_ls)
        for item in first_page_ls:
            item = item.replace(" ", ",")
            item = item.replace("-", ",")
            item = item.replace("·", ",")
            item = item.replace("，", ",")
            item = item.replace(":", ",")
            if "\n" and "\r" and "," not in item:
                # if not re.search(" ", item):
                print("满足条件的项", item, len(item))
                title_ls.append(item)
                yes_signal += 1
            else:
                new_no_signal = no_signal + 1
            if new_no_signal > no_signal and yes_signal > 0:
                # print(new_no_signal, no_signal, yes_signal)
                break
            else:
                no_signal += 1
        title = "".join(title_ls)
        # 获取文档信息
        if not title or duplate_rate(title, doc_name) < 70:
            title = doc_name
    # 打印语言
    language = is_contains_chinese(strs=title)
    # print("中文") if language else print("英文")
    # 输出标题和语言
    # print(title)
    return title, language


if __name__ == '__main__':
    # print(get_pdf_title("isct_a-118.pdf"))
    get_doc_title_and_language(
        doc_name="新冠肺炎.pdf")
