# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         图片模糊度计算
# Author:       Alleyf
# Date:         2023/4/5 9:30
# Description:
# -------------------------------------------------------------------------------
import argparse
from pathlib import Path
from traceback import format_exc

import cv2
import numpy as np


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def judge_deblur(img_name, input_path=r"../../media/"):
    """

    :param input_path: 待检测模糊度的图片的路径
    :param img_name: 待检测的图片名
    :return: 是否需要去模糊（True：去模糊；Flase：不去模糊）
    """
    # 设置参数
    fm = 120
    for file in Path(input_path).rglob("*" + img_name):
        # img_file = open(img_url, 'r', encoding='utf-8')  # 打开图像
        # print(img_url, file)
        # 拉普拉斯算子
        image = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        # print(image.ndim)
        # 黑白图（ndim=2）和RGB图单独处理（ndim=3）
        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # GGG
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        # Brenner 检测
        # frame = ImageToMatrix(file)
        # score = Brenner(frame)
        print(fm)
    return True if fm < 100 else False


if __name__ == '__main__':
    # print("Start...")
    # input_Folder = input("请输入源文件夹:")
    # output_Folder = input("请输入结果文件夹:")
    try:
        print(judge_deblur(img_name="m3.png"))
    except Exception as err:
        print(f"程序运行失败！！！请联系数据处理中心:{err}")
        print(format_exc())
