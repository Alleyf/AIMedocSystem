import os

from django.contrib import admin

from .models import MeDocs, User, DocTxt, DocImgTxt
# Register your models here.
from .utils.encrypt import md5


# admin.site.register(MeDocs)
# admin.site.register(DocTxt)
# admin.site.register(DocImgTxt)


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
        print(len(obj.password), obj, obj.password)
        super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(MeDocs)
class MedocsAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    fields = (("clkscore", "fedbakscore"), "user", "language", "date", "docfile")
    list_per_page = 10
    list_max_show_all = 10
    search_fields = ("name",)
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        name = request.FILES.get("docfile").name.replace(" ", "_")
        # print(self, name, obj.docfile.name)
        obj.name = name[:-4]
        # print(obj.name)
        super(MedocsAdmin, self).save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        # print("当前删除的对象为", queryset)
        DocTxt.objects.filter(doc_name__contains=queryset[0].name).all().delete()
        DocImgTxt.objects.filter(doc_name__contains=queryset[0].name).all().delete()
        super(MedocsAdmin, self).delete_queryset(request, queryset)
        os.system('python ./manage.py rebuild_index --noinput')


@admin.register(DocTxt)
class DocTxtAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
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


admin.site.site_header = "医道有易——后台管理"
admin.site.site_title = "医道有易——后台管理"
admin.site.index_title = "医道有易——后台管理首页"
# 分页，每页显示条数
list_per_page = 5

# 分页，显示全部（真实数据<该值时，才会有显示全部）
list_max_show_all = 10

list_editable = ("username", "password", "name", "avatar")

save_as_continue = True
