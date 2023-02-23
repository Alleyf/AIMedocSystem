import os

import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from medocsys.utils.query import query_elastics, query_elastics_fulltext


def trans_ch(txt):
    words = jieba.lcut(txt)
    newtxt = ''.join(words)
    return newtxt


def get_word_cloud(doc_name: str, content: str):
    # keyword = request.session['info']['keyword']
    # keyword = "心脏病"
    txt = content.replace('\n', "")
    txt = trans_ch(txt)
    mask = np.array(Image.open("./medocsys/static/images/background_default.jpg"))  # 将你的背景图片名与此句的"love.png"替换
    wordcloud = WordCloud(background_color="#10203d",
                          width=300,
                          height=240,
                          max_words=200,
                          max_font_size=80,
                          mask=mask,
                          contour_width=4,
                          contour_color='steelblue',
                          # font_path="../static/font/msyh.ttc"
                          font_path="./medocsys/static/font/msyh.ttc"
                          ).generate(txt)
    path = os.path.join('./media/wordcloud/', doc_name + '.png')
    print(path)
    if wordcloud.to_file(path):
        return path[1:], True
    return '', False


if __name__ == '__main__':
    # keyword = request.session['info']['keyword']
    # keyword = "心脏病"
    # doc_name, txt = query_elastics_fulltext(key=keyword)
    # print(doc_name, txt)
    get_word_cloud(keyword="fuzzy")
    # print(txt)
    # with open("wordCloud.txt", 'w') as f:
    #     f.write(txt)
