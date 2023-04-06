import os
import re
from io import BytesIO

from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page

from medocsys import models
from medocsys.models import User
from medocsys.utils.code import check_code
from medocsys.utils.form import LoginForm, RegisterModelForm
from medocsys.utils.get_random_strs import generate_random_str


# @gzip_page
def login(request):
    """登录"""
    if request.method == "GET":
        request.session.clear()
        request.session.flush()
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功,获取输入信息
        # {'username': 'alleyf', 'password': '123', 'code': 'csfd'}
        # 验证码校验,取出并出栈验证码，防止后面校验多出数据库中没有的验证码
        usr_input_code = form.cleaned_data.pop('code')
        checkcode = request.session.get('checkimgcode', '')
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
            # print(avatar_name1)
            if not avatar_name1:
                avatar_name = usrobj.avatar.name
            elif not avatar_name2:
                avatar_name = avatar_name1[0].replace("/", '')
            else:
                avatar_name = avatar_name1[0].replace(avatar_name2[0], '')
            # print(usrobj.avatar.name, avatar_name)
            request.session["info"] = {"id": usrobj.id, "name": usrobj.username, "avatar": avatar_name}
            # 设置用户信息保存7天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect("/chart/list/")
        form.add_error("username", "用户名或密码错误")
        return render(request, "login.html", {'form': form})
        # return render(request, "landing.html", {'form': form})
    return render(request, "login.html", {'form': form})


@csrf_exempt
def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {'form': form})
    # print(type(request.POST), request.POST)
    form = RegisterModelForm(data=request.POST, files=request.FILES)
    # print(request.POST, request.FILES)
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
            # print(request.FILES['avatar'].name)
            form.instance.avatar.name = request.FILES['avatar'].name
        form.save()
        return redirect('/login/')
    else:
        return render(request, "register.html", {'form': form})


# @gzip_page
def logout(request):
    """注销"""
    request.session.clear()
    request.session.flush()
    return redirect("/index/")


@gzip_page
@csrf_exempt
def checkcode_email(request):
    if request.method == "POST":
        # print(request.POST)
        email_des = request.POST.get('email')
        code = generate_random_str(randomlength=4)
        request.session['checkcode'] = code
        request.session.set_expiry(60)
        title = "智检慧医-注册验证码"
        contents = "您正在请求<strong>注册新账户</strong>的操作验证码, 您的验证码是:\n" + "<strong>" + code + "</strong>" + "\n请不要向其他人提供此验证码, 这可能使您的账户遭受攻击这是系统自动发送的邮件，请不要回复此邮件如果该验证码不是您本人请求的, 请忽略此邮件."
        email_src = "467807892@qq.com"
        status_code = send_mail(title, contents, email_src, [email_des])
        if status_code != 0:
            status = "发送成功"
        else:
            status = "发送失败"
        # print(status)
        # return JsonResponse({'status': status, 'code': code})
        return JsonResponse({'status': status})
    return redirect('/login/')


# @gzip_page
@csrf_exempt
def checkimgcode(request):
    """图片验证码"""
    # 调用函数生成图片验证码
    # print(request.method)
    img, code = check_code()
    # 将验证码写入到自己的session中(以便于后续校验)
    request.session['checkimgcode'] = code
    # 给session设置有效时长为60s
    request.session.set_expiry(60)
    # 将图片写入内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
    # if stream:
    #     return JsonResponse({'status': 200})
    # return JsonResponse({'status': 403})


# @cache_page(60 * 60 * 24 * 7)
def index(request):
    return render(request, "landing.html")


@csrf_exempt
def get_rank(request):
    queryset = models.User.objects.all().order_by('-read_num')
    users = []
    for item in queryset:
        upload_num = 0
        querysetdoc = models.MeDocs.objects.all()
        for doc in querysetdoc:
            if doc.user_id == item.pk:
                upload_num += 1
        user = {
            'avatar': "/media/" + item.avatar.name,
            'name': item.username,
            'read_num': item.read_num,
            'upload_num': upload_num,
            'register_date': item.register_date
        }
        users.append(user)
    context = {
        'status': 200,
        'rankinfo': users,
        'all_user': len(queryset)
    }
    # print(context)
    return JsonResponse(context)
