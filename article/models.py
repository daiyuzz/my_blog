from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
# timezone用来处理时间相关的事务
from django.utils import timezone


# Create your models here.

# 博客文章数据模型
class ArticlePost(models.Model):

    # 文章作者，指定on_delete删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # models.CharField 为字符串字段，用于保存较短的字符串，如标题。
    title = models.CharField(max_length=100)

    # 文章正文，保存大量文本使用，TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now指定其创建数据时将默认写入当前时间。
    created = models.DateTimeField(default=timezone.now)

    # 文章更新，参数 auto_now = true 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta用于给 model定义元数据
    class Meta:
        # 指定模型返回的数据的排列顺序
        # ‘-created’表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__定义当调用对象的str()方法时返回的值
    def __str__(self):
        return self.title

