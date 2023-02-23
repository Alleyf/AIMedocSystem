from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render


class LoginAuth(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):
        # 1.排除哪些不需要登录的页面
        # request.path_info获取当前用户请求的url
        print(request.path_info)
        if request.path_info in ["/login/", '/register/', '/checkcode/']:
            return
        # 2.读取当前访问的用户的session信息,如果能读到,说明已登录鉴权,可以继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            if request.path_info == '/':
                return render(request, "doc_query.html")
            return
        # 3.没有登录过,返回到登录界面
        return redirect("/login/")

    def process_response(self, request, response):
        usrname = request.session.get("info").get('name') if request.session.get("info") else "nobody"
        # print("{}.走了".format(usrname))
        return response
