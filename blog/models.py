from django.db import models
from django.contrib.auth.models import User


class TagSheet(models.Model):
    tag=models.CharField(max_length=32,unique=True,primary_key=True)

    def __str__(self):
        return self.tag

class TypeSheet(models.Model):
    type=models.CharField(max_length=32,unique=True,primary_key=True)

    def __str__(self):
        return self.type


class ArticleSheet(models.Model):
    title=models.CharField(max_length=64,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content=models.TextField(null=False)
    tag=models.ForeignKey('TagSheet',on_delete=models.CASCADE,null=True)
    type=models.ForeignKey('TypeSheet',on_delete=models.CASCADE,null=False,default=1)

class CommentSheet(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    article=models.ForeignKey('ArticleSheet',on_delete=models.CASCADE)
