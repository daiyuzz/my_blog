from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
# timezone用来处理时间相关的事务
from django.utils import timezone
from django.urls import reverse
# 引入标签
from taggit.managers import TaggableManager
from PIL import Image


# Create your models here.

class ArticleColumn(models.Model):
    """栏目的model"""
    title = models.CharField(max_length=100, blank=True,verbose_name="名称")
    created = models.DateTimeField(default=timezone.now,verbose_name="创建时间")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = verbose_name_plural = "文章分类"



# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者，指定on_delete删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="作者")

    # models.CharField 为字符串字段，用于保存较短的字符串，如标题。
    title = models.CharField(max_length=100,verbose_name="标题")

    # 文章正文，保存大量文本使用，TextField
    body = models.TextField(verbose_name="正文")

    # 文章创建时间。参数 default=timezone.now指定其创建数据时将默认写入当前时间。
    created = models.DateTimeField(default=timezone.now,verbose_name="创建时间")

    # 文章更新，参数 auto_now = true 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    # 统计浏览量
    total_views = models.PositiveIntegerField(default=0,verbose_name="浏览量")

    # 文章标签
    tags = TaggableManager(blank=True,verbose_name="文章标签")

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d', blank=True,verbose_name="文章标题图")

    # 文章栏目的“一对多”外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name="类别",
    )

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的save()的功能
        article = super(ArticlePost, self).save(*args, **kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    # 内部类 class Meta用于给 model定义元数据
    class Meta:
        # 指定模型返回的数据的排列顺序
        # ‘-created’表明数据应该以倒序排列
        ordering = ('-created',)
        verbose_name_plural = verbose_name = "文章"

    # 函数 __str__定义当调用对象的str()方法时返回的值
    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
