from rest_framework.pagination import PageNumberPagination


class DocTxtSearchPageNumberPagination(PageNumberPagination):
    """文章搜索分页器"""
    # 每页显示几条
    page_size = 10
    # 最大数量
    max_page_size = 5000
    # 前端自定义查询的数量，?size=10
    page_size_query_param = "size"
    # 查询参数
    page_query_param = "page"
