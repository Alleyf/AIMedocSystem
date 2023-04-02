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

"""--------------------------------------��ȡͼƬ�е�������Ϣ-------------------------------------"""

""" **********************************Paddleʶ��API***********************************"""


def paddle_ocr(img_path):
    """
    :param img_path: ��ʶ���ͼƬ·��
    :return: ͼƬʶ����ı����
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


""" **********************************��Ѷ��ʽʶ��API***********************************"""

# def tencent_ocr_formula(imgpath, Id="AKIDbCkEezGTbecVJ4kLsKhzRo6KTXYYTJ4k", Key="dAc6Umz674vgMwSsDTdhgZN5hDezENRQ"):
#     try:
#         # ʵ����һ����֤���������Ҫ������Ѷ���˻�secretId��secretKey,�˴�����ע����Կ�Եı���
#         # ��Կ��ǰ��https://console.cloud.tencent.com/cam/capi��վ���л�ȡ
#         cred = credential.Credential(Id, Key)
#         base_str = image_to_base64(imgpath)
#         # ʵ����һ��httpѡ���ѡ�ģ�û�����������������
#         httpProfile = HttpProfile()
#         httpProfile.endpoint = "ocr.tencentcloudapi.com"
#
#         # ʵ����һ��clientѡ���ѡ�ģ�û�����������������
#         clientProfile = ClientProfile()
#         clientProfile.httpProfile = httpProfile
#         # ʵ����Ҫ�����Ʒ��client����,clientProfile�ǿ�ѡ��
#         client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
#
#         # ʵ����һ���������,ÿ���ӿڶ����Ӧһ��request����
#         req = models.FormulaOCRRequest()
#         params = {
#             "ImageBase64": base_str
#         }
#         req.from_json_string(json.dumps(params))
#
#         # ���ص�resp��һ��FormulaOCRResponse��ʵ��������������Ӧ
#         resp = client.FormulaOCR(req)
#         result = resp.to_json_string()
#         res = json.loads(result)
#         # ����json��ʽ���ַ����ذ�->Latex��ʽ
#         return res['FormulaInfos'][0]['DetectedText']
#
#     except TencentCloudSDKException as err:
#         return err


""" **********************************��Ѷ����ʶ��API***********************************"""


def tencent_ocr_geberaltext(imgpath, Id="AKIDbCkEezGTbecVJ4kLsKhzRo6KTXYYTJ4k", Key="dAc6Umz674vgMwSsDTdhgZN5hDezENRQ"):
    try:
        # ʵ����һ����֤���������Ҫ������Ѷ���˻�secretId��secretKey,�˴�����ע����Կ�Եı���
        # ��Կ��ǰ��https://console.cloud.tencent.com/cam/capi��վ���л�ȡ
        cred = credential.Credential(Id, Key)
        base_str = image_to_base64(imgpath)
        # ʵ����һ��httpѡ���ѡ�ģ�û�����������������
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # ʵ����һ��clientѡ���ѡ�ģ�û�����������������
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # ʵ����Ҫ�����Ʒ��client����,clientProfile�ǿ�ѡ��
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        # ʵ����һ���������,ÿ���ӿڶ����Ӧһ��request����
        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageBase64": base_str
        }
        req.from_json_string(json.dumps(params))

        # ���ص�resp��һ��GeneralAccurateOCRResponse��ʵ��������������Ӧ
        resp = client.GeneralAccurateOCR(req)
        # ���json��ʽ���ַ����ذ�
        result = resp.to_json_string()
        # תΪ�ֵ䲢����
        res = json.loads(result)
        # ������ȡ�ı�
        text = []
        for item in res['TextDetections']:
            text.append(item["DetectedText"])
        # res_txt = ",".join(text)
        return text
    except TencentCloudSDKException as err:
        # return err
        return []


""" **********************************����ʶ��API***********************************"""

"""
PaddleocrĿǰ֧����Ӣ�ġ�Ӣ�ġ�����������������ͨ���޸�lang���������л�
��������Ϊ`ch`, `en`, `french`, `german`, `korean`, `japan`��
"""


def local_ocr(img_path):
    """
    :param img_path:��ʶ���ͼƬ·��
    :return: ʶ���ı����
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
    # # ��ʾ���
    # from PIL import Image
    #
    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
    # im_show = Image.fromarray(im_show)
    # im_show.save('result.jpg')


""" **********************************�ۺ�ʶ��API***********************************"""


def integrated_ocr(img_path: str):
    """
    :param img_path: ��ʶ���ͼƬ·��
    :return: ����ʶ�����ۺϺ�Ľ��
    """

    paddle_txt = paddle_ocr(img_path)  # �нϴ������
    tencent_txt = tencent_ocr_geberaltext(img_path)
    local_txt = local_ocr(img_path)

    # merge_txt = list_merge("paddle", paddle_txt)
    merge_txt = list_merge(tencent_txt, local_txt, paddle_txt)
    # print("�ɽ�API�����", paddle_txt)
    # print("��ѶAPI�����", tencent_txt)
    # print("����API�����", local_txt)
    # print("�ϲ���Ľ����", merge_txt)

    return merge_txt


""" **********************************��������**************************************"""

"""�ַ����ϲ���ȥ��"""
"""
����:
        ����������Ҳ�пɱ����, ��: �����ĸ����ǿɱ��.
    ��ʽ:
        ���β�����ǰ��д�� *args, ���� **kwargs,
        ����� * ���ʾ���Խ������е� λ�ò���, �γ�Ԫ��.
        ����� ** ���ʾ���Խ������е� �ؼ��ֲ���, �γ��ֵ�.
    ϸ��:
        1. ���λ�ò���, һ���� *args��ʾ.
        2. ����ǹؼ��ֲ���, һ���� **kwargs       kw: keyword �ؼ��ֵ���˼.
        3. �ɱ���������β�, ��ʾ���Խ��������ʵ��, ����0��, ���������.
"""


def list_merge(*args):
    """
    :param args: ���ϲ�ȥ�ص��б�Ԫ��Ϊ�ַ�������������
    :return: ���غϲ���Ľ��
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


"""�б��ȥ������ϵԪ��"""
"""
for i in range(len(iterator))���ᶯ̬��鱻��������ĳ���
for item in iterator��for index,value in enumerate(iterator)�ᶯ̬����������ĳ���
"""


def list_remove_duplicate(self: list):
    """
    :param self: ��Ԫ�س����������е��б�
    :return: ȥ�غ���б�
    """
    for index, item in enumerate(self):
        if index > 0:
            if operator.contains(item, self[index - 1]):
                self.remove(self[index - 1])
            if operator.eq(item.lower(), self[index - 1].lower()):
                self.remove(self[index - 1])
    return self


"""ͼƬתbase64��ʽ"""


def image_to_base64(path):
    f = open(path, 'rb')
    imagebytes = base64.b64encode(f.read())
    f.close()
    imagestr = str(imagebytes)
    # ת��base64����ַ�����ʽΪ b'ͼƬbase64�ַ���'��ǰ����� b'��ĩβ���� '��������Ҫ��ȡһ��
    realimagestr = "\"" + imagestr[2:len(imagestr) - 1] + "\""
    return realimagestr


"""���ķ���תӢ�ķ���"""


def str_replace(data):
    """ ��д������ķ��Ŷ��滻��Ӣ�� """
    china_tab = ['��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '%', '#', '@', '&', "��", ' ', '\n', '��']
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
