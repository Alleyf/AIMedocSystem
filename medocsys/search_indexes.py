# 索引模型类的名称必须是 模型类名称 + Index
from haystack import indexes
from .models import DocTxt, DocImgTxt


# 必须继承  indexes.SearchIndex, indexes.Indexable
class DocTxtIndex(indexes.SearchIndex, indexes.Indexable):
    # 以下的字段，是es里面对应的字段
    # 第一个必须这样写
    text = indexes.CharField(document=True, use_template=True)

    # 下面的就是和你model里面的一样了
    id = indexes.IntegerField(model_attr='id')
    page_id = indexes.IntegerField(model_attr='page_id')
    doc_name = indexes.CharField(model_attr='doc_name')

    #  必须这个写，返回的就是你的model名称
    def get_model(self):
        """返回建立索引的模型类"""
        return DocTxt

    # 返回你的查询的结果，可以改成一定的条件的，但是格式就是这样
    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        # 写入es的数据
        query_set = self.get_model().objects.all()
        return query_set


class DocImgTxtIndex(indexes.SearchIndex, indexes.Indexable):
    # 以下的字段，是es里面对应的字段
    # 第一个必须这样写
    text = indexes.CharField(document=True, use_template=True)

    # 下面的就是和你model里面的一样了
    id = indexes.IntegerField(model_attr='id')
    doc_name = indexes.CharField(model_attr='doc_name')
    page_id = indexes.IntegerField(model_attr='page_id')
    page_img_num = indexes.IntegerField(model_attr='page_img_num')

    #  必须这个写，返回的就是你的model名称
    def get_model(self):
        """返回建立索引的模型类"""
        return DocImgTxt

    # 返回你的查询的结果，可以改成一定的条件的，但是格式就是这样
    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        # 写入es的数据
        query_set = self.get_model().objects.all()
        return query_set
