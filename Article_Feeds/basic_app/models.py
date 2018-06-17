# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=10)
    articlecategory =  models.CharField(max_length=100)   


class Articles(models.Model):
    article_type = models.CharField(max_length=30)
    article_name = models.CharField(max_length=30)
    article_body = models.CharField(max_length=2000)
    published_by = models.CharField(max_length=20)
    likes = models.ManyToManyField(User,related_name='likes',blank="True")
    dislikes = models.ManyToManyField(User,related_name='dislikes',blank="True")
    blocks = models.ManyToManyField(User,related_name='blocks',blank="True")


    def __str__(self):
        return self.article_name
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()
    def total_blocks(self):
        return self.blocks.count()

