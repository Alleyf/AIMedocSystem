"""--------------------------------------自定义分页组件类------------------------------------"""
"""-----------------------------------------信息栏------------------------------------------"""
"""datetime: 2022-12-15 1:13"""
"""author:   Alleyf"""
"""email:    alleyf@qq.com"""
"""-------------------------------------views.py使用教程-------------------------------------"""
"""
def phone_list(request):
    # 1.搜索参数初始化
    search_dict = {}
    # 获取号码搜索参数
    search_data = request.GET.get(key="m", default='')
    if search_data:
        search_dict['mobile__contains'] = search_data
    # 2.页码参数初始化
    pagesize = 10
    pageplus = 5
    # 3.筛选符合条件的数据
    queryset = models.PrettyNum.objects.filter(**search_dict).order_by('-level')
    # 4.实例化页面对象
    page_obj = pagination.Pagination(request, query_set=queryset, page_size=pagesize, page_plus=pageplus)
    # 5.获取页面数据
    page_queryset = page_obj.page_queryset
     # 6.获取分页展示所需的信息
    # 6.1方法一：获取django模板信息
    # pagels, pageinfo = page_obj.djangotemplateinfo()
    # context = {
    #     页面数据信息
    #     'page_queryset': page_queryset,
    #     搜索参数    
    #     'search_data': search_data,
    #     页码标号    
    #     'pagels': pagels,
    #     当前及前后页信息
    #     'pageinfo': pageinfo
    # }
    # return render(request, 'phone_list.html',context)
    # 6.2方法二：获取html字符串
    page_str = page_obj.htmlstr()
    context = {
    #     页面数据信息
        'page_queryset': page_queryset,
    #     搜索参数         
        'search_data': search_data,
    #     分页html字符串组件 
        'page_str': page_str
    }
    return render(request, 'phone_list.html', context)
"""
"""-------------------------------------前端页面使用教程-------------------------------------"""
"""
        <div class="text-center">
            <ul class="pagination pagination-xs">
                {#                方法二对应的分页展示方法#}
                                    {{ page_str }}
                {#                方法一对应的分页展示方法#}
                {#                <li>#}
                {#                    <a href="?page={{ pageinfo.lpage }}&&m={{ search_data }}"><i class="fa fa-less-than"></i></a>#}
                {#                </li>#}
                {#                {% for page in pagels %}#}
                {#                    {% if page != pageinfo.nowpage %}#}
                {#                        <li>#}
                {#                            <a href="?page={{ page }}&&m={{ search_data }}">{{ page }}</a>#}
                {#                        </li>#}
                {#                    {% else %}#}
                {#                        <li class="active">#}
                {#                            <a href="?page={{ page }}&&m={{ search_data }}">{{ page }}</a>#}
                {#                        </li>#}
                {#                    {% endif %}#}
                {#                {% endfor %}#}
                {#                <li>#}
                {#                    <a href="?page={{ pageinfo.npage }}&&m={{ search_data }}"><i class="fa fa-greater-than"></i></a>#}
                {#                </li>#}
                {#                <li style="width: 150px;float: right">#}
                {#                    <form method="get">#}
                {#                        <div class="input-group">#}
                {#                            <input type="text" name="page"#}
                {#                                   placeholder="Search for ···"#}
                {#                                   class="form-control"#}
                {#                                   value={{ pageinfo.nowpage }}>#}
                {#                            <span class="input-group-btn">#}
                {#                        <button class="btn btn-default"><i class=" fa-brands fa-airbnb"></i> </button>#}
                {#                        </span>#}
                {#                        </div>#}
                {#                    </form>#}
                {#                </li>#}
            </ul>
        </div>
"""
"""----------------------------------------分页类定义---------------------------------------"""
from django.utils.safestring import mark_safe  # 确保html字符串安全
import copy  # 深拷贝


class Pagination(object):
    """构造函数"""

    def __init__(self, request, query_set, page_size=10, page_param='page', page_plus=2):
        """
        :param request: 请求的对象
        :param query_set: 符合条件的查询的数据
        :param page_size: 每页展示的数据量
        :param page_param: 在url中获取分页参数 eg:/phone/list/?page=10
        :param page_plus:   显示当前页的前后几页（页码）
        """
        page = request.GET.get(key=page_param, default="1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict  # url的get参数
        self.page = page
        self.page_size = page_size
        self.page_param = page_param
        self.page_plus = page_plus
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = query_set[self.start:self.end]
        self.total_cnt = query_set.count()
        total_page_cnt, remainder = divmod(self.total_cnt, page_size)
        if remainder:
            total_page_cnt += 1
        self.total_page_cnt = total_page_cnt

    """方法1：Django模板法"""

    def djangotemplateinfo(self):
        # 显示当前页的前两页和后两页页码增量为2
        pagels = []
        pagestart = self.page - self.page_plus
        pageend = self.page + self.page_plus
        # 若总页数小于5时
        if self.total_page_cnt < 5:
            pagestart = 1
            pageend = self.total_page_cnt
        # 若总页数大于等于5
        else:
            # 若当前页小于等于页码增量
            if self.page <= self.page_plus:
                pagestart = 1
                pageend = 2 * self.page_plus + 1
            # 若当前页尾大于总页数
            elif pageend > self.total_page_cnt:
                pagestart -= self.page_plus
                pageend = self.total_page_cnt
            # 正常情况下
            else:
                pagestart = self.page - self.page_plus
                pageend = self.page + self.page_plus
        # 生成页码标号
        for i in range(pagestart, pageend + 1):
            pagels.append(i)
        # 当前页和其前后页信息
        pageinfo = {'nowpage': self.page, 'lpage': 1 if self.page <= 2 else self.page - 1,
                    'npage': pageend if self.page + 1 > pageend else self.page + 1, 'total_page': self.total_page_cnt}
        return pagels, pageinfo

    """方法2：HTML字符串法"""

    def htmlstr(self):
        # 显示当前页的前两页和后两页页码增量为2
        self.start = self.page - self.page_plus
        self.end = self.page + self.page_plus
        # 若总页数小于5时
        if self.total_page_cnt < 5:
            self.start = 1
            self.end = self.total_page_cnt
        # 若总页数大于等于5
        else:
            # 若当前页小于等于页码增量
            if self.page <= self.page_plus:
                self.start = 1
                self.end = 2 * self.page_plus + 1
            # 若当前页尾大于总页数
            elif self.end > self.total_page_cnt:
                self.start -= self.page_plus
                self.end = self.total_page_cnt
            # 正常情况下
            else:
                self.start = self.page - self.page_plus
                self.end = self.page + self.page_plus

        # 生成页码
        page_str_ls = []
        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_ls.append(
            '<li class="page-item"><a class="page-link" href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        self.query_dict.setlist(self.page_param, [self.page - 1])
        if self.page > 1:
            prev = '<li class="page-item"><a class="page-link" href="?{}"><i class="fa fa-less-than"></i></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li class="page-item"><a class="page-link" href="?{}"><i class="fa fa-less-than"></i></a></li>'.format(
                self.query_dict.urlencode())
        page_str_ls.append(prev)
        # 页面
        for i in range(self.start, self.end + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active page-item"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_ls.append(ele)
        # 下一页
        self.query_dict.setlist(self.page_param, [self.page + 1])
        if self.page < self.total_page_cnt:
            nxt = '<li class="page-item"><a class="page-link" href="?{}"><i class="fa fa-greater-than"></i></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_cnt])
            nxt = '<li class="page-item"><a class="page-link" href="?{}"><i class="fa fa-greater-than"></i></a></li>'.format(
                self.query_dict.urlencode())
        page_str_ls.append(nxt)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_cnt])
        page_str_ls.append(
            '<li class="page-item"><a class="page-link" href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        search_string = """
        <li class="page-item" style="width: 150px;float: right">
                <form method="get">
                    <div class="input-group">
                        <input type="text" name="page"
                                   placeholder="Page"
                                   class="form-control"
                                   value={}>
                        <span class="input-group-btn">
                        <button class="btn btn-outline-primary" type="button"><i class=" fa-brands fa-airbnb"></i> </button>
                        </span>
                    </div>
                </form>
        </li>
        """.format(self.page)
        page_str_ls.append(search_string)
        page_str = mark_safe("".join(page_str_ls))
        return page_str


"""----------------------------------------分割结束符---------------------------------------"""
