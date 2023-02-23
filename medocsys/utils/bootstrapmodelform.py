from django import forms

"""----------1简约型(class=input form-control)--------------2酷炫型(class=input-item)---------"""


# 1.适合增改查的风格
class BootStrap1:
    boostrap_exclude_fields = ['docfile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2.批量设置样式：循环找到所有的字段,给其添加相同样式
        for name, field in self.fields.items():
            if name in self.boostrap_exclude_fields:
                continue
            # 有责修改样式
            if field.widget.attrs:
                field.widget.attrs["class"] = "input form-control"
                field.widget.attrs["placeholder"] = field.label

            # 无责添加样式
            else:
                field.widget.attrs = {"class": "input form-control", "placeholder": field.label}


# 2.适合登陆注册的风格
class BootStrap2:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2.批量设置样式：循环找到所有的字段,给其添加相同样式
        for name, field in self.fields.items():
            # 有责修改样式
            if field.widget.attrs:
                field.widget.attrs["class"] = "input-item"
                field.widget.attrs["placeholder"] = field.label

            # 无责添加样式
            else:
                field.widget.attrs = {"class": "input-item", "placeholder": field.label}


class BootStrapModelForm1(BootStrap1, forms.ModelForm):
    pass


class BootStrapModelForm2(BootStrap2, forms.ModelForm):
    pass


class BootStrapForm1(BootStrap1, forms.Form):
    pass


class BootStrapForm2(BootStrap2, forms.Form):
    pass
