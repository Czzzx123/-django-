from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BlogCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, verbose_name="分类"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name
        ordering = ["-pub_time"]

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    content = models.TextField(verbose_name="评论内容")
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments", verbose_name="所属博客"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论者")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
