import os

from django.contrib import admin

from .models import MeDocs, User, DocTxt, DocImgTxt
# Register your models here.
from .utils.del_img import del_img
from .utils.encrypt import md5


# @admin.register(User)
# class UserAdmin(AjaxAdmin):
#     actions = ('upload_file',)
#
#     def upload_file(self, request, queryset):
#         # 这里的upload 就是和params中配置的key一样
#         upload = request.FILES['upload']
#         print(upload)
#         pass
#
#     upload_file.short_description = '文件上传对话框'
#     upload_file.type = 'success'
#     upload_file.icon = 'el-icon-upload'
#     upload_file.enable = True
#
#     upload_file.layer = {
#         'params': [{
#             'type': 'file',
#             'key': 'upload',
#             'label': '文件'
#         }]
#     }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_per_page = 10
    list_max_show_all = 10
    search_fields = ("username",)
    preserve_filters = True

    # exclude = ("code", "confirm_password")
    # form = UserModelForm

    def save_model(self, request, obj, form, change):
        # print(len(obj.password), obj, obj.password)
        if len(obj.password) != 32:
            obj.password = md5(obj.password)
        # print(len(obj.password), obj, obj.password)
        super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(MeDocs)
class MedocsAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    fields = ("name", ("clkscore", "fedbakscore"), "user", "language", "date", "category")
    list_per_page = 10
    list_max_show_all = 10
    search_fields = ("name",)
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        if request.FILES.get("docfile"):
            name = request.FILES.get("docfile").name.replace(" ", "_")
            # print(self, name, obj.docfile.name)
            obj.name = name[:-4]
        # print(obj.name)
        super(MedocsAdmin, self).save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        # print("当前删除的对象为", queryset)
        DocTxt.objects.filter(doc_name__contains=queryset[0].name).all().delete()
        DocImgTxt.objects.filter(doc_name__contains=queryset[0].name).all().delete()
        url = "./media/docs/" + queryset[0].name + ".pdf"
        # print(url, os.path.exists(url))
        if os.path.exists(url):
            os.remove(url)
        del_img(img_name=queryset[0].name)
        super(MedocsAdmin, self).delete_queryset(request, queryset)
        os.system('python ./manage.py rebuild_index --noinput')


@admin.register(DocTxt)
class DocTxtAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_max_show_all = 10
    search_fields = ("doc_name",)

    def delete_model(self, request, obj):
        # print("当前删除的对象为", obj)
        os.system('python ./manage.py rebuild_index --noinput')
        super(DocTxtAdmin, self).delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # print("当前删除的对象为", queryset)
        super(DocTxtAdmin, self).delete_queryset(request, queryset)
        os.system('python ./manage.py rebuild_index --noinput')


@admin.register(DocImgTxt)
class DocImgTxtAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_per_page = 10
    list_max_show_all = 10
    search_fields = ("doc_name",)

    def delete_model(self, request, obj):
        # print(obj)
        os.system('python ./manage.py rebuild_index --noinput')
        super(DocImgTxtAdmin, self).delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # print("当前删除的对象为", queryset)
        super(DocImgTxtAdmin, self).delete_queryset(request, queryset)
        os.system('python ./manage.py rebuild_index --noinput')


admin.site.site_header = "智检慧医——后台管理"
admin.site.site_title = "智检慧医——后台管理"
admin.site.index_title = "智检慧医——后台管理首页"
# 分页，每页显示条数
list_per_page = 5

# 分页，显示全部（真实数据<该值时，才会有显示全部）
list_max_show_all = 10

list_editable = ("username", "password", "name", "avatar")

save_as_continue = True
