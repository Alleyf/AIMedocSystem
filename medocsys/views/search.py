from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackOrderingFilter, HaystackHighlightFilter

from .paginations import DocTxtSearchPageNumberPagination
from ..models import *
from ..serializers import DocTxtIndexSerializer


class DocTxtSearchViewSet(HaystackViewSet):
    """
    文章搜索
    """
    # index_models = [DocTxt]  # 表模型,可以添加多个
    index_models = [DocTxt]  # 表模型,可以添加多个
    serializer_class = DocTxtIndexSerializer
    # serializer_class = DocTxtIndexSerializer
    # serializer_class = PDFImageIndexSerializer
    pagination_class = DocTxtSearchPageNumberPagination

    # 高亮,排序
    # HaystackOrderingFilter:排序,
    # HaystackHighlightFilter:内置高亮,如果使用了方式自定义高亮,就不要配置这个了
    # filter_backends = [HaystackOrderingFilter, HaystackHighlightFilter]

    # ordering_fields = 'id'

    # """    """

    # 重写,自己可以构造数据
    def list(self, request, *args, **kwargs):
        response = super(DocTxtSearchViewSet, self).list(request, *args, **kwargs)
        # data = response.data
        # 本文修改返回数据,把返回的索引字段去掉,您可以根据自己的需求,把这一句注释掉
        # [item.pop('text') for item in data['results']]
        return response
