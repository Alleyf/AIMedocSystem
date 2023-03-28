import fitz

from medocsys.utils.search import duplate_rate


def get_doc_title(doc_name: str):
    # 1.使用PyPDF2库：PyPDF2是用来提取PDF文档内容的库，可以把PDF文档转换成文本，并且可以提取其中的文本，所以可以用它来提取PDF文档中的论文题目：
    # url = '../../media/docs/' + doc_name  # 测试
    url = './media/docs/' + doc_name + '.pdf'  # 实际
    # print(url)
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
            item = item.replace("　", ",")
            item = item.replace("＊", ",")
            if "\n" and "\r" and "," not in item:
                # if not re.search(" ", item):
                # print("满足条件的项", item, len(item))
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
    # language_status = is_contains_chinese(strs=title)
    # language = "中文" if language_status else "英文"
    # print("中文") if language else print("英文")
    # 输出标题和语言
    # print(title)
    # return title, language
    return title


if __name__ == '__main__':
    # print(get_pdf_title("isct_a-118.pdf"))
    print(get_doc_title(
        doc_name="高效液相色谱法测定人血浆中百草枯浓度_孙斌.pdf"))
