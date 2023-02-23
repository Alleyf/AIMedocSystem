from haystack.utils import Highlighter

from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer, HighlighterMixin

from .models import DocTxt
from .search_indexes import *


class DocTxtSerializer(serializers.ModelSerializer):
    """
    序列化器
    """

    # 对外键的序列化
    # user = serializers.CharField(source='user.username')

    class Meta:
        model = DocTxt
        # 返回除了搜索字段外的所需要的其他字段数据, 可以将所有需要返回的字段数据写上,便于提取
        # fields = ('id', 'name', 'user', 'content')
        fields = ('id', 'doc_name', 'page_id')


class DocImgTxtSerializer(serializers.ModelSerializer):
    """
    序列化器
    """

    # 对外键的序列化
    # user = serializers.CharField(source='user.username')

    class Meta:
        model = DocImgTxt
        # 返回除了搜索字段外的所需要的其他字段数据, 可以将所有需要返回的字段数据写上,便于提取
        # fields = ('id', 'name', 'user', 'content')
        fields = ('id', 'doc_name', 'page_id', 'page_img_num')


# 写法一:普通序列化,使用内置的高亮
class DocTxtIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """

    # 变量名称必须为 object 否则无法返回
    # 变量名称必须为 object 否则无法返回,
    # 返回除搜索字段以外的字段,由上面DocTxtSerializer自定义返回字段
    object = DocTxtSerializer(read_only=True)  # 只读,不可以进行反序列化

    class Meta:
        index_classes = [DocTxtIndex, DocImgTxtIndex]  # 索引类的名称,可以有多个

        # text 由索引类进行返回, object 由序列化类进行返回,第一个参数必须是text
        # 返回字段,不写默认全部返回
        # text字段必须有,不然无法实现搜索
        # 控制的是建立的索引字段
        fields = ['text', object]
        # fields = ['text']
        # 忽略字段
        # ignore_fields = ['title']
        # 排除字段，除了该字段,其他的都返回,
        # exclude = ['title']

#
# # 写法二:自定义高亮,比内置的要慢一点
# class DocTxtIndexSerializer(HighlighterMixin, HaystackSerializer):
#     """
#     SKU索引结果数据序列化器
#     """
#     # 变量名称必须为 object 否则无法返回,
#     # 返回除搜索字段以外的字段,由上面ArticleSerializer自定义返回字段
#     object = DocTxtSerializer(read_only=True)  # 只读,不可以进行反序列化
#     # 高亮显示字段配置
#     # highlighter_class = Highlighter
#     # 前端自定义css名称
#     highlighter_css_class = "my-highlighter-class"
#     # html
#     highlighter_html_tag = "em"
#     # 最宽
#     highlighter_max_length = 200
#
#     class Meta:
#         index_classes = [DocTxtIndex]  # 索引类的名称,可以有多个
#         fields = ['text', object]
