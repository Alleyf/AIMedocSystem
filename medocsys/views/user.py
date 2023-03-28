from django.contrib import messages
from django.shortcuts import render, redirect
from medocsys import models
from medocsys.models import User
from medocsys.utils import pagination
from medocsys.utils.form import UserModelForm, RstModelForm

"""***********************用户函数***********************"""


def user_list(request):
    """用户管理"""
    # 生成测试数据
    # for i in range(200):
    #     models.UserInfo.objects.create(name="alleyf", password="123456", age=20, account=2000,
    #                                    create_time="2022-12-15", gender=1, depart_id=1)
    queryset = models.User.objects.all()
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'queryset': page_obj.page_queryset,
        'page_str': page_obj.htmlstr()
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """添加用户modelform版"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_modelform_add.html', {'form': form})
    # 用户提交数据,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法,则保存数据并添加到表中
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_modelform_add.html', {'form': form})


def user_delete(request, nid):
    """删除用户"""
    models.User.objects.filter(id=nid).first().delete()
    return redirect('/user/list/')


def user_info(request, nid):
    rowobj = User.objects.filter(id=nid).first()
    if request.method == "GET":
        # （instance=rowobj）将默认数据显示在表单中
        form = RstModelForm(instance=rowobj)
        return render(request, 'user_edit.html', {'form': form})
    print(request.FILES)
    form = RstModelForm(data=request.POST, instance=rowobj, files=request.FILES)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据,如果想要再保存用户输入以外的字段的值
        # form.instance.字段名 = 值
        form.save()
        avatar_name = request.FILES.get('avatar')
        if avatar_name:
            request.session['info']['avatar'] = avatar_name.name
            print(form.cleaned_data, request.session['info']['avatar'])
            request.session.set_expiry(60 * 60 * 24 * 7)
        # print(request.session.info.avatar, request.FILES.get('avatar').name)
        # request.session['info']['avatar'] = request.FILES.get('avatar').name
        # messages.success(request, "用户信息修改成功")
        # return render(request, 'user_edit.html', {'form': form})
        return redirect('/doc/query/')
    else:
        messages.success(request, "用户信息修改失败")
        return render(request, 'user_edit.html', {'form': form})
