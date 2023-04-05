import os
import re
import time
from os import path
import fitz

from medocsys.utils.img_deblur import deblur
from medocsys.utils.get_cover import get_doc_cover
from medocsys.utils.img_blur_detect import judge_deblur
from medocsys.utils.ocr import integrated_ocr

"""单文件上传(默认上传到static/doc/目录)"""


def upload(file_obj, url="./medocsys/static/doc/"):
    url += file_obj.name
    f = open(url, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    return True


"""多文件上传(默认上传到static/doc/目录)"""


def upload_mul(file_list, url="./media/docs/"):
    start_time = time.perf_counter()
    for f in file_list:
        des = url + f.name.replace(" ", "_")
        # print(des)
        destination = open(des, 'wb')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    end_time = time.perf_counter()
    cost_time = end_time - start_time
    return True, cost_time


"""提取PDF文件内容"""


# def extract_content(url):
#     doc = fitz.open(url)
#     txt_content = ""
#     for page in doc:
#         txt_content += page.get_text("text")
#     return txt_content
# 自动提取文件夹中pdf每一页的内容
def extract_txt_info(url):
    # st = 'docs/(.*?).pdf'  # 正则表达式
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    # name = re.findall(st, url)
    # print(name)
    pdf_document = fitz.open(url)
    txt_ls = []
    for current_page in range(len(pdf_document)):
        # for text in pdf_document.getText(current_page):
        page = pdf_document.load_page(current_page)
        text = page.get_text("text")
        txt_ls.append(text)
        # pdf_dict = {"name": name[0], "text_list": txt_ls}
    # pdf_list.append(pdf_dict)
    # res = {"pdf_list":pdf_list}
    # print("%s 文本提取成功" % f)
    # print(pdf_list)
    return txt_ls


"""提取文件夹中PDF图片信息"""


def extract_img_widget(file, url, filedic, filelist, imgindex, tempcurrentpage, tempname, mul) -> list:
    if mul:
        f = file
        real_url = path.join(url, file)
    else:
        # f = file.name[14:]  # 测试
        f = file.name[22:]  # 实际
        real_url = url
    st = 'docs/(.*?).pdf'  # 正则表达式
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    name = re.findall(st, url)[0]
    # print(name)
    pdf_document = fitz.open(real_url)
    # 上传文献封面
    get_doc_cover(pdf_document, name)
    for current_page in range(len(pdf_document)):
        img_txt = ""
        for image in pdf_document.get_page_images(current_page):
            xref = image[0]
            pix = fitz.Pixmap(pdf_document, xref)
            # 判断图片是否来自同页且同一文档
            if current_page + 1 == tempcurrentpage and tempname == name:
                # same_page_flag = True
                imgindex += 1
            else:
                # same_page_flag = False
                imgindex = 0
                tempname = name
                tempcurrentpage = current_page + 1
            imgurl = "./media/docimgs/%s-%s-%s.png" % (name, tempcurrentpage, imgindex + 1)  # 实际
            # imgurl = "../../media/docimgs/%s-%s-%s.png" % (name, tempcurrentpage, imgindex + 1)  # 测试
            if pix.n < 4:  # this is GRAY or RGB
                # print(imgurl)
                pix._writeIMG(imgurl, 1)
                # if same_page_flag:
                # img_txt += paddle_ocr(imgurl=imgurl) + "|"
                # filedic['content'] = img_txt
                # print("%s 图片提取并识别成功,识别结果为：%s" % (name, filedic['content']))
                if filedic['filename'] == name:
                    if filedic['filepage'] == tempcurrentpage:
                        filedic['filepageimgnumber'] += 1
                    else:
                        filedic = {'filename': name, 'filepage': tempcurrentpage, 'filepageimgnumber': 1}
                else:
                    filedic = {'filename': name, 'filepage': tempcurrentpage, 'filepageimgnumber': 1}

            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1._writeIMG(imgurl, 1)
                pix1 = None
                if filedic['filename'] == name:
                    if filedic['filepage'] == tempcurrentpage:
                        filedic['filepageimgnumber'] += 1
                    else:
                        filedic = {'filename': name, 'filepage': tempcurrentpage, 'filepageimgnumber': 1}

                else:
                    filedic = {'filename': name, 'filepage': tempcurrentpage, 'filepageimgnumber': 1}
            pix = None
            # 对模糊图像进行去模糊
            # print("待检测的图像名为", imgurl[16:])
            if judge_deblur(img_name=imgurl[16:], input_path=r"./media/"):  # 实际
                deblur(img_name=imgurl[16:])
            # if judge_deblur(img_name=imgurl[20:]):  # 测试
            #     deblur(img_name=imgurl[20:])
            img_txt += integrated_ocr(img_path=imgurl) + "|"
        if img_txt not in ["", "|", " "]:
            filedic['content'] = img_txt
            filelist.append(filedic)
            print("%s 图片提取并识别成功,识别结果为：%s" % (name, filedic['content']))
    return filelist


# 提取整个文件夹的PDF：mul=True
# 提取单个PDF：mul=False
def extract_img_info(url, mul):
    # start = time.perf_counter()
    filedic = {'filename': '', 'filepage': 0, 'filepageimgnumber': 0, 'content': ""}
    filelist = []
    imgindex = 0
    tempcurrentpage = 0
    tempname = ""
    if mul:
        file = os.listdir(url)
        for f in file:
            extract_img_widget(f, url, filedic, filelist, imgindex, tempcurrentpage, tempname, mul)
    else:
        f = open(url, mode='r')
        extract_img_widget(f, url, filedic, filelist, imgindex, tempcurrentpage, tempname, mul)
    # end = time.perf_counter()
    # print("耗时：" + str(end - start) + "秒")
    return filelist


if __name__ == '__main__':
    # txt_info = extract_txt_info("../../media/docs/谷歌深度强化学习布局布线.pdf")
    # print(len(txt_info['text_list']), txt_info['text_list'][6])
    img_txt = extract_img_info("../../media/docs/ENSITE_NAVX和双LAS_省略_左心房线性消融治疗阵发性心房颤动_陈明龙.pdf", mul=False)
    # print(img_txt)
    # print(extract_img_info("../static/doc/", mul=True))
    # print(extract_img("../static/doc/", mul=True))
