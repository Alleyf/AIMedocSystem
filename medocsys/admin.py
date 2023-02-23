from django.contrib import admin

from .models import MeDocs, User, DocTxt, DocImgTxt

# Register your models here.
admin.site.register(MeDocs)
admin.site.register(User)
admin.site.register(DocTxt)
admin.site.register(DocImgTxt)

# 分页，每页显示条数
list_per_page = 5

# 分页，显示全部（真实数据<该值时，才会有显示全部）
list_max_show_all = 10

search_fields = ("username", "password", "name")

list_editable = ("username", "password", "name", "avatar")

date_hierarchy = 'create_time'

preserve_filters = True

save_as_continue = True
