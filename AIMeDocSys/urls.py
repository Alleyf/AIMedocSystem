"""StaffingSystem URL Configuration"""
from django.conf import settings
# from django.conf import settings  ##新增
from django.conf.urls import url  ## 新增
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.routers import SimpleRouter
# 导入restframework的辅助函数get_schema_view
from rest_framework.schemas import get_schema_view

# 导入swagger的两个Render类
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from medocsys.views import user, account, doc, chart, search, img, medocrobot

# 利用get_schema_view()方法，传入两个Render类得到一个schema view
schema_view = get_schema_view(title='API', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])
router = SimpleRouter()
# router.register('search/txt', search.DocTxtSearchViewSet, basename='searchtxt_api')
# router.register('search/imgtxt', search.DocImgTxtSearchViewSet, basename='searchimgtxt_api')
# router.register('checkcode', account.checkimgcode, basename='checkcode_api')
urlpatterns = [
    # 访问localhost:8000/docs/即可
    path('docs/', schema_view, name="swagger接口文档"),
    url(r'^admin/', admin.site.urls),
    url(r'^images/(?P<path>(.+))/$', img.images),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}, name='static'),  # 新增的路径
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # *********************用户*********************
    # path("user/list/", user.user_list),
    # path("user/modelform/add/", user.user_add),
    path("user/<int:nid>/edit/", user.user_info),
    # path("user/<int:nid>/delete/", user.user_delete),
    # *********************首页*********************
    path("index/", account.index),
    # *********************注册和登录*********************
    # 登录
    path("login/", account.login),
    # 注册
    path("register/", account.register),
    # 注销
    path("logout/", account.logout),
    # 图片验证码
    path("checkimgcode/", account.checkimgcode),
    # 邮箱验证码
    path("checkcode/", account.checkcode_email),
    # *********************机器人助手*********************
    path("chat/", medocrobot.chat),
    # *********************文档管理*********************
    # 文档列表
    path("doc/list/", doc.doc_list),
    # 添加文档(ajax异步上传)
    path("doc/add/", doc.doc_add),
    # # 添加文档(form同步上传)
    # path("doc/upload/", doc.doc_upload),
    # 删除文献
    path("doc/del/", doc.doc_del),
    # # 传递编辑信息
    # path("doc/edit/details", doc.doc_edit_details),
    # # 编辑文献
    # path("doc/edit/", doc.doc_edit),
    # 查看文献
    path("doc/view/", doc.doc_view),
    # 查看文献具体信息
    path("doc/details/", doc.doc_details),
    # 基于ajax异步请求没有反馈分
    # path("doc/search/", doc.doc_search),
    # 基于form同步请求有反馈分
    path("doc/query/", doc.doc_query),
    # 点赞接口
    path("doc/<int:nid>/thumbup/", doc.doc_thumbup),
    # 点踩接口
    path("doc/<int:nid>/thumbdown/", doc.doc_thumbdown),
    # 点击量接口
    path("doc/<int:nid>/clk/", doc.doc_clk),
    # 获取知网数据接口
    path("doc/external/", doc.doc_external),
    # 搜索文献
    # url(r'^search/', doc.MySearchView()),
    # re_path(r'search_one/(?P<pk>\d+)/', search.DocTxtSearchViewSet.as_view({'get': 'retrieve'})),
    # path('search/', search.DocTxtSearchViewSet.as_view({'get': 'list'})),
    # *********************数据可视化*********************
    path("chart/list/", chart.chart_list),
    # 柱状图接口
    path("chart/bar/", chart.chart_bar),
    # 饼状图接口
    path("chart/pie/", chart.chart_pie),
    # 折线图接口1
    path("chart/line/", chart.chart_line),
    # 医学知识图谱
    path("chart/graph/all/", chart.medicine_search_all),
    path("chart/graph/<str:value>/", chart.medicine_search_one),
    path("chart/graph/", chart.index),
]

urlpatterns += router.urls
