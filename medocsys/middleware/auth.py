from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LoginAuth(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):
        # 1.排除哪些不需要登录的页面
        # request.path_info获取当前用户请求的url
        # print("当前访问的路由为" + request.path_info)
        if request.path_info in ["/index/", "/login/", '/register/', '/checkcode/', '/checkimgcode/']:
            return
        # 2.读取当前访问的用户的session信息,如果能读到,说明已登录鉴权,可以继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            if request.path_info == '/':
                # return render(request, "doc_query.html")
                return redirect('/chart/list/')
            return
        # 3.没有登录过,返回到登录界面
        # return redirect("/login/")
        return redirect("/index/")

    def process_response(self, request, response):
        usrname = request.session.get("info").get('name') if request.session.get("info") else "nobody"
        # print("{}.走了".format(usrname))
        return response
