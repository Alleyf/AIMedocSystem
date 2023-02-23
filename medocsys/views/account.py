import re
from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect

from medocsys.models import User
from medocsys.utils.code import check_code
from medocsys.utils.form import LoginForm, RegisterModelForm


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功,获取输入信息
        # {'username': 'alleyf', 'password': '123', 'code': 'csfd'}
        # 验证码校验,取出并出栈验证码，防止后面校验多出数据库中没有的验证码
        usr_input_code = form.cleaned_data.pop('code')
        checkcode = request.session.get('checkcode', '')
        if checkcode.lower() != usr_input_code.lower():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        # 去数据库校验用户名和密码是否存在且正确
        usrobj = User.objects.filter(**form.cleaned_data).first()
        if usrobj:
            # 用户名和密码正确
            # 构建session信息
            # 取出用户的头像名
            pattern = re.compile('/.+')  # 匹配从ab开始，到ef结束的内容
            avatar_name1 = pattern.findall(usrobj.avatar.name)
            pattern = re.compile('/.+/')
            avatar_name2 = pattern.findall(usrobj.avatar.name)
            print(avatar_name1)
            if not avatar_name1:
                avatar_name = usrobj.avatar.name
            elif not avatar_name2:
                avatar_name = avatar_name1[0].replace("/", '')
            else:
                avatar_name = avatar_name1[0].replace(avatar_name2[0], '')
            print(usrobj.avatar.name, avatar_name)
            request.session["info"] = {"id": usrobj.id, "name": usrobj.username, "avatar": avatar_name}
            # 设置用户信息保存7天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect("/doc/query/")
        form.add_error("username", "用户名或密码错误")
        return render(request, "login.html", {'form': form})
    return render(request, "login.html", {'form': form})


def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {'form': form})
    now = datetime.now()
    # avatarname = now.strftime("%Y%m%d%H%M%S")
    # print(type(request.POST), request.POST)
    form = RegisterModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 验证码校验,取出并出栈验证码，防止后面校验多出数据库中没有的验证码
        usr_input_code = form.cleaned_data.pop('code')
        checkcode = request.session.get('checkcode', '')
        if checkcode.lower() != usr_input_code.lower():
            form.add_error('code', '验证码错误')
            return render(request, 'register.html', {'form': form})
        if request.FILES:
            # form.instance.avatar.name = "images/avatars/" + avatarname + ".png"
            # 修改用户头像名
            print(request.FILES['avatar'].name)
            form.instance.avatar.name = request.FILES['avatar'].name
        form.save()
        return redirect('/login/')
    else:
        return render(request, "register.html", {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    request.session.flush()
    return redirect("/login/")


def checkcode(request):
    """图片验证码"""
    # 调用函数生成图片验证码
    img, code = check_code()
    # 将验证码写入到自己的session中(以便于后续校验)
    request.session['checkcode'] = code
    # 给session设置有效时长为60s
    request.session.set_expiry(60)
    # 将图片写入内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
