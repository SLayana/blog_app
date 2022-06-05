from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    title = models.CharField(max_length=150)
    content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title


class Comment(models.Model):

    comment = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = "comments"

    def __str__(self):
        return self.comment