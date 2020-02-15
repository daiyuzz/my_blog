from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField

from mptt.models import MPTTModel,TreeForeignKey
# Create your views here.


# 博文评论
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="文章"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="用户"
    )
    body = RichTextField(verbose_name="评论内容")
    created = models.DateTimeField(auto_now_add=True,verbose_name="评论时间")

    # 新增,mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增,记录二级评论回复给谁,
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 替换Meta为MPTTMeta
    class MPTTMeta:
        ordering=('created',)
        verbose_name_plural = verbose_name = "博客评论"

    def __str__(self):
        return self.body[:20]