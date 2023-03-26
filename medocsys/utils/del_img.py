import os
import re


def del_img(img_name: str) -> bool:
    try:
        img_url = "./media/docimgs/"
        repattern = r'-'
        # 遍历当前路径下所有文件
        file = os.listdir(img_url)
        for f in file:
            # 字符串拼接
            img = re.split(repattern, f)[0]
            if img == img_name:
                os.remove(img_url + f)
                # 打印出来
                print("删除了", f)
                return True
    except Exception as e:
        print(e)
        return False
