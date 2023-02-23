# 提取图像
import os
import time
from os import path
import fitz


# 自动提取文件夹中pdf图片函数
def get_pdf_img(url: str):
    start = time.perf_counter()
    filedic = {'filename': '', 'filepage': 0, 'filepageimgnumber': 0}
    filelist = []
    imgindex = 0
    tempcurrentpage = 0
    tempname = ""
    file = os.listdir(url)
    for f in file:
        # 字符串拼接
        real_url = path.join(url, f)
        pdf_document = fitz.open(real_url)
        for current_page in range(len(pdf_document)):
            for image in pdf_document.get_page_images(current_page):
                xref = image[0]
                pix = fitz.Pixmap(pdf_document, xref)
                # 判断图片是否来自同页且同一文档
                if current_page + 1 == tempcurrentpage and tempname == f[:-4]:
                    # tempcurrentpage = current_page
                    imgindex += 1
                else:
                    imgindex = 0
                    tempname = f[:-4]
                    tempcurrentpage = current_page + 1

                if pix.n < 4:  # this is GRAY or RGB
                    # pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix._writeIMG("../../media/docimgs/%s-%s-%s.png" % (f[:-4], tempcurrentpage, imgindex + 1), 1)
                    print("%s 图片提取成功" % f[:-4])
                    if filedic['filename'] == f[:-4]:
                        if filedic['filepage'] == tempcurrentpage:
                            filedic['filepageimgnumber'] += 1
                        else:
                            filedic = {'filename': f[:-4], 'filepage': tempcurrentpage, 'filepageimgnumber': 1}
                            filelist.append(filedic)
                    else:
                        filedic = {'filename': f[:-4], 'filepage': tempcurrentpage, 'filepageimgnumber': 1}
                        filelist.append(filedic)

                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1._writeIMG("../../media/docimgs/%s-%s-%s.png" % (f[:-4], tempcurrentpage, imgindex + 1), 1)
                    print("%s 图片提取成功" % f[:-4])
                    pix1 = None
                    if filedic['filename'] == f[:-4]:
                        if filedic['filepage'] == tempcurrentpage:
                            filedic['filepageimgnumber'] += 1
                        else:
                            filedic = {'filename': f[:-4], 'filepage': tempcurrentpage, 'filepageimgnumber': 1}
                            filelist.append(filedic)

                    else:
                        filedic = {'filename': f[:-4], 'filepage': tempcurrentpage, 'filepageimgnumber': 1}
                        filelist.append(filedic)
                pix = None
    end = time.perf_counter()
    print("耗时{}秒".format(end - start))
    return filelist


if __name__ == '__main__':
    print(get_pdf_img("../static/doc"))
