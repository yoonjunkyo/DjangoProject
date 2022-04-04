"""
Definition of models.
"""

from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = "images/", null=True, blank=True)
    
# 게시글의 제목(postname)이 Post object 대신하기
    def __str__(self):
        return self.title