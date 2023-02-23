from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from medocsys import models
from medocsys.utils import bootstrapmodelform
from medocsys.utils.encrypt import md5


# class UserModelForm(bootstrapmodelform.BootStrapModelForm1):
#     name = forms.CharField(label="用户名", min_length=1)
#
#     # 数据库中的字段
#     class Meta:
#         model = models.UserInfo
#         fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-control input"}),
#             "create_time": forms.DateTimeInput(attrs={"class": " form-control input", "type": "datetime-local"}),
#         }


# class PhoneModelForm(bootstrapmodelform.BootStrapModelForm1):
#     # 验证：方式1
#     # pnumber = forms.CharField(
#     #     label="号码",
#     #     # 正则表达式校验格式
#     #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
#     # )
#
#     class Meta:
#         model = models.PrettyNum
#         # fields = "__all__" 展示所有字段
#         fields = ["mobile", "price", "level", "status"]
#         # exclude = ["字段名"] 排除某个字段
#
#     # 验证：方式2(钩子方法)
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#         exist = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
#         if exist:
#             raise ValidationError("手机号已存在")
#         elif len(txt_mobile) != 11:
#             # 验证不通过抛出异常
#             raise ValidationError("格式错误")
#             # 验证通过,返回用户输入值
#         return txt_mobile


# class EditPhoneModelForm(bootstrapmodelform.BootStrapModelForm1):
#     class Meta:
#         model = models.PrettyNum
#         # fields = "__all__" 展示所有字段
#         fields = ['mobile', 'price', 'level', 'status']
#         # exclude = ["字段名"] 排除某个字段
#
#     # 验证：方式2(钩子方法)
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#         exist = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=self.instance.pk).exists()
#         if exist:
#             raise ValidationError("手机号已存在")
#         elif len(txt_mobile) != 11:
#             # 验证不通过抛出异常
#             raise ValidationError("格式错误")
#             # 验证通过,返回用户输入值
#         return txt_mobile


class UserModelForm(bootstrapmodelform.BootStrapModelForm1):
    confirm_password = forms.fields.CharField(
        label="确认密码",
        max_length=64,
        # render_value=True使校验失败后值不被清空
        widget=forms.PasswordInput(render_value=True),
        # 正则表达式校验格式
        validators=[RegexValidator(r'^[\w]{6,16}$', '6~16位，包含大小写字母和数字的组合')],
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
        required=True
    )

    class Meta:
        model = models.User
        fields = ["username", "password", "confirm_password", "email", "code", 'avatar']
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control input"}, render_value=True),
            "avatar": forms.FileInput(attrs={"class": "images-circle"})
        }

    # 验证用户名是否已存在
    def clean_username(self):
        username = self.cleaned_data["username"]
        exist = models.User.objects.filter(username=username).exists()
        if exist:
            raise ValidationError("用户名已存在")
        # return什么数据库到时候保存的就是什么值
        return username

    # 对密码进行md5加密
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    # 验证密码是否一致
    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm = md5(self.cleaned_data["confirm_password"])
        if confirm != password:
            raise ValidationError("密码不一致")
        return confirm


class RstModelForm(bootstrapmodelform.BootStrapModelForm1):
    confirm_password = forms.fields.CharField(
        label="确认密码",
        max_length=64,
        # render_value=True使校验失败后值不被清空
        widget=forms.PasswordInput(render_value=False),
        # 正则表达式校验格式
        validators=[RegexValidator(r'^[\w]{6,16}$', '6~16位，包含大小写字母和数字的组合')],
    )

    class Meta:
        model = models.User
        fields = ["username", "email", "password", "confirm_password", "avatar"]
        widgets = {
            "password": forms.PasswordInput(attrs={"autocomplete": "False"}, render_value=False),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "images-circle",
                "style": "display:none"
            })
        }

    # 对密码进行md5加密
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        md5_pwd = md5(pwd)
        # 去数据库校验输入的密码是否和原密码一样
        exist = models.User.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exist:
            raise ValidationError("密码不能和原密码一致")
        return md5_pwd

    # 验证密码是否一致
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != password:
            raise ValidationError("密码不一致")
        return confirm


class LoginForm(bootstrapmodelform.BootStrapForm2):
    """登录表单"""
    username = forms.CharField(
        label="用户名",
        max_length=32,
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label="密码",
        max_length=64,
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class RegisterModelForm(bootstrapmodelform.BootStrapModelForm2, UserModelForm):
    pass


class MeDocsModelForm(bootstrapmodelform.BootStrapModelForm1):
    class Meta:
        model = models.MeDocs
        fields = ['docfile']
        widgets = {
            'docfile': forms.ClearableFileInput(
                attrs={
                    'multiple': True,
                    'class': "doc",
                    'style': "display:none"
                })
        }


class DocTxtModelForm(bootstrapmodelform.BootStrapModelForm1):
    class Meta:
        model = models.DocTxt
        fields = []


class DocImgTxtModelForm(bootstrapmodelform.BootStrapModelForm1):
    class Meta:
        model = models.DocImgTxt
        fields = []
        # exclude = [""]
