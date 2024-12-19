from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    summary = models.TextField(blank=True, null=True, verbose_name="摘要")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="作者",
        null=True,  # 允许为空
        default=1   # 设置默认值为ID为1的用户
    )
    tags = TaggableManager(verbose_name="标签", blank=True)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
