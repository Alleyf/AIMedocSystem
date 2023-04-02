# coding=gbk
import base64
import json
import operator
import time

import requests
from paddleocr import PaddleOCR
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

"""--------------------------------------提取图片中的文字信息-------------------------------------"""

""" **********************************Paddle识别API***********************************"""


def paddle_ocr(img_path):
    """
    :param img_path: 待识别的图片路径
    :return: 图片识别的文本结果
    """
    password = '8907'
    url = "http://www.iinside.cn:7001/api_req"
    data = {
        'password': password,
        'reqmode': 'ocr_pp'
    }
    files = [('image_ocr_pp', ('name.PNG', open(img_path, 'rb'), 'application/octet-stream'))]
    headers = {}
    response = requests.post(url, headers=headers, data=data, files=files)
    # result = ",".join(json.loads(response.text)['data'])
    result = json.loads(response.text)['data']
    if result:
        return result
    else:
        return []


""" **********************************腾讯公式识别API***********************************"""

# def tencent_ocr_formula(imgpath, Id="AKIDbCkEezGTbecVJ4kLsKhzRo6KTXYYTJ4k", Key="dAc6Umz674vgMwSsDTdhgZN5hDezENRQ"):
#     try:
#         # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
#         # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
#         cred = credential.Credential(Id, Key)
#         base_str = image_to_base64(imgpath)
#         # 实例化一个http选项，可选的，没有特殊需求可以跳过
#         httpProfile = HttpProfile()
#         httpProfile.endpoint = "ocr.tencentcloudapi.com"
#
#         # 实例化一个client选项，可选的，没有特殊需求可以跳过
#         clientProfile = ClientProfile()
#         clientProfile.httpProfile = httpProfile
#         # 实例化要请求产品的client对象,clientProfile是可选的
#         client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
#
#         # 实例化一个请求对象,每个接口都会对应一个request对象
#         req = models.FormulaOCRRequest()
#         params = {
#             "ImageBase64": base_str
#         }
#         req.from_json_string(json.dumps(params))
#
#         # 返回的resp是一个FormulaOCRResponse的实例，与请求对象对应
#         resp = client.FormulaOCR(req)
#         result = resp.to_json_string()
#         res = json.loads(result)
#         # 返回json格式的字符串回包->Latex公式
#         return res['FormulaInfos'][0]['DetectedText']
#
#     except TencentCloudSDKException as err:
#         return err


""" **********************************腾讯文字识别API***********************************"""


def tencent_ocr_geberaltext(imgpath, Id="AKIDbCkEezGTbecVJ4kLsKhzRo6KTXYYTJ4k", Key="dAc6Umz674vgMwSsDTdhgZN5hDezENRQ"):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(Id, Key)
        base_str = image_to_base64(imgpath)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageBase64": base_str
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
        resp = client.GeneralAccurateOCR(req)
        # 输出json格式的字符串回包
        result = resp.to_json_string()
        # 转为字典并返回
        res = json.loads(result)
        # 单独提取文本
        text = []
        for item in res['TextDetections']:
            text.append(item["DetectedText"])
        # res_txt = ",".join(text)
        return text
    except TencentCloudSDKException as err:
        # return err
        return []


""" **********************************本地识别API***********************************"""

"""
Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
"""


def local_ocr(img_path):
    """
    :param img_path:待识别的图片路径
    :return: 识别文本结果
    """
    ocr = PaddleOCR(
        det_model_dir='./medocsys/utils/OCR_Infer/ch_PP-OCRv3_det_slim_infer',
        rec_model_dir='./medocsys/utils/OCR_Infer/ch_PP-OCRv3_rec_slim_infer',
        cls_model_dir='./medocsys/utils/OCR_Infer/ch_ppocr_mobile_v2.0_cls_slim_infer',
        use_angle_cls=True
    )
    # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    res_txt = []
    for item in result:
        for field in item:
            res_txt.append(field[-1][0])
    # res_txt = ",".join(res_txt)
    return res_txt
    # return result
    # # 显示结果
    # from PIL import Image
    #
    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
    # im_show = Image.fromarray(im_show)
    # im_show.save('result.jpg')


""" **********************************综合识别API***********************************"""


def integrated_ocr(img_path: str):
    """
    :param img_path: 待识别的图片路径
    :return: 三种识别结果综合后的结果
    """

    paddle_txt = paddle_ocr(img_path)  # 有较大的问题
    tencent_txt = tencent_ocr_geberaltext(img_path)
    local_txt = local_ocr(img_path)

    # merge_txt = list_merge("paddle", paddle_txt)
    merge_txt = list_merge(tencent_txt, local_txt, paddle_txt)
    # print("飞浆API结果：", paddle_txt)
    # print("腾讯API结果：", tencent_txt)
    # print("本地API结果：", local_txt)
    # print("合并后的结果：", merge_txt)

    return merge_txt


""" **********************************公共函数**************************************"""

"""字符串合并并去重"""
"""
概述:
        不定长参数也叫可变参数, 即: 参数的个数是可变的.
    格式:
        在形参名的前边写上 *args, 或者 **kwargs,
        如果是 * 则表示可以接收所有的 位置参数, 形成元组.
        如果是 ** 则表示可以接收所有的 关键字参数, 形成字典.
    细节:
        1. 如果位置参数, 一般用 *args表示.
        2. 如果是关键字参数, 一般用 **kwargs       kw: keyword 关键字的意思.
        3. 可变参数用于形参, 表示可以接收任意个实参, 最少0个, 最多无数个.
"""


def list_merge(*args):
    """
    :param args: 待合并去重的列表，元素为字符串（不定长）
    :return: 返回合并后的结果
    """
    new_ls = []
    for item in args:
        item.sort(key=len, reverse=True)
        print(item)
        for i in range(len(item)):
            item[i] = item[i].replace(" ", "")
            item[i] = str_replace(item[i])
        new_ls += item
    new_ls = list(set(new_ls))
    new_ls.sort(key=len)
    new_ls = list_remove_duplicate(new_ls)
    merge_str = ",".join(new_ls)
    return merge_str


"""列表除去包含关系元素"""
"""
for i in range(len(iterator))不会动态检查被迭代对象的长度
for item in iterator和for index,value in enumerate(iterator)会动态检查迭代对象的长度
"""


def list_remove_duplicate(self: list):
    """
    :param self: 按元素长度升序排列的列表
    :return: 去重后的列表
    """
    for index, item in enumerate(self):
        if index > 0:
            if operator.contains(item, self[index - 1]):
                self.remove(self[index - 1])
            if operator.eq(item.lower(), self[index - 1].lower()):
                self.remove(self[index - 1])
    return self


"""图片转base64格式"""


def image_to_base64(path):
    f = open(path, 'rb')
    imagebytes = base64.b64encode(f.read())
    f.close()
    imagestr = str(imagebytes)
    # 转成base64后的字符串格式为 b'图片base64字符串'，前面多了 b'，末尾多了 '，所以需要截取一下
    realimagestr = "\"" + imagestr[2:len(imagestr) - 1] + "\""
    return realimagestr


"""中文符号转英文符号"""


def str_replace(data):
    """ 把写错的中文符号都替换成英文 """
    china_tab = ['：', '；', '，', '。', '！', '？', '【', '】', '“', '（', '）', '%', '#', '@', '&', "‘", ' ', '\n', '”']
    english_tab = [':', ';', ',', '.', '!', '?', '[', ']', '"', '(', ')', '%', '#', '@', '&', "'", ' ', '', '"']
    for index in range(len(china_tab)):
        if china_tab[index] in data:
            data = data.replace(china_tab[index], english_tab[index])
    return data


"""--------------------------------------------------------------------------------------------"""

if __name__ == '__main__':
    # s = time.perf_counter()
    print(integrated_ocr(img_path="../../media/m3_restoration.png"))
    # e = time.perf_counter()
    # print(e - s)
    # print(list_remove_duplicate(["fancs", "fancai", "request", "requestment"]))
