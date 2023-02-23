import time

from django.db import models


class User(models.Model):
    """平台用户"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    email = models.CharField(verbose_name="邮箱", max_length=64)
    # upload_to="avatars/"  这是存储到本地的avatars/文件下面,如果没有文件夹就自动创建文件夹
    avatar = models.FileField(upload_to="./avatars",
                              default='/default.jpg',
                              verbose_name="头像")

    class Meta:
        verbose_name_plural = "平台用户"

    def __str__(self):
        return self.username


class MeDocs(models.Model):
    """文档"""
    languages_choices = (
        (1, "中文"),
        (2, "英文")
    )
    name = models.CharField(verbose_name="文献名称", max_length=64, db_index=True)
    # 相关性总分为60
    relscore = models.FloatField(verbose_name="相关性得分", default=0)
    # 点击率总分为30
    clkscore = models.FloatField(verbose_name="点击量得分", default=0)
    # 反馈总分为10
    fedbakscore = models.FloatField(verbose_name="用户反馈得分", default=0)
    allscore = models.FloatField(verbose_name="总分", default=0)
    user = models.ForeignKey(verbose_name="贡献者", to='User', null=True, blank=True, on_delete=models.SET_NULL, default=1)
    language = models.SmallIntegerField(verbose_name="语言", default=1, choices=languages_choices)
    date = models.DateField(verbose_name="日期", default=time.strftime("%Y-%m-%d", time.localtime()))
    docfile = models.FileField(upload_to="./docs", verbose_name="文献", null=True, blank=True)

    class Meta:
        verbose_name = "文献"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DocTxt(models.Model):
    """PDF信息"""
    doc_name = models.CharField(verbose_name="文献名称", max_length=64, default="")
    page_id = models.SmallIntegerField(verbose_name="页码", default=1)
    txt_content = models.TextField(verbose_name="文本内容", default="", null=True, blank=True)

    class Meta:
        verbose_name = "文献文本内容"
        verbose_name_plural = verbose_name  # 模型名称(复数)

    def __str__(self):
        return self.doc_name + "第" + str(self.page_id) + "页"


class DocImgTxt(models.Model):
    """PDF图片信息"""
    doc_name = models.CharField(verbose_name="文献名称", max_length=64, default="")
    page_id = models.SmallIntegerField(verbose_name="页码", default=1)
    page_img_num = models.SmallIntegerField(verbose_name="页面图片数", default=0, null=True, blank=True)
    img_content = models.TextField(verbose_name="图片内容", default="", null=True, blank=True)

    class Meta:
        verbose_name = "文献图片内容"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.doc_name + "第" + str(self.page_id) + "页"
