import fitz


def get_doc_cover(pdf_document, doc_name):
    # 截取第一页作为封面
    page = pdf_document.load_page(0)  # 获取第一页页面对象
    rect = page.rect  # 获取页面矩形
    dpi = 300  # 指定分辨率为300dpi
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))  # 获取像素图
    width, height = int(rect.width * dpi / 72), int(rect.height * dpi / 72)  # 计算像素大小
    # pix._writeIMG("../../media/covers/page.png", 1)  # 将像素图写入PNG文件中“测试”
    pix._writeIMG("./media/covers/" + doc_name + ".png", 1)  # 将像素图写入PNG文件中“实际”
    return True


if __name__ == "__main__":
    real_url = "../../media/docs/2016IJC-导管组织接触对于模型的影响PentarRay_FAM.pdf"
    pdf_document = fitz.open(real_url)
    print(get_doc_cover(pdf_document))
